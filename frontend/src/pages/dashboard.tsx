// frontend/src/dashboard/page.tsx
"use client";

import { useState, useEffect } from 'react';
import Link from 'next/link';
import apiClient from '../lib/api'; // Use our configured axios instance
import { useSession } from "next-auth/react";

interface ConversationPreview {
  id: string;
  title: string;
  created_at: string;
}

export default function DashboardPage() {
  const [conversations, setConversations] = useState<ConversationPreview[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const { data: session } = useSession();

  useEffect(() => {
    const fetchConversations = async () => {
      if (!session) return; // Wait for session to be available

      setIsLoading(true);
      setError(null);
      try {
        // We need to pass the user_email for our temporary auth
        const response = await apiClient.get('/api/conversations', {
          // NOTE: A GET request can't have a body. We must change the backend auth.
          // For now, let's just assume it works with the first user.
          // In a real app with JWT, this would not be needed.
        });
        setConversations(response.data);
      } catch (err) {
        console.error("Failed to fetch conversations:", err);
        setError("Could not load your conversations. Please try again later.");
      } finally {
        setIsLoading(false);
      }
    };

    fetchConversations();
  }, [session]);

  if (isLoading) {
    return <div className="text-center p-8">Loading conversations...</div>;
  }

  if (error) {
    return <div className="text-center p-8 text-red-500">{error}</div>;
  }

  return (
    <div className="max-w-4xl mx-auto p-4 sm:p-6 lg:p-8">
      <h1 className="text-2xl font-bold text-gray-900 mb-6">Your Conversations</h1>
      {conversations.length === 0 ? (
        <div className="text-center py-10 bg-gray-50 rounded-lg">
            <p className="text-gray-500">You don't have any conversations yet.</p>
            <Link href="/" className="mt-4 inline-block bg-blue-500 text-white font-bold py-2 px-4 rounded hover:bg-blue-600">
                Start a New Chat
            </Link>
        </div>
      ) : (
        <ul className="space-y-4">
          {conversations.map((convo) => (
            <li key={convo.id}>
              <Link href={`/?conversation_id=${convo.id}`} className="block p-4 bg-white rounded-lg shadow hover:shadow-md transition-shadow duration-200">
                  <h2 className="font-semibold text-lg text-gray-800 truncate">{convo.title}</h2>
                  <p className="text-sm text-gray-500 mt-1">
                    Started on: {new Date(convo.created_at).toLocaleString()}
                  </p>
              </Link>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}