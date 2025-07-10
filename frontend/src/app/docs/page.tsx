// // frontend/src/app/docs/page.tsx
// "use client";

// import { useState, useEffect, FC } from 'react';
// import apiClient from '../../lib/api';
// import { useSession } from "next-auth/react";
// import { FaFilePdf, FaFileWord, FaFileAlt, FaTrashAlt } from 'react-icons/fa';

// // --- Type Definition ---
// interface FileMetadata {
//   id: string;
//   file_name: string;
//   processing_status: string;
//   chunk_count: number;
//   file_type: string;
// }

// // --- Helper Components ---
// const FileIcon: FC<{ fileType: string }> = ({ fileType }) => {
//     if (fileType.includes('pdf')) return <FaFilePdf className="text-red-500" />;
//     if (fileType.includes('word')) return <FaFileWord className="text-blue-500" />;
//     return <FaFileAlt className="text-gray-500" />;
// };

// const StatusIndicator: FC<{ status: string }> = ({ status }) => {
//     const statusStyles: { [key: string]: string } = {
//         completed: 'bg-green-500',
//         processing: 'bg-yellow-500 animate-pulse',
//         failed: 'bg-red-500',
//         uploaded: 'bg-blue-400',
//     };
//     const colorClass = statusStyles[status] || 'bg-gray-400';

//     return <span className={`inline-block w-3 h-3 rounded-full ${colorClass}`} title={status}></span>;
// }

// // --- Main Page Component ---
// export default function DocsPage() {
//     const [files, setFiles] = useState<FileMetadata[]>([]);
//     const [isLoading, setIsLoading] = useState(true);
//     const [error, setError] = useState<string | null>(null);
//     const { data: session } = useSession();

//     const fetchFiles = async () => {
//         if (!session?.user?.email) return;
//         setIsLoading(true);
//        try {
//             // Change how the request is made
//             const response = await apiClient.get('/api/files', {
//                 params: { // <-- Use 'params' to add query parameters
//                     user_email: session.user.email 
//                 }
//             });
//             setFiles(response.data);
//         } catch (err) {
//             console.error("Failed to fetch files:", err);
//             setError("Could not load your documents. Please try refreshing the page.");
//         } finally {
//             setIsLoading(false);
//         }
//     };
    
//     useEffect(() => {
//         if (session) {
//             fetchFiles();
//         }
//     }, [session]);

//     const handleDelete = async (fileId: string) => {
//         if (!window.confirm("Are you sure you want to delete this file and all its data? This cannot be undone.")) {
//             return;
//         }
        
//        try {
//             await apiClient.delete(`/api/files/${fileId}`, {
//                 params: { // <-- Use 'params' here as well
//                     user_email: session?.user?.email 
//                 }
//             });
//             setFiles(prevFiles => prevFiles.filter(file => file.id !== fileId));
//         }   catch (err) {
//             console.error("Failed to delete file:", err);
//             alert("Could not delete the file. Please try again.");
//         }
//     };

//     if (isLoading) {
//         return <div className="text-center p-8 text-gray-500">Loading documents...</div>;
//     }
    
//     if (error) {
//         return <div className="text-center p-8 text-red-500">{error}</div>;
//     }

//     return (
//         <div className="max-w-4xl mx-auto p-4 sm:p-6 lg:p-8">
//             <h1 className="text-2xl font-bold text-gray-900 mb-6">Your Documents</h1>
//             <div className="bg-white shadow-md rounded-lg overflow-hidden">
//                 <table className="min-w-full divide-y divide-gray-200">
//                     <thead className="bg-gray-50">
//                         <tr>
//                             <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">File Name</th>
//                             <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Status</th>
//                             <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Chunks</th>
//                             <th scope="col" className="relative px-6 py-3"><span className="sr-only">Delete</span></th>
//                         </tr>
//                     </thead>
//                     <tbody className="bg-white divide-y divide-gray-200">
//                         {files.length === 0 ? (
//                             <tr>
//                                 <td colSpan={4} className="px-6 py-4 text-center text-gray-500">
//                                     You haven't uploaded any documents yet. Go to the Chat page to upload one!
//                                 </td>
//                             </tr>
//                         ) : (
//                             files.map((file) => (
//                                 <tr key={file.id}>
//                                     <td className="px-6 py-4 whitespace-nowrap">
//                                         <div className="flex items-center">
//                                             <div className="text-xl mr-4 flex-shrink-0">
//                                                 <FileIcon fileType={file.file_type} />
//                                             </div>
//                                             <div className="text-sm font-medium text-gray-900 truncate">{file.file_name}</div>
//                                         </div>
//                                     </td>
//                                     <td className="px-6 py-4 whitespace-nowrap">
//                                         <div className="flex items-center space-x-2">
//                                             <StatusIndicator status={file.processing_status} />
//                                             <span className="text-sm text-gray-600 capitalize">{file.processing_status}</span>
//                                         </div>
//                                     </td>
//                                     <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500 text-center">{file.chunk_count}</td>
//                                     <td className="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
//                                         <button 
//                                             onClick={() => handleDelete(file.id)}
//                                             className="text-red-600 hover:text-red-900 transition-colors"
//                                             title="Delete File"
//                                         >
//                                             <FaTrashAlt />
//                                         </button>
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

// frontend/src/app/docs/page.tsx
"use client";

import { useState, useEffect, FC } from 'react';
import apiClient from '../../lib/api';
import { useSession } from "next-auth/react";
import { FaFilePdf, FaFileWord, FaFileAlt, FaTrashAlt } from 'react-icons/fa';

// --- Type Definition ---
interface FileMetadata {
  id: string;
  file_name: string;
  processing_status: string;
  chunk_count: number;
  file_type: string;
  upload_date: string;
}

// --- Reusable Helper Components ---
const FileIcon: FC<{ fileType: string }> = ({ fileType }) => {
    if (fileType.includes('pdf')) return <FaFilePdf className="text-red-500" />;
    if (fileType.includes('word')) return <FaFileWord className="text-blue-500" />;
    return <FaFileAlt className="text-gray-500" />;
};

const StatusIndicator: FC<{ status: string }> = ({ status }) => {
    const statusStyles: { [key: string]: string } = {
        completed: 'bg-green-500',
        processing: 'bg-yellow-500 animate-pulse',
        failed: 'bg-red-500',
        uploaded: 'bg-blue-400',
    };
    const colorClass = statusStyles[status] || 'bg-gray-400';
    return <span className={`inline-block w-3 h-3 rounded-full ${colorClass}`} title={status}></span>;
}

const FileTable: FC<{ files: FileMetadata[], onDelete: (id: string) => void, isHistory?: boolean }> = ({ files, onDelete, isHistory = false }) => (
    <div className={`bg-white shadow-md rounded-lg overflow-hidden ${isHistory ? 'opacity-80' : ''}`}>
        <table className="min-w-full divide-y divide-gray-200">
            <thead className="bg-gray-50">
                <tr>
                    <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">File Name</th>
                    {isHistory && <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Uploaded</th>}
                    <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Status</th>
                    <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Chunks</th>
                    <th scope="col" className="relative px-6 py-3"><span className="sr-only">Delete</span></th>
                </tr>
            </thead>
            <tbody className="bg-white divide-y divide-gray-200">
                {files.length === 0 ? (
                    <tr><td colSpan={isHistory ? 5 : 4} className="px-6 py-4 text-center text-gray-500">No documents found.</td></tr>
                ) : (
                    files.map((file) => (
                        <tr key={file.id}>
                            <td className="px-6 py-4 whitespace-nowrap"><div className="flex items-center"><div className="text-xl mr-4 flex-shrink-0"><FileIcon fileType={file.file_type} /></div><div className="text-sm font-medium text-gray-900 truncate">{file.file_name}</div></div></td>
                            {isHistory && <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{new Date(file.upload_date).toLocaleString()}</td>}
                            <td className="px-6 py-4 whitespace-nowrap"><div className="flex items-center space-x-2"><StatusIndicator status={file.processing_status} /><span className="text-sm text-gray-600 capitalize">{file.processing_status}</span></div></td>
                            <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500 text-center">{file.chunk_count}</td>
                            <td className="px-6 py-4 whitespace-nowrap text-right text-sm font-medium"><button onClick={() => onDelete(file.id)} className="text-red-600 hover:text-red-900 transition-colors" title="Delete File"><FaTrashAlt /></button></td>
                        </tr>
                    ))
                )}
            </tbody>
        </table>
    </div>
);

// --- Main Page Component ---
export default function DocsPage() {
    const [activeFiles, setActiveFiles] = useState<FileMetadata[]>([]);
    const [historyFiles, setHistoryFiles] = useState<FileMetadata[]>([]);
    const [showAllHistory, setShowAllHistory] = useState(false);
    const [isLoading, setIsLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);
    const { data: session } = useSession();

     const fetchFiles = async () => {
        if (!session?.user?.email) return;
        setIsLoading(true);
        setError(null);
        try {
            // Construct the URLs with query parameters manually
            const activeUrl = `/api/files/active?user_email=${encodeURIComponent(session.user.email)}`;
            const historyUrl = `/api/files/history?user_email=${encodeURIComponent(session.user.email)}&limit=${showAllHistory ? 100 : 5}`;

            const [activeRes, historyRes] = await Promise.all([
                apiClient.get(activeUrl), // Call with the simple URL
                apiClient.get(historyUrl)  // Call with the simple URL
            ]);
            setActiveFiles(activeRes.data);
            setHistoryFiles(historyRes.data);
        } catch (err) {
            console.error("Failed to fetch files:", err);
            setError("Could not load your documents. Please try refreshing the page.");
        } finally {
            setIsLoading(false);
        }
    };
    
    useEffect(() => {
        if (session) {
            fetchFiles();
        }
    }, [session, showAllHistory]);

    const getUniqueLatestFiles = (files: FileMetadata[]): FileMetadata[] => {
    if (!files || files.length === 0) {
        return [];
    }

    const latestFilesMap = new Map<string, FileMetadata>();

    for (const file of files) {
            if (!latestFilesMap.has(file.file_name)) {
                latestFilesMap.set(file.file_name, file);
            }
        }

        // Return the values from the map, which are the unique latest files.
        return Array.from(latestFilesMap.values());
    };

    const uniqueActiveFiles = getUniqueLatestFiles(activeFiles);

    const handleDelete = async (fileId: string) => {
        if (!window.confirm("Are you sure you want to delete this file and all its data? This cannot be undone.")) return;
        try {
            // Also simplify the delete call
            const deleteUrl = `/api/files/${fileId}?user_email=${encodeURIComponent(session!.user!.email!)}`;
            await apiClient.delete(deleteUrl);
            fetchFiles();
        } catch (err) {
            console.error("Failed to delete file:", err);
            alert("Could not delete the file. Please try again.");
        }
    };

    if (isLoading) return <div className="text-center p-8 text-gray-500">Loading documents...</div>;
    if (error) return <div className="text-center p-8 text-red-500">{error}</div>;

    return (
        <div className="max-w-5xl mx-auto p-4 sm:p-6 lg:p-8 space-y-12">
            {/* Section 1: Active Documents */}
            <div>
                <h1 className="text-2xl font-bold text-gray-900">Your Documents</h1>
                <p className="text-sm text-gray-500 mt-1 mb-4">These are the documents currently available for chat and retrieval.</p>
                <FileTable files={uniqueActiveFiles} onDelete={handleDelete} />
            </div>

            {/* Section 2: Upload History */}
            <div>
                <div className="flex justify-between items-center mb-4">
                    <div>
                        <h2 className="text-2xl font-bold text-gray-900">Upload History</h2>
                        <p className="text-sm text-gray-500 mt-1">A log of your most recent upload attempts.</p>
                    </div>
                    {historyFiles.length > 5 && (
                        <button 
                            onClick={() => setShowAllHistory(!showAllHistory)}
                            className="text-sm font-medium text-blue-600 hover:text-blue-800"
                        >
                            {showAllHistory ? 'Show Less' : 'Show All'}
                        </button>
                    )}
                </div>
                <FileTable files={historyFiles} onDelete={handleDelete} isHistory={true} />
            </div>
        </div>
    );
}