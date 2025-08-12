
"use client";

import { useState, FormEvent, useEffect, useRef } from 'react';
import { useSession } from "next-auth/react";
import apiClient from '../lib/api';
import { useChat } from '../context/ChatContext';
import { FaSave } from 'react-icons/fa';
import { LuListRestart } from 'react-icons/lu';
import FileSelectionPanel from './FileSelectionPanel';
import PromptEditorModal from './PromptEditorModal';
import MessageRenderer from './MessageRenderer';

// Default Prompt Templates
const DEFAULT_RAG_PROMPT = `You are an expert assistant. Use ONLY the following pieces of context to answer the user's question.\nIf the answer is not in the context, just say you don't have enough information from the documents.\n\nCONTEXT:\n{context}\n\nQUESTION:\n{question}\n\nANSWER:`;
const DEFAULT_CODE_PROMPT = `You are an expert programmer and master of algorithms. Provide a clear, concise, and correct code solution to the user's request.\nExplain the code briefly if necessary. Use the following context if it is relevant.\n\nCONTEXT:\n{context}\n\nREQUEST:\n{question}\n\nCODE:`;
const DEFAULT_PROMPTS: { [key: string]: string } = {
    "codellama": DEFAULT_CODE_PROMPT,
    "dolphin-mistral": DEFAULT_CODE_PROMPT,
    "agent-mode": DEFAULT_RAG_PROMPT, // Add this line
};

export default function ChatWindow() {
  // State for UI and parameters
  const [prompt, setPrompt] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [showSaveModal, setShowSaveModal] = useState(false);
  const [chatTitle, setChatTitle] = useState("");
  const [selectedFileIds, setSelectedFileIds] = useState<string[]>([]);
  const [selectedModel, setSelectedModel] = useState<string>("agent-mode");
  const [promptTemplateText, setPromptTemplateText] = useState<string>(DEFAULT_RAG_PROMPT);
  const [isPromptModalOpen, setIsPromptModalOpen] = useState(false);
  const [temperature, setTemperature] = useState(0.8);
  const [topP, setTopP] = useState(1.0);
  const [maxTokens, setMaxTokens] = useState(1024);
  const [lastTokenCount, setLastTokenCount] = useState(null);

  // Global state from context
  const { conversation, addMessage, conversationId, setConversationId, clearChat } = useChat();
  const { data: session } = useSession();
  const chatEndRef = useRef<HTMLDivElement>(null);

  // Effects
  useEffect(() => { chatEndRef.current?.scrollIntoView({ behavior: "smooth" }); }, [conversation]);
  useEffect(() => {
    const defaultPrompt = DEFAULT_PROMPTS[selectedModel] || DEFAULT_RAG_PROMPT;
    setPromptTemplateText(defaultPrompt);
  }, [selectedModel]);

  // Handlers
  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();
    if (isLoading || !prompt.trim()) return;
    setIsLoading(true);
    const userQuery = prompt;
    addMessage({ role: 'user', message: userQuery });
    setPrompt('');

    try {
      const response = await apiClient.post('/api/chat', {
        prompt: userQuery,
        conversation_id: conversationId,
        user_email: session?.user?.email,
        selected_file_ids: selectedFileIds,
        selected_model: selectedModel,
        custom_prompt_template: promptTemplateText,
        temperature, top_p: topP, max_tokens: maxTokens,
      });
      const data = response.data;
      addMessage({ role: 'ai', message: data.response });
      if (data.token_counts) setLastTokenCount(data.token_counts);
      if (data.conversation_id) setConversationId(data.conversation_id);
    } catch (error) {
      console.error("An error occurred during chat submission:", error);
      addMessage({ role: 'ai', message: 'Sorry, an error occurred. Please try again.' });
    } finally {
      setIsLoading(false);
    }
  };

  const handleSaveChat = async () => {
    if (!chatTitle.trim() || !conversationId) return alert("Please enter a title for the chat.");
    try {
      await apiClient.put(`/api/conversations/${conversationId}/title`, { new_title: chatTitle, user_email: session?.user?.email });
      alert("Chat saved successfully!");
      setShowSaveModal(false);
      setChatTitle("");
      clearChat();
    } catch (err) {
      console.error("Failed to save chat title:", err);
      alert("Could not save the chat title.");
    }
  };

  return (
    <>
      <PromptEditorModal isOpen={isPromptModalOpen} onClose={() => setIsPromptModalOpen(false)} initialPrompt={promptTemplateText} onSave={(newPrompt) => setPromptTemplateText(newPrompt)} />
      <div className="flex w-[calc(100vw-4rem)] h-[calc(99vh-4rem)] mx-auto p-4 bg-gradient-to-br from-blue-50/80 via-white/90 to-purple-50/80 backdrop-blur-sm">
        {showSaveModal && (
          <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
            <div className="bg-white/95 backdrop-blur-md p-6 rounded-2xl shadow-2xl border border-white/20 w-full max-w-sm">
              <h3 className="text-lg font-bold mb-4">Save Conversation</h3>
              <p className="text-sm text-gray-600 mb-4">Give this chat a title to find it later in "Past Chats".</p>
              <input type="text" value={chatTitle} onChange={(e) => setChatTitle(e.target.value)} placeholder="e.g., Project Planning Notes" className="w-full p-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500" />
              <div className="mt-6 flex justify-end space-x-3">
                <button onClick={() => setShowSaveModal(false)} className="px-4 py-2 bg-gray-200 text-gray-800 rounded-md hover:bg-gray-300">Cancel</button>
                <button onClick={handleSaveChat} className="px-4 py-2 bg-blue-500 text-white rounded-md hover:bg-blue-600">Save & New Chat</button>
              </div>
            </div>
          </div>
        )}
        
        {/* --- THIS IS THE MAIN LAYOUT FIX --- */}
        {/* This container uses flex-col to stack the message area on top of the input form. */}
        <div className="flex-1 flex flex-col p-4">
          
          {/* 1. Chat Messages Area */}
          {/* This div grows to fill available space (flex-1) and handles its own scrolling (overflow-y-auto). */}
          {/* The `min-h-0` is a flexbox trick to prevent the container from overflowing its parent. */}
          <div className="flex-1 overflow-y-auto min-h-0 p-6 bg-white/30 backdrop-blur-md rounded-2xl shadow-lg border border-white/20">
            {conversation.map((msg, index) => (
              <div key={index} className={`my-4 p-4 rounded-2xl shadow-sm border backdrop-blur-sm ${
                msg.role === 'user' 
                  ? 'bg-blue-500/10 border-blue-200/50 ml-auto text-gray-800' 
                  : 'bg-white/70 border-gray-200/50 mr-auto text-gray-800'
              }`} style={{ maxWidth: '90%' }}>
                <p className="font-semibold capitalize text-xs text-gray-500 mb-2 tracking-wide">{msg.role}</p>
                <MessageRenderer content={msg.message} role={msg.role} />
              </div>
            ))}
            {isLoading && (
              <div className="my-4 p-4 rounded-2xl shadow-sm border backdrop-blur-sm bg-white/70 border-gray-200/50 mr-auto animate-pulse" style={{ maxWidth: '90%' }}>
                <p className="font-semibold capitalize text-xs text-gray-500 mb-2 tracking-wide">AI</p>
                <div className="flex items-center space-x-2">
                  <div className="w-2 h-2 bg-blue-500 rounded-full animate-bounce"></div>
                  <div className="w-2 h-2 bg-blue-500 rounded-full animate-bounce" style={{ animationDelay: '0.1s' }}></div>
                  <div className="w-2 h-2 bg-blue-500 rounded-full animate-bounce" style={{ animationDelay: '0.2s' }}></div>
                  <span className="text-gray-600 ml-2">Thinking...</span>
                </div>
              </div>
            )}
            <div ref={chatEndRef} />
          </div>

          {/* 2. Input Form Area */}
          {/* This div sits below the message area and does not grow. It is always visible. */}
          <div className="mt-4 flex-shrink-0">
            <div className="flex items-center space-x-3 p-4 bg-white/40 backdrop-blur-md rounded-2xl shadow-lg border border-white/30">
              <button 
                onClick={clearChat} 
                className="p-3 bg-white/60 backdrop-blur-sm border border-white/40 rounded-xl hover:bg-white/80 hover:scale-105 transition-all duration-200 shadow-sm" 
                title="New Chat"
              >
                <LuListRestart className="w-5 h-5 text-gray-700" />
              </button>
              <form onSubmit={handleSubmit} className="flex-1 flex">
                <input 
                  type="text" 
                  value={prompt} 
                  onChange={(e) => setPrompt(e.target.value)} 
                  placeholder="Ask a question..." 
                  className="flex-1 p-3 bg-white/70 backdrop-blur-sm border border-white/40 rounded-l-xl focus:outline-none focus:ring-2 focus:ring-blue-500/50 focus:bg-white/90 transition-all duration-200" 
                  disabled={isLoading} 
                />
                <button 
                  type="submit" 
                  className="p-3 bg-gradient-to-r from-blue-500 to-blue-600 text-white rounded-r-xl hover:from-blue-600 hover:to-blue-700 disabled:from-gray-400 disabled:to-gray-500 hover:scale-105 transition-all duration-200 shadow-lg disabled:hover:scale-100" 
                  disabled={isLoading || !prompt.trim()}
                >
                  {isLoading ? (
                    <div className="w-5 h-5 border-2 border-white/30 border-t-white rounded-full animate-spin"></div>
                  ) : 'Send'}
                </button>
              </form>
              <button 
                onClick={() => setShowSaveModal(true)} 
                className="p-3 bg-white/60 backdrop-blur-sm border border-white/40 rounded-xl hover:bg-white/80 hover:scale-105 transition-all duration-200 shadow-sm disabled:opacity-50 disabled:cursor-not-allowed disabled:hover:scale-100" 
                title="Save Chat" 
                disabled={!conversationId || conversation.length < 2}
              >
                <FaSave className="w-5 h-5 text-gray-700" />
              </button>
            </div>
          </div>
        </div>
        
        {/* 3. The Side Panel (unaffected by the layout change) */}
        <FileSelectionPanel
          selectedFileIds={selectedFileIds} onSelectionChange={setSelectedFileIds}
          selectedModel={selectedModel} onModelChange={setSelectedModel}
          onEditPrompt={() => setIsPromptModalOpen(true)}
          temperature={temperature} setTemperature={setTemperature}
          topP={topP} setTopP={setTopP}
          maxTokens={maxTokens} setMaxTokens={setMaxTokens}
          lastTokenCount={lastTokenCount}
        />
      </div>
    </>
  );
}