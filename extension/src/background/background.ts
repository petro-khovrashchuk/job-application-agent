import { processApplication } from "../api/backend_client";
import {
  GenerateApplicationMessage,
  GenerateResultMessage,
  ScrapeJobPageMessage,
  ScrapeResultMessage,
} from "../messaging/message_types";
import { saveJobContext } from "../storage/context_storage";

type BackgroundMessage = ScrapeJobPageMessage | GenerateApplicationMessage;

chrome.runtime.onMessage.addListener((message: BackgroundMessage, sender, sendResponse) => {
  if (message.action === "SCRAPE_JOB_PAGE") {
    handleScrapeJob(sendResponse);
    return true;
  }

  if (message.action === "GENERATE_APPLICATION") {
    handleGenerate(message).catch((error) => {
      const response: GenerateResultMessage = {
        action: "GENERATE_RESULT",
        payload: { error: error?.message ?? "Unknown error" },
      };
      chrome.runtime.sendMessage(response);
    });
    sendResponse({ accepted: true });
    return false;
  }

  return false;
});

function handleScrapeJob(sendResponse: (response: unknown) => void) {
  chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
    const activeTab = tabs[0];
    if (!activeTab?.id) {
      reportScrapeResult({
        jobDescriptionMarkdown: "",
        jobUrl: "",
        error: "No active tab found.",
      });
      sendResponse({ success: false });
      return;
    }

    chrome.tabs.sendMessage(activeTab.id, { action: "SCRAPE_JOB_PAGE" }, (response) => {
      if (chrome.runtime.lastError) {
        reportScrapeResult({
          jobDescriptionMarkdown: "",
          jobUrl: "",
          error: chrome.runtime.lastError.message,
        });
        sendResponse({ success: false });
        return;
      }

      const payload: ScrapeResultMessage["payload"] = {
        jobDescriptionMarkdown: response?.jobDescriptionMarkdown ?? "",
        jobUrl: response?.jobUrl ?? "",
        jobTitle: response?.jobTitle,
      };
      void saveJobContext(payload);
      reportScrapeResult(payload);
      sendResponse({ success: true });
    });
  });
}

async function handleGenerate(message: GenerateApplicationMessage) {
  const request = {
    cv_markdown: message.payload.cvMarkdown,
    job_description_markdown: message.payload.jobDescriptionMarkdown,
    user_wishes: message.payload.userWishes,
  };

  const data = await processApplication(request);

  const result: GenerateResultMessage = {
    action: "GENERATE_RESULT",
    payload: { response: data },
  };

  chrome.runtime.sendMessage(result);
}

function reportScrapeResult(payload: ScrapeResultMessage["payload"]) {
  const finalMessage: ScrapeResultMessage = {
    action: "SCRAPE_RESULT",
    payload,
  };
  chrome.runtime.sendMessage(finalMessage);
}
