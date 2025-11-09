import { NextResponse } from 'next/server'
import type { NextRequest } from 'next/server'

export function middleware(request: NextRequest) {
  const hostname = request.headers.get('host') || '';
  
  // 特定のプレビューURL（c83ads2dp）の場合、本番環境にリダイレクト
  if (hostname.includes('c83ads2dp')) {
    const productionUrl = new URL(request.url);
    productionUrl.host = 'reaction-signal-app.vercel.app';
    
    console.log('🔄 リダイレクト:', hostname, '→', productionUrl.host);
    
    return NextResponse.redirect(productionUrl, 307); // 307 = 一時的リダイレクト
  }
  
  return NextResponse.next();
}

export const config = {
  matcher: [
    /*
     * Match all request paths except for the ones starting with:
     * - api (API routes)
     * - _next/static (static files)
     * - _next/image (image optimization files)
     * - favicon.ico (favicon file)
     */
    '/((?!api|_next/static|_next/image|favicon.ico).*)',
  ],
}
