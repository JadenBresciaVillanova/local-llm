// frontend/src/lib/api.ts

import axios from 'axios';
import { getSession } from 'next-auth/react';

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

// Create the axios instance
const apiClient = axios.create({
  baseURL: API_URL,
});

// Use an interceptor to dynamically add the Authorization header
apiClient.interceptors.request.use(
  async (config) => {
    const session = await getSession();
    
    // Let's use the same property name we defined in the session callback
    const token = (session as any)?.accessToken;

    console.log("Interceptor check. Session:", session);
    console.log("Interceptor check. Token:", token);

    if (token) {
      config.headers['Authorization'] = `Bearer ${token}`;
      console.log("Authorization header attached.");
    } else {
      console.log("No token found, request will be unauthenticated.");
    }
    
    return config;
  },
  (error) => {
    // This handles errors that happen when preparing the request
    return Promise.reject(error);
  }
);

export default apiClient;