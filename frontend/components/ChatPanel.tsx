"use client";

import { FormEvent, useEffect, useRef, useState } from "react";

import { ChatSource, ChatMessage, chat, loadHistory } from "@/lib/api";

interface Message {
  id: string;
  role: "user" | "assistant";
  content: string;
  sources?: ChatSource[];
}

interface Props {
  chatId: string;
  onMessageSent?: () => void;
}

export function ChatPanel({ chatId, onMessageSent }: Props) {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState("");
  const [pending, setPending] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [historyLoading, setHistoryLoading] = useState(false);
  const scrollRef = useRef<HTMLDivElement>(null);
  // Tracks the chat id we most recently kicked off a load for, so a
  // late response from a previous chat doesn't overwrite the current
  // one's view.
  const loadedForRef = useRef<string | null>(null);

  // Reset + load history whenever the active chat changes
  useEffect(() => {
    let cancelled = false;

    loadedForRef.current = chatId;
    setMessages([]);
    setError(null);
    setHistoryLoading(true);

    (async () => {
      try {
        const history: ChatMessage[] = await loadHistory(chatId);

        if (cancelled || loadedForRef.current !== chatId) return;

        setMessages(
          history.map((m, i) => ({
            id: `r-${chatId}-${i}`,
            role: m.role,
            content: m.content,
          }))
        );
      } catch (err) {
        if (cancelled || loadedForRef.current !== chatId) return;
        setError(
          err instanceof Error ? err.message : "Failed to load history"
        );
      } finally {
        if (!cancelled && loadedForRef.current === chatId) {
          setHistoryLoading(false);
        }
      }
    })();

    return () => {
      cancelled = true;
    };
  }, [chatId]);

  // Auto-scroll to bottom on new messages
  useEffect(() => {
    const el = scrollRef.current;
    if (el) el.scrollTop = el.scrollHeight;
  }, [messages, pending]);

  async function handleSubmit(e: FormEvent) {
    e.preventDefault();
    const question = input.trim();
    if (!question || pending) return;

    const userMessage: Message = {
      id: `u-${Date.now()}`,
      role: "user",
      content: question,
    };
    setMessages((prev) => [...prev, userMessage]);
    setInput("");
    setPending(true);
    setError(null);

    try {
      const res = await chat(question, chatId);
      const assistantMessage: Message = {
        id: `a-${Date.now()}`,
        role: "assistant",
        content: res.answer,
        sources: res.sources,
      };
      setMessages((prev) => [...prev, assistantMessage]);
      onMessageSent?.();
    } catch (err) {
      setError(err instanceof Error ? err.message : "Chat failed");
    } finally {
      setPending(false);
    }
  }

  return (
    <section className="flex flex-col h-full">
      <header className="px-4 py-3 border-b border-zinc-200 dark:border-zinc-800 flex items-center justify-between">
        <h2 className="text-sm font-semibold text-zinc-700 dark:text-zinc-300">
          Chat
        </h2>
        <span className="text-xs text-zinc-500" title={chatId}>
          chat: {chatId}
        </span>
      </header>

      <div
        ref={scrollRef}
        className="flex-1 overflow-y-auto p-4 space-y-4"
      >
        {messages.length === 0 && historyLoading && (
          <p className="text-sm text-zinc-500 text-center mt-8">
            Loading history…
          </p>
        )}
        {messages.length === 0 && !historyLoading && (
          <p className="text-sm text-zinc-500 text-center mt-8">
            Ask a question about your uploaded documents.
          </p>
        )}
        {messages.map((msg) => (
          <div
            key={msg.id}
            className={`flex ${
              msg.role === "user" ? "justify-end" : "justify-start"
            }`}
          >
            <div
              className={`max-w-[80%] rounded-lg px-3 py-2 ${
                msg.role === "user"
                  ? "bg-zinc-900 text-zinc-50 dark:bg-zinc-50 dark:text-zinc-900"
                  : "bg-zinc-100 text-zinc-900 dark:bg-zinc-800 dark:text-zinc-100"
              }`}
            >
              <p className="text-sm whitespace-pre-wrap">{msg.content}</p>
              {msg.sources && msg.sources.length > 0 && (
                <details className="mt-2 text-xs opacity-80">
                  <summary className="cursor-pointer">
                    {msg.sources.length} source
                    {msg.sources.length === 1 ? "" : "s"}
                  </summary>
                  <ul className="mt-1 space-y-0.5">
                    {msg.sources.map((src, i) => (
                      <li key={i} className="font-mono">
                        {src.filename} · chunk {src.chunk_id} ·{" "}
                        {src.score.toFixed(3)}
                      </li>
                    ))}
                  </ul>
                </details>
              )}
            </div>
          </div>
        ))}
        {pending && (
          <div className="flex justify-start">
            <div className="bg-zinc-100 dark:bg-zinc-800 rounded-lg px-3 py-2 text-sm text-zinc-500">
              Thinking…
            </div>
          </div>
        )}
        {error && (
          <p className="text-xs text-red-600 dark:text-red-400 text-center">
            {error}
          </p>
        )}
      </div>

      <form
        onSubmit={handleSubmit}
        className="border-t border-zinc-200 dark:border-zinc-800 p-4 flex gap-2"
      >
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Ask about your documents…"
          disabled={pending}
          className="flex-1 rounded-md border border-zinc-300 dark:border-zinc-700
            bg-white dark:bg-zinc-900 px-3 py-2 text-sm
            focus:outline-none focus:ring-2 focus:ring-zinc-400
            disabled:opacity-50"
        />
        <button
          type="submit"
          disabled={pending || !input.trim()}
          className="rounded-md bg-zinc-900 px-4 py-2 text-sm font-medium text-zinc-50
            hover:bg-zinc-800 disabled:opacity-50
            dark:bg-zinc-50 dark:text-zinc-900 dark:hover:bg-zinc-200"
        >
          Send
        </button>
      </form>
    </section>
  );
}