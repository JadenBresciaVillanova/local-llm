// local-llm-nextjs/src/components/ChatWindow.tsx
// "use client";

// import { useState, FormEvent } from 'react';
// // import axios from 'axios';
// import apiClient from '../lib/api'; 
// // src/components/ChatWindow.tsx
// import { useSession } from "next-auth/react";

// interface Message {
//   role: 'user' | 'ai';
//   message: string;
// }

// const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

// export default function ChatWindow() {
//   const [prompt, setPrompt] = useState('');
//   const [conversation, setConversation] = useState<Message[]>([]);
//   const [conversationId, setConversationId] = useState<string | null>(null);
//   const [isLoading, setIsLoading] = useState(false);
//    const { data: session } = useSession();

//   const handleSubmit = async (e: FormEvent) => {
//     e.preventDefault();
//     if (!prompt.trim() || isLoading) return;

//     const userMessage: Message = { role: 'user', message: prompt };
//     setConversation(prev => [...prev, userMessage]);
//     setPrompt('');
//     setIsLoading(true);

//      try {
//       const response = await apiClient.post('/api/chat', {
//         prompt,
//         conversation_id: conversationId,
//         // The Insecure Shortcut: Send the email directly
//         user_email: session?.user?.email, 
//       });

//       const data = response.data as { response: string; conversation_id: string };
//       const aiMessage: Message = { role: 'ai', message: data.response };
//       setConversation(prev => [...prev, aiMessage]);
//       setConversationId(data.conversation_id);
//     } catch (error) {
//       console.error("Error fetching AI response:", error);
//       const errorMessage: Message = { role: 'ai', message: 'Sorry, I encountered an error.' };
//       setConversation(prev => [...prev, errorMessage]);
//     } finally {
//       setIsLoading(false);
//     }
//   };

//   return (
//     <div className="flex flex-col h-screen max-w-2xl mx-auto p-4 bg-gray-50">
//       <div className="flex-1 overflow-y-auto p-4 bg-white rounded-lg shadow-md">
//         {conversation.map((msg, index) => (
//           <div key={index} className={`my-2 p-3 rounded-lg ${
//             msg.role === 'user' ? 'bg-blue-100 ml-auto' : 'bg-gray-200 mr-auto'
//           }`} style={{ maxWidth: '80%' }}>
//             <p className="font-semibold capitalize">{msg.role}</p>
//             <p className="whitespace-pre-wrap">{msg.message}</p>
//           </div>
//         ))}
//         {isLoading && (
//           <div className="my-2 p-3 rounded-lg bg-gray-200 mr-auto" style={{ maxWidth: '80%' }}>
//             <p className="font-semibold capitalize">AI</p>
//             <p className="animate-pulse">Thinking...</p>
//           </div>
//         )}
//       </div>

//       <form onSubmit={handleSubmit} className="mt-4 flex">
//         <input
//           type="text"
//           value={prompt}
//           onChange={(e) => setPrompt(e.target.value)}
//           placeholder="Ask me anything..."
//           className="flex-1 p-2 border border-gray-300 rounded-l-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
//           disabled={isLoading}
//         />
//         <button
//           type="submit"
//           className="p-2 bg-blue-500 text-white rounded-r-lg hover:bg-blue-600 disabled:bg-blue-300"
//           disabled={isLoading}
//         >
//           {isLoading ? 'Sending...' : 'Send'}
//         </button>
//       </form>
//     </div>
//   );
// }

// frontend/src/components/ChatWindow.tsx
// "use client";

// import { useState, FormEvent } from 'react';
// import { useSession } from "next-auth/react";
// import apiClient from '../lib/api';
// import FileUploader from './FileUploader'; // Import the uploader component

// // The interface for a single message in the conversation
// interface Message {
//   role: 'user' | 'ai';
//   message: string;
// }

// export default function ChatWindow() {
//   // --- STATE MANAGEMENT ---
//   const [prompt, setPrompt] = useState('');
//   const [conversation, setConversation] = useState<Message[]>([]);
//   const [conversationId, setConversationId] = useState<string | null>(null);
//   const [isLoading, setIsLoading] = useState(false);
  
//   // New state for the file uploader
//   const [isUploaderOpen, setIsUploaderOpen] = useState(false);
//   const [attachedFile, setAttachedFile] = useState<File | null>(null);
  
//   const { data: session } = useSession();

//   // --- HANDLERS ---

//   // Called when a file is selected in the FileUploader modal
//   const handleFileSelect = (file: File) => {
//     console.log("File selected and attached:", file);
//     setAttachedFile(file);
//     // The modal closes itself via the onClose prop
//   };

//   // Main handler for submitting the form (sending a message)
//   const handleSubmit = async (e: FormEvent) => {
//     e.preventDefault();
//     if ((!prompt.trim() && !attachedFile) || isLoading) return;

//     // TODO: The logic here will need to change.
//     // If a file is attached, it should be uploaded first.
//     // For now, it just sends the text prompt.
//     if (attachedFile) {
//         console.log("Submitting with attached file:", attachedFile.name);
//         // We will build the upload logic in the next step.
//         // For now, let's add a placeholder message.
//     }

//     const userMessage: Message = { role: 'user', message: prompt };
//     setConversation(prev => [...prev, userMessage]);
//     setPrompt('');
//     setIsLoading(true);

//      try {
//       // NOTE: This currently only sends the text prompt.
//       // We will need to create a new API endpoint for file uploads.
//       const response = await apiClient.post('/api/chat', {
//         prompt,
//         conversation_id: conversationId,
//         user_email: session?.user?.email, 
//       });

//       const data = response.data as { response: string; conversation_id: string };
//       const aiMessage: Message = { role: 'ai', message: data.response };
//       setConversation(prev => [...prev, aiMessage]);
//       setConversationId(data.conversation_id);
//     } catch (error) {
//       console.error("Error fetching AI response:", error);
//       const errorMessage: Message = { role: 'ai', message: 'Sorry, I encountered an error.' };
//       setConversation(prev => [...prev, errorMessage]);
//     } finally {
//       setIsLoading(false);
//     }
//   };

//   // --- RENDER ---
//   return (
//     <div className="flex flex-col h-screen max-w-2xl mx-auto p-4 bg-gray-50">
      
//       {/* Conditionally render the uploader modal */}
//       {isUploaderOpen && (
//         <FileUploader 
//           onFileSelect={handleFileSelect} 
//           onClose={() => setIsUploaderOpen(false)} 
//         />
//       )}
      
//       {/* Chat history display area */}
//       <div className="flex-1 overflow-y-auto p-4 bg-white rounded-lg shadow-md">
//         {conversation.map((msg, index) => (
//           <div key={index} className={`my-2 p-3 rounded-lg ${
//             msg.role === 'user' ? 'bg-blue-100 ml-auto' : 'bg-gray-200 mr-auto'
//           }`} style={{ maxWidth: '80%' }}>
//             <p className="font-semibold capitalize">{msg.role}</p>
//             <p className="whitespace-pre-wrap">{msg.message}</p>
//           </div>
//         ))}
//         {isLoading && (
//           <div className="my-2 p-3 rounded-lg bg-gray-200 mr-auto" style={{ maxWidth: '80%' }}>
//             <p className="font-semibold capitalize">AI</p>
//             <p className="animate-pulse">Thinking...</p>
//           </div>
//         )}
//       </div>

//       {/* Input form area */}
//       <form onSubmit={handleSubmit} className="mt-4">
        
//         {/* Show attached file info if a file is selected */}
//         {attachedFile && (
//           <div className="mb-2 p-2 bg-gray-100 rounded-lg flex justify-between items-center text-sm">
//             <span className='truncate pr-2'>📎 {attachedFile.name}</span>
//             <button
//               type="button"
//               onClick={() => setAttachedFile(null)}
//               className="text-red-500 hover:text-red-700 font-bold flex-shrink-0"
//               aria-label="Remove attached file"
//             >
//               ×
//             </button>
//           </div>
//         )}
        
//         <div className="flex">
//           {/* File Upload Button */}
//           <button
//             type="button"
//             onClick={() => setIsUploaderOpen(true)}
//             className="p-2 border border-r-0 border-gray-300 bg-gray-100 text-gray-600 rounded-l-lg hover:bg-gray-200"
//             aria-label="Attach file"
//           >
//             <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
//               <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15.172 7l-6.586 6.586a2 2 0 102.828 2.828l6.414-6.586a4 4 0 00-5.656-5.656l-6.415 6.585a6 6 0 108.486 8.486L20.5 13" />
//             </svg>
//           </button>
          
//           {/* Text Input */}
//           <input
//             type="text"
//             value={prompt}
//             onChange={(e) => setPrompt(e.target.value)}
//             placeholder={attachedFile ? "Describe the document or ask a question..." : "Ask me anything..."}
//             className="flex-1 p-2 border border-gray-300 focus:outline-none focus:ring-2 focus:ring-blue-500"
//             disabled={isLoading}
//           />

//           {/* Send Button */}
//           <button
//             type="submit"
//             className="p-2 bg-blue-500 text-white rounded-r-lg hover:bg-blue-600 disabled:bg-blue-300"
//             disabled={isLoading || (!prompt.trim() && !attachedFile)}
//           >
//             {isLoading ? 'Sending...' : 'Send'}
//           </button>
//         </div>
//       </form>
//     </div>
//   );
// }

// frontend/src/components/ChatWindow.tsx
// "use client";

// import { useState, FormEvent } from 'react';
// import { useSession } from "next-auth/react";
// import apiClient from '../lib/api';
// import FileUploader from './FileUploader';

// // Interface for a single message in the conversation
// interface Message {
//   role: 'user' | 'ai';
//   message: string;
// }

// // Interface for the file metadata response from our API
// interface FileMetadata {
//   id: string;
//   file_name: string;
//   // you can add other fields here if needed in the UI
// }

// export default function ChatWindow() {
//   const [prompt, setPrompt] = useState('');
//   const [conversation, setConversation] = useState<Message[]>([]);
//   const [conversationId, setConversationId] = useState<string | null>(null);
//   const [isLoading, setIsLoading] = useState(false);
//   const [isUploaderOpen, setIsUploaderOpen] = useState(false);
//   const [attachedFile, setAttachedFile] = useState<File | null>(null);
//   const { data: session } = useSession();

//   const handleFileSelect = (file: File) => {
//     setAttachedFile(file);
//     // The FileUploader modal will close itself via its onClose prop
//   };

//   const handleSubmit = async (e: FormEvent) => {
//     e.preventDefault();
//     if ((!prompt.trim() && !attachedFile) || isLoading) return;

//     setIsLoading(true);
//     let userQuery = prompt;
//     let uploadedFileId: string | null = null;
//     // --- START: FILE UPLOAD LOGIC ---
//     if (attachedFile) {
//       // Create a temporary message to show the upload is in progress
//       const uploadMessageId = Date.now(); // Unique key for updating this message later
//       const tempUploadingMessage: Message & { id: number } = { 
//         id: uploadMessageId,
//         role: 'ai', 
//         message: `Uploading ${attachedFile.name}...` 
//       };
//       // Use a functional update to get the latest state
//       setConversation(prev => [...prev, tempUploadingMessage]);
      
//       const formData = new FormData();
//       formData.append('file', attachedFile);
//       if (session?.user?.email) {
//         formData.append('user_email', session.user.email);
//       } else {
//         // Handle case where session is not available, though it should be
//         alert("You must be logged in to upload files.");
//         setIsLoading(false);
//         return;
//       }

//       try {
//         // Use the configured apiClient to send the FormData
//         const response = await apiClient.post<FileMetadata>('/api/files/upload', formData, {
//           headers: {
//             // Axios sets the correct Content-Type for FormData automatically
//             // 'Content-Type': 'multipart/form-data', // This line is not needed
//           },
//         });

//         const uploadedFile = response.data;
//         const uploadedFileId = response.data.id;
//         console.log('✅ File uploaded successfully. File ID:', uploadedFile.id);

//         // Update the temporary message to show success
//         setConversation(prev => prev.map(msg => 
//           (msg as any).id === uploadMessageId 
//             ? { ...msg, message: `✅ Successfully uploaded ${uploadedFile.file_name}.` } 
//             : msg
//         ));

//       } catch (error) {
//         console.error("File upload failed:", error);
//         // Update the temporary message to show the error
//         setConversation(prev => prev.map(msg => 
//           (msg as any).id === uploadMessageId 
//             ? { ...msg, message: `❌ Failed to upload ${attachedFile.name}. Please try again.` } 
//             : msg
//         ));
//         setIsLoading(false);
//         return; // Stop execution if the upload fails
//       }
//     }
//     // --- END: FILE UPLOAD LOGIC ---

//     // Display the user's text prompt in the chat
//     const userMessage: Message = { role: 'user', message: userQuery };
//     setConversation(prev => [...prev, userMessage]);

//     // Clear the form inputs for the next message
//     setPrompt('');
//     setAttachedFile(null);

//     // Now, call the chat endpoint
//     try {
//       const response = await apiClient.post('/api/chat', {
//         prompt: userQuery,
//         conversation_id: conversationId,
//         user_email: session?.user?.email,
//         file_id: uploadedFileId,
//         // In the future, we can pass the uploaded file ID here to the chat endpoint
//         // uploaded_file_id: uploadedFileId,
//       });

//       const data = response.data as { response: string; conversation_id: string };
//       const aiMessage: Message = { role: 'ai', message: data.response };
//       setConversation(prev => [...prev, aiMessage]);
//       setConversationId(data.conversation_id);
//     } catch (error) {
//       console.error("Error fetching AI response:", error);
//       const errorMessage: Message = { role: 'ai', message: 'Sorry, I encountered an error communicating with the AI.' };
//       setConversation(prev => [...prev, errorMessage]);
//     } finally {
//       setIsLoading(false);
//     }
//   };

//   // --- RENDER ---
//   return (
//     <div className="flex flex-col h-screen max-w-2xl mx-auto p-4 bg-gray-50">
      
//       {/* Conditionally render the uploader modal */}
//       {isUploaderOpen && (
//         <FileUploader 
//           onFileSelect={handleFileSelect} 
//           onClose={() => setIsUploaderOpen(false)} 
//         />
//       )}
      
//       <div className="flex-1 overflow-y-auto p-4 bg-white rounded-lg shadow-md">
//         {conversation.map((msg, index) => (
//           <div key={index} className={`my-2 p-3 rounded-lg ${
//             msg.role === 'user' ? 'bg-blue-100 ml-auto' : 'bg-gray-200 mr-auto'
//           }`} style={{ maxWidth: '80%' }}>
//             <p className="font-semibold capitalize">{msg.role}</p>
//             <p className="whitespace-pre-wrap">{msg.message}</p>
//           </div>
//         ))}
//         {isLoading && (
//           <div className="my-2 p-3 rounded-lg bg-gray-200 mr-auto" style={{ maxWidth: '80%' }}>
//             <p className="font-semibold capitalize">AI</p>
//             <p className="animate-pulse">Thinking...</p>
//           </div>
//         )}
//       </div>

//       <form onSubmit={handleSubmit} className="mt-4">
//         {attachedFile && (
//           <div className="mb-2 p-2 bg-gray-100 rounded-lg flex justify-between items-center text-sm">
//             <span className='truncate pr-2'>📎 {attachedFile.name}</span>
//             <button
//               type="button"
//               onClick={() => setAttachedFile(null)}
//               className="text-red-500 hover:text-red-700 font-bold flex-shrink-0"
//               aria-label="Remove attached file"
//             >
//               ×
//             </button>
//           </div>
//         )}
        
//         <div className="flex">
//           <button
//             type="button"
//             onClick={() => setIsUploaderOpen(true)}
//             className="p-2 border border-r-0 border-gray-300 bg-gray-100 text-gray-600 rounded-l-lg hover:bg-gray-200"
//             aria-label="Attach file"
//           >
//             <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
//               <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15.172 7l-6.586 6.586a2 2 0 102.828 2.828l6.414-6.586a4 4 0 00-5.656-5.656l-6.415 6.585a6 6 0 108.486 8.486L20.5 13" />
//             </svg>
//           </button>
          
//           <input
//             type="text"
//             value={prompt}
//             onChange={(e) => setPrompt(e.target.value)}
//             placeholder={attachedFile ? "Describe the document or ask a question..." : "Ask me anything..."}
//             className="flex-1 p-2 border border-gray-300 focus:outline-none focus:ring-2 focus:ring-blue-500"
//             disabled={isLoading}
//           />

//           <button
//             type="submit"
//             className="p-2 bg-blue-500 text-white rounded-r-lg hover:bg-blue-600 disabled:bg-blue-300"
//             disabled={isLoading || (!prompt.trim() && !attachedFile)}
//           >
//             {isLoading ? 'Sending...' : 'Send'}
//           </button>
//         </div>
//       </form>
//     </div>
//   );
// }

// "use client";

// import { useState, FormEvent } from 'react';
// import { useSession } from "next-auth/react";
// import apiClient from '../lib/api';
// import FileUploader from './FileUploader';

// // Interface for a single message in the conversation
// interface Message {
//   role: 'user' | 'ai';
//   message: string;
// }

// // Interface for the file metadata response from our API
// interface FileMetadata {
//   id: string;
//   file_name: string;
// }

// export default function ChatWindow() {
//   // --- STATE MANAGEMENT ---
//   const [prompt, setPrompt] = useState('');
//   const [conversation, setConversation] = useState<Message[]>([]);
//   const [conversationId, setConversationId] = useState<string | null>(null);
//   const [isLoading, setIsLoading] = useState(false);
//   const [isUploaderOpen, setIsUploaderOpen] = useState(false);
//   const [attachedFile, setAttachedFile] = useState<File | null>(null);
//   const { data: session } = useSession();

//   // --- HANDLERS ---
//   const handleFileSelect = (file: File) => {
//     setAttachedFile(file);
//   };

//   const handleSubmit = async (e: FormEvent) => {
//     e.preventDefault();
//     // Disable form if loading or if there's no text and no file
//     if (isLoading || (!prompt.trim() && !attachedFile)) return;

//     setIsLoading(true);
//     const userQuery = prompt;

//     // Add user's prompt to the conversation UI immediately
//     if (userQuery) {
//         const userMessage: Message = { role: 'user', message: userQuery };
//         setConversation(prev => [...prev, userMessage]);
//     }
    
//     // Clear inputs immediately for better UX
//     setPrompt('');
//     setAttachedFile(null); 

//     let uploadedFileId: string | null = null;

//     try {
//       // --- SEQUENTIAL STEP 1: Handle File Upload (if any) ---
//       if (attachedFile) {
//         const tempId = Date.now(); // Unique key for updating this message later
//         const tempUploadingMessage: Message & { id: number } = { 
//           id: tempId,
//           role: 'ai', 
//           message: `Uploading ${attachedFile.name}...` 
//         };
//         setConversation(prev => [...prev, tempUploadingMessage]);
        
//         const formData = new FormData();
//         formData.append('file', attachedFile);
//         if (session?.user?.email) {
//           formData.append('user_email', session.user.email);
//         } else {
//             throw new Error("You must be logged in to upload files.");
//         }

//         // AWAIT the upload call. This is the critical fix.
//         const uploadResponse = await apiClient.post<FileMetadata>('/api/files/upload', formData);
        
//         uploadedFileId = uploadResponse.data.id; // Capture the ID
//         console.log('✅ File uploaded successfully. File ID:', uploadedFileId);

//         // Update UI message to show success and next step
//         setConversation(prev => prev.map(msg => 
//             (msg as any).id === tempId 
//             ? { ...msg, message: `✅ Successfully uploaded ${uploadResponse.data.file_name}. Now processing...` } 
//             : msg
//         ));
//       }

//       // --- SEQUENTIAL STEP 2: Call the Chat Endpoint ---
//       const response = await apiClient.post('/api/chat', {
//         prompt: userQuery,
//         conversation_id: conversationId,
//         user_email: session?.user?.email,
//         file_id: uploadedFileId, // Pass the ID we just received (or null if no file)
//       });

//       const data = response.data as { response: string; conversation_id: string };
//       const aiMessage: Message = { role: 'ai', message: data.response };
      
//       // Add the final AI response to the conversation
//       setConversation(prev => [...prev, aiMessage]);
//       // If you want to continue the conversation, you would set the ID.
//       // For a RAG-per-query model, you might not want to set this.
//       setConversationId(data.conversation_id);

//     } catch (error) {
//       console.error("An error occurred during the process:", error);
//       const errorMessage: Message = { role: 'ai', message: 'Sorry, something went wrong. Please check the console for details.' };
//       setConversation(prev => [...prev, errorMessage]);
//     } finally {
//       setIsLoading(false);
//     }
//   };

//   // --- RENDER ---
//   return (
//     <div className="flex flex-col h-screen max-w-2xl mx-auto p-4 bg-gray-50">
      
//       {isUploaderOpen && (
//         <FileUploader 
//           onFileSelect={handleFileSelect} 
//           onClose={() => setIsUploaderOpen(false)} 
//         />
//       )}
      
//       <div className="flex-1 overflow-y-auto p-4 bg-white rounded-lg shadow-md">
//         {conversation.map((msg, index) => (
//           <div key={index} className={`my-2 p-3 rounded-lg ${
//             msg.role === 'user' ? 'bg-blue-100 ml-auto' : 'bg-gray-200 mr-auto'
//           }`} style={{ maxWidth: '80%' }}>
//             <p className="font-semibold capitalize">{msg.role}</p>
//             <p className="whitespace-pre-wrap">{msg.message}</p>
//           </div>
//         ))}
//         {isLoading && (
//           <div className="my-2 p-3 rounded-lg bg-gray-200 mr-auto" style={{ maxWidth: '80%' }}>
//             <p className="font-semibold capitalize">AI</p>
//             <p className="animate-pulse">Thinking...</p>
//           </div>
//         )}
//       </div>

//       <form onSubmit={handleSubmit} className="mt-4">
//         {attachedFile && (
//           <div className="mb-2 p-2 bg-gray-100 rounded-lg flex justify-between items-center text-sm">
//             <span className='truncate pr-2'>📎 {attachedFile.name}</span>
//             <button
//               type="button"
//               onClick={() => setAttachedFile(null)}
//               className="text-red-500 hover:text-red-700 font-bold flex-shrink-0"
//               aria-label="Remove attached file"
//             >
//               ×
//             </button>
//           </div>
//         )}
        
//         <div className="flex">
//           <button
//             type="button"
//             onClick={() => setIsUploaderOpen(true)}
//             className="p-2 border border-r-0 border-gray-300 bg-gray-100 text-gray-600 rounded-l-lg hover:bg-gray-200"
//             aria-label="Attach file"
//           >
//             <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
//               <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15.172 7l-6.586 6.586a2 2 0 102.828 2.828l6.414-6.586a4 4 0 00-5.656-5.656l-6.415 6.585a6 6 0 108.486 8.486L20.5 13" />
//             </svg>
//           </button>
          
//           <input
//             type="text"
//             value={prompt}
//             onChange={(e) => setPrompt(e.target.value)}
//             placeholder={attachedFile ? "Ask a question about the file..." : "Ask me anything..."}
//             className="flex-1 p-2 border border-gray-300 focus:outline-none focus:ring-2 focus:ring-blue-500"
//             disabled={isLoading}
//           />

//           <button
//             type="submit"
//             className="p-2 bg-blue-500 text-white rounded-r-lg hover:bg-blue-600 disabled:bg-blue-300"
//             disabled={isLoading || (!prompt.trim() && !attachedFile)}
//           >
//             {isLoading ? 'Sending...' : 'Send'}
//           </button>
//         </div>
//       </form>
//     </div>
//   );
// }

// frontend/src/components/ChatWindow.tsx
// "use client";

// import { useState, FormEvent, useEffect, useRef } from 'react';
// import { useSession } from "next-auth/react";
// import apiClient from '../lib/api';
// import FileUploader from './FileUploader';
// import { useChat } from '../context/ChatContext'; // 👈 Import the hook


// interface FileMetadata {
//   id: string;
//   file_name: string;
// }

// export default function ChatWindow() {
//   // Local state for UI elements
//   const [prompt, setPrompt] = useState('');
//   const [isLoading, setIsLoading] = useState(false);
//   const [isUploaderOpen, setIsUploaderOpen] = useState(false);
//   const [attachedFile, setAttachedFile] = useState<File | null>(null);
  
//   // Shared state from context
//   const { 
//     conversation, 
//     addMessage, 
//     conversationId, 
//     setConversationId,
//     clearChat // Use the clear function
//   } = useChat();

//   const { data: session } = useSession();
//   const chatEndRef = useRef<HTMLDivElement>(null);

//   // Effect to scroll to the bottom of the chat on new messages
//   useEffect(() => {
//     chatEndRef.current?.scrollIntoView({ behavior: "smooth" });
//   }, [conversation]);


//   const handleSubmit = async (e: FormEvent) => {
//     e.preventDefault();
//     if (isLoading || (!prompt.trim() && !attachedFile)) return;

//     setIsLoading(true);
//     const userQuery = prompt;

//     // Add user's prompt to shared state
//     if (userQuery) {
//         addMessage({ role: 'user', message: userQuery });
//     }
    
//     // Clear local UI state
//     setPrompt('');
//     setAttachedFile(null); 

//     let uploadedFileId: string | null = null;

//     try {
//       if (attachedFile) {
//         addMessage({ role: 'ai', message: `Uploading ${attachedFile.name}...` });
        
//         const formData = new FormData();
//         formData.append('file', attachedFile);
//         if (session?.user?.email) {
//           formData.append('user_email', session.user.email);
//         }

//         const uploadResponse = await apiClient.post<FileMetadata>('/api/files/upload', formData);
//         uploadedFileId = uploadResponse.data.id;
        
//         // This is a bit tricky, we can't easily update the "uploading" message.
//         // For now, let's just add a new success message.
//         addMessage({ role: 'ai', message: `✅ Processing ${uploadResponse.data.file_name}...` });
//       }

//       // Call the chat endpoint
//       const response = await apiClient.post('/api/chat', {
//         prompt: userQuery,
//         conversation_id: conversationId,
//         user_email: session?.user?.email,
//         file_id: uploadedFileId,
//       });

//       const data = response.data;
//       addMessage({ role: 'ai', message: data.response });
//       setConversationId(data.conversation_id);

//     } catch (error) {
//       console.error("An error occurred:", error);
//       addMessage({ role: 'ai', message: 'Sorry, an error occurred. Please try again.' });
//     } finally {
//       setIsLoading(false);
//     }
//   };

//   return (
//     <div className="flex flex-col h-[calc(100vh-4rem)] max-w-2xl mx-auto pt-4 bg-gray-50">
      
//       {isUploaderOpen && (
//         <FileUploader 
//           onFileSelect={(file) => setAttachedFile(file)} 
//           onClose={() => setIsUploaderOpen(false)} 
//         />
//       )}
      
//       <div className="flex-1 overflow-y-auto px-4 bg-white rounded-lg shadow-md">
//         {conversation.map((msg, index) => (
//           <div key={index} className={`my-2 p-3 rounded-lg ${msg.role === 'user' ? 'bg-blue-100 ml-auto' : 'bg-gray-200 mr-auto'}`} style={{ maxWidth: '80%' }}>
//             <p className="font-semibold capitalize">{msg.role}</p>
//             <p className="whitespace-pre-wrap">{msg.message}</p>
//           </div>
//         ))}
//         {isLoading && (
//           <div className="my-2 p-3 rounded-lg bg-gray-200 mr-auto animate-pulse" style={{ maxWidth: '80%' }}>
//             <p className="font-semibold capitalize">AI</p>
//             <p>Thinking...</p>
//           </div>
//         )}
//         <div ref={chatEndRef} />
//       </div>

//       <div className="mt-4 flex items-center space-x-2">
//         <button 
//             onClick={clearChat}
//             className="p-2 border border-gray-300 rounded-lg hover:bg-gray-100"
//             title="New Chat"
//         >
//             +
//         </button>
//         <form onSubmit={handleSubmit} className="flex-1 flex">
//             {attachedFile && (
//           <div className="mb-2 p-2 bg-gray-100 rounded-lg flex justify-between items-center text-sm">
//             <span className='truncate pr-2'>📎 {attachedFile.name}</span>
//             <button
//               type="button"
//               onClick={() => setAttachedFile(null)}
//               className="text-red-500 hover:text-red-700 font-bold flex-shrink-0"
//               aria-label="Remove attached file"
//             >
//               ×
//             </button>
//           </div>
//         )}
        
//         <div className="flex w-full">
//           <button
//             type="button"
//             onClick={() => setIsUploaderOpen(true)}
//             className="p-2 border border-r-0 border-gray-300 bg-gray-100 text-gray-600 rounded-l-lg hover:bg-gray-200"
//             aria-label="Attach file"
//           >
//             <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
//               <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15.172 7l-6.586 6.586a2 2 0 102.828 2.828l6.414-6.586a4 4 0 00-5.656-5.656l-6.415 6.585a6 6 0 108.486 8.486L20.5 13" />
//             </svg>
//           </button>
          
//           <input
//             type="text"
//             value={prompt}
//             onChange={(e) => setPrompt(e.target.value)}
//             placeholder={attachedFile ? "Ask a question about the file..." : "Ask me anything..."}
//             className="flex-1 p-2 border border-gray-300 focus:outline-none focus:ring-2 focus:ring-blue-500"
//             disabled={isLoading}
//           />

//           <button
//             type="submit"
//             className="p-2 bg-blue-500 text-white rounded-r-lg hover:bg-blue-600 disabled:bg-blue-300"
//             disabled={isLoading || (!prompt.trim() && !attachedFile)}
//           >
//             {isLoading ? 'Sending...' : 'Send'}
//           </button>
//         </div>
//         </form>
//       </div>
//     </div>
//   );
// }
// "use client";

// import { useState, FormEvent, useEffect, useRef } from 'react';
// import { useSession } from "next-auth/react";
// import apiClient from '../lib/api';
// import FileUploader from './FileUploader';
// import { useChat } from '../context/ChatContext';
// import { FaSave } from 'react-icons/fa'; // Import the save icon

// // Type for API response
// interface FileMetadata {
//   id: string;
//   file_name: string;
// }

// export default function ChatWindow() {
//   // Local state for UI elements controlled by this component
//   const [prompt, setPrompt] = useState('');
//   const [isLoading, setIsLoading] = useState(false);
//   const [isUploaderOpen, setIsUploaderOpen] = useState(false);
//   const [attachedFile, setAttachedFile] = useState<File | null>(null);
//   const [showSaveModal, setShowSaveModal] = useState(false);
//   const [chatTitle, setChatTitle] = useState("");

//   // Shared state from our global context
//   const { 
//     conversation, 
//     addMessage, 
//     conversationId, 
//     setConversationId,
//     clearChat
//   } = useChat();

//   const { data: session } = useSession();
//   const chatEndRef = useRef<HTMLDivElement>(null);

//   // Effect to scroll to the bottom of the chat on new messages
//   useEffect(() => {
//     chatEndRef.current?.scrollIntoView({ behavior: "smooth" });
//   }, [conversation]);

//   // Handler for submitting the main chat form
//   const handleSubmit = async (e: FormEvent) => {
//     e.preventDefault();
//     if (isLoading || (!prompt.trim() && !attachedFile)) return;

//     setIsLoading(true);
//     const userQuery = prompt;

//     if (userQuery) {
//         addMessage({ role: 'user', message: userQuery });
//     }
    
//     setPrompt('');
//     setAttachedFile(null); 

//     let uploadedFileId: string | null = null;

//     try {
//       if (attachedFile) {
//         addMessage({ role: 'ai', message: `Uploading ${attachedFile.name}...` });
        
//         const formData = new FormData();
//         formData.append('file', attachedFile);
//         if (session?.user?.email) {
//           formData.append('user_email', session.user.email);
//         }

//         const uploadResponse = await apiClient.post<FileMetadata>('/api/files/upload', formData);
//         uploadedFileId = uploadResponse.data.id;
        
//         addMessage({ role: 'ai', message: `✅ Processing ${uploadResponse.data.file_name}...` });
//       }

//       const response = await apiClient.post('/api/chat', {
//         prompt: userQuery,
//         conversation_id: conversationId,
//         user_email: session?.user?.email,
//         file_id: uploadedFileId,
//       });

//       const data = response.data;
//       addMessage({ role: 'ai', message: data.response });
//       setConversationId(data.conversation_id);

//     } catch (error) {
//       console.error("An error occurred:", error);
//       addMessage({ role: 'ai', message: 'Sorry, an error occurred. Please try again.' });
//     } finally {
//       setIsLoading(false);
//     }
//   };

//   // Handler for saving the chat title from the modal
//   const handleSaveChat = async () => {
//     if (!chatTitle.trim() || !conversationId) {
//         alert("Please enter a title for the chat.");
//         return;
//     }
//     try {
//         await apiClient.put(
//             `/api/conversations/${conversationId}/title`, 
//             { new_title: chatTitle }, // FastAPI's embed=True requires this object structure
//             // Our insecure auth needs the user_email in the body
//             // A proper JWT auth would not need this.
//             { data: { user_email: session?.user?.email } }
//         );
//         alert("Chat saved successfully!");
//         setShowSaveModal(false);
//         setChatTitle("");
//         clearChat(); // Start a new chat after saving
//     } catch (err) {
//         console.error("Failed to save chat title:", err);
//         alert("Could not save the chat title.");
//     }
//   };


//   return (
//     <div className="flex flex-col h-[calc(100vh-4rem)] max-w-2xl mx-auto pt-4 bg-gray-50">
      
//       {/* Save Modal */}
//       {showSaveModal && (
//         <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
//             <div className="bg-white p-6 rounded-lg shadow-xl w-full max-w-sm">
//                 <h3 className="text-lg font-bold mb-4">Save Conversation</h3>
//                 <p className="text-sm text-gray-600 mb-4">Give this chat a title to find it later in "Past Chats".</p>
//                 <input
//                     type="text"
//                     value={chatTitle}
//                     onChange={(e) => setChatTitle(e.target.value)}
//                     placeholder="e.g., Sarah's Color Research"
//                     className="w-full p-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500"
//                 />
//                 <div className="mt-6 flex justify-end space-x-3">
//                     <button onClick={() => setShowSaveModal(false)} className="px-4 py-2 bg-gray-200 text-gray-800 rounded-md hover:bg-gray-300">Cancel</button>
//                     <button onClick={handleSaveChat} className="px-4 py-2 bg-blue-500 text-white rounded-md hover:bg-blue-600">Save & New Chat</button>
//                 </div>
//             </div>
//         </div>
//       )}

//       {/* File Uploader Modal */}
//       {isUploaderOpen && (
//         <FileUploader 
//           onFileSelect={(file) => setAttachedFile(file)} 
//           onClose={() => setIsUploaderOpen(false)} 
//         />
//       )}
      
//       {/* Chat Messages Area */}
//       <div className="flex-1 overflow-y-auto p-4 bg-white rounded-lg shadow-md mx-4">
//         {conversation.map((msg, index) => (
//           <div key={index} className={`my-2 p-3 rounded-lg ${msg.role === 'user' ? 'bg-blue-100 ml-auto' : 'bg-gray-200 mr-auto'}`} style={{ maxWidth: '80%' }}>
//             <p className="font-semibold capitalize">{msg.role}</p>
//             <p className="whitespace-pre-wrap">{msg.message}</p>
//           </div>
//         ))}
//         {isLoading && (
//           <div className="my-2 p-3 rounded-lg bg-gray-200 mr-auto animate-pulse" style={{ maxWidth: '80%' }}>
//             <p className="font-semibold capitalize">AI</p>
//             <p>Thinking...</p>
//           </div>
//         )}
//         <div ref={chatEndRef} />
//       </div>

//       {/* Input Form Area */}
//       <div className="mt-4 px-4 sm:px-0">
//         {attachedFile && (
//           <div className="mb-2 p-2 bg-gray-100 rounded-lg flex justify-between items-center text-sm">
//             <span className='truncate pr-2'>📎 {attachedFile.name}</span>
//             <button type="button" onClick={() => setAttachedFile(null)} className="text-red-500 hover:text-red-700 font-bold flex-shrink-0" aria-label="Remove attached file">×</button>
//           </div>
//         )}
//         <div className="flex items-center space-x-2">
//             <button onClick={clearChat} className="p-2 border border-gray-300 rounded-lg hover:bg-gray-100" title="New Chat">+</button>
//             <form onSubmit={handleSubmit} className="flex-1 flex">
//                 <button type="button" onClick={() => setIsUploaderOpen(true)} className="p-2 border border-r-0 border-gray-300 bg-gray-100 text-gray-600 rounded-l-lg hover:bg-gray-200" aria-label="Attach file">
//                     <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15.172 7l-6.586 6.586a2 2 0 102.828 2.828l6.414-6.586a4 4 0 00-5.656-5.656l-6.415 6.585a6 6 0 108.486 8.486L20.5 13" /></svg>
//                 </button>
//                 <input
//                     type="text"
//                     value={prompt}
//                     onChange={(e) => setPrompt(e.target.value)}
//                     placeholder={attachedFile ? "Ask a question about the file..." : "Ask me anything..."}
//                     className="flex-1 p-2 border border-gray-300 focus:outline-none focus:ring-2 focus:ring-blue-500"
//                     disabled={isLoading}
//                 />
//                 <button type="submit" className="p-2 bg-blue-500 text-white rounded-r-lg hover:bg-blue-600 disabled:bg-blue-300" disabled={isLoading || (!prompt.trim() && !attachedFile)}>
//                     {isLoading ? 'Sending...' : 'Send'}
//                 </button>
//             </form>
//             <button 
//                 onClick={() => setShowSaveModal(true)}
//                 className="p-2 border border-gray-300 rounded-lg hover:bg-gray-100 disabled:opacity-50 disabled:cursor-not-allowed"
//                 title="Save Chat"
//                 disabled={!conversationId || conversation.length < 2}
//             >
//                 <FaSave />
//             </button>
//         </div>
//       </div>
//     </div>
//   );
// }

// "use client";

// import { useState, FormEvent, useEffect, useRef } from 'react';
// import { useSession } from "next-auth/react";
// import apiClient from '../lib/api';
// import { useChat } from '../context/ChatContext';
// import { FaSave, FaPlus } from 'react-icons/fa';
// import FileSelectionPanel from './FileSelectionPanel';

// export default function ChatWindow() {
//   // UI State
//   const [prompt, setPrompt] = useState('');
//   const [isLoading, setIsLoading] = useState(false);
//   const [showSaveModal, setShowSaveModal] = useState(false);
//   const [chatTitle, setChatTitle] = useState("");

//   // State for selected files from the side panel
//   const [selectedFileIds, setSelectedFileIds] = useState<string[]>([]);

//   // Global Chat State
//   const {
//     conversation,
//     addMessage,
//     conversationId,
//     setConversationId,
//     clearChat
//   } = useChat();

//   const { data: session } = useSession();
//   const chatEndRef = useRef<HTMLDivElement>(null);

//   // Scroll to bottom on new message
//   useEffect(() => {
//     chatEndRef.current?.scrollIntoView({ behavior: "smooth" });
//   }, [conversation]);

//   // Main chat submission handler
//   const handleSubmit = async (e: FormEvent) => {
//     e.preventDefault();
//     if (isLoading || !prompt.trim()) return;

//     setIsLoading(true);
//     const userQuery = prompt;
//     addMessage({ role: 'user', message: userQuery });
//     setPrompt('');

//     try {
//       const response = await apiClient.post('/api/chat', {
//         prompt: userQuery,
//         conversation_id: conversationId,
//         user_email: session?.user?.email,
//         selected_file_ids: selectedFileIds, // Pass the selected file IDs from the panel
//       });

//       const data = response.data;
//       addMessage({ role: 'ai', message: data.response });
//       // Ensure the conversation ID is set for subsequent messages
//       if (data.conversation_id) {
//         setConversationId(data.conversation_id);
//       }

//     } catch (error) {
//       console.error("An error occurred during chat submission:", error);
//       addMessage({ role: 'ai', message: 'Sorry, an error occurred. Please try again.' });
//     } finally {
//       setIsLoading(false);
//     }
//   };

//   // Handler for saving chat title
//   const handleSaveChat = async () => {
//     if (!chatTitle.trim() || !conversationId) {
//       alert("Please enter a title for the chat.");
//       return;
//     }
//     try {
//       // The payload needs to be structured this way for FastAPI's Body(..., embed=True)
//       const payload = { new_title: chatTitle };
//       // The auth dependency still needs the email
//       const config = { data: { user_email: session?.user?.email } };
      
//       await apiClient.put(`/api/conversations/${conversationId}/title`, payload, config);

//       alert("Chat saved successfully!");
//       setShowSaveModal(false);
//       setChatTitle("");
//       clearChat(); // Start a new chat after saving
//     } catch (err) {
//       console.error("Failed to save chat title:", err);
//       alert("Could not save the chat title.");
//     }
//   };


//   return (
//     // Main container uses flex-row to place chat and panel side-by-side
//     <div className="flex h-[calc(100vh-4rem)] bg-white">
      
//       {/* Save Modal (positioned globally, so location in JSX doesn't matter) */}
//       {showSaveModal && (
//         <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
//             <div className="bg-white p-6 rounded-lg shadow-xl w-full max-w-sm">
//                 <h3 className="text-lg font-bold mb-4">Save Conversation</h3>
//                 <p className="text-sm text-gray-600 mb-4">Give this chat a title to find it later in "Past Chats".</p>
//                 <input
//                     type="text"
//                     value={chatTitle}
//                     onChange={(e) => setChatTitle(e.target.value)}
//                     placeholder="e.g., Project Planning Notes"
//                     className="w-full p-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500"
//                 />
//                 <div className="mt-6 flex justify-end space-x-3">
//                     <button onClick={() => setShowSaveModal(false)} className="px-4 py-2 bg-gray-200 text-gray-800 rounded-md hover:bg-gray-300">Cancel</button>
//                     <button onClick={handleSaveChat} className="px-4 py-2 bg-blue-500 text-white rounded-md hover:bg-blue-600">Save & New Chat</button>
//                 </div>
//             </div>
//         </div>
//       )}
      
//       {/* Main Chat Container (takes up remaining space) */}
//       <div className="flex-1 flex flex-col p-4">
//         {/* Chat Messages Area */}
//         <div className="flex-1 overflow-y-auto p-4 bg-white rounded-lg shadow-inner border border-gray-200">
//           {conversation.map((msg, index) => (
//             <div key={index} className={`my-2 p-3 rounded-lg ${msg.role === 'user' ? 'bg-blue-100 ml-auto' : 'bg-gray-200 mr-auto'}`} style={{ maxWidth: '80%' }}>
//               <p className="font-semibold capitalize">{msg.role}</p>
//               <p className="whitespace-pre-wrap">{msg.message}</p>
//             </div>
//           ))}
//           {isLoading && (
//             <div className="my-2 p-3 rounded-lg bg-gray-200 mr-auto animate-pulse" style={{ maxWidth: '80%' }}>
//               <p className="font-semibold capitalize">AI</p>
//               <p>Thinking...</p>
//             </div>
//           )}
//           <div ref={chatEndRef} />
//         </div>

//         {/* Input Form Area */}
//         <div className="mt-4">
//           <div className="flex items-center space-x-2">
//               <button onClick={clearChat} className="p-3 border border-gray-300 rounded-lg hover:bg-gray-100" title="New Chat">
//                 <FaPlus />
//               </button>
//               <form onSubmit={handleSubmit} className="flex-1 flex">
//                   <input
//                       type="text"
//                       value={prompt}
//                       onChange={(e) => setPrompt(e.target.value)}
//                       placeholder="Ask a question..."
//                       className="flex-1 p-2.5 border border-gray-300 rounded-l-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
//                       disabled={isLoading}
//                   />
//                   <button type="submit" className="p-2.5 bg-blue-500 text-white rounded-r-lg hover:bg-blue-600 disabled:bg-blue-300" disabled={isLoading || !prompt.trim()}>
//                       {isLoading ? '...' : 'Send'}
//                   </button>
//               </form>
//               <button 
//                   onClick={() => setShowSaveModal(true)}
//                   className="p-3 border border-gray-300 rounded-lg hover:bg-gray-100 disabled:opacity-50 disabled:cursor-not-allowed"
//                   title="Save Chat"
//                   disabled={!conversationId || conversation.length < 2}
//               >
//                   <FaSave />
//               </button>
//           </div>
//         </div>
//       </div>

//       {/* NEW: File Selection Panel */}
//       <FileSelectionPanel 
//         selectedFileIds={selectedFileIds}
//         onSelectionChange={setSelectedFileIds}
//       />
//     </div>
//   );
// }
// "use client";

// import { useState, FormEvent, useEffect, useRef } from 'react';
// import { useSession } from "next-auth/react";
// import apiClient from '../lib/api';
// import { useChat } from '../context/ChatContext';
// import { FaSave, FaPlus } from 'react-icons/fa';
// import FileSelectionPanel from './FileSelectionPanel';

// export default function ChatWindow() {
//   // UI State
//   const [prompt, setPrompt] = useState('');
//   const [isLoading, setIsLoading] = useState(false);
//   const [showSaveModal, setShowSaveModal] = useState(false);
//   const [chatTitle, setChatTitle] = useState("");

//   // State for selected files from the side panel
//   const [selectedFileIds, setSelectedFileIds] = useState<string[]>([]);

//   // Global Chat State
//   const {
//     conversation,
//     addMessage,
//     conversationId,
//     setConversationId,
//     clearChat
//   } = useChat();

//   const { data: session } = useSession();
//   const chatEndRef = useRef<HTMLDivElement>(null);

//   // Scroll to bottom on new message
//   useEffect(() => {
//     chatEndRef.current?.scrollIntoView({ behavior: "smooth" });
//   }, [conversation]);

//   // Main chat submission handler
//   const handleSubmit = async (e: FormEvent) => {
//     e.preventDefault();
//     if (isLoading || !prompt.trim()) return;

//     setIsLoading(true);
//     const userQuery = prompt;
//     addMessage({ role: 'user', message: userQuery });
//     setPrompt('');

//     try {
//       const response = await apiClient.post('/api/chat', {
//         prompt: userQuery,
//         conversation_id: conversationId,
//         user_email: session?.user?.email,
//         selected_file_ids: selectedFileIds,
//       });

//       const data = response.data;
//       addMessage({ role: 'ai', message: data.response });
//       if (data.conversation_id) {
//         setConversationId(data.conversation_id);
//       }

//     } catch (error) {
//       console.error("An error occurred during chat submission:", error);
//       addMessage({ role: 'ai', message: 'Sorry, an error occurred. Please try again.' });
//     } finally {
//       setIsLoading(false);
//     }
//   };

//   // Handler for saving chat title
//   const handleSaveChat = async () => {
//     if (!chatTitle.trim() || !conversationId) {
//         alert("Please enter a title for the chat.");
//         return;
//     }
//     try {
//         // --- THIS IS THE FIX ---
//         // Combine everything the backend needs into a single payload object.
//         const payload = {
//           new_title: chatTitle,
//           user_email: session?.user?.email // Add email to the main body
//         };

//         // Call apiClient.put with just the url and the single payload.
//         await apiClient.put(`/api/conversations/${conversationId}/title`, payload);
//         // --- END FIX ---

//         alert("Chat saved successfully!");
//         setShowSaveModal(false);
//         setChatTitle("");
//         clearChat(); // Start a new chat after saving
//     } catch (err) {
//         console.error("Failed to save chat title:", err);
//         alert("Could not save the chat title.");
//     }
//   };


//   return (
//     // Main container uses flex-row to place chat and panel side-by-side
//     <div className="flex h-[calc(100vh-4rem)] bg-white">
      
//       {/* Save Modal */}
//       {showSaveModal && (
//         <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
//             <div className="bg-white p-6 rounded-lg shadow-xl w-full max-w-sm">
//                 <h3 className="text-lg font-bold mb-4">Save Conversation</h3>
//                 <p className="text-sm text-gray-600 mb-4">Give this chat a title to find it later in "Past Chats".</p>
//                 <input
//                     type="text"
//                     value={chatTitle}
//                     onChange={(e) => setChatTitle(e.target.value)}
//                     placeholder="e.g., Project Planning Notes"
//                     className="w-full p-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500"
//                 />
//                 <div className="mt-6 flex justify-end space-x-3">
//                     <button onClick={() => setShowSaveModal(false)} className="px-4 py-2 bg-gray-200 text-gray-800 rounded-md hover:bg-gray-300">Cancel</button>
//                     <button onClick={handleSaveChat} className="px-4 py-2 bg-blue-500 text-white rounded-md hover:bg-blue-600">Save & New Chat</button>
//                 </div>
//             </div>
//         </div>
//       )}
      
//       {/* Main Chat Container */}
//       <div className="flex-1 flex flex-col p-4">
//         {/* Chat Messages Area */}
//         <div className="flex-1 overflow-y-auto p-4 bg-white rounded-lg shadow-inner border border-gray-200">
//           {conversation.map((msg, index) => (
//             <div key={index} className={`my-2 p-3 rounded-lg ${msg.role === 'user' ? 'bg-blue-100 ml-auto' : 'bg-gray-200 mr-auto'}`} style={{ maxWidth: '80%' }}>
//               <p className="font-semibold capitalize">{msg.role}</p>
//               <p className="whitespace-pre-wrap">{msg.message}</p>
//             </div>
//           ))}
//           {isLoading && (
//             <div className="my-2 p-3 rounded-lg bg-gray-200 mr-auto animate-pulse" style={{ maxWidth: '80%' }}>
//               <p className="font-semibold capitalize">AI</p>
//               <p>Thinking...</p>
//             </div>
//           )}
//           <div ref={chatEndRef} />
//         </div>

//         {/* Input Form Area */}
//         <div className="mt-4">
//           <div className="flex items-center space-x-2">
//               <button onClick={clearChat} className="p-3 border border-gray-300 rounded-lg hover:bg-gray-100" title="New Chat">
//                 <FaPlus />
//               </button>
//               <form onSubmit={handleSubmit} className="flex-1 flex">
//                   <input
//                       type="text"
//                       value={prompt}
//                       onChange={(e) => setPrompt(e.target.value)}
//                       placeholder="Ask a question..."
//                       className="flex-1 p-2.5 border border-gray-300 rounded-l-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
//                       disabled={isLoading}
//                   />
//                   <button type="submit" className="p-2.5 bg-blue-500 text-white rounded-r-lg hover:bg-blue-600 disabled:bg-blue-300" disabled={isLoading || !prompt.trim()}>
//                       {isLoading ? '...' : 'Send'}
//                   </button>
//               </form>
//               <button 
//                   onClick={() => setShowSaveModal(true)}
//                   className="p-3 border border-gray-300 rounded-lg hover:bg-gray-100 disabled:opacity-50 disabled:cursor-not-allowed"
//                   title="Save Chat"
//                   disabled={!conversationId || conversation.length < 2}
//               >
//                   <FaSave />
//               </button>
//           </div>
//         </div>
//       </div>

//       {/* File Selection Panel */}
//       <FileSelectionPanel 
//         selectedFileIds={selectedFileIds}
//         onSelectionChange={setSelectedFileIds}
//       />
//     </div>
//   );
// }

// "use client";

// import { useState, FormEvent, useEffect, useRef } from 'react';
// import { useSession } from "next-auth/react";
// import apiClient from '../lib/api';
// import { useChat } from '../context/ChatContext';
// import { FaSave, FaPlus } from 'react-icons/fa';
// import FileSelectionPanel from './FileSelectionPanel';

// export default function ChatWindow() {
//   // UI State
//   const [prompt, setPrompt] = useState('');
//   const [isLoading, setIsLoading] = useState(false);
//   const [showSaveModal, setShowSaveModal] = useState(false);
//   const [chatTitle, setChatTitle] = useState("");

//   // State for context and model selection
//   const [selectedFileIds, setSelectedFileIds] = useState<string[]>([]);
//   // NEW: Add state for the selected model
//   const [selectedModel, setSelectedModel] = useState<string>("llama3:8b");

//   // Global Chat State
//   const {
//     conversation,
//     addMessage,
//     conversationId,
//     setConversationId,
//     clearChat
//   } = useChat();

//   const { data: session } = useSession();
//   const chatEndRef = useRef<HTMLDivElement>(null);

//   // Scroll to bottom on new message
//   useEffect(() => {
//     chatEndRef.current?.scrollIntoView({ behavior: "smooth" });
//   }, [conversation]);

//   // Main chat submission handler
//   const handleSubmit = async (e: FormEvent) => {
//     e.preventDefault();
//     if (isLoading || !prompt.trim()) return;

//     setIsLoading(true);
//     const userQuery = prompt;
//     addMessage({ role: 'user', message: userQuery });
//     setPrompt('');

//     try {
//       // Add the selected model to the API request payload
//       const response = await apiClient.post('/api/chat', {
//         prompt: userQuery,
//         conversation_id: conversationId,
//         user_email: session?.user?.email,
//         selected_file_ids: selectedFileIds,
//         selected_model: selectedModel, // <-- Pass the selected model
//       });

//       const data = response.data;
//       addMessage({ role: 'ai', message: data.response });
//       if (data.conversation_id) {
//         setConversationId(data.conversation_id);
//       }

//     } catch (error) {
//       console.error("An error occurred during chat submission:", error);
//       addMessage({ role: 'ai', message: 'Sorry, an error occurred. Please try again.' });
//     } finally {
//       setIsLoading(false);
//     }
//   };

//   // Handler for saving chat title
//   const handleSaveChat = async () => {
//     if (!chatTitle.trim() || !conversationId) {
//       alert("Please enter a title for the chat.");
//       return;
//     }
//     try {
//       const payload = {
//         new_title: chatTitle,
//         user_email: session?.user?.email
//       };
//       await apiClient.put(`/api/conversations/${conversationId}/title`, payload);

//       alert("Chat saved successfully!");
//       setShowSaveModal(false);
//       setChatTitle("");
//       clearChat();
//     } catch (err) {
//       console.error("Failed to save chat title:", err);
//       alert("Could not save the chat title.");
//     }
//   };


//   return (
//     <div className="flex h-[calc(100vh-4rem)] bg-white">
      
//       {/* Save Modal */}
//       {showSaveModal && (
//         <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
//             <div className="bg-white p-6 rounded-lg shadow-xl w-full max-w-sm">
//                 <h3 className="text-lg font-bold mb-4">Save Conversation</h3>
//                 <p className="text-sm text-gray-600 mb-4">Give this chat a title to find it later in "Past Chats".</p>
//                 <input
//                     type="text"
//                     value={chatTitle}
//                     onChange={(e) => setChatTitle(e.target.value)}
//                     placeholder="e.g., Project Planning Notes"
//                     className="w-full p-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500"
//                 />
//                 <div className="mt-6 flex justify-end space-x-3">
//                     <button onClick={() => setShowSaveModal(false)} className="px-4 py-2 bg-gray-200 text-gray-800 rounded-md hover:bg-gray-300">Cancel</button>
//                     <button onClick={handleSaveChat} className="px-4 py-2 bg-blue-500 text-white rounded-md hover:bg-blue-600">Save & New Chat</button>
//                 </div>
//             </div>
//         </div>
//       )}
      
//       {/* Main Chat Container */}
//       <div className="flex-1 flex flex-col p-4">
//         {/* Chat Messages Area */}
//         <div className="flex-1 overflow-y-auto p-4 bg-white rounded-lg shadow-inner border border-gray-200">
//           {conversation.map((msg, index) => (
//             <div key={index} className={`my-2 p-3 rounded-lg ${msg.role === 'user' ? 'bg-blue-100 ml-auto' : 'bg-gray-200 mr-auto'}`} style={{ maxWidth: '80%' }}>
//               <p className="font-semibold capitalize">{msg.role}</p>
//               <p className="whitespace-pre-wrap">{msg.message}</p>
//             </div>
//           ))}
//           {isLoading && (
//             <div className="my-2 p-3 rounded-lg bg-gray-200 mr-auto animate-pulse" style={{ maxWidth: '80%' }}>
//               <p className="font-semibold capitalize">AI</p>
//               <p>Thinking...</p>
//             </div>
//           )}
//           <div ref={chatEndRef} />
//         </div>

//         {/* Input Form Area */}
//         <div className="mt-4">
//           <div className="flex items-center space-x-2">
//               <button onClick={clearChat} className="p-3 border border-gray-300 rounded-lg hover:bg-gray-100" title="New Chat">
//                 <FaPlus />
//               </button>
//               <form onSubmit={handleSubmit} className="flex-1 flex">
//                   <input
//                       type="text"
//                       value={prompt}
//                       onChange={(e) => setPrompt(e.target.value)}
//                       placeholder="Ask a question..."
//                       className="flex-1 p-2.5 border border-gray-300 rounded-l-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
//                       disabled={isLoading}
//                   />
//                   <button type="submit" className="p-2.5 bg-blue-500 text-white rounded-r-lg hover:bg-blue-600 disabled:bg-blue-300" disabled={isLoading || !prompt.trim()}>
//                       {isLoading ? '...' : 'Send'}
//                   </button>
//               </form>
//               <button 
//                   onClick={() => setShowSaveModal(true)}
//                   className="p-3 border border-gray-300 rounded-lg hover:bg-gray-100 disabled:opacity-50 disabled:cursor-not-allowed"
//                   title="Save Chat"
//                   disabled={!conversationId || conversation.length < 2}
//               >
//                   <FaSave />
//               </button>
//           </div>
//         </div>
//       </div>

//       {/* File Selection Panel */}
//       <FileSelectionPanel 
//         selectedFileIds={selectedFileIds}
//         onSelectionChange={setSelectedFileIds}
//         // Pass the new model selection state and handler down
//         selectedModel={selectedModel}
//         onModelChange={setSelectedModel}
//       />
//     </div>
//   );
// }
// "use client";

// import { useState, FormEvent, useEffect, useRef } from 'react';
// import { useSession } from "next-auth/react";
// import apiClient from '../lib/api';
// import { useChat } from '../context/ChatContext';
// import { FaSave, FaPlus } from 'react-icons/fa';
// import FileSelectionPanel from './FileSelectionPanel';
// import PromptEditorModal from './PromptEditorModal'; // Import the new modal

// // --- Default Prompt Templates ---
// const DEFAULT_RAG_PROMPT = `You are an expert assistant. Use ONLY the following pieces of context to answer the user's question.
// If the answer is not in the context, just say you don't have enough information from the documents.

// CONTEXT:
// {context}

// QUESTION:
// {question}

// ANSWER:`;

// const DEFAULT_CODE_PROMPT = `You are an expert programmer and master of algorithms. Provide a clear, concise, and correct code solution to the user's request.
// Explain the code briefly if necessary. Use the following context if it is relevant.

// CONTEXT:
// {context}

// REQUEST:
// {question}

// CODE:`;

// const DEFAULT_PROMPTS: { [key: string]: string } = {
//     "codellama": DEFAULT_CODE_PROMPT,
//     "dolphin-mistral:7b": DEFAULT_CODE_PROMPT,
// };

// export default function ChatWindow() {
//   // UI State
//   const [prompt, setPrompt] = useState('');
//   const [isLoading, setIsLoading] = useState(false);
//   const [showSaveModal, setShowSaveModal] = useState(false);
//   const [chatTitle, setChatTitle] = useState("");

//   // State for context, model, and prompt selection
//   const [selectedFileIds, setSelectedFileIds] = useState<string[]>([]);
//   const [selectedModel, setSelectedModel] = useState<string>("llama3:8b");
//   const [promptTemplateText, setPromptTemplateText] = useState<string>(DEFAULT_RAG_PROMPT);
//   const [isPromptModalOpen, setIsPromptModalOpen] = useState(false);

//   // Global Chat State
//   const { conversation, addMessage, conversationId, setConversationId, clearChat } = useChat();
//   const { data: session } = useSession();
//   const chatEndRef = useRef<HTMLDivElement>(null);

//   // Effect to scroll to the bottom on new message
//   useEffect(() => {
//     chatEndRef.current?.scrollIntoView({ behavior: "smooth" });
//   }, [conversation]);

//   // Effect to update prompt template when the model changes
//   useEffect(() => {
//     const defaultPrompt = DEFAULT_PROMPTS[selectedModel] || DEFAULT_RAG_PROMPT;
//     setPromptTemplateText(defaultPrompt);
//   }, [selectedModel]);

//   // Main chat submission handler
//   const handleSubmit = async (e: FormEvent) => {
//     e.preventDefault();
//     if (isLoading || !prompt.trim()) return;

//     setIsLoading(true);
//     const userQuery = prompt;
//     addMessage({ role: 'user', message: userQuery });
//     setPrompt('');

//     try {
//       const response = await apiClient.post('/api/chat', {
//         prompt: userQuery,
//         conversation_id: conversationId,
//         user_email: session?.user?.email,
//         selected_file_ids: selectedFileIds,
//         selected_model: selectedModel,
//         custom_prompt_template: promptTemplateText, // Pass the custom prompt
//       });

//       const data = response.data;
//       addMessage({ role: 'ai', message: data.response });
//       if (data.conversation_id) {
//         setConversationId(data.conversation_id);
//       }

//     } catch (error) {
//       console.error("An error occurred during chat submission:", error);
//       addMessage({ role: 'ai', message: 'Sorry, an error occurred. Please try again.' });
//     } finally {
//       setIsLoading(false);
//     }
//   };

//   // Handler for saving chat title
//   const handleSaveChat = async () => {
//     if (!chatTitle.trim() || !conversationId) {
//       alert("Please enter a title for the chat.");
//       return;
//     }
//     try {
//       const payload = {
//         new_title: chatTitle,
//         user_email: session?.user?.email
//       };
//       await apiClient.put(`/api/conversations/${conversationId}/title`, payload);
//       alert("Chat saved successfully!");
//       setShowSaveModal(false);
//       setChatTitle("");
//       clearChat();
//     } catch (err) {
//       console.error("Failed to save chat title:", err);
//       alert("Could not save the chat title.");
//     }
//   };

//   return (
//     <>
//       {/* The new modal for editing the prompt */}
//       <PromptEditorModal
//         isOpen={isPromptModalOpen}
//         onClose={() => setIsPromptModalOpen(false)}
//         initialPrompt={promptTemplateText}
//         onSave={(newPrompt) => setPromptTemplateText(newPrompt)}
//       />

//       <div className="flex h-[calc(100vh-4rem)] bg-white">
        
//         {/* Save Modal */}
//         {showSaveModal && (
//           <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
//               <div className="bg-white p-6 rounded-lg shadow-xl w-full max-w-sm">
//                   <h3 className="text-lg font-bold mb-4">Save Conversation</h3>
//                   <p className="text-sm text-gray-600 mb-4">Give this chat a title to find it later in "Past Chats".</p>
//                   <input
//                       type="text"
//                       value={chatTitle}
//                       onChange={(e) => setChatTitle(e.target.value)}
//                       placeholder="e.g., Project Planning Notes"
//                       className="w-full p-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500"
//                   />
//                   <div className="mt-6 flex justify-end space-x-3">
//                       <button onClick={() => setShowSaveModal(false)} className="px-4 py-2 bg-gray-200 text-gray-800 rounded-md hover:bg-gray-300">Cancel</button>
//                       <button onClick={handleSaveChat} className="px-4 py-2 bg-blue-500 text-white rounded-md hover:bg-blue-600">Save & New Chat</button>
//                   </div>
//               </div>
//           </div>
//         )}
        
//         {/* Main Chat Container */}
//         <div className="flex-1 flex flex-col p-4">
//           {/* Chat Messages Area */}
//           <div className="flex-1 overflow-y-auto p-4 bg-white rounded-lg shadow-inner border border-gray-200">
//             {conversation.map((msg, index) => (
//               <div key={index} className={`my-2 p-3 rounded-lg ${msg.role === 'user' ? 'bg-blue-100 ml-auto' : 'bg-gray-200 mr-auto'}`} style={{ maxWidth: '80%' }}>
//                 <p className="font-semibold capitalize">{msg.role}</p>
//                 <p className="whitespace-pre-wrap">{msg.message}</p>
//               </div>
//             ))}
//             {isLoading && (
//               <div className="my-2 p-3 rounded-lg bg-gray-200 mr-auto animate-pulse" style={{ maxWidth: '80%' }}>
//                 <p className="font-semibold capitalize">AI</p>
//                 <p>Thinking...</p>
//               </div>
//             )}
//             <div ref={chatEndRef} />
//           </div>

//           {/* Input Form Area */}
//           <div className="mt-4">
//             <div className="flex items-center space-x-2">
//                 <button onClick={clearChat} className="p-3 border border-gray-300 rounded-lg hover:bg-gray-100" title="New Chat">
//                   <FaPlus />
//                 </button>
//                 <form onSubmit={handleSubmit} className="flex-1 flex">
//                     <input
//                         type="text"
//                         value={prompt}
//                         onChange={(e) => setPrompt(e.target.value)}
//                         placeholder="Ask a question..."
//                         className="flex-1 p-2.5 border border-gray-300 rounded-l-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
//                         disabled={isLoading}
//                     />
//                     <button type="submit" className="p-2.5 bg-blue-500 text-white rounded-r-lg hover:bg-blue-600 disabled:bg-blue-300" disabled={isLoading || !prompt.trim()}>
//                         {isLoading ? '...' : 'Send'}
//                     </button>
//                 </form>
//                 <button 
//                     onClick={() => setShowSaveModal(true)}
//                     className="p-3 border border-gray-300 rounded-lg hover:bg-gray-100 disabled:opacity-50 disabled:cursor-not-allowed"
//                     title="Save Chat"
//                     disabled={!conversationId || conversation.length < 2}
//                 >
//                     <FaSave />
//                 </button>
//             </div>
//           </div>
//         </div>

//         {/* File Selection Panel */}
//         <FileSelectionPanel 
//           selectedFileIds={selectedFileIds}
//           onSelectionChange={setSelectedFileIds}
//           selectedModel={selectedModel}
//           onModelChange={setSelectedModel}
//           onEditPrompt={() => setIsPromptModalOpen(true)}
//         />
//       </div>
//     </>
//   );
// }

// "use client";

// import { useState, FormEvent, useEffect, useRef } from 'react';
// import { useSession } from "next-auth/react";
// import apiClient from '../lib/api';
// import { useChat } from '../context/ChatContext';
// import { FaSave, FaPlus } from 'react-icons/fa';
// import FileSelectionPanel from './FileSelectionPanel';
// import PromptEditorModal from './PromptEditorModal';

// const DEFAULT_RAG_PROMPT = `You are an expert assistant. Use ONLY the following pieces of context to answer the user's question.\nIf the answer is not in the context, just say you don't have enough information from the documents.\n\nCONTEXT:\n{context}\n\nQUESTION:\n{question}\n\nANSWER:`;
// const DEFAULT_CODE_PROMPT = `You are an expert programmer and master of algorithms. Provide a clear, concise, and correct code solution to the user's request.\nExplain the code briefly if necessary. Use the following context if it is relevant.\n\nCONTEXT:\n{context}\n\nREQUEST:\n{question}\n\nCODE:`;
// const DEFAULT_PROMPTS: { [key: string]: string } = { "codellama": DEFAULT_CODE_PROMPT, "dolphin-mistral:7b": DEFAULT_CODE_PROMPT };

// export default function ChatWindow() {
//   const [prompt, setPrompt] = useState('');
//   const [isLoading, setIsLoading] = useState(false);
//   const [showSaveModal, setShowSaveModal] = useState(false);
//   const [chatTitle, setChatTitle] = useState("");
//   const [selectedFileIds, setSelectedFileIds] = useState<string[]>([]);
//   const [selectedModel, setSelectedModel] = useState<string>("llama3:8b");
//   const [promptTemplateText, setPromptTemplateText] = useState<string>(DEFAULT_RAG_PROMPT);
//   const [isPromptModalOpen, setIsPromptModalOpen] = useState(false);

//   // --- NEW STATE FOR PARAMETERS ---
//   const [temperature, setTemperature] = useState(0.8);
//   const [topP, setTopP] = useState(1.0);
//   const [maxTokens, setMaxTokens] = useState(1024);
//   const [lastTokenCount, setLastTokenCount] = useState(null);

//   const { conversation, addMessage, conversationId, setConversationId, clearChat } = useChat();
//   const { data: session } = useSession();
//   const chatEndRef = useRef<HTMLDivElement>(null);

//   useEffect(() => { chatEndRef.current?.scrollIntoView({ behavior: "smooth" }); }, [conversation]);
//   useEffect(() => {
//     const defaultPrompt = DEFAULT_PROMPTS[selectedModel] || DEFAULT_RAG_PROMPT;
//     setPromptTemplateText(defaultPrompt);
//   }, [selectedModel]);

//   const handleSubmit = async (e: FormEvent) => {
//     e.preventDefault();
//     if (isLoading || !prompt.trim()) return;
//     setIsLoading(true);
//     const userQuery = prompt;
//     addMessage({ role: 'user', message: userQuery });
//     setPrompt('');

//     try {
//       const response = await apiClient.post('/api/chat', {
//         prompt: userQuery,
//         conversation_id: conversationId,
//         user_email: session?.user?.email,
//         selected_file_ids: selectedFileIds,
//         selected_model: selectedModel,
//         custom_prompt_template: promptTemplateText,
//         // Add new parameters to the request payload
//         temperature: temperature,
//         top_p: topP,
//         max_tokens: maxTokens,
//       });

//       const data = response.data;
//       addMessage({ role: 'ai', message: data.response });
//       // Update token count display from the response
//       if (data.token_counts) {
//         setLastTokenCount(data.token_counts);
//       }
//       if (data.conversation_id) {
//         setConversationId(data.conversation_id);
//       }
//     } catch (error) {
//       console.error("An error occurred during chat submission:", error);
//       addMessage({ role: 'ai', message: 'Sorry, an error occurred. Please try again.' });
//     } finally {
//       setIsLoading(false);
//     }
//   };

//   const handleSaveChat = async () => {
//     if (!chatTitle.trim() || !conversationId) return alert("Please enter a title for the chat.");
//     try {
//       await apiClient.put(`/api/conversations/${conversationId}/title`, { new_title: chatTitle, user_email: session?.user?.email });
//       alert("Chat saved successfully!");
//       setShowSaveModal(false);
//       setChatTitle("");
//       clearChat();
//     } catch (err) {
//       console.error("Failed to save chat title:", err);
//       alert("Could not save the chat title.");
//     }
//   };

//   return (
//     <>
//       <PromptEditorModal isOpen={isPromptModalOpen} onClose={() => setIsPromptModalOpen(false)} initialPrompt={promptTemplateText} onSave={(newPrompt) => setPromptTemplateText(newPrompt)} />
//       <div className="flex h-[calc(100vh-4rem)] bg-white">
//         {showSaveModal && (
//           <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
//             <div className="bg-white p-6 rounded-lg shadow-xl w-full max-w-sm">
//               <h3 className="text-lg font-bold mb-4">Save Conversation</h3>
//               <p className="text-sm text-gray-600 mb-4">Give this chat a title to find it later in "Past Chats".</p>
//               <input type="text" value={chatTitle} onChange={(e) => setChatTitle(e.target.value)} placeholder="e.g., Project Planning Notes" className="w-full p-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500" />
//               <div className="mt-6 flex justify-end space-x-3">
//                 <button onClick={() => setShowSaveModal(false)} className="px-4 py-2 bg-gray-200 text-gray-800 rounded-md hover:bg-gray-300">Cancel</button>
//                 <button onClick={handleSaveChat} className="px-4 py-2 bg-blue-500 text-white rounded-md hover:bg-blue-600">Save & New Chat</button>
//               </div>
//             </div>
//           </div>
//         )}
//         <div className="flex-1 flex flex-col p-4">
//           <div className="flex-1 overflow-y-auto p-4 bg-white rounded-lg shadow-inner border border-gray-200">
//             {conversation.map((msg, index) => (
//               <div key={index} className={`my-2 p-3 rounded-lg ${msg.role === 'user' ? 'bg-blue-100 ml-auto' : 'bg-gray-200 mr-auto'}`} style={{ maxWidth: '80%' }}>
//                 <p className="font-semibold capitalize">{msg.role}</p>
//                 <p className="whitespace-pre-wrap">{msg.message}</p>
//               </div>
//             ))}
//             {isLoading && (<div className="my-2 p-3 rounded-lg bg-gray-200 mr-auto animate-pulse" style={{ maxWidth: '80%' }}><p className="font-semibold capitalize">AI</p><p>Thinking...</p></div>)}
//             <div ref={chatEndRef} />
//           </div>
//           <div className="mt-4">
//             <div className="flex items-center space-x-2">
//               <button onClick={clearChat} className="p-3 border border-gray-300 rounded-lg hover:bg-gray-100" title="New Chat"><FaPlus /></button>
//               <form onSubmit={handleSubmit} className="flex-1 flex">
//                 <input type="text" value={prompt} onChange={(e) => setPrompt(e.target.value)} placeholder="Ask a question..." className="flex-1 p-2.5 border border-gray-300 rounded-l-lg focus:outline-none focus:ring-2 focus:ring-blue-500" disabled={isLoading} />
//                 <button type="submit" className="p-2.5 bg-blue-500 text-white rounded-r-lg hover:bg-blue-600 disabled:bg-blue-300" disabled={isLoading || !prompt.trim()}>{isLoading ? '...' : 'Send'}</button>
//               </form>
//               <button onClick={() => setShowSaveModal(true)} className="p-3 border border-gray-300 rounded-lg hover:bg-gray-100 disabled:opacity-50 disabled:cursor-not-allowed" title="Save Chat" disabled={!conversationId || conversation.length < 2}><FaSave /></button>
//             </div>
//           </div>
//         </div>
//         <FileSelectionPanel
//           selectedFileIds={selectedFileIds} onSelectionChange={setSelectedFileIds}
//           selectedModel={selectedModel} onModelChange={setSelectedModel}
//           onEditPrompt={() => setIsPromptModalOpen(true)}
//           temperature={temperature} setTemperature={setTemperature}
//           topP={topP} setTopP={setTopP}
//           maxTokens={maxTokens} setMaxTokens={setMaxTokens}
//           lastTokenCount={lastTokenCount}
//         />
//       </div>
//     </>
//   );
// }

"use client";

import { useState, FormEvent, useEffect, useRef } from 'react';
import { useSession } from "next-auth/react";
import apiClient from '../lib/api';
import { useChat } from '../context/ChatContext';
import { FaSave, FaPlus } from 'react-icons/fa';
import FileSelectionPanel from './FileSelectionPanel';
import PromptEditorModal from './PromptEditorModal';

// Default Prompt Templates
const DEFAULT_RAG_PROMPT = `You are an expert assistant. Use ONLY the following pieces of context to answer the user's question.\nIf the answer is not in the context, just say you don't have enough information from the documents.\n\nCONTEXT:\n{context}\n\nQUESTION:\n{question}\n\nANSWER:`;
const DEFAULT_CODE_PROMPT = `You are an expert programmer and master of algorithms. Provide a clear, concise, and correct code solution to the user's request.\nExplain the code briefly if necessary. Use the following context if it is relevant.\n\nCONTEXT:\n{context}\n\nREQUEST:\n{question}\n\nCODE:`;
const DEFAULT_PROMPTS: { [key: string]: string } = { "codellama": DEFAULT_CODE_PROMPT, "dolphin-mistral": DEFAULT_CODE_PROMPT, "dolphin-mistral:7b": DEFAULT_CODE_PROMPT };

export default function ChatWindow() {
  // State for UI and parameters
  const [prompt, setPrompt] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [showSaveModal, setShowSaveModal] = useState(false);
  const [chatTitle, setChatTitle] = useState("");
  const [selectedFileIds, setSelectedFileIds] = useState<string[]>([]);
  const [selectedModel, setSelectedModel] = useState<string>("llama3:8b");
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
      <div className="flex w-[calc(100vw-4rem)] h-[calc(99vh-4rem)] mx-auto p-4 bg-white">
        {showSaveModal && (
          <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
            <div className="bg-white p-6 rounded-lg shadow-xl w-full max-w-sm">
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
          <div className="flex-1 overflow-y-auto min-h-0 p-4 bg-white rounded-lg shadow-inner border border-gray-200">
            {conversation.map((msg, index) => (
              <div key={index} className={`my-2 p-3 rounded-lg ${msg.role === 'user' ? 'bg-blue-100 ml-auto' : 'bg-gray-200 mr-auto'}`} style={{ maxWidth: '80%' }}>
                <p className="font-semibold capitalize">{msg.role}</p>
                <p className="whitespace-pre-wrap">{msg.message}</p>
              </div>
            ))}
            {isLoading && (<div className="my-2 p-3 rounded-lg bg-gray-200 mr-auto animate-pulse" style={{ maxWidth: '80%' }}><p className="font-semibold capitalize">AI</p><p>Thinking...</p></div>)}
            <div ref={chatEndRef} />
          </div>

          {/* 2. Input Form Area */}
          {/* This div sits below the message area and does not grow. It is always visible. */}
          <div className="mt-4 flex-shrink-0">
            <div className="flex items-center space-x-2">
              <button onClick={clearChat} className="p-3 border border-gray-300 rounded-lg hover:bg-gray-100" title="New Chat"><FaPlus /></button>
              <form onSubmit={handleSubmit} className="flex-1 flex">
                <input type="text" value={prompt} onChange={(e) => setPrompt(e.target.value)} placeholder="Ask a question..." className="flex-1 p-2.5 border border-gray-300 rounded-l-lg focus:outline-none focus:ring-2 focus:ring-blue-500" disabled={isLoading} />
                <button type="submit" className="p-2.5 bg-blue-500 text-white rounded-r-lg hover:bg-blue-600 disabled:bg-blue-300" disabled={isLoading || !prompt.trim()}>{isLoading ? '...' : 'Send'}</button>
              </form>
              <button onClick={() => setShowSaveModal(true)} className="p-3 border border-gray-300 rounded-lg hover:bg-gray-100 disabled:opacity-50 disabled:cursor-not-allowed" title="Save Chat" disabled={!conversationId || conversation.length < 2}><FaSave /></button>
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