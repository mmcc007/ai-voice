import type { Metadata } from 'next';
import { Inter } from 'next/font/google';
import './globals.css';

const inter = Inter({ subsets: ['latin'] });

export const metadata: Metadata = {
  title: 'AI Voice Calling App',
  description: 'Make outbound calls with LiveKit AI voice agents',
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body className={inter.className}>
        <div className="min-h-screen flex flex-col">
          <header className="bg-primary p-4 text-white">
            <div className="container mx-auto">
              <h1 className="text-2xl font-bold">AI Voice Calling</h1>
            </div>
          </header>
          <main className="flex-grow container mx-auto p-4">
            {children}
          </main>
          <footer className="bg-gray-100 p-4 text-center text-gray-600">
            <div className="container mx-auto">
              <p>© {new Date().getFullYear()} AI Voice Calling App</p>
            </div>
          </footer>
        </div>
      </body>
    </html>
  );
}
