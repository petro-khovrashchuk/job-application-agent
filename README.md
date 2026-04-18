# Job Application Agent (Backend + Chrome Extension)

A local-first MVP that stitches together a FastAPI backend and a Chrome Manifest V3 extension. The extension stores your base CV, scrapes job postings, and sends structured prompts (CV, job description, user wishes) to the backend, which leverages mock/HTTP LLM providers to return a tailored CV, cover letter, and application form data.

## Architecture overview

- **Backend** (FastAPI + Pydantic) exposes `/process` and uses dependency-injected LLM providers (default mock, or any HTTP endpoint such as OpenAI GPT‑4o Mini). The prompt builder keeps each prompt in a reusable service module, and JSON is required for form data so the extension just renders key/value pairs. Form field presets drive the required keys and are configured via `backend/app/form_fields.json`.
- **Chrome Extension** (TypeScript + Vite) consists of a popup, background service worker, and content script. The content script scrapes job pages and converts them to Markdown via Turndown. The background script mediates messaging, calls the backend via `fetch`, caches job context, and the popup renders the tailored outputs while persisting the CV to `chrome.storage.local`.

## Prerequisites

- Node.js >= 18 (for building the extension)
- Python 3.12+ (backend uses FastAPI, httpx, pydantic-settings)
- Chrome or Chromium for loading the unpacked extension

## Backend setup

1. Create a virtual environment and install dependencies:
   ```bash
   cd backend
   python -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```
2. Copy or edit `.env.example` into `.env` and fill in:
   ```ini
   DEV_ORIGIN=http://localhost:3000
   CHROME_EXTENSION_ID=<your-extension-id>
   LLM_PROVIDER_URL=https://api.openai.com/v1/chat/completions
   LLM_PROVIDER_API_KEY=sk-...
   LLM_PROVIDER_TYPE=openai
   LLM_PROVIDER_MODEL=gpt-4o-mini
   LLM_PROVIDER_TIMEOUT_SECONDS=120
   ```
   - `DEV_ORIGIN` must match the URL your popup is served from.
   - `CHROME_EXTENSION_ID` is the ID shown on `chrome://extensions` (32 characters).
   - The LLM settings let you plug in any OpenAI-compatible service.
3. Start the backend:
   ```bash
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```
   Errors and request logs appear on the console; we also raise friendly 503s when the LLM call times out.

## Extension setup

1. Install dependencies inside `extension/`:
   ```bash
   cd ../extension
   npm install
   ```
2. During development, use `npm run dev` to launch Vite and keep rebuilding; for the production build run `npm run build` (this copies `manifest.json` into `dist/`).
3. Load the extension from Chrome:
   - Open `chrome://extensions`, enable Developer mode, click "Load unpacked", and point to `extension/dist` after building.
   - If you want to test without rebuilding, you can load directly from the source directory and use the `npm run dev` server.
4. The popup persists your CV, lets you refresh job context, and shows results with copy buttons. Form data is rendered as a list, with bullets for arrays.

## Form fields preset

The backend ships with `backend/app/form_fields.json`. Update that JSON to change which personal fields the LLM should include in the form data response.

## LLM configuration

- The backend defaults to a mock provider (`MockLLMProvider`).
- Set `LLM_PROVIDER_URL` / `LLM_PROVIDER_TYPE=openai` / `LLM_PROVIDER_API_KEY` to hit real services (e.g., GPT‑4o Mini).
- `LLM_PROVIDER_TIMEOUT_SECONDS` controls how long the HTTP provider waits before raising `LLMProviderError`.
- The extension keeps reusing the same `/process` data format; no code changes are needed when you switch LLM providers—just update `.env`.

## Troubleshooting

- **Form data still looks weird**: Make sure the LLM returns JSON under a ````json ... ``` `` block. The prompt in `PromptBuilder` now enumerates the fields it expects.
- **Backend logs not showing POST requests**: You can add additional logging inside `JobAgentService.craft_application` to trace the pipeline and confirm the request actually hits the LLM.
- **Webpack/Vite doesn’t rebuild**: Run `npm run dev` in a separate terminal so hot reload works; `npm run build` copies `manifest.json` into `dist` for production.

## Next steps

- If you want to add another preset, just extend `form_fields.json` and re-run the backend. The prompt builder will automatically include the new list.
- To persist job context between tabs, the background script already stores it in `chrome.storage.local`, so the popup shows the latest scraped markdown even after navigation.
- Want to log to a file? Wrap `uvicorn` with a logging config or use `logging.basicConfig(filename="backend.log", level=logging.INFO)` in `app/main.py`.
