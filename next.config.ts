import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  // output: 'export', ← この行を削除またはコメントアウト
  images: {
    unoptimized: true,
  },
  async redirects() {
    const redirects = [];
    const isPreview = process.env.VERCEL_ENV === 'preview';
    const isTargetPreview = process.env.VERCEL_URL?.includes('c83ads2dp');
    
    if (isPreview && isTargetPreview) {
      redirects.push({
        source: '/:path*',
        destination: 'https://reaction-signal-app.vercel.app/:path*',
        permanent: false,
      });
    }
    
    return redirects;
  },
};

export default nextConfig;
