"use client";

import { useCallback, useState } from "react";

import { ChatPanel } from "@/components/ChatPanel";
import { DocumentPanel } from "@/components/DocumentPanel";
import { HistorySidebar } from "@/components/HistorySidebar";
import { createHistory } from "@/lib/api";

function makeChatId(): string {
  return `chat-${Date.now()}`;
}

export default function Home() {
  const [chatId, setChatId] = useState("default");
  // Bumped after the user sends a message so the sidebar refetches counts.
  const [refreshKey, setRefreshKey] = useState(0);

  const handleSelectChat = useCallback((id: string) => {
    setChatId(id);
    setRefreshKey((k) => k + 1);
  }, []);

  const handleNewChat = useCallback(async () => {
    const id = makeChatId();
    setChatId(id);
    setRefreshKey((k) => k + 1);
    try {
      await createHistory(id);
    } catch {
      // The chat will be created lazily on the first message; refresh now
      // so the sidebar reflects any partial state.
    }
    setRefreshKey((k) => k + 1);
  }, []);

  const handleMessageSent = useCallback(() => {
    setRefreshKey((k) => k + 1);
  }, []);

  return (
    <div className="flex h-screen w-full bg-white dark:bg-black text-zinc-900 dark:text-zinc-100">
      <HistorySidebar
        activeChatId={chatId}
        onSelectChat={handleSelectChat}
        onNewChat={handleNewChat}
        refreshKey={refreshKey}
      />
      <main className="flex flex-1 min-w-0">
        <div className="w-80 shrink-0">
          <DocumentPanel chatId={chatId} />
        </div>
        <div className="flex-1 min-w-0">
          <ChatPanel chatId={chatId} onMessageSent={handleMessageSent} />
        </div>
      </main>
    </div>
  );
}