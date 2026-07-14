# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this is

An AI skincare/haircare advisor. A FastAPI backend orchestrates Google Gemini agents that build a user profile and recommend products/routines from a local catalog; a React (Vite) frontend provides the chat UI plus profile, routine, and ingredient panels.

## Commands

Backend (run **from the `backend/` directory** — `product_search` opens `products.json` via a relative path, so uvicorn fails to find the catalog if launched from the repo root):

```bash
source venv/bin/activate          # venv lives at repo root
cd backend
uvicorn main:app --reload         # serves on http://localhost:8000
python agent.py                   # alternative: terminal REPL, no server (type 'quit' to exit)
```

There is no `requirements.txt`; deps (`fastapi`, `uvicorn`, `google-generativeai`, `python-dotenv`, `pydantic`) are already installed in `venv/`. `backend/.env` must define `GEMINI_API_KEY`.

Frontend:

```bash
cd frontend
npm run dev        # Vite dev server on http://localhost:5173 (CORS-allowlisted in main.py)
npm run build
npm run lint       # oxlint
```

There is no test suite.

## Architecture

**Request flow:** `frontend/src/App.jsx` → `POST /chat` → `agent.run()` (`backend/agent.py`) → one of the agents in `backend/agents.py` → Gemini with auto-executed tool calls from `backend/tools.py`, which mutate `backend/state.py`. The frontend then re-polls `/profile/{session_id}` and `/routine/{session_id}` to refresh its panels.

**Agent routing (`agent.py:run`) is keyword-based, not model-based.** If the message contains any `recommendation_keywords` (recommend, routine, product, cleanser, ingredient, …) it goes to the Recommendation Agent; otherwise the Intake Agent. The two agents are separate `GenerativeModel` instances (both `gemini-2.5-flash`) with different system prompts and different tool sets:
- **Intake Agent** — only gathers profile info (`get_skin_type_info`, `get_hair_type_info`, `update_user_profile`). Never recommends.
- **Recommendation Agent** — `product_search`, `update_recommended_products`, `update_user_routine`, `ingredient_search`, `update_user_profile`.

**Shared state is process-global, NOT per-session.** `state.user_profile`, `state.user_recommended_products`, and `state.user_routine` are module-level singletons. Only `main.py`'s `history` dict is keyed by `session_id` — and even that conversation history is **never actually passed into the Gemini chats** (each agent call does `start_chat(...).send_message(...)` fresh). So the app is effectively single-user with no real multi-turn memory in the LLM. Treat this as a known limitation when touching state or sessions.

**Escalation:** agents emit a literal `Requires escalation: <reason>` string for medical/prescription/human requests; `main.py` detects this prefix and sets `escalation_required` on the response.

**Data sources:**
- `products.json` — the only real product catalog; `product_search` filters by `category` + `skin_types`/`hair_types`, drops products containing the user's allergens, caps at 5, and auto-calls `update_recommended_products`. Never invent product names outside this file.
- Skin/hair type facts are hardcoded dicts in `tools.py` (`get_skin_type_info`, `get_hair_type_info`).
- `ingredient_search` is **not** a lookup — it makes a live Gemini call asking for JSON and parses the result.

**`prompts.py` (`SYSTEM_PROMPT`, `FEW_SHOT_PROMPT`) is legacy** — imported in `agent.py` but unused by the current routing. The live prompts are `INTAKE_AGENT_PROMPT` and `RECOMMENDATION_AGENT_PROMPT` in `agents.py`.

## Conventions

- Profile fields are `{"value": ..., "confidence": ...}` pairs, where confidence is `verified`/`inferred`/`estimated`. `build_profile_context()` in `agent.py` flattens these into the text context sent to each agent.
- Tool docstrings are load-bearing — Gemini uses them for function-calling. When adding/editing a tool, write the docstring with Args, return shape, and edge cases (see existing tools for the pattern).
