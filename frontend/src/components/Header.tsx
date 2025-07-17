// frontend/src/components/Header.tsx
"use client";

import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { useSession, signOut } from 'next-auth/react'; // Import session hooks

export default function Header() {
  const pathname = usePathname();
  const { data: session } = useSession(); // Get session data

  const navLinkClasses = (path: string) => 
    // ... (no change to this function)
    `px-3 py-2 rounded-md text-sm font-medium transition-colors ${
      pathname === path 
        ? 'bg-blue-500 text-white' 
        : 'text-gray-700 hover:bg-gray-200'
    }`;


  return (
    <header className="bg-white shadow-sm sticky top-0 z-40">
      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:p-8">
        <div className="flex items-center justify-between h-6">
          <div className="flex-shrink-0">
              <Link href="/" className="text-xl font-bold text-gray-800">LocalAI</Link>
          </div>
          <div className="flex items-center space-x-4">
            {session && (
                <>
                    <nav className="flex space-x-4">
                        <Link href="/chats" className={navLinkClasses('/chats')}>Past Chats</Link>
                        <Link href="/" className={navLinkClasses('/')}>Chat</Link>
                        <Link href="/docs" className={navLinkClasses('/docs')}>Docs</Link>
                        <Link href="/models" className={navLinkClasses('/models')}>Models</Link>
                    </nav>
                    <div className="flex items-center space-x-2">
                        <span className="text-sm text-gray-500">{session.user?.email}</span>
                        <button 
                            onClick={() => signOut()}
                            className="px-3 py-1 bg-red-500 text-white text-xs font-semibold rounded-md hover:bg-red-600"
                        >
                            Sign Out
                        </button>
                    </div>
                </>
            )}
          </div>
        </div>
      </div>
    </header>
  );
}