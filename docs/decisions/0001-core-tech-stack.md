# ADR 0001: Core technology stack selection

**Status:** Accepted
**Date:** 2026-07-18

## Context

MyPA is an end-to-end multi-agent personal assistant — deliberately built in code
rather than as a no-code workflow (an earlier n8n-based design was rejected for this
reason). Per `ARCHITECTURE.md`, the system splits into three independently deployable
parts: a backend gateway, a separate AI service, and a frontend. The team is two
developers; one is coming from a Java/Spring background and using this project as a
learning vehicle into Python and AI engineering. The stack needs to support the full
production toolchain (observability, evals, guardrails, deployment) rather than a
prototype-only setup.

## Decision

### Backend gateway: Python + FastAPI

- Async-native, which fits an I/O-bound service that mostly proxies to a slower AI
  service and streams responses back to clients.
- Pydantic-based request/response validation and automatic OpenAPI docs out of the box.
- Same language as the AI service — one language across both backend services means
  shared schemas/models can be reused directly instead of duplicated across a language
  boundary.

### Frontend: React + Redux Toolkit (RTK Query) + TypeScript

- React: largest ecosystem, well suited to a chat-style streaming UI.
- Redux Toolkit: predictable global state for concerns many components need to share —
  auth, the active conversation, the approval queue.
- RTK Query: removes hand-rolled data-fetching boilerplate, pairs naturally with the
  backend's REST/SSE endpoints.
- TypeScript: catches a class of bugs at build time — the closest available analogue to
  compile-time safety from Java.

### AI service: LangGraph, OpenAI + Gemini, LangSmith / Langfuse

- **LangGraph** over a hand-rolled agent loop: gives explicit graph structure, built-in
  human-in-the-loop interrupts (required by the approval-gate design in
  `ARCHITECTURE.md` §2), and checkpointed state.
- **LangGraph over CrewAI/AutoGen** for now: deliberately deferred, not rejected — parked
  for a later framework-comparison phase once the team has hands-on experience with one
  framework's tradeoffs, rather than choosing blind between three.
- **OpenAI** as primary model + embeddings provider: mature tool-calling support, an
  embeddings API in the same account, and a key already in hand.
- **Gemini** as a secondary provider: avoids hard vendor lock-in from day one and gives a
  fallback/cost-comparison path later.
- **LangSmith** (primary) / **Langfuse** (open-source alternative), both on OpenTelemetry:
  wired in from Phase 0 rather than bolted on at the end.

## Alternatives considered

- **Backend:** Django (heavier, sync-first, more than an API gateway needs); Node/Express
  (would split the team across two backend languages instead of one).
- **Frontend:** Vue/Svelte (smaller ecosystems); plain Redux without Toolkit (more
  boilerplate, a dated pattern).
- **AI orchestration:** a hand-rolled prompt-chaining state machine (re-solves what
  LangGraph already provides); CrewAI/AutoGen (parked, see above — not rejected outright).

## Consequences

**Positive**
- One language (Python) spans the backend gateway and AI service.
- Type safety on both ends: TypeScript on the frontend, Pydantic + mypy/ty on the backend.
- LangGraph's interrupt mechanism directly supports the safety-by-design human-approval
  requirement rather than needing to be built from scratch.
- Observability is a first-class citizen from Phase 0, not retrofitted later.

**Trade-offs**
- FastAPI + LangGraph is a newer combination than, say, Django + Celery — less
  battle-tested prior art to lean on when debugging.
- Running two separate Python services (backend gateway, AI service) means duplicated
  dependency management overhead versus a single monolith.
- Two LLM providers (OpenAI + Gemini) doubles the credential and config surface from day
  one, even though only one is in active use initially.