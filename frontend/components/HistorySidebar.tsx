"use client";

import { useCallback, useEffect, useState } from "react";

import { deleteHistory, HistoryEntry, listHistory } from "@/lib/api";

interface Props {
  activeChatId: string;
  onSelectChat: (chatId: string) => void;
  onNewChat: () => void | Promise<void>;
  refreshKey: number;
}

export function HistorySidebar({
  activeChatId,
  onSelectChat,
  onNewChat,
  refreshKey,
}: Props) {
  const [chats, setChats] = useState<HistoryEntry[]>([]);
  const [loading, setLoading] = useState(true);

  const refresh = useCallback(async () => {
    try {
      const res = await listHistory();
      setChats(res);
    } catch {
      // Soft-fail — sidebar is non-critical
      setChats([]);
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    void refresh();
  }, [refresh, refreshKey]);

  async function handleDelete(chatId: string, e: React.MouseEvent) {
    e.stopPropagation();
    if (!confirm(`Delete chat "${chatId}"?`)) return;
    try {
      await deleteHistory(chatId);
      if (chatId === activeChatId) void onNewChat();
      await refresh();
    } catch {
      // ignore — refresh on next mount
    }
  }

  return (
    <aside className="flex flex-col h-full w-56 border-r border-zinc-200 dark:border-zinc-800 bg-zinc-50 dark:bg-zinc-950">
      <header className="px-3 py-3 border-b border-zinc-200 dark:border-zinc-800 flex items-center justify-between">
        <h2 className="text-xs font-semibold uppercase tracking-wide text-zinc-600 dark:text-zinc-400">
          History
        </h2>
        <button
          onClick={onNewChat}
          className="text-xs text-zinc-600 hover:text-zinc-900 dark:text-zinc-400 dark:hover:text-zinc-100"
          title="Start a new chat"
        >
          + New
        </button>
      </header>

      <div className="flex-1 overflow-y-auto">
        {loading ? (
          <p className="p-3 text-xs text-zinc-500">Loading…</p>
        ) : chats.length === 0 ? (
          <p className="p-3 text-xs text-zinc-500">No chats yet.</p>
        ) : (
          <ul>
            {chats.map((chat) => {
              const isActive = chat.chat_id === activeChatId;
              return (
                <li key={chat.chat_id}>
                  <button
                    onClick={() => onSelectChat(chat.chat_id)}
                    className={`w-full text-left px-3 py-2 flex items-center justify-between gap-2 text-sm ${
                      isActive
                        ? "bg-zinc-200 dark:bg-zinc-800"
                        : "hover:bg-zinc-100 dark:hover:bg-zinc-900"
                    }`}
                  >
                    <span className="truncate" title={chat.chat_id}>
                      {chat.chat_id}
                    </span>
                    <span className="flex items-center gap-2 shrink-0">
                      <span className="text-xs text-zinc-500">
                        {chat.messages}
                      </span>
                      <span
                        role="button"
                        tabIndex={0}
                        onClick={(e) => void handleDelete(chat.chat_id, e)}
                        onKeyDown={(e) => {
                          if (e.key === "Enter" || e.key === " ") {
                            e.preventDefault();
                            void handleDelete(chat.chat_id, e as unknown as React.MouseEvent);
                          }
                        }}
                        className="text-xs text-red-600 hover:text-red-700 dark:text-red-400 dark:hover:text-red-300"
                        title={`Delete ${chat.chat_id}`}
                      >
                        ×
                      </span>
                    </span>
                  </button>
                </li>
              );
            })}
          </ul>
        )}
      </div>
    </aside>
  );
}