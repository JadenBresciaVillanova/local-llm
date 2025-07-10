// frontend/src/app/page.tsx
"use client";

import { useSession, signIn } from "next-auth/react";
import ChatWindow from "../components/ChatWindow";

export default function Home() {
  const { data: session, status } = useSession();

  // Show a loading state while the session is being checked
  if (status === "loading") {
    return (
        <div className="flex justify-center items-center h-screen">
            <p className="text-gray-500">Loading session...</p>
        </div>
    );
  }

  // If the user is authenticated, show the chat window
  if (session) {
    return <ChatWindow />;
  }

  // If the user is not authenticated, show a sign-in prompt
  return (
    <div className="flex flex-col items-center justify-center min-h-[calc(100vh-4rem)] text-center p-4">
        <h1 className="text-4xl font-bold mb-4 text-gray-800">Welcome to Local RAG</h1>
        <p className="text-lg text-gray-600 mb-8">Please sign in to chat with your documents.</p>
        <button 
            onClick={() => signIn("github")}
            className="px-6 py-3 bg-gray-800 text-white font-semibold rounded-lg shadow-md hover:bg-gray-900 transition-colors"
        >
            Sign in with GitHub
        </button>
    </div>
  );
}