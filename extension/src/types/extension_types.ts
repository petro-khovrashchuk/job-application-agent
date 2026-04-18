export interface ApplicationRequest {
  cv_markdown: string;
  job_description_markdown: string;
  user_wishes: string;
}

export interface ApplicationResponse {
  tailored_cv: string;
  cover_letter: string;
  form_data: Record<string, string>;
}
