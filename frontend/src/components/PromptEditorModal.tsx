// frontend/src/components/PromptEditorModal.tsx
"use client";

import { useState, useEffect } from 'react';

interface PromptEditorModalProps {
  isOpen: boolean;
  onClose: () => void;
  initialPrompt: string;
  onSave: (newPrompt: string) => void;
}

export default function PromptEditorModal({ isOpen, onClose, initialPrompt, onSave }: PromptEditorModalProps) {
  const [editText, setEditText] = useState(initialPrompt);

  useEffect(() => {
    setEditText(initialPrompt);
  }, [initialPrompt]);

  if (!isOpen) return null;

  const handleSave = () => {
    onSave(editText);
    onClose();
  };

  return (
    <div className="fixed inset-0 bg-black bg-opacity-60 flex items-center justify-center z-50">
      <div className="bg-white rounded-lg shadow-xl p-6 w-full max-w-2xl flex flex-col h-[70vh]">
        <h2 className="text-xl font-bold mb-4">Edit Prompt Template</h2>
        <p className="text-sm text-gray-500 mb-4">
          Edit the template below. Use `{'{context}'}` and `{'{question}'}` as placeholders.
        </p>
        <textarea
          value={editText}
          onChange={(e) => setEditText(e.target.value)}
          className="w-full flex-grow p-3 border border-gray-300 rounded-md font-mono text-sm resize-none"
        />
        <div className="mt-6 flex justify-end space-x-3">
          <button onClick={onClose} className="px-4 py-2 bg-gray-200 text-gray-800 rounded-md hover:bg-gray-300">
            Cancel
          </button>
          <button onClick={handleSave} className="px-4 py-2 bg-blue-500 text-white rounded-md hover:bg-blue-600">
            Save and Close
          </button>
        </div>
      </div>
    </div>
  );
}