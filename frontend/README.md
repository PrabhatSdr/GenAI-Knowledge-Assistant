# GenAI Knowledge Assistant — Frontend

Next.js 16 + React 19 + Tailwind v4 UI for the FastAPI backend in `../backend`.

## Run

You need **two terminals**:

**Terminal 1 — backend:**
```powershell
cd "..\backend"
.\venv\Scripts\activate
uvicorn main:app --reload
```
→ `http://localhost:8000`

**Terminal 2 — frontend:**
```powershell
npm run dev
```
→ `http://localhost:3000`

The browser talks to the backend via `NEXT_PUBLIC_API_URL` in `.env.local`
(default `http://localhost:8000`). CORS is configured in `backend/main.py`.

## Build

```powershell
npm run build   # production build
npm start       # serve the build
```

## Layout

- `app/page.tsx` — split-view shell (sidebar + docs | chat)
- `components/DocumentPanel.tsx` — upload PDFs, list & delete documents
- `components/ChatPanel.tsx` — message list, send box, sources under each answer
- `components/HistorySidebar.tsx` — chat list, switch chat_id, delete chat
- `lib/api.ts` — typed fetch wrappers for `/api/*`

## Stack

| | |
|---|---|
| Framework | Next.js 16 (App Router) |
| Language  | TypeScript |
| Styling   | Tailwind CSS v4 |
| HTTP      | Native `fetch` (no axios) |