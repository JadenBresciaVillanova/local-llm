// frontend/src/app/layout.tsx
import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "../styles/globals.css";
import Providers from "../components/Providers";
import Header from "../components/Header";
import { ChatProvider } from "../context/ChatContext"; // 👈 1. Import the provider

const inter = Inter({ subsets: ["latin"] });

export const metadata: Metadata = {
  title: "Local RAG Chat",
  description: "Chat with your documents locally.",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body className={inter.className}>
        <Providers>
          <ChatProvider> {/* 👈 2. Wrap the layout with ChatProvider */}
            <div className="flex flex-col min-h-screen bg-gray-100">
              <Header />
              <main className="flex-1">
                  {children}
              </main>
            </div>
          </ChatProvider>
        </Providers>
      </body>
    </html>
  );
}