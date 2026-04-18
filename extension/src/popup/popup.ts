import "./styles.css";
import { loadCvMarkdown, saveCvMarkdown } from "../storage/cv_storage";
import {
  BackgroundResponseMessage,
  GenerateApplicationMessage,
  ScrapeResultMessage,
} from "../messaging/message_types";

const cvField = document.getElementById("cv-markdown") as HTMLTextAreaElement;
const wishesField = document.getElementById("user-wishes") as HTMLTextAreaElement;
const saveButton = document.getElementById("save-cv") as HTMLButtonElement;
const refreshContextButton = document.getElementById("refresh-context") as HTMLButtonElement;
const processButton = document.getElementById("process-application") as HTMLButtonElement;
const jobPreview = document.getElementById("job-context-preview") as HTMLPreElement;
const jobUrlLabel = document.getElementById("job-url") as HTMLDivElement;
const statusBar = document.getElementById("status-bar") as HTMLDivElement;
const resultsSection = document.getElementById("results") as HTMLElement;
const tailoredCvOutput = document.getElementById("tailored-cv-output") as HTMLPreElement;
const coverLetterOutput = document.getElementById("cover-letter-output") as HTMLPreElement;
const formDataList = document.getElementById("form-data-output") as HTMLUListElement;

let currentJobMarkdown = "";
let currentJobUrl = "";

function setStatus(message: string, state: "info" | "loading" | "success" | "error" = "info") {
  statusBar.textContent = message;
  statusBar.dataset.state = state;
}

function setLoading(isLoading: boolean) {
  processButton.disabled = isLoading;
  refreshContextButton.disabled = isLoading;
  saveButton.disabled = isLoading;
  processButton.textContent = isLoading ? "Processing…" : "Process Application";
}

async function restoreCv() {
  const saved = await loadCvMarkdown();
  if (saved) {
    cvField.value = saved;
    setStatus("Loaded saved CV.", "success");
  } else {
    setStatus("Paste your base CV to get started.");
  }
}

saveButton.addEventListener("click", async () => {
  await saveCvMarkdown(cvField.value.trim());
  setStatus("CV saved to storage.", "success");
});

refreshContextButton.addEventListener("click", () => {
  setStatus("Scanning current tab for job context…", "loading");
  chrome.runtime.sendMessage({ action: "SCRAPE_JOB_PAGE" }, () => {
    if (chrome.runtime.lastError) {
      setStatus(chrome.runtime.lastError.message, "error");
    }
  });
});

processButton.addEventListener("click", () => {
  if (!currentJobMarkdown) {
    setStatus("No job context yet. Please refresh context first.", "error");
    return;
  }

  const payload: GenerateApplicationMessage["payload"] = {
    cvMarkdown: cvField.value.trim(),
    jobDescriptionMarkdown: currentJobMarkdown,
    userWishes: wishesField.value.trim(),
  };

  setLoading(true);
  setStatus("Sending request to backend…", "loading");
  resultsSection.hidden = true;

  chrome.runtime.sendMessage({ action: "GENERATE_APPLICATION", payload }, () => {
    if (chrome.runtime.lastError) {
      setLoading(false);
      setStatus(chrome.runtime.lastError.message, "error");
    }
  });
});

chrome.runtime.onMessage.addListener((message: BackgroundResponseMessage) => {
  if (message.action === "SCRAPE_RESULT") {
    if (message.payload.error) {
      setStatus(message.payload.error, "error");
      jobPreview.textContent = "";
      jobUrlLabel.textContent = "";
      currentJobMarkdown = "";
      return;
    }

    currentJobMarkdown = message.payload.jobDescriptionMarkdown;
    currentJobUrl = message.payload.jobUrl;
    jobPreview.textContent = currentJobMarkdown || "No text was captured from the current page.";
    jobUrlLabel.textContent = currentJobUrl;
    setStatus("Job context ready. Submit when you are ready.", "success");
    return;
  }

  if (message.action === "GENERATE_RESULT") {
    setLoading(false);
    if (message.payload.error) {
      setStatus(message.payload.error, "error");
      return;
    }

    const response = message.payload.response;
    if (!response) {
      setStatus("Backend returned no data.", "error");
      return;
    }

    tailoredCvOutput.textContent = response.tailored_cv;
    coverLetterOutput.textContent = response.cover_letter;

    formDataList.innerHTML = "";
    Object.entries(response.form_data ?? {}).forEach(([key, value]) => {
      const item = document.createElement("li");
      item.textContent = `${key}: ${value}`;
      formDataList.appendChild(item);
    });

    resultsSection.hidden = false;
    setStatus("Application package ready.", "success");
  }
});

const copyButtons = document.querySelectorAll<HTMLButtonElement>("button[data-copy-target]");
copyButtons.forEach((button) => {
  button.addEventListener("click", async () => {
    const targetId = button.dataset.copyTarget as string;
    const target = document.getElementById(targetId);
    if (!target) {
      return;
    }

    try {
      await navigator.clipboard.writeText(target.textContent ?? "");
      button.textContent = "Copied";
      setTimeout(() => {
        button.textContent = "Copy";
      }, 1200);
    } catch (error) {
      setStatus("Clipboard copy failed.", "error");
    }
  });
});

restoreCv();
