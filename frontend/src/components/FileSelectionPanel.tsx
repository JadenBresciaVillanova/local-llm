// "use client";

// import { useState, useEffect, FC } from 'react';
// import apiClient from '../lib/api';
// import { useSession } from "next-auth/react";
// import { FaFilePdf, FaFileWord, FaFileAlt, FaSync } from 'react-icons/fa';
// import FileUploader from './FileUploader'; // Import the uploader

// // --- Type Definition ---
// interface FileMetadata {
//   id: string;
//   file_name: string;
//   file_type: string;
// }

// // --- Props Definition ---
// interface FileSelectionPanelProps {
//     selectedFileIds: string[];
//     onSelectionChange: (ids: string[]) => void;
// }

// // Reusable Icon component
// const FileIcon: FC<{ fileType: string }> = ({ fileType }) => {
//     if (fileType.includes('pdf')) return <FaFilePdf className="text-red-500" />;
//     if (fileType.includes('word')) return <FaFileWord className="text-blue-500" />;
//     return <FaFileAlt className="text-gray-500" />;
// };

// export default function FileSelectionPanel({ selectedFileIds, onSelectionChange }: FileSelectionPanelProps) {
//     const [files, setFiles] = useState<FileMetadata[]>([]);
//     const [isLoading, setIsLoading] = useState(true);
//     const [isUploaderOpen, setIsUploaderOpen] = useState(false); // State to control modal
//     const { data: session } = useSession();

//     const fetchFiles = async () => {
//         if (!session?.user?.email) return;
//         setIsLoading(true);
//         try {
//             const url = `/api/files/active?user_email=${encodeURIComponent(session.user.email)}`;
//             const response = await apiClient.get<FileMetadata[]>(url);
//             setFiles(response.data);
//         } catch (err) {
//             console.error("Failed to fetch active files:", err);
//         } finally {
//             setIsLoading(false);
//         }
//     };

//     useEffect(() => {
//         if (session) {
//             fetchFiles();
//         }
//     }, [session]);

//     const handleCheckboxChange = (fileId: string) => {
//         const newSelection = selectedFileIds.includes(fileId)
//             ? selectedFileIds.filter(id => id !== fileId)
//             : [...selectedFileIds, fileId];
//         onSelectionChange(newSelection);
//     };

//     // This function will be called by the uploader on success
//     const handleUploadSuccess = () => {
//         setIsUploaderOpen(false); // Close the modal
//         fetchFiles(); // Refresh the file list
//     };

//     return (
//         <>
//             {/* The Uploader Modal (only rendered when needed) */}
//             {isUploaderOpen && (
//                 <FileUploader 
//                     onUploadSuccess={handleUploadSuccess}
//                     onClose={() => setIsUploaderOpen(false)}
//                 />
//             )}

//             <div className="w-64 flex-shrink-0 border-l border-gray-200 bg-gray-50 p-3 flex flex-col">
//                 <div className="flex justify-between items-center mb-3">
//                     <h3 className="text-sm font-semibold text-gray-700">Context Files</h3>
//                     <button onClick={fetchFiles} disabled={isLoading} className="p-1 text-gray-500 hover:text-gray-800 disabled:text-gray-300">
//                         <FaSync className={isLoading ? 'animate-spin' : ''} />
//                     </button>
//                 </div>
//                 <div className="flex-1 overflow-y-auto">
//                     {isLoading && <p className="text-xs text-gray-500">Loading...</p>}
//                     {!isLoading && files.length === 0 && <p className="text-xs text-gray-500">No documents found.</p>}
//                     <ul className="space-y-2">
//                         {files.map(file => (
//                             <li key={file.id}>
//                                 <label className="flex items-center space-x-2 p-2 rounded-md hover:bg-gray-200 cursor-pointer">
//                                     <input type="checkbox" className="form-checkbox h-4 w-4 text-blue-600 rounded" checked={selectedFileIds.includes(file.id)} onChange={() => handleCheckboxChange(file.id)} />
//                                     <FileIcon fileType={file.file_type} />
//                                     <span className="text-xs font-medium text-gray-800 truncate" title={file.file_name}>
//                                         {file.file_name}
//                                     </span>
//                                 </label>
//                             </li>
//                         ))}
//                     </ul>
//                 </div>

//                 {/* --- NEW SECTION AT THE BOTTOM --- */}
//                 <div className="mt-4 pt-4 border-t border-gray-200">
//                     <button
//                         onClick={() => setIsUploaderOpen(true)}
//                         className="w-full px-4 py-2 text-sm font-semibold text-white bg-blue-600 rounded-md hover:bg-blue-700"
//                     >
//                         Upload New Document
//                     </button>
//                 </div>
//             </div>
//         </>
//     );
// }
// "use client";

// import { useState, useEffect, FC } from 'react';
// import apiClient from '../lib/api';
// import { useSession } from "next-auth/react";
// import { FaFilePdf, FaFileWord, FaFileAlt, FaSync, FaPencilAlt } from 'react-icons/fa';
// import FileUploader from './FileUploader';

// // A hardcoded list of some popular Ollama models for the dropdown.
// // You can customize this list with the models you have downloaded.
// const AVAILABLE_MODELS = [
//     "llama3:8b",
//     "codellama",
//     "mistral",
//     "dolphin-mistral:7b",
//     "llava",
//     "gemma:7b"
// ];

// // --- Type Definition ---
// interface FileMetadata {
//   id: string;
//   file_name: string;
//   file_type: string;
// }

// // --- Props Definition ---
// interface FileSelectionPanelProps {
//     selectedFileIds: string[];
//     onSelectionChange: (ids: string[]) => void;
//     // New props for model selection
//     selectedModel: string;
//     onModelChange: (model: string) => void;
//     onEditPrompt: () => void;
// }

// // Reusable Icon component
// const FileIcon: FC<{ fileType: string }> = ({ fileType }) => {
//     if (fileType.includes('pdf')) return <FaFilePdf className="text-red-500" />;
//     if (fileType.includes('word')) return <FaFileWord className="text-blue-500" />;
//     return <FaFileAlt className="text-gray-500" />;
// };

// export default function FileSelectionPanel({ selectedModel, onModelChange, onEditPrompt, ...props }: FileSelectionPanelProps) {
//     const [files, setFiles] = useState<FileMetadata[]>([]);
//     const [isLoading, setIsLoading] = useState(true);
//     const [isUploaderOpen, setIsUploaderOpen] = useState(false);
//     const { data: session } = useSession();

//     const fetchFiles = async () => {
//         if (!session?.user?.email) return;
//         setIsLoading(true);
//         try {
//             const url = `/api/files/active?user_email=${encodeURIComponent(session.user.email)}`;
//             const response = await apiClient.get<FileMetadata[]>(url);
//             setFiles(response.data);
//         } catch (err) {
//             console.error("Failed to fetch active files:", err);
//         } finally {
//             setIsLoading(false);
//         }
//     };

//     useEffect(() => {
//         if (session) {
//             fetchFiles();
//         }
//     }, [session]);

//     const handleCheckboxChange = (fileId: string) => {
//         const newSelection = selectedFileIds.includes(fileId)
//             ? selectedFileIds.filter(id => id !== fileId)
//             : [...selectedFileIds, fileId];
//         onSelectionChange(newSelection);
//     };

//     const handleUploadSuccess = () => {
//         setIsUploaderOpen(false);
//         fetchFiles();
//     };

//     return (
//         <>
//             {isUploaderOpen && (
//                 <FileUploader 
//                     onUploadSuccess={handleUploadSuccess}
//                     onClose={() => setIsUploaderOpen(false)}
//                 />
//             )}

//             <div className="w-64 flex-shrink-0 border-l border-gray-200 bg-gray-50 p-3 flex flex-col">
                
//                 {/* --- NEW MODEL SELECTION SECTION --- */}
//                 <div className="pb-4 border-b border-gray-200">
//                     <label htmlFor="model-select" className="text-sm font-semibold text-gray-700 block mb-2">
//                         Chat Model
//                     </label>
//                     <select
//                         id="model-select"
//                         value={selectedModel}
//                         onChange={(e) => onModelChange(e.target.value)}
//                         className="w-full p-2 border border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500 text-sm"
//                     >
//                         {AVAILABLE_MODELS.map(model => (
//                             <option key={model} value={model}>{model}</option>
//                         ))}
//                     </select>
//                 </div>

//                 {/* --- Existing Context Files Section --- */}
//                 <div className="flex-grow pt-4 flex flex-col">
//                     <div className="flex justify-between items-center mb-3">
//                         <h3 className="text-sm font-semibold text-gray-700">Context Files</h3>
//                         <button onClick={fetchFiles} disabled={isLoading} className="p-1 text-gray-500 hover:text-gray-800 disabled:text-gray-300">
//                             <FaSync className={isLoading ? 'animate-spin' : ''} />
//                         </button>
//                     </div>
//                     <div className="flex-1 overflow-y-auto">
//                         {isLoading && <p className="text-xs text-gray-500">Loading...</p>}
//                         {!isLoading && files.length === 0 && <p className="text-xs text-gray-500">No documents found.</p>}
//                         <ul className="space-y-2">
//                             {files.map(file => (
//                                 <li key={file.id}>
//                                     <label className="flex items-center space-x-2 p-2 rounded-md hover:bg-gray-200 cursor-pointer">
//                                         <input type="checkbox" className="form-checkbox h-4 w-4 text-blue-600 rounded" checked={selectedFileIds.includes(file.id)} onChange={() => handleCheckboxChange(file.id)} />
//                                         <FileIcon fileType={file.file_type} />
//                                         <span className="text-xs font-medium text-gray-800 truncate" title={file.file_name}>
//                                             {file.file_name}
//                                         </span>
//                                     </label>
//                                 </li>
//                             ))}
//                         </ul>
//                     </div>
//                     <div className="mt-4 pt-4 border-t border-gray-200">
//                         <button onClick={() => setIsUploaderOpen(true)} className="w-full px-4 py-2 text-sm font-semibold text-white bg-blue-600 rounded-md hover:bg-blue-700">
//                             Upload New Document
//                         </button>
//                     </div>
//                 </div>
//             </div>
//         </>
//     );
// }
// "use client";

// import { useState, useEffect, FC } from 'react';
// import apiClient from '../lib/api';
// import { useSession } from "next-auth/react";
// import { FaFilePdf, FaFileWord, FaFileAlt, FaSync, FaPencilAlt } from 'react-icons/fa';
// import FileUploader from './FileUploader';

// // A hardcoded list of models for the dropdown.
// const AVAILABLE_MODELS = [
//     "llama3:8b",
//     "codellama",
//     "mistral",
//     "dolphin-mistral:7b",
//     "llava",
//     "gemma:7b"
// ];

// // --- Type Definition ---
// interface FileMetadata {
//   id: string;
//   file_name: string;
//   file_type: string;
// }

// // --- Props Definition ---
// interface FileSelectionPanelProps {
//     selectedFileIds: string[];
//     onSelectionChange: (ids: string[]) => void;
//     selectedModel: string;
//     onModelChange: (model: string) => void;
//     // New prop to handle the button click
//     onEditPrompt: () => void;
// }

// // Reusable Icon component
// const FileIcon: FC<{ fileType: string }> = ({ fileType }) => {
//     if (fileType.includes('pdf')) return <FaFilePdf className="text-red-500" />;
//     if (fileType.includes('word')) return <FaFileWord className="text-blue-500" />;
//     return <FaFileAlt className="text-gray-500" />;
// };

// export default function FileSelectionPanel({ selectedFileIds, onSelectionChange, selectedModel, onModelChange, onEditPrompt }: FileSelectionPanelProps) {
//     const [files, setFiles] = useState<FileMetadata[]>([]);
//     const [isLoading, setIsLoading] = useState(true);
//     const [isUploaderOpen, setIsUploaderOpen] = useState(false);
//     const { data: session } = useSession();

//     const fetchFiles = async () => {
//         if (!session?.user?.email) return;
//         setIsLoading(true);
//         try {
//             const url = `/api/files/active?user_email=${encodeURIComponent(session.user.email)}`;
//             const response = await apiClient.get<FileMetadata[]>(url);
//             setFiles(response.data);
//         } catch (err) {
//             console.error("Failed to fetch active files:", err);
//         } finally {
//             setIsLoading(false);
//         }
//     };

//     useEffect(() => {
//         if (session) {
//             fetchFiles();
//         }
//     }, [session]);

//     const handleCheckboxChange = (fileId: string) => {
//         const newSelection = selectedFileIds.includes(fileId)
//             ? selectedFileIds.filter(id => id !== fileId)
//             : [...selectedFileIds, fileId];
//         onSelectionChange(newSelection);
//     };

//     const handleUploadSuccess = () => {
//         setIsUploaderOpen(false);
//         fetchFiles();
//     };

//     return (
//         <>
//             {isUploaderOpen && (
//                 <FileUploader 
//                     onUploadSuccess={handleUploadSuccess}
//                     onClose={() => setIsUploaderOpen(false)}
//                 />
//             )}

//             <div className="w-64 flex-shrink-0 border-l border-gray-200 bg-gray-50 p-3 flex flex-col">
                
//                 {/* --- MODEL & PROMPT SECTION --- */}
//                 <div className="pb-4 border-b border-gray-200">
//                     <label htmlFor="model-select" className="text-sm font-semibold text-gray-700 block mb-2">
//                         Chat Model
//                     </label>
//                     <select
//                         id="model-select"
//                         value={selectedModel}
//                         onChange={(e) => onModelChange(e.target.value)}
//                         className="w-full p-2 border border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500 text-sm"
//                     >
//                         {AVAILABLE_MODELS.map(model => (
//                             <option key={model} value={model}>{model}</option>
//                         ))}
//                     </select>
                    
//                     {/* --- NEW EDIT PROMPT BUTTON --- */}
//                     <div className="mt-3">
//                         <button 
//                             onClick={onEditPrompt}
//                             className="w-full flex items-center justify-center px-4 py-2 text-xs font-semibold text-gray-700 bg-white border border-gray-300 rounded-md hover:bg-gray-100 transition-colors"
//                         >
//                             <FaPencilAlt className="mr-2" />
//                             Edit Prompt Template
//                         </button>
//                     </div>
//                 </div>

//                 {/* --- Existing Context Files Section --- */}
//                 <div className="flex-grow pt-4 flex flex-col">
//                     <div className="flex justify-between items-center mb-3">
//                         <h3 className="text-sm font-semibold text-gray-700">Context Files</h3>
//                         <button onClick={fetchFiles} disabled={isLoading} className="p-1 text-gray-500 hover:text-gray-800 disabled:text-gray-300">
//                             <FaSync className={isLoading ? 'animate-spin' : ''} />
//                         </button>
//                     </div>
//                     <div className="flex-1 overflow-y-auto">
//                         {isLoading && <p className="text-xs text-gray-500">Loading...</p>}
//                         {!isLoading && files.length === 0 && <p className="text-xs text-gray-500">No documents found.</p>}
//                         <ul className="space-y-2">
//                             {files.map(file => (
//                                 <li key={file.id}>
//                                     <label className="flex items-center space-x-2 p-2 rounded-md hover:bg-gray-200 cursor-pointer">
//                                         <input type="checkbox" className="form-checkbox h-4 w-4 text-blue-600 rounded" checked={selectedFileIds.includes(file.id)} onChange={() => handleCheckboxChange(file.id)} />
//                                         <FileIcon fileType={file.file_type} />
//                                         <span className="text-xs font-medium text-gray-800 truncate" title={file.file_name}>
//                                             {file.file_name}
//                                         </span>
//                                     </label>
//                                 </li>
//                             ))}
//                         </ul>
//                     </div>
//                     <div className="mt-4 pt-4 border-t border-gray-200">
//                         <button onClick={() => setIsUploaderOpen(true)} className="w-full px-4 py-2 text-sm font-semibold text-white bg-blue-600 rounded-md hover:bg-blue-700">
//                             Upload New Document
//                         </button>
//                     </div>
//                 </div>
//             </div>
//         </>
//     );
// }
"use client";

import { useState, useEffect, FC } from 'react';
import apiClient from '../lib/api';
import { useSession } from "next-auth/react";
import { FaFilePdf, FaFileWord, FaFileAlt, FaSync, FaPencilAlt, FaCircle } from 'react-icons/fa';
import FileUploader from './FileUploader';
import ParameterSliders from './ParameterSliders'; // Import the new component
import { useDockerStatus } from '../hooks/useDockerStatus';

const AVAILABLE_MODELS = [
    { value: "agent-mode", label: "AI Routes to Ideal Model" }, // The new Agent Mode
    { value: "llama3.1:8b", label: "llama3.1:8b" },
    { value: "llama3:8b", label: "llama3:8b" },
    { value: "codellama:7b", label: "codellama:7b" },
    { value: "dolphin-mistral:7b", label: "dolphin-mistral:7b" },
    { value: "gemma:7b", label: "gemma:7b" },
    { value: "deepseek-r1:7b", label: "deepseek-r1:7b" },
    { value: "gpt-oss:20b", label: "gpt-oss:20b" },
    { value: "qwen3:8b", label: "qwen3:8b" },
];
interface FileMetadata { id: string; file_name: string; file_type: string; }

interface FileSelectionPanelProps {
    selectedFileIds: string[];
    onSelectionChange: (ids: string[]) => void;
    selectedModel: string;
    onModelChange: (model: string) => void;
    onEditPrompt: () => void;
    // Props for the new parameter sliders
    temperature: number;
    setTemperature: (value: number) => void;
    topP: number;
    setTopP: (value: number) => void;
    maxTokens: number;
    setMaxTokens: (value: number) => void;
    lastTokenCount: any;
}

const FileIcon: FC<{ fileType: string }> = ({ fileType }) => {
    if (fileType.includes('pdf')) return <FaFilePdf className="text-red-500" />;
    if (fileType.includes('word')) return <FaFileWord className="text-blue-500" />;
    return <FaFileAlt className="text-gray-500" />;
};

export default function FileSelectionPanel({
    selectedFileIds, onSelectionChange, selectedModel, onModelChange, onEditPrompt,
    temperature, setTemperature, topP, setTopP, maxTokens, setMaxTokens, lastTokenCount
}: FileSelectionPanelProps) {
    const [files, setFiles] = useState<FileMetadata[]>([]);
    const [isLoading, setIsLoading] = useState(true);
    const [isUploaderOpen, setIsUploaderOpen] = useState(false);
    const { data: session } = useSession();
    
    // Docker status hook
    const { services, isLoading: dockerLoading, refresh: refreshDockerStatus, getStatusColor, getStatusText } = useDockerStatus();

    const fetchFiles = async () => {
        if (!session?.user?.email) return;
        setIsLoading(true);
        try {
            const url = `/api/files/active?user_email=${encodeURIComponent(session.user.email)}`;
            const response = await apiClient.get<FileMetadata[]>(url);
            setFiles(response.data);
        } catch (err) {
            console.error("Failed to fetch active files:", err);
        } finally {
            setIsLoading(false);
        }
    };

    useEffect(() => { if (session) { fetchFiles(); } }, [session]);
    const handleCheckboxChange = (fileId: string) => {
        const newSelection = selectedFileIds.includes(fileId) ? selectedFileIds.filter(id => id !== fileId) : [...selectedFileIds, fileId];
        onSelectionChange(newSelection);
    };
    const handleUploadSuccess = () => { setIsUploaderOpen(false); fetchFiles(); };

    return (
        <>
            {isUploaderOpen && (<FileUploader onUploadSuccess={handleUploadSuccess} onClose={() => setIsUploaderOpen(false)} />)}
            <div className="w-64 flex-shrink-0 border-l border-white/30 bg-white/20 backdrop-blur-md p-4 flex flex-col">
                <div className="pb-4 border-b border-white/20">
                    <label htmlFor="model-select" className="text-sm font-semibold text-gray-800 block mb-2">Chat Model</label>
                    <select id="model-select" value={selectedModel} onChange={(e) => onModelChange(e.target.value)} className="w-full p-3 bg-white/70 backdrop-blur-sm border border-white/40 rounded-xl shadow-sm focus:ring-2 focus:ring-blue-500/50 focus:border-blue-500/50 text-sm transition-all duration-200">
                        {AVAILABLE_MODELS.map(model => (  <option key={model.value} value={model.value}>{model.label}</option>))}
                    </select>
                    <div className="mt-3">
                        <button onClick={onEditPrompt} className="w-full flex items-center justify-center px-4 py-2 text-xs font-semibold text-gray-700 bg-white/60 backdrop-blur-sm border border-white/40 rounded-xl hover:bg-white/80 hover:scale-105 transition-all duration-200 shadow-sm">
                            <FaPencilAlt className="mr-2" />Edit Prompt Template
                        </button>
                    </div>
                    {/* --- NEW: Parameter Sliders Section --- */}
                    <div className="mt-4">
                        <ParameterSliders
                            temperature={temperature} setTemperature={setTemperature}
                            topP={topP} setTopP={setTopP}
                            maxTokens={maxTokens} setMaxTokens={setMaxTokens}
                            lastTokenCount={lastTokenCount}
                        />
                    </div>
                </div>
                <div className="flex-grow pt-4 flex flex-col">
                    <div className="flex justify-between items-center mb-3">
                        <h3 className="text-sm font-semibold text-gray-800">Context Files</h3>
                        <button onClick={fetchFiles} disabled={isLoading} className="p-2 text-gray-600 hover:text-gray-800 hover:bg-white/40 rounded-lg transition-all duration-200 disabled:text-gray-400">
                            <FaSync className={isLoading ? 'animate-spin' : ''} />
                        </button>
                    </div>
                    <div className="flex-1 overflow-y-auto">
                        {isLoading && <p className="text-xs text-gray-500">Loading...</p>}
                        {!isLoading && files.length === 0 && <p className="text-xs text-gray-500">No documents found.</p>}
                        <ul className="space-y-2">
                            {files.map(file => (
                                <li key={file.id}>
                                    <label className="flex items-center space-x-2 p-2 rounded-xl hover:bg-white/40 cursor-pointer transition-all duration-200">
                                        <input type="checkbox" className="form-checkbox h-4 w-4 text-blue-600 rounded" checked={selectedFileIds.includes(file.id)} onChange={() => handleCheckboxChange(file.id)} />
                                        <FileIcon fileType={file.file_type} />
                                        <span className="text-xs font-medium text-gray-800 truncate" title={file.file_name}>{file.file_name}</span>
                                    </label>
                                </li>
                            ))}
                        </ul>
                    </div>
                    
                    {/* Docker Services Status Section */}
                    <div className="mt-4 pt-4 border-t border-white/20">
                        <div className="flex justify-between items-center mb-3">
                            <h3 className="text-sm font-semibold text-gray-800">Services Status</h3>
                            <button 
                                onClick={refreshDockerStatus} 
                                disabled={dockerLoading} 
                                className="p-2 text-gray-600 hover:text-gray-800 hover:bg-white/40 rounded-lg transition-all duration-200 disabled:text-gray-400"
                                title="Refresh status"
                            >
                                <FaSync className={dockerLoading ? 'animate-spin' : ''} />
                            </button>
                        </div>
                        <div className="space-y-2">
                            {services.map(service => (
                                <div key={service.name} className="flex items-center justify-between py-1.5 px-2 rounded-lg bg-white/20 backdrop-blur-sm">
                                    <span className="text-xs text-gray-800 font-medium">{service.displayName}</span>
                                    <div className="flex items-center space-x-1">
                                        <FaCircle className={`text-xs ${getStatusColor(service.status)}`} />
                                        <span className={`text-xs ${getStatusColor(service.status)}`}>
                                            {getStatusText(service.status)}
                                        </span>
                                    </div>
                                </div>
                            ))}
                        </div>
                    </div>
                    
                    <div className="mt-4 pt-4 border-t border-white/20">
                        <button onClick={() => setIsUploaderOpen(true)} className="w-full px-4 py-3 text-sm font-semibold text-white bg-gradient-to-r from-blue-500 to-blue-600 rounded-xl hover:from-blue-600 hover:to-blue-700 hover:scale-105 transition-all duration-200 shadow-lg">
                            Upload New Document
                        </button>
                    </div>
                </div>
            </div>
        </>
    );
}