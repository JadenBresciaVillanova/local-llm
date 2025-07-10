// frontend/src/context/ChatContext.tsx
"use client";

import React, { createContext, useState, useContext, ReactNode } from 'react';

// Define the shape of a single message
interface Message {
  role: 'user' | 'ai';
  message: string;
}

// Define the shape of the context's value
interface ChatContextType {
  conversation: Message[];
  conversationId: string | null;
  setConversation: React.Dispatch<React.SetStateAction<Message[]>>;
  setConversationId: React.Dispatch<React.SetStateAction<string | null>>;
  addMessage: (message: Message) => void;
  clearChat: () => void;
}

// Create the context with a default undefined value
const ChatContext = createContext<ChatContextType | undefined>(undefined);

// Create the provider component
export const ChatProvider = ({ children }: { children: ReactNode }) => {
  const [conversation, setConversation] = useState<Message[]>([]);
  const [conversationId, setConversationId] = useState<string | null>(null);

  // Helper function to easily add a message
  const addMessage = (message: Message) => {
    setConversation(prev => [...prev, message]);
  };

  // Function to clear the chat and start a new one
  const clearChat = () => {
    setConversation([]);
    setConversationId(null);
  };

  const value = {
    conversation,
    conversationId,
    setConversation,
    setConversationId,
    addMessage,
    clearChat
  };

  return <ChatContext.Provider value={value}>{children}</ChatContext.Provider>;
};

// Create a custom hook for easy access to the context
export const useChat = () => {
  const context = useContext(ChatContext);
  if (context === undefined) {
    throw new Error('useChat must be used within a ChatProvider');
  }
  return context;
};