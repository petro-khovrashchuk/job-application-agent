import { ApplicationRequest, ApplicationResponse } from "../types/extension_types";

const BACKEND_URL = "http://localhost:8000/process";

export async function processApplication(
  payload: ApplicationRequest,
): Promise<ApplicationResponse> {
  const response = await fetch(BACKEND_URL, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(payload),
  });

  if (!response.ok) {
    throw new Error(`Backend error: ${response.status} ${response.statusText}`);
  }

  return response.json();
}
