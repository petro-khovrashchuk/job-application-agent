import { htmlToMarkdown } from "../utils/turndown";
import { ScrapeJobPageMessage } from "../messaging/message_types";

type ContentMessage = ScrapeJobPageMessage;

chrome.runtime.onMessage.addListener((message: ContentMessage, sender, sendResponse) => {
  if (message.action !== "SCRAPE_JOB_PAGE") {
    return false;
  }

  const html = document.body?.innerHTML ?? "";
  const markdown = htmlToMarkdown(html);

  sendResponse({
    jobDescriptionMarkdown: markdown,
    jobUrl: window.location.href,
    jobTitle: document.title,
  });

  return true;
});
