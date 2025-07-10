// frontend/src/components/Providers.tsx
"use client";

import { SessionProvider } from "next-auth/react";
import React from "react";

// This is a client component that wraps its children in the SessionProvider
export default function Providers({ children }: { children: React.ReactNode }) {
  return <SessionProvider>{children}</SessionProvider>;
}