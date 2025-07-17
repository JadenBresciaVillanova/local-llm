// frontend/src/app/chats/page.tsx
// "use client";

// import { useState, useEffect, FC } from 'react';
// import apiClient from '../../lib/api';
// import { useSession } from "next-auth/react";
// import Link from 'next/link';
// import { FaTrashAlt, FaDownload } from 'react-icons/fa';

// interface ConversationSummary {
//   id: string;
//   title: string;
//   summary: string;
//   created_at: string;
// }

// export default function PastChatsPage() {
//     const [conversations, setConversations] = useState<ConversationSummary[]>([]);
//     const [isLoading, setIsLoading] = useState(true);
//     const [error, setError] = useState<string | null>(null);
//     const { data: session } = useSession();

//     const fetchConversations = async () => {
//         if (!session?.user?.email) return;
//         setIsLoading(true);
//         try {
//             const response = await apiClient.get('/api/conversations', {
//                 params: { user_email: session.user.email }
//             });
//             setConversations(response.data);
//         } catch (err) {
//             console.error("Failed to fetch conversations:", err);
//             setError("Could not load your past chats.");
//         } finally {
//             setIsLoading(false);
//         }
//     };

//     useEffect(() => {
//         if (session) {
//             fetchConversations();
//         }
//     }, [session]);

//     const handleDelete = async (convoId: string) => {
//         if (!window.confirm("Delete this conversation forever?")) return;
//         try {
//             await apiClient.delete(`/api/conversations/${convoId}`, {
//                 params: { user_email: session?.user?.email }
//             });
//             setConversations(prev => prev.filter(c => c.id !== convoId));
//         } catch (err) {
//             console.error("Failed to delete conversation:", err);
//             alert("Could not delete conversation.");
//         }
//     };

//     const handleDownload = async (convoId: string) => {
//         try {
//             const response = await apiClient.get(`/api/conversations/${convoId}/export/csv`, {
//                 params: { user_email: session?.user?.email },
//                 responseType: 'blob', // Important for file downloads
//             });
//             const url = window.URL.createObjectURL(new Blob([response.data]));
//             const link = document.createElement('a');
//             link.href = url;
//             link.setAttribute('download', `conversation_${convoId}.csv`);
//             document.body.appendChild(link);
//             link.click();
//             link.remove();
//         } catch (err) {
//             console.error("Failed to download:", err);
//             alert("Could not download conversation.");
//         }
//     };

//     if (isLoading) return <div className="text-center p-8">Loading chats...</div>;
//     if (error) return <div className="text-center p-8 text-red-500">{error}</div>;

//     return (
//         <div className="max-w-5xl mx-auto p-4 sm:p-6 lg:p-8">
//             <h1 className="text-2xl font-bold text-gray-900 mb-6">Past Conversations</h1>
//             <div className="bg-white shadow-md rounded-lg overflow-hidden">
//                 <table className="min-w-full divide-y divide-gray-200">
//                     <thead className="bg-gray-50">
//                         <tr>
//                             <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Title & Summary</th>
//                             <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Date</th>
//                             <th className="relative px-6 py-3"><span className="sr-only">Actions</span></th>
//                         </tr>
//                     </thead>
//                     <tbody className="bg-white divide-y divide-gray-200">
//                         {conversations.length === 0 ? (
//                             <tr><td colSpan={3} className="px-6 py-4 text-center text-gray-500">No past conversations found.</td></tr>
//                         ) : (
//                             conversations.map((convo) => (
//                                 <tr key={convo.id}>
//                                     <td className="px-6 py-4">
//                                         <Link href={`/chats/${convo.id}`} className="hover:underline">
//                                             <div className="text-sm font-medium text-gray-900">{convo.title}</div>
//                                             <div className="text-sm text-gray-500 truncate max-w-md">{convo.summary}</div>
//                                         </Link>
//                                     </td>
//                                     <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{new Date(convo.created_at).toLocaleString()}</td>
//                                     <td className="px-6 py-4 whitespace-nowrap text-right text-sm font-medium space-x-4">
//                                         <button onClick={() => handleDownload(convo.id)} className="text-blue-600 hover:text-blue-900" title="Download CSV"><FaDownload /></button>
//                                         <button onClick={() => handleDelete(convo.id)} className="text-red-600 hover:text-red-900" title="Delete"><FaTrashAlt /></button>
//                                     </td>
//                                 </tr>
//                             ))
//                         )}
//                     </tbody>
//                 </table>
//             </div>
//         </div>
//     );
// }
"use client";

import { useState, useEffect, FC } from 'react';
import apiClient from '../../lib/api';
import { useSession } from "next-auth/react";
import Link from 'next/link';
import { FaTrashAlt, FaDownload, FaRocket } from 'react-icons/fa'; // Added FaRocket for "Load"
import { useRouter } from 'next/navigation'; // NEW: Import Next.js router
import { useChat } from '../../context/ChatContext'; // NEW: Import the chat context hook

interface ConversationSummary {
  id: string;
  title: string;
  summary: string;
  created_at: string;
}

export default function PastChatsPage() {
    const [conversations, setConversations] = useState<ConversationSummary[]>([]);
    const [isLoading, setIsLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);
    const { data: session } = useSession();
    const router = useRouter(); // NEW: Initialize the router for redirection
    const { setConversation, setConversationId } = useChat(); // NEW: Get setters from context

    const fetchConversations = async () => {
        if (!session?.user?.email) return;
        setIsLoading(true);
        try {
            const response = await apiClient.get('/api/conversations', {
                params: { user_email: session.user.email }
            });
            setConversations(response.data);
        } catch (err) {
            console.error("Failed to fetch conversations:", err);
            setError("Could not load your past chats.");
        } finally {
            setIsLoading(false);
        }
    };

    useEffect(() => {
        if (session) {
            fetchConversations();
        }
    }, [session]);

    // NEW: Function to load a chat into the main chat window
    const handleLoadChat = async (convoId: string) => {
        try {
            // 1. Fetch the full details of the selected conversation
            const response = await apiClient.get(`/api/conversations/${convoId}`, {
                params: { user_email: session?.user?.email }
            });
            const chatDetails = response.data;

            // 2. Populate the global chat context with this chat's data
            setConversation(chatDetails.messages);
            setConversationId(chatDetails.id);

            // 3. Redirect the user to the main chat page
            router.push('/');

        } catch (err) {
            console.error("Failed to load conversation:", err);
            alert("Could not load this conversation.");
        }
    };

    const handleDelete = async (convoId: string) => {
        // ... (This function is unchanged)
        if (!window.confirm("Delete this conversation forever?")) return;
        try {
            await apiClient.delete(`/api/conversations/${convoId}`, {
                params: { user_email: session?.user?.email }
            });
            setConversations(prev => prev.filter(c => c.id !== convoId));
        } catch (err) {
            console.error("Failed to delete conversation:", err);
            alert("Could not delete conversation.");
        }
    };

    const handleDownload = async (convoId: string) => {
        // ... (This function is unchanged)
        try {
            const response = await apiClient.get(`/api/conversations/${convoId}/export/csv`, {
                params: { user_email: session?.user?.email },
                responseType: 'blob',
            });
            const url = window.URL.createObjectURL(new Blob([response.data]));
            const link = document.createElement('a');
            link.href = url;
            link.setAttribute('download', `conversation_${convoId}.csv`);
            document.body.appendChild(link);
            link.click();
            link.remove();
        } catch (err) {
            console.error("Failed to download:", err);
            alert("Could not download conversation.");
        }
    };

    if (isLoading) return <div className="text-center p-8">Loading chats...</div>;
    if (error) return <div className="text-center p-8 text-red-500">{error}</div>;

    return (
        <div className="max-w-5xl mx-auto p-4 sm:p-6 lg:p-8">
            <h1 className="text-2xl font-bold text-gray-900 mb-6">Past Conversations</h1>
            <div className="bg-white shadow-md rounded-lg overflow-hidden">
                <table className="min-w-full divide-y divide-gray-200">
                    <thead className="bg-gray-50">
                        <tr>
                            <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Title & Summary</th>
                            <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Date</th>
                            <th className="relative px-6 py-3"><span className="sr-only">Actions</span></th>
                        </tr>
                    </thead>
                    <tbody className="bg-white divide-y divide-gray-200">
                        {conversations.length === 0 ? (
                            <tr><td colSpan={3} className="px-6 py-4 text-center text-gray-500">No past conversations found.</td></tr>
                        ) : (
                            conversations.map((convo) => (
                                <tr key={convo.id}>
                                    <td className="px-6 py-4">
                                        {/* This link now goes to the read-only view */}
                                        <Link href={`/chats/${convo.id}`} className="hover:underline">
                                            <div className="text-sm font-medium text-gray-900">{convo.title}</div>
                                            <div className="text-sm text-gray-500 truncate max-w-md">{convo.summary}</div>
                                        </Link>
                                    </td>
                                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{new Date(convo.created_at).toLocaleString()}</td>
                                    <td className="px-6 py-4 whitespace-nowrap text-right text-sm font-medium space-x-4">
                                        {/* NEW: Load Chat button */}
                                        <button onClick={() => handleLoadChat(convo.id)} className="text-green-600 hover:text-green-900" title="Load Chat"><FaRocket /></button>
                                        <button onClick={() => handleDownload(convo.id)} className="text-blue-600 hover:text-blue-900" title="Download CSV"><FaDownload /></button>
                                        <button onClick={() => handleDelete(convo.id)} className="text-red-600 hover:text-red-900" title="Delete"><FaTrashAlt /></button>
                                    </td>
                                </tr>
                            ))
                        )}
                    </tbody>
                </table>
            </div>
        </div>
    );
}