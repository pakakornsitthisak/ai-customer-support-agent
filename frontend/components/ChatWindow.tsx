"use client";

import { useEffect, useRef, useState } from "react";

import { deleteSession, sendMessage } from "../lib/api";
import ChatInput from "./ChatInput";
import MessageBubble from "./MessageBubble";

interface Message {
  id: number;
  role: "user" | "assistant";
  content: string;
}

const INITIAL_MESSAGE: Message = {
  id: 1,
  role: "assistant",
  content:
    "Hello! I'm your AI customer support assistant. How can I help you today?",
};

function createSessionId(): string {
  return crypto.randomUUID();
}

export default function ChatWindow() {
  const [messages, setMessages] = useState<Message[]>([
    INITIAL_MESSAGE,
  ]);

  const [loading, setLoading] = useState(false);

  const [sessionId, setSessionId] = useState("default");

  const messagesEndRef = useRef<HTMLDivElement | null>(null);

  // --------------------------------------------------
  // Initialize session from localStorage
  // --------------------------------------------------

  useEffect(() => {
    const storedSessionId =
      window.localStorage.getItem("support_session_id");

    if (storedSessionId) {
      setSessionId(storedSessionId);
      return;
    }

    const newSessionId = createSessionId();

    window.localStorage.setItem(
      "support_session_id",
      newSessionId,
    );

    setSessionId(newSessionId);
  }, []);

  // --------------------------------------------------
  // Scroll to latest message
  // --------------------------------------------------

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({
      behavior: "smooth",
    });
  }, [messages, loading]);

  // --------------------------------------------------
  // Send message
  // --------------------------------------------------

  async function handleSend(message: string) {
    const userMessage: Message = {
      id: Date.now(),
      role: "user",
      content: message,
    };

    setMessages((current) => [
      ...current,
      userMessage,
    ]);

    setLoading(true);

    try {
      const response = await sendMessage(
        message,
        sessionId,
      );

      const assistantMessage: Message = {
        id: Date.now() + 1,
        role: "assistant",
        content: response.answer,
      };

      setMessages((current) => [
        ...current,
        assistantMessage,
      ]);
    } catch (error) {
      console.error("Failed to send message:", error);

      const errorMessage: Message = {
        id: Date.now() + 1,
        role: "assistant",
        content:
          "Sorry, I couldn't connect to the support service. Please try again.",
      };

      setMessages((current) => [
        ...current,
        errorMessage,
      ]);
    } finally {
      setLoading(false);
    }
  }

  // --------------------------------------------------
  // Start new conversation
  // --------------------------------------------------

  async function handleNewConversation() {
    if (loading) {
      return;
    }

    const oldSessionId = sessionId;

    try {
      await deleteSession(oldSessionId);
    } catch (error) {
      console.error(
        "Failed to clear previous session:",
        error,
      );
    }

    const newSessionId = createSessionId();

    window.localStorage.setItem(
      "support_session_id",
      newSessionId,
    );

    setSessionId(newSessionId);

    setMessages([
      {
        ...INITIAL_MESSAGE,
        id: Date.now(),
      },
    ]);
  }

  // --------------------------------------------------
  // Render
  // --------------------------------------------------

  return (
    <div className="flex h-screen flex-col bg-gray-50">
      {/* Header */}

      <header className="border-b bg-white">
        <div className="mx-auto flex w-full max-w-5xl items-center justify-between px-6 py-4">
          <div>
            <h1 className="text-lg font-semibold text-gray-900">
              AI Customer Support
            </h1>

            <div className="mt-1 flex items-center gap-2">
              <span className="h-2 w-2 rounded-full bg-green-500" />

              <span className="text-xs text-gray-500">
                Online
              </span>
            </div>
          </div>

          <button
            type="button"
            onClick={handleNewConversation}
            disabled={loading}
            className="rounded-lg border border-gray-300 bg-white px-4 py-2 text-sm font-medium text-gray-700 transition hover:bg-gray-50 disabled:cursor-not-allowed disabled:opacity-50"
          >
            New conversation
          </button>
        </div>
      </header>

      {/* Messages */}

      <main className="flex-1 overflow-y-auto px-4 py-6">
        <div className="mx-auto flex max-w-4xl flex-col gap-4">
          {messages.map((message) => (
            <MessageBubble
              key={message.id}
              role={message.role}
              content={message.content}
            />
          ))}

          {/* Loading indicator */}

          {loading && (
            <div className="flex justify-start">
              <div className="rounded-2xl bg-gray-100 px-4 py-3 text-sm text-gray-500">
                AI is thinking...
              </div>
            </div>
          )}

          <div ref={messagesEndRef} />
        </div>
      </main>

      {/* Input */}

      <ChatInput
        onSend={handleSend}
        disabled={loading}
      />
    </div>
  );
}