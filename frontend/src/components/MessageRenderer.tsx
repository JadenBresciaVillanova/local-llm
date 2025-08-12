import React from 'react';
import CodeBlock from './CodeBlock';

interface MessageRendererProps {
  content: string;
  role: 'user' | 'ai';
}

const MessageRenderer: React.FC<MessageRendererProps> = ({ content, role }) => {
  // Parse the message content to handle code blocks and markdown
  const parseMessage = (text: string) => {
    const parts = [];
    let lastIndex = 0;
    
    // Regex to match code blocks ```language\ncode\n```
    const codeBlockRegex = /```(\w+)?\n?([\s\S]*?)```/g;
    
    let match;
    
    // First, handle code blocks
    while ((match = codeBlockRegex.exec(text)) !== null) {
      // Add text before the code block
      if (match.index > lastIndex) {
        const beforeText = text.slice(lastIndex, match.index).trim();
        if (beforeText) {
          parts.push(...parseTextContent(beforeText, parts.length));
        }
      }
      
      // Add the code block
      const language = match[1] || 'text';
      const code = match[2].trim();
      parts.push(
        <CodeBlock 
          key={parts.length} 
          code={code} 
          language={language} 
          inline={false}
        />
      );
      
      lastIndex = match.index + match[0].length;
    }
    
    // Add remaining text after last code block
    if (lastIndex < text.length) {
      const remainingText = text.slice(lastIndex).trim();
      if (remainingText) {
        parts.push(...parseTextContent(remainingText, parts.length));
      }
    }
    
    return parts.length > 0 ? parts : [parseTextContent(text, 0)];
  };

  // Enhanced text content parser for markdown-like formatting
  const parseTextContent = (text: string, startKey: number) => {
    const parts = [];
    const lines = text.split('\n');
    
    for (let i = 0; i < lines.length; i++) {
      const line = lines[i];
      const trimmedLine = line.trim();
      
      // Handle headings (## Heading or **Heading**)
      if (trimmedLine.match(/^##\s+(.+)/) || trimmedLine.match(/^\*\*([^*]+)\*\*:?\s*$/)) {
        const headingMatch = trimmedLine.match(/^##\s+(.+)/) || trimmedLine.match(/^\*\*([^*]+)\*\*:?\s*$/);
        if (headingMatch) {
          parts.push(
            <h3 key={startKey + parts.length} className="text-lg font-bold text-gray-800 mt-3 mb-2">
              {headingMatch[1].replace(/:\s*$/, '')}
            </h3>
          );
          continue;
        }
      }
      
      // Handle bullet points
      if (trimmedLine.match(/^[-*]\s+(.+)/)) {
        const bulletMatch = trimmedLine.match(/^[-*]\s+(.+)/);
        if (bulletMatch) {
          parts.push(
            <div key={startKey + parts.length} className="flex items-start mt-1 mb-1">
              <span className="text-blue-600 mr-2 mt-1">•</span>
              <span>{parseInlineElements(bulletMatch[1])}</span>
            </div>
          );
          continue;
        }
      }
      
      // Handle regular text with inline formatting
      if (trimmedLine) {
        parts.push(
          <div key={startKey + parts.length} className="mb-1">
            {parseInlineElements(trimmedLine)}
          </div>
        );
      } else if (i < lines.length - 1) {
        // Add spacing for empty lines (but not at the end)
        parts.push(
          <div key={startKey + parts.length} className="h-2"></div>
        );
      }
    }
    
    return parts;
  };
  
  // Helper function to parse inline elements (code, bold, etc.)
  const parseInlineElements = (text: string) => {
    const parts = [];
    let lastIndex = 0;
    
    // Combined regex for inline code and function names
    const inlineRegex = /(`[^`]+`)|(\b\w+\(\))/g;
    let match;
    
    while ((match = inlineRegex.exec(text)) !== null) {
      // Add text before the match
      if (match.index > lastIndex) {
        const beforeText = text.slice(lastIndex, match.index);
        parts.push(beforeText);
      }
      
      if (match[1]) {
        // Inline code (backticks)
        const code = match[1].slice(1, -1); // Remove backticks
        parts.push(
          <CodeBlock 
            key={parts.length} 
            code={code} 
            inline={true}
          />
        );
      } else if (match[2]) {
        // Function names like add() or findMedian()
        parts.push(
          <span key={parts.length} className="text-red-600 font-mono">
            {match[2]}
          </span>
        );
      }
      
      lastIndex = match.index + match[0].length;
    }
    
    // Add remaining text
    if (lastIndex < text.length) {
      const remainingText = text.slice(lastIndex);
      parts.push(remainingText);
    }
    
    return parts.length > 0 ? parts : text;
  };
  
  const parsedContent = parseMessage(content);
  
  return (
    <div className="whitespace-pre-wrap">
      {Array.isArray(parsedContent) ? parsedContent : parsedContent}
    </div>
  );
};

export default MessageRenderer;