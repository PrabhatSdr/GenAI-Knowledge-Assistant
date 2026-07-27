"use client";

import { useCallback, useEffect, useState } from "react";

import {
  deleteDocument,
  DocumentMetadata,
  listDocuments,
  uploadPdf,
} from "@/lib/api";

function formatBytes(bytes: number): string {
  if (bytes < 1024) return `${bytes} B`;
  if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(1)} KB`;
  return `${(bytes / (1024 * 1024)).toFixed(1)} MB`;
}

function formatDate(iso: string): string {
  try {
    return new Date(iso).toLocaleString();
  } catch {
    return iso;
  }
}

interface Props {
  chatId: string;
}

export function DocumentPanel({ chatId }: Props) {
  const [docs, setDocs] = useState<DocumentMetadata[]>([]);
  const [loading, setLoading] = useState(true);
  const [uploading, setUploading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const refresh = useCallback(async () => {
    try {
      const res = await listDocuments(chatId);
      setDocs(res.documents);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to load documents");
    } finally {
      setLoading(false);
    }
  }, [chatId]);

  useEffect(() => {
    void refresh();
  }, [refresh]);

  async function handleUpload(file: File) {
    setUploading(true);
    setError(null);
    try {
      await uploadPdf(file, chatId);
      await refresh();
    } catch (err) {
      setError(err instanceof Error ? err.message : "Upload failed");
    } finally {
      setUploading(false);
    }
  }

  async function handleDelete(filename: string) {
    if (!confirm(`Delete ${filename}?`)) return;
    try {
      await deleteDocument(filename);
      await refresh();
    } catch (err) {
      setError(err instanceof Error ? err.message : "Delete failed");
    }
  }

  return (
    <section className="flex flex-col h-full border-r border-zinc-200 dark:border-zinc-800">
      <header className="px-4 py-3 border-b border-zinc-200 dark:border-zinc-800">
        <h2 className="text-sm font-semibold text-zinc-700 dark:text-zinc-300">
          Documents
        </h2>
      </header>

      <div className="p-4 border-b border-zinc-200 dark:border-zinc-800">
        <label className="block">
          <span className="sr-only">Upload PDF</span>
          <input
            type="file"
            accept="application/pdf"
            disabled={uploading}
            onChange={(e) => {
              const file = e.target.files?.[0];
              if (file) void handleUpload(file);
            }}
            className="block w-full text-sm text-zinc-700 dark:text-zinc-300
              file:mr-3 file:py-2 file:px-3
              file:rounded-md file:border-0
              file:bg-zinc-900 file:text-zinc-50
              hover:file:bg-zinc-800
              dark:file:bg-zinc-50 dark:file:text-zinc-900
              dark:hover:file:bg-zinc-200
              disabled:opacity-50"
          />
        </label>
        {uploading && (
          <p className="mt-2 text-xs text-zinc-500">Uploading & indexing…</p>
        )}
        {error && (
          <p className="mt-2 text-xs text-red-600 dark:text-red-400">{error}</p>
        )}
      </div>

      <div className="flex-1 overflow-y-auto">
        {loading ? (
          <p className="p-4 text-sm text-zinc-500">Loading…</p>
        ) : docs.length === 0 ? (
          <p className="p-4 text-sm text-zinc-500">
            No documents yet. Upload a PDF to get started.
          </p>
        ) : (
          <ul className="divide-y divide-zinc-200 dark:divide-zinc-800">
            {docs.map((doc) => (
              <li
                key={doc.filename}
                className="px-4 py-3 flex items-start justify-between gap-3"
              >
                <div className="min-w-0 flex-1">
                  <p
                    className="text-sm font-medium text-zinc-900 dark:text-zinc-100 truncate"
                    title={doc.filename}
                  >
                    {doc.original_filename ?? doc.filename}
                  </p>
                  <p className="text-xs text-zinc-500 dark:text-zinc-400 mt-0.5">
                    {formatBytes(doc.size_bytes)} · {doc.chunks} chunks
                  </p>
                  <p className="text-xs text-zinc-400 dark:text-zinc-500 mt-0.5">
                    {formatDate(doc.uploaded_at)}
                  </p>
                </div>
                <button
                  onClick={() => void handleDelete(doc.filename)}
                  className="text-xs text-red-600 hover:text-red-700 dark:text-red-400 dark:hover:text-red-300"
                  aria-label={`Delete ${doc.filename}`}
                >
                  Delete
                </button>
              </li>
            ))}
          </ul>
        )}
      </div>
    </section>
  );
}