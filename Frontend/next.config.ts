import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  /* config options here */
  swcMinify: true,
  images: {
    domains: ['unsplash.com'],
    remotePatterns: [
      {
        protocol: 'https',
        hostname: 'unsplash.com',
        pathname: '**',
      },
    ],
  },
};

export default nextConfig;
