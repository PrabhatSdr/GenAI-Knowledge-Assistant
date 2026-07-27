/**
 * Typed fetch wrappers for the GenAI Knowledge Assistant backend.
 *
 * All endpoints live under `${API_URL}/api/*`.
 * The backend is FastAPI on port 8000; CORS is configured in main.py.
 */

const API_URL =
  process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000";

const BASE = `${API_URL}/api`;

// -------------------------------------------------------------
// Types (mirror backend/services/metadata_service.py record shape)
// -------------------------------------------------------------

export interface DocumentMetadata {
  filename: string;
  original_filename: string | null;
  size_bytes: number;
  chunks: number;
  characters: number;
  uploaded_at: string;
}

export interface DocumentsResponse {
  count: number;
  documents: DocumentMetadata[];
}

export interface ChatSource {
  filename: string;
  chunk_id: number;
  score: number;
}

export interface ChatResponse {
  answer: string;
  sources: ChatSource[];
}

export interface HistoryEntry {
  chat_id: string;
  messages: number;
}

export interface ChatMessage {
  role: "user" | "assistant";
  content: string;
}

// -------------------------------------------------------------
// Helpers
// -------------------------------------------------------------

async function handle<T>(res: Response): Promise<T> {
  if (!res.ok) {
    let detail = res.statusText;
    try {
      const body = await res.json();
      if (body?.detail) detail = String(body.detail);
    } catch {
      // ignore parse errors, fall back to statusText
    }
    throw new Error(`${res.status} ${detail}`);
  }
  return res.json() as Promise<T>;
}

// -------------------------------------------------------------
// Documents
// -------------------------------------------------------------

export async function listDocuments(
  chatId?: string
): Promise<DocumentsResponse> {
  const qs = chatId ? `?chat_id=${encodeURIComponent(chatId)}` : "";
  const res = await fetch(`${BASE}/documents${qs}`, { cache: "no-store" });
  return handle<DocumentsResponse>(res);
}

export async function deleteDocument(filename: string): Promise<void> {
  const res = await fetch(`${BASE}/documents/${encodeURIComponent(filename)}`, {
    method: "DELETE",
  });
  await handle<{ message: string }>(res);
}

export async function uploadPdf(
  file: File,
  chatId: string = "default"
): Promise<{
  message: string;
  original_filename: string;
  stored_filename: string;
  chat_id: string;
  ingestion: {
    filename: string;
    size_bytes: number;
    characters: number;
    chunks: number;
    message: string;
  };
}> {
  const form = new FormData();
  form.append("file", file);

  const res = await fetch(
    `${BASE}/upload?chat_id=${encodeURIComponent(chatId)}`,
    {
      method: "POST",
      body: form,
    }
  );

  return handle(res);
}

// -------------------------------------------------------------
// Chat
// -------------------------------------------------------------

export async function chat(
  question: string,
  chatId: string = "default"
): Promise<ChatResponse> {
  const res = await fetch(
    `${BASE}/chat?chat_id=${encodeURIComponent(chatId)}`,
    {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ question }),
    }
  );
  return handle<ChatResponse>(res);
}

// -------------------------------------------------------------
// History
// -------------------------------------------------------------

export async function listHistory(): Promise<HistoryEntry[]> {
  const res = await fetch(`${BASE}/history`, { cache: "no-store" });
  return handle<HistoryEntry[]>(res);
}

export async function loadHistory(chatId: string): Promise<ChatMessage[]> {
  const res = await fetch(
    `${BASE}/history/${encodeURIComponent(chatId)}`,
    { cache: "no-store" }
  );
  return handle<ChatMessage[]>(res);
}

export async function deleteHistory(chatId: string): Promise<void> {
  const res = await fetch(
    `${BASE}/history/${encodeURIComponent(chatId)}`,
    { method: "DELETE" }
  );
  await handle<{ message: string }>(res);
}

export async function createHistory(chatId: string): Promise<HistoryEntry> {
  const res = await fetch(`${BASE}/history`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ chat_id: chatId }),
  });
  return handle<HistoryEntry>(res);
}