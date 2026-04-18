import { ApplicationResponse } from "../types/extension_types";

export interface ScrapeJobPageMessage {
  action: "SCRAPE_JOB_PAGE";
}

export interface ScrapeResultMessage {
  action: "SCRAPE_RESULT";
  payload: {
    jobDescriptionMarkdown: string;
    jobUrl: string;
    jobTitle?: string;
    error?: string;
  };
}

export interface GenerateApplicationMessage {
  action: "GENERATE_APPLICATION";
  payload: {
    cvMarkdown: string;
    jobDescriptionMarkdown: string;
    userWishes: string;
  };
}

export interface GenerateResultMessage {
  action: "GENERATE_RESULT";
  payload: {
    response?: ApplicationResponse;
    error?: string;
  };
}

export type BackgroundRequestMessage = ScrapeJobPageMessage | GenerateApplicationMessage;
export type BackgroundResponseMessage = ScrapeResultMessage | GenerateResultMessage;
export type JobContextPayload = ScrapeResultMessage["payload"];
