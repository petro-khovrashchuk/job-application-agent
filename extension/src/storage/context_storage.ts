import { JobContextPayload } from "../messaging/message_types";

const JOB_CONTEXT_KEY = "job_agent_job_context";

export function saveJobContext(payload: JobContextPayload): Promise<void> {
  return new Promise((resolve) => {
    chrome.storage.local.set({ [JOB_CONTEXT_KEY]: payload }, () => {
      resolve();
    });
  });
}

export function loadJobContext(): Promise<JobContextPayload | null> {
  return new Promise((resolve) => {
    chrome.storage.local.get([JOB_CONTEXT_KEY], (result) => {
      resolve(result[JOB_CONTEXT_KEY] ?? null);
    });
  });
}
