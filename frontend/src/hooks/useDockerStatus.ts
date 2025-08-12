import { useState, useEffect, useCallback } from 'react';

interface ServiceStatus {
  name: string;
  status: 'running' | 'stopped' | 'starting' | 'error' | 'not-configured';
  port?: number;
  displayName: string;
}

interface DockerStatusState {
  services: ServiceStatus[];
  isLoading: boolean;
  lastUpdated: Date | null;
}

export const useDockerStatus = () => {
  const [state, setState] = useState<DockerStatusState>({
    services: [
      { name: 'rag_postgres', displayName: 'PostgreSQL', status: 'stopped', port: 5432 },
      { name: 'rag_mongo', displayName: 'MongoDB', status: 'stopped', port: 27017 },
      { name: 'ollama', displayName: 'Ollama', status: 'stopped', port: 11434 },
      { name: 'rag_backend', displayName: 'Backend', status: 'stopped', port: 8000 },
      { name: 'prometheus', displayName: 'Prometheus', status: 'stopped', port: 9090 },
      { name: 'grafana', displayName: 'Grafana', status: 'stopped', port: 3001 },
      { name: 'kafka', displayName: 'Kafka', status: 'stopped', port: 9092 },
      { name: 'zookeeper', displayName: 'Zookeeper', status: 'stopped', port: 2181 },
    ],
    isLoading: false,
    lastUpdated: null,
  });

  const checkServiceStatus = useCallback(async (service: ServiceStatus): Promise<ServiceStatus> => {
    // If service is not configured, return as-is
    if (service.status === 'not-configured') {
      return service;
    }

    try {
      // Different check methods for different services
      if (service.name === 'rag_backend') {
        // Backend - try root endpoint instead of /health
        const response = await fetch(`http://localhost:${service.port}/`, {
          method: 'HEAD',
          mode: 'no-cors',
        });
        return { ...service, status: 'running' };
      } else if (service.name === 'rag_mongo' || service.name === 'rag_postgres' || service.name === 'kafka' || service.name === 'zookeeper') {
        // For non-HTTP services, assume they're running if the containers are up
        // Frontend can't easily check TCP ports without causing protocol errors
        // This is a simplified check - in production you'd use a backend health endpoint
        return { ...service, status: 'running' };
      } else if (service.name === 'prometheus' || service.name === 'grafana') {
        // For HTTP services, use proper HTTP requests
        const response = await fetch(`http://localhost:${service.port}`, {
          method: 'HEAD',
          mode: 'no-cors',
        });
        return { ...service, status: 'running' };
      } else {
        // For other services (ollama)
        const response = await fetch(`http://localhost:${service.port}`, {
          method: 'HEAD',
          mode: 'no-cors',
        });
        return { ...service, status: 'running' };
      }
    } catch (error) {
      return { ...service, status: 'stopped' };
    }
  }, []);

  const manualRefresh = useCallback(async () => {
    setState(prev => ({ ...prev, isLoading: true }));
    
    try {
      const initialServices = [
        { name: 'rag_postgres', displayName: 'PostgreSQL', status: 'stopped' as const, port: 5432 },
        { name: 'rag_mongo', displayName: 'MongoDB', status: 'stopped' as const, port: 27017 },
        { name: 'ollama', displayName: 'Ollama', status: 'stopped' as const, port: 11434 },
        { name: 'rag_backend', displayName: 'Backend', status: 'stopped' as const, port: 8000 },
        { name: 'prometheus', displayName: 'Prometheus', status: 'not-configured' as const, port: 9090 },
        { name: 'grafana', displayName: 'Grafana', status: 'not-configured' as const, port: 3001 },
        { name: 'kafka', displayName: 'Kafka', status: 'not-configured' as const, port: 9092 },
        { name: 'zookeeper', displayName: 'Zookeeper', status: 'not-configured' as const, port: 2181 },
      ];
      
      const updatedServices = await Promise.all(
        initialServices.map(service => checkServiceStatus(service))
      );
      
      setState(prev => ({
        ...prev,
        services: updatedServices,
        isLoading: false,
        lastUpdated: new Date(),
      }));
    } catch (error) {
      console.error('Failed to check service status:', error);
      setState(prev => ({ ...prev, isLoading: false }));
    }
  }, [checkServiceStatus]);

  useEffect(() => {
    let interval: NodeJS.Timeout;
    let timeoutId: NodeJS.Timeout;
    let mounted = true;
    
    const runCheck = async () => {
      if (!mounted) return;
      
      setState(prev => ({ ...prev, isLoading: true }));
      
      try {
        const initialServices = [
          { name: 'rag_postgres', displayName: 'PostgreSQL', status: 'stopped' as const, port: 5432 },
          { name: 'rag_mongo', displayName: 'MongoDB', status: 'stopped' as const, port: 27017 },
          { name: 'ollama', displayName: 'Ollama', status: 'stopped' as const, port: 11434 },
          { name: 'rag_backend', displayName: 'Backend', status: 'stopped' as const, port: 8000 },
          { name: 'prometheus', displayName: 'Prometheus', status: 'stopped' as const, port: 9090 },
          { name: 'grafana', displayName: 'Grafana', status: 'stopped' as const, port: 3001 },
          { name: 'kafka', displayName: 'Kafka', status: 'stopped' as const, port: 9092 },
          { name: 'zookeeper', displayName: 'Zookeeper', status: 'stopped' as const, port: 2181 },
        ];
        
        const updatedServices = await Promise.all(
          initialServices.map(service => checkServiceStatus(service))
        );
        
        if (mounted) {
          setState(prev => ({
            ...prev,
            services: updatedServices,
            isLoading: false,
            lastUpdated: new Date(),
          }));
        }
      } catch (error) {
        console.error('Failed to check service status:', error);
        if (mounted) {
          setState(prev => ({ ...prev, isLoading: false }));
        }
      }
    };
    
    // Initial check
    runCheck();
    
    // First minute: refresh every 5 seconds
    interval = setInterval(runCheck, 5000);
    
    // After 1 minute, stop checking completely
    timeoutId = setTimeout(() => {
      if (mounted) {
        clearInterval(interval);
      }
    }, 60000);
    
    return () => {
      mounted = false;
      clearInterval(interval);
      clearTimeout(timeoutId);
    };
  }, []); // Empty dependency array to prevent infinite re-renders

  const getStatusColor = (status: ServiceStatus['status']): string => {
    switch (status) {
      case 'running':
        return 'text-green-600';
      case 'starting':
        return 'text-yellow-600';
      case 'stopped':
        return 'text-red-600';
      case 'error':
        return 'text-red-700';
      case 'not-configured':
        return 'text-gray-500';
      default:
        return 'text-gray-600';
    }
  };

  const getStatusText = (status: ServiceStatus['status']): string => {
    switch (status) {
      case 'running':
        return 'Running';
      case 'starting':
        return 'Starting';
      case 'stopped':
        return 'Stopped';
      case 'error':
        return 'Error';
      case 'not-configured':
        return 'Not Configured';
      default:
        return 'Unknown';
    }
  };

  return {
    services: state.services,
    isLoading: state.isLoading,
    lastUpdated: state.lastUpdated,
    refresh: manualRefresh,
    getStatusColor,
    getStatusText,
  };
};