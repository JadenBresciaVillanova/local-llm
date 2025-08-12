// frontend/src/app/metrics/page.tsx
"use client";

import { useState, useEffect, FC } from 'react';
import { useSession } from "next-auth/react";
import { FaChartBar, FaServer, FaEye, FaCopy, FaExternalLinkAlt } from 'react-icons/fa';

interface MetricSection {
  title: string;
  description: string;
  icon: React.ReactNode;
  content: React.ReactNode;
}

const CodeBlock: FC<{ code: string; language?: string }> = ({ code, language = "json" }) => {
  const [copied, setCopied] = useState(false);

  const handleCopy = () => {
    navigator.clipboard.writeText(code);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <div className="relative">
      <button
        onClick={handleCopy}
        className="absolute top-2 right-2 p-2 text-gray-400 hover:text-gray-600 transition-colors"
        title="Copy to clipboard"
      >
        <FaCopy className={copied ? "text-green-500" : ""} />
      </button>
      <pre className="bg-gray-900 text-green-400 p-4 rounded-lg overflow-x-auto text-sm">
        <code>{code}</code>
      </pre>
    </div>
  );
};

const MetricCard: FC<{ title: string; description: string; children: React.ReactNode }> = ({ 
  title, 
  description, 
  children 
}) => (
  <div className="bg-white shadow-md rounded-lg p-6">
    <h3 className="text-lg font-semibold text-gray-900 mb-2">{title}</h3>
    <p className="text-sm text-gray-600 mb-4">{description}</p>
    {children}
  </div>
);

export default function MetricsPage() {
  const { data: session } = useSession();
  const [activeSection, setActiveSection] = useState<string>('prometheus');

  const prometheusMetrics = `# Prometheus Metrics Documentation

## Default FastAPI Metrics
- http_requests_total: Total HTTP requests by method and status
- http_request_duration_seconds: Request latency histogram
- http_requests_in_progress: Current active requests

## Custom Application Metrics
- chat_requests_total: Total chat requests processed
- chat_failures_total: Total chat request failures
- embedding_creation_total: Total embeddings created
- file_uploads_total: Total file uploads
- document_chunks_created_total: Total document chunks created
- llm_response_latency_seconds: LLM response time histogram

## Access Metrics
GET http://localhost:8000/metrics`;

  const kafkaEventSchema = `{
  "event_type": "file_uploaded",
  "user_id": "user@example.com", 
  "timestamp": "2025-01-10T15:00:00Z",
  "metadata": {
    "file_name": "report.pdf",
    "file_size": 1024000,
    "num_chunks": 42,
    "processing_time_ms": 5000
  }
}

// Other Event Types:
// - file_deleted
// - chat_started
// - chat_message_sent
// - embedding_created
// - chunk_retrieved`;

  const grafanaDashboards = `# Grafana Dashboards Configuration

## 1. Overview Dashboard
- Request counts and rates
- Error rates by endpoint
- Active users count
- System health status

## 2. LLM Performance Dashboard  
- Response latency percentiles
- Token generation rates
- Model usage distribution
- Cache hit rates

## 3. Document Processing Dashboard
- File upload trends
- Chunk creation rates
- Processing success/failure rates
- Storage usage metrics

## 4. User Activity Dashboard
- Most active users
- Document interaction patterns
- Conversation lengths
- Feature usage analytics`;

  const sections: MetricSection[] = [
    {
      title: "Prometheus Metrics",
      description: "Application metrics collected and exposed via Prometheus for monitoring performance and usage.",
      icon: <FaChartBar className="text-orange-500" />,
      content: (
        <div className="space-y-4">
          <MetricCard 
            title="Metrics Endpoint"
            description="Access real-time metrics at the /metrics endpoint"
          >
            <div className="flex items-center space-x-2 mb-4">
              <a 
                href="http://localhost:8000/metrics" 
                target="_blank" 
                rel="noopener noreferrer"
                className="inline-flex items-center px-4 py-2 bg-orange-500 text-white rounded-md hover:bg-orange-600 transition-colors"
              >
                View Metrics <FaExternalLinkAlt className="ml-2" />
              </a>
            </div>
            <CodeBlock code={prometheusMetrics} language="yaml" />
          </MetricCard>
        </div>
      )
    },
    {
      title: "Kafka Event Logs", 
      description: "Structured event logging system for tracking user actions and system events.",
      icon: <FaServer className="text-green-500" />,
      content: (
        <div className="space-y-4">
          <MetricCard
            title="Event Schema"
            description="Standardized event format for all application events"
          >
            <CodeBlock code={kafkaEventSchema} />
          </MetricCard>
          <MetricCard
            title="Event Topics"
            description="Kafka topics for different event categories"
          >
            <div className="grid grid-cols-2 gap-4">
              <div className="bg-gray-50 p-3 rounded">
                <h4 className="font-medium">user-actions</h4>
                <p className="text-sm text-gray-600">File uploads, chat interactions</p>
              </div>
              <div className="bg-gray-50 p-3 rounded">
                <h4 className="font-medium">system-events</h4>
                <p className="text-sm text-gray-600">Processing status, errors</p>
              </div>
            </div>
          </MetricCard>
        </div>
      )
    },
    {
      title: "Grafana Dashboards",
      description: "Visual dashboards and alerts for monitoring application health and performance.", 
      icon: <FaEye className="text-blue-500" />,
      content: (
        <div className="space-y-4">
          <MetricCard
            title="Dashboard Access"
            description="Access Grafana dashboards for real-time monitoring"
          >
            <div className="flex items-center space-x-2 mb-4">
              <a 
                href="http://localhost:3001" 
                target="_blank" 
                rel="noopener noreferrer"
                className="inline-flex items-center px-4 py-2 bg-blue-500 text-white rounded-md hover:bg-blue-600 transition-colors"
              >
                Open Grafana <FaExternalLinkAlt className="ml-2" />
              </a>
            </div>
            <CodeBlock code={grafanaDashboards} language="yaml" />
          </MetricCard>
        </div>
      )
    }
  ];

  return (
    <div className="max-w-5xl mx-auto p-4 sm:p-6 lg:p-8 space-y-8">
      {/* Page Header */}
      <div>
        <h1 className="text-2xl font-bold text-gray-900">Metrics & Monitoring</h1>
        <p className="text-sm text-gray-500 mt-1 mb-6">
          Monitor application performance, user activity, and system health through comprehensive observability tools.
        </p>
      </div>

      {/* Section Navigation */}
      <div className="flex space-x-2 bg-gray-100 p-1 rounded-lg">
        {sections.map((section, index) => (
          <button
            key={index}
            onClick={() => setActiveSection(section.title.toLowerCase().replace(/\s+/g, '_'))}
            className={`flex items-center space-x-2 px-4 py-2 rounded-md text-sm font-medium transition-colors ${
              activeSection === section.title.toLowerCase().replace(/\s+/g, '_')
                ? 'bg-white text-gray-900 shadow-sm'
                : 'text-gray-600 hover:text-gray-900'
            }`}
          >
            {section.icon}
            <span>{section.title}</span>
          </button>
        ))}
      </div>

      {/* Active Section Content */}
      {sections.map((section, index) => {
        const sectionKey = section.title.toLowerCase().replace(/\s+/g, '_');
        return activeSection === sectionKey ? (
          <div key={index}>
            <div className="mb-6">
              <div className="flex items-center space-x-3 mb-2">
                <div className="text-2xl">{section.icon}</div>
                <h2 className="text-xl font-bold text-gray-900">{section.title}</h2>
              </div>
              <p className="text-gray-600">{section.description}</p>
            </div>
            {section.content}
          </div>
        ) : null;
      })}
    </div>
  );
}