"use client";

import { useState, useCallback, DragEvent } from 'react';
import apiClient from '../lib/api';
import { useSession } from "next-auth/react";

// Define the component's new props
interface FileUploaderProps {
  onUploadSuccess: () => void; // A function to call when upload is done
  onClose: () => void;
}

const ACCEPTED_FILE_TYPES = {
  'application/pdf': ['.pdf'],
  'application/vnd.openxmlformats-officedocument.wordprocessingml.document': ['.docx'],
  'text/plain': ['.txt'],
};
const MAX_FILE_SIZE = 10 * 1024 * 1024; // 10 MB

export default function FileUploader({ onUploadSuccess, onClose }: FileUploaderProps) {
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [isDragging, setIsDragging] = useState(false);
  const [isUploading, setIsUploading] = useState(false);
  const { data: session } = useSession();

  const handleValidation = (file: File): boolean => {
    if (!ACCEPTED_FILE_TYPES[file.type as keyof typeof ACCEPTED_FILE_TYPES]) {
      setError(`File type not supported. Please upload a PDF, DOCX, or TXT file.`);
      return false;
    }
    if (file.size > MAX_FILE_SIZE) {
      setError(`File is too large. Maximum size is ${MAX_FILE_SIZE / 1024 / 1024} MB.`);
      return false;
    }
    setError(null);
    return true;
  };

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file && handleValidation(file)) {
      setSelectedFile(file);
    }
  };

  const handleDrop = useCallback((e: DragEvent<HTMLDivElement>) => { e.preventDefault(); e.stopPropagation(); setIsDragging(false); const file = e.dataTransfer.files?.[0]; if (file && handleValidation(file)) { setSelectedFile(file); } }, []);
  const handleDragOver = (e: DragEvent<HTMLDivElement>) => { e.preventDefault(); e.stopPropagation(); };
  const handleDragEnter = (e: DragEvent<HTMLDivElement>) => { e.preventDefault(); e.stopPropagation(); setIsDragging(true); };
  const handleDragLeave = (e: DragEvent<HTMLDivElement>) => { e.preventDefault(); e.stopPropagation(); setIsDragging(false); };

  const handleUpload = async () => {
    if (!selectedFile || !session?.user?.email) {
      setError("No file selected or user not logged in.");
      return;
    }

    setIsUploading(true);
    setError(null);

    const formData = new FormData();
    formData.append('file', selectedFile);
    formData.append('user_email', session.user.email);

    try {
      // --- THIS IS THE FIX ---
      // We removed the third argument (the config object with the headers).
      // The browser will now correctly set the Content-Type with the required boundary.
      await apiClient.post('/api/files/upload', formData);
      // --- END FIX ---

      onUploadSuccess();
    } catch (err: any) {
      console.error("File upload failed:", err);
      setError(err.response?.data?.detail || "An unexpected error occurred during upload.");
    } finally {
      setIsUploading(false);
    }
  };

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div className="bg-white rounded-lg shadow-xl p-6 w-full max-w-md">
        <h2 className="text-xl font-bold mb-4">Upload a Document</h2>
        <div
          onDrop={handleDrop} onDragOver={handleDragOver} onDragEnter={handleDragEnter} onDragLeave={handleDragLeave}
          className={`border-2 border-dashed rounded-lg p-8 text-center cursor-pointer transition-colors ${
            isDragging ? 'border-blue-500 bg-blue-50' : 'border-gray-300 hover:border-gray-400'
          }`}
          onClick={() => document.getElementById('file-input')?.click()}
        >
          <input id="file-input" type="file" className="hidden" accept={Object.values(ACCEPTED_FILE_TYPES).flat().join(',')} onChange={handleFileChange} />
          <p className="text-gray-500">Drag & drop a file here, or click to select</p>
          <p className="text-xs text-gray-400 mt-1">PDF, DOCX, TXT up to 10MB</p>
        </div>
        
        {error && <p className="text-red-500 text-sm mt-2">{error}</p>}

        {selectedFile && !error && (
          <div className="mt-4 p-3 bg-gray-100 rounded-lg">
            <p className="font-semibold text-gray-700">Selected file:</p>
            <p className="text-sm text-gray-600">{selectedFile.name} ({(selectedFile.size / 1024).toFixed(2)} KB)</p>
          </div>
        )}

        <div className="mt-6 flex justify-end space-x-3">
          <button onClick={onClose} className="px-4 py-2 bg-gray-200 text-gray-800 rounded-md hover:bg-gray-300" disabled={isUploading}>
            Cancel
          </button>
          <button 
            onClick={handleUpload} 
            disabled={!selectedFile || !!error || isUploading}
            className="px-4 py-2 bg-blue-500 text-white rounded-md hover:bg-blue-600 disabled:bg-blue-300 disabled:cursor-not-allowed"
          >
            {isUploading ? 'Uploading...' : 'Upload File'}
          </button>
        </div>
      </div>
    </div>
  );
}