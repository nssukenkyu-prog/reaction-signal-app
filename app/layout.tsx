import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";
import RedirectHandler from "./components/RedirectHandler";  // ← 追加

const inter = Inter({ subsets: ["latin"] });

export const metadata: Metadata = {
  title: "リアクショントレーニングシステム",
  description: "島根県大田市内の方々にご利用いただけますするWebアプリケーション",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="ja">
      <body className={inter.className}>
        <RedirectHandler />  {/* ← 追加 */}
        <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-red-50">
          {/* ヘッダー */}
          <header className="bg-white shadow-md border-b-4 border-red-600">
            <div className="container mx-auto px-4 py-4">
              <div className="flex flex-col items-center text-center space-y-2">
                <h1 className="text-2xl md:text-3xl font-bold text-gray-800">
                  ⚡リアクショントレーニングシステム⚡<br />⛰️島根県大田市限定版⛰️
                </h1>
                <p className="text-xs md:text-sm text-gray-500 max-w-2xl">
                  本システムは2025年11月9日開催の<br />島根県大田市と学校法人日本体育大学の<br />自治体連携協定推進事業に際して作成されました。
                </p>
                <div className="flex items-center space-x-2 text-xs md:text-sm text-gray-500">
                  <span className="bg-red-100 text-red-700 px-2 py-1 rounded">認知</span>
                  <span className="bg-blue-100 text-blue-700 px-2 py-1 rounded">判断</span>
                  <span className="bg-green-100 text-green-700 px-2 py-1 rounded">行動</span>
                </div>
              </div>
            </div>
          </header>

          {/* メインコンテンツ */}
          <main className="container mx-auto px-4 py-8">
            {children}
          </main>

          {/* フッター */}
          <footer className="bg-gray-800 text-white py-6 mt-16">
            <div className="container mx-auto px-4 text-center">
              <p className="text-sm">
                島根県大田市内の方々にご利用いただけます
              </p>
              <p className="text-xs text-gray-400 mt-2">
                Built by Kedo Bot and Yuzu Bot / NSSU
              </p>
            </div>
          </footer>
        </div>
      </body>
    </html>
  );
}
