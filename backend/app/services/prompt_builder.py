from typing import Dict

from ..schemas.request import ProcessRequest


class PromptBuilder:
    """Encapsulates prompt templates so they can evolve outside business logic."""

    def build(self, request: ProcessRequest) -> Dict[str, str]:
        cv_prompt = (
            "Create a tailored CV dataset using the base markdown CV and the job description.\n"
            f"Base CV:\n{request.cv_markdown}\n\n"
            f"Job Description:\n{request.job_description_markdown}\n\n"
            f"User Wishes:\n{request.user_wishes}\n\n"
            "Structure the output as a clean markdown snippet that emphasizes alignment."
        )

        cover_letter_prompt = (
            "Draft a concise cover letter that references why the applicant fits the role.\n"
            f"Job Description:\n{request.job_description_markdown}\n\n"
            f"User Wishes:\n{request.user_wishes}\n\n"
            "Reference the applicant's strengths from the provided CV."
        )

        form_prompt = (
            "Extract structured form data for application submission based on the inputs.\n"
            f"Target Job:\n{request.job_description_markdown}\n\n"
            f"Applicant Notes:\n{request.user_wishes}\n\n"
            "Return key: value pairs for fields such as desired role and availability."
        )

        return {
            "tailored_cv": cv_prompt,
            "cover_letter": cover_letter_prompt,
            "form_data": form_prompt,
        }
