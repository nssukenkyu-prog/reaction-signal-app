import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  images: {
    unoptimized: true,
  },
  async redirects() {
    const redirects = [];
    const isPreview = process.env.VERCEL_ENV === 'preview';
    const vercelUrl = process.env.VERCEL_URL || '';
    
    // より広範囲でプレビュー環境を検出
    const isNotProductionUrl = !vercelUrl.includes('reaction-signal-app.vercel.app');
    
    console.log('🔍 Debug Info:');
    console.log('VERCEL_ENV:', process.env.VERCEL_ENV);
    console.log('VERCEL_URL:', vercelUrl);
    console.log('isPreview:', isPreview);
    console.log('isNotProductionUrl:', isNotProductionUrl);
    
    // プレビュー環境で、かつ本番URLでない場合にリダイレクト
    if (isPreview && isNotProductionUrl) {
      console.log('✅ Redirect条件に該当 - リダイレクト設定を追加');
      redirects.push({
        source: '/:path*',
        destination: 'https://reaction-signal-app.vercel.app/:path*',
        permanent: false,
      });
    } else {
      console.log('❌ Redirect条件に非該当');
    }
    
    return redirects;
  },
};

export default nextConfig;
