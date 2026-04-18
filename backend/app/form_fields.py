from pathlib import Path
import json
from typing import List

_JSON_PATH = Path(__file__).with_name("form_fields.json")

class FormFieldPreset:
    personal_fields: List[str] = []


def load_form_fields() -> FormFieldPreset:
    if not _JSON_PATH.exists():
        return FormFieldPreset()
    with open(_JSON_PATH, "r", encoding="utf-8") as fh:
        data = json.load(fh)
    preset = FormFieldPreset()
    preset.personal_fields = data.get("personal_fields", [])
    return preset

FORM_FIELD_PRESET = load_form_fields()
