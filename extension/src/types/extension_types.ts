export interface ApplicationRequest {
  cv_markdown: string;
  job_description_markdown: string;
  user_wishes: string;
}

export type FormValue = string | string[] | Record<string, unknown>;

export interface ApplicationResponse {
  tailored_cv: string;
  cover_letter: string;
  form_data: Record<string, FormValue>;
}
