// frontend/src/app/chats/[convo_id]/page.tsx
"use client";

import { useState, useEffect } from 'react';
import apiClient from '../../../lib/api';
import { useSession } from "next-auth/react";
import { useParams } from 'next/navigation';

interface Message {
  role: string;
  message: string;
}

interface ConversationDetail {
  id: string;
  title: string;
  summary: string;
  created_at: string;
  messages: Message[];
}

export default function ChatDetailPage() {
    const [conversation, setConversation] = useState<ConversationDetail | null>(null);
    const [isLoading, setIsLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);
    const { data: session } = useSession();
    const params = useParams();
    const convo_id = params?.convo_id as string;

    useEffect(() => {
        if (session?.user?.email && convo_id) {
            setIsLoading(true);
            apiClient.get(`/api/conversations/${convo_id}`, {
                params: { user_email: session.user.email }
            })
            .then(response => setConversation(response.data))
            .catch(err => {
                console.error("Failed to fetch conversation:", err);
                setError("Could not load this conversation.");
            })
            .finally(() => setIsLoading(false));
        }
    }, [session, convo_id]);

    if (isLoading) return <div className="text-center p-8">Loading conversation...</div>;
    if (error) return <div className="text-center p-8 text-red-500">{error}</div>;
    if (!conversation) return <div className="text-center p-8">Conversation not found.</div>;

    return (
        <div className="max-w-2xl mx-auto p-4">
            <h1 className="text-2xl font-bold mb-2">{conversation.title}</h1>
            <p className="text-sm text-gray-500 mb-6">Started on: {new Date(conversation.created_at).toLocaleString()}</p>
            <div className="space-y-4">
                {conversation.messages.map((msg, index) => (
                    <div key={index} className={`p-3 rounded-lg ${msg.role === 'user' ? 'bg-blue-100' : 'bg-gray-200'}`}>
                        <p className="font-semibold capitalize">{msg.role}</p>
                        <p className="whitespace-pre-wrap">{msg.message}</p>
                    </div>
                ))}
            </div>
        </div>
    );
}