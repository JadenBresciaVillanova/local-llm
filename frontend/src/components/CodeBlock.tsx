import React, { useState } from 'react';
import { Prism as SyntaxHighlighter } from 'react-syntax-highlighter';
import { oneDark } from 'react-syntax-highlighter/dist/esm/styles/prism';
import { FaCopy, FaCheck, FaEdit, FaSave, FaTimes } from 'react-icons/fa';

interface CodeBlockProps {
  code: string;
  language?: string;
  inline?: boolean;
}

const CodeBlock: React.FC<CodeBlockProps> = ({ code, language = 'text', inline = false }) => {
  const [copied, setCopied] = useState(false);
  const [isEditing, setIsEditing] = useState(false);
  const [editedCode, setEditedCode] = useState(code);

  const handleCopy = async () => {
    try {
      await navigator.clipboard.writeText(isEditing ? editedCode : code);
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    } catch (err) {
      console.error('Failed to copy code:', err);
    }
  };

  const handleEdit = () => {
    setIsEditing(true);
    setEditedCode(code);
  };

  const handleSave = () => {
    setIsEditing(false);
    // Note: In a real app, you might want to emit this change to a parent component
  };

  const handleCancel = () => {
    setIsEditing(false);
    setEditedCode(code);
  };

  // For inline code (backticks)
  if (inline) {
    return (
      <code className="bg-gray-100 text-red-600 px-1.5 py-0.5 rounded text-sm font-mono">
        {code}
      </code>
    );
  }

  // For code blocks (triple backticks)
  return (
    <div className="relative group my-2 rounded-xl overflow-hidden bg-[#1e1e1e] border border-gray-700/50">
      {/* Header with language and action buttons */}
      <div className="flex items-center justify-between px-4 py-2 bg-gray-800/80 backdrop-blur-sm border-b border-gray-700/50">
        <span className="text-sm text-gray-300 font-medium capitalize">
          {language || 'code'}
        </span>
        <div className="flex items-center space-x-2">
          {!isEditing ? (
            <>
              <button
                onClick={handleEdit}
                className="flex items-center space-x-1 px-2 py-1 rounded-md text-gray-300 hover:text-white hover:bg-gray-700/50 transition-colors"
                title="Edit code"
              >
                <FaEdit className="w-3 h-3" />
                <span className="text-xs">Edit</span>
              </button>
              <button
                onClick={handleCopy}
                className="flex items-center space-x-1 px-2 py-1 rounded-md text-gray-300 hover:text-white hover:bg-gray-700/50 transition-colors"
                title="Copy code"
              >
                {copied ? <FaCheck className="w-3 h-3" /> : <FaCopy className="w-3 h-3" />}
                <span className="text-xs">{copied ? 'Copied!' : 'Copy'}</span>
              </button>
            </>
          ) : (
            <>
              <button
                onClick={handleSave}
                className="flex items-center space-x-1 px-2 py-1 rounded-md text-green-300 hover:text-green-100 hover:bg-green-700/50 transition-colors"
                title="Save changes"
              >
                <FaSave className="w-3 h-3" />
                <span className="text-xs">Save</span>
              </button>
              <button
                onClick={handleCancel}
                className="flex items-center space-x-1 px-2 py-1 rounded-md text-red-300 hover:text-red-100 hover:bg-red-700/50 transition-colors"
                title="Cancel editing"
              >
                <FaTimes className="w-3 h-3" />
                <span className="text-xs">Cancel</span>
              </button>
            </>
          )}
        </div>
      </div>
      
      {/* Code content */}
      <div className="relative">
        {isEditing ? (
          <textarea
            value={editedCode}
            onChange={(e) => setEditedCode(e.target.value)}
            className="w-full h-64 p-4 bg-[#1e1e1e] text-gray-100 font-mono text-sm resize-none focus:outline-none border-none"
            style={{ lineHeight: '1.5' }}
          />
        ) : (
          <SyntaxHighlighter
            language={language}
            style={{
              ...oneDark,
              'pre[class*="language-"]': {
                ...oneDark['pre[class*="language-"]'],
                textShadow: 'none', // Remove text shadow
              },
              'code[class*="language-"]': {
                ...oneDark['code[class*="language-"]'],
                textShadow: 'none', // Remove text shadow
              }
            }}
            customStyle={{
              margin: 0,
              padding: '16px',
              background: 'transparent',
              fontSize: '14px',
              lineHeight: '1.5',
              textShadow: 'none', // Explicitly remove text shadow
            }}
            wrapLines={true}
            wrapLongLines={true}
          >
            {editedCode}
          </SyntaxHighlighter>
        )}
      </div>
    </div>
  );
};

export default CodeBlock;