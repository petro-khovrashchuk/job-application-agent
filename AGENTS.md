# AGENTS.md

## General Rules
- Follow SOLID principles
- Prefer modular, small files over monoliths
- Separate concerns: API, services, prompts, UI, storage, scraping
- Do not mix business logic with routing or UI layers
- Keep code readable and hackathon-friendly
- Avoid unnecessary abstractions
- Use clear, consistent naming

## Backend (Python / FastAPI)
- Use FastAPI with async endpoints
- Use Pydantic for request/response validation
- Keep routes thin (no business logic)
- Put logic in service layer
- Use dependency inversion for LLM service
- Define an abstract base class for LLM providers
- Default to a mock LLM provider (no API keys required)
- Keep prompt construction in a separate module
- Use environment variables for config
- Enable CORS for Chrome extension + localhost

## Extension (TypeScript / Chrome MV3)
- Use Manifest V3
- Use TypeScript
- Use chrome.storage.local for persistence
- Separate:
  - popup UI
  - background script
  - content script
  - API client
- Keep scraping logic in content script only
- Use Turndown for HTML → Markdown conversion
- Use message passing via chrome.runtime
- Keep UI simple and functional (hackathon-ready)

## Data Flow
- Popup → Content Script → Background → Backend → Popup
- Always validate data before sending
- Handle loading and error states

## Constraints
- No database
- No authentication
- No external dependencies unless necessary
- Keep everything runnable locally
- Use mock data where external APIs would be required

## Output Expectations (for Codex)
- Always provide file-by-file code when scaffolding
- Include folder structure
- Ensure imports are consistent
- Ensure project runs without modification
