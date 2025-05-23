import type { Metadata } from 'next'
import './globals.css'

export const metadata: Metadata = {
  title: 'Emoji Chat',
  description: 'Chat with emojis - Express yourself with AI-generated emoji responses',
}

export const viewport = {
  width: 'device-width',
  initialScale: 1,
  maximumScale: 1,
  userScalable: false,
  viewportFit: 'cover',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  )
}
