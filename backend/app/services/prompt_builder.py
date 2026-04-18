from typing import Dict

from ..schemas.request import ProcessRequest
from ..form_fields import FORM_FIELD_PRESET


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

        personal_section = "\n".join(FORM_FIELD_PRESET.personal_fields)
        form_prompt = (
            "Extract structured form data needed for a job application form.\n"
            f"Target Job:\n{request.job_description_markdown}\n\n"
            f"Applicant Notes:\n{request.user_wishes}\n\n"
            "Respond with valid JSON only. Include at least the following keys: reference_id, job_title, department, "
            "location, availability, recruiter_name, application_status, required_skills (list), benefits (list), "
            "next_steps (list).\n"
            "Place any additional context inside an \"extras\" object.\n"
            "Use the following personal fields when relevant, and fill missing ones with empty strings: \n"
            f"{personal_section}"
        )

        return {
            "tailored_cv": cv_prompt,
            "cover_letter": cover_letter_prompt,
            "form_data": form_prompt,
        }
