import type { Metadata } from 'next';
import './globals.css';

export const metadata: Metadata = {
  title: 'NexusQuant Explosive Hunter V3',
  description: 'AI trading platform for highest-conviction NIFTY and SENSEX option premium expansion moves.',
};

export default function RootLayout({ children }: Readonly<{ children: React.ReactNode }>) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
