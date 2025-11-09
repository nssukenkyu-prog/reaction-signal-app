'use client';

import { useEffect } from 'react';

export default function RedirectHandler() {
    useEffect(() => {
          // プレビュー環境（c83ads2dp）の場合、本番環境にリダイレクト
                  if (typeof window !== 'undefined' && window.location.hostname.includes('c83ads2dp')) {
                          const productionUrl = window.location.href.replace(
                                    window.location.origin,
                                    'https://reaction-signal-app.vercel.app'
                                  );
                          console.log('🔄 リダイレクト:', window.location.href, '→', productionUrl);
                          window.location.replace(productionUrl);
                  }
    }, []);

  return null;
}
