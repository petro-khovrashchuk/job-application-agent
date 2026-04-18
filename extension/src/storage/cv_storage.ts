const CV_STORAGE_KEY = "job_agent_cv";

export function saveCvMarkdown(markdown: string): Promise<void> {
  return new Promise((resolve) => {
    chrome.storage.local.set({ [CV_STORAGE_KEY]: markdown }, () => {
      resolve();
    });
  });
}

export function loadCvMarkdown(): Promise<string | null> {
  return new Promise((resolve) => {
    chrome.storage.local.get([CV_STORAGE_KEY], (result) => {
      resolve(result[CV_STORAGE_KEY] ?? null);
    });
  });
}
