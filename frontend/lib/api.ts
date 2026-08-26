const API_URL =
  process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

interface ChatResponse {
  answer: string;
}

export async function sendMessage(
  message: string,
  sessionId: string,
): Promise<ChatResponse> {
  const response = await fetch(`${API_URL}/chat`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      message,
      session_id: sessionId,
    }),
  });

  if (!response.ok) {
    throw new Error(
      `Chat request failed: ${response.status}`,
    );
  }

  return response.json();
}

export async function deleteSession(
  sessionId: string,
): Promise<void> {
  const response = await fetch(
    `${API_URL}/sessions/${encodeURIComponent(sessionId)}`,
    {
      method: "DELETE",
    },
  );

  if (!response.ok) {
    throw new Error(
      `Delete session failed: ${response.status}`,
    );
  }
}