/** @type {import('next').NextConfig} */
const nextConfig = {
  // Use static export for production builds, but allow rewrites for development
  ...(process.env.NODE_ENV === 'production' ? {
    output: 'export',
    trailingSlash: true,
  } : {}),

  images: {
    unoptimized: true
  },

  // API rewrites for development - proxy API calls to backend
  // These only work in development mode (not with static export)
  async rewrites() {
    if (process.env.NODE_ENV === 'production') {
      return [];
    }

    return [
      {
        source: '/api/:path*',
        destination: 'http://localhost:8000/api/:path*',
      },
      {
        source: '/health',
        destination: 'http://localhost:8000/health',
      },
    ];
  },
}

module.exports = nextConfig
