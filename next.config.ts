import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  images: {
    unoptimized: true,
  },
  async redirects() {
    const vercelUrl = process.env.VERCEL_URL || '';
    
    console.log('🔍 VERCEL_URL:', vercelUrl);
    
    // 特定のプレビューURL（c83ads2dp）の場合のみリダイレクト
    if (vercelUrl.includes('c83ads2dp')) {
      console.log('✅ 特定プレビューURL検出 - リダイレクト実行');
      return [
        {
          source: '/:path*',
          destination: 'https://reaction-signal-app.vercel.app/:path*',
          permanent: false,
        },
      ];
    }
    
    console.log('❌ リダイレクト条件非該当');
    return [];
  },
};

export default nextConfig;
