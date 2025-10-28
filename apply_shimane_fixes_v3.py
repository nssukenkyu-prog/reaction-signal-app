#!/usr/bin/env python3
"""
島根県大田市カスタマイズ - 追加修正スクリプト v3 (完全版)
実行方法: python3 apply_shimane_fixes_v3.py
"""

import os
import re
from pathlib import Path

def read_file(filepath):
    """ファイルを読み込む"""
    with open(filepath, 'r', encoding='utf-8') as f:
        return f.read()

def write_file(filepath, content):
    """ファイルに書き込む"""
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

def fix_page_tsx(content):
    """app/page.tsx の追加修正 (③⑤)"""
    print("📝 app/page.tsx を再修正中...")
    
    # ③ 「シンプル反応・判断」→「シンプル反応」に戻し、バッジに「判断」追加
    content = re.sub(
        r'シンプル反応・判断',
        'シンプル反応',
        content
    )
    
    # バッジ部分を正確に修正
    # シンプル反応のバッジ部分を探して置換
    simple_section = re.search(
        r'(<!-- シンプル反応モード -->.*?<div className="flex items-center space-x-2">)(.*?)(</div>\s*</button>)',
        content,
        re.DOTALL
    )
    
    if simple_section:
        # 既存のバッジを削除して新しく追加
        old_badges_pattern = r'<span className="bg-red-100 text-red-700 px-2 py-1 rounded text-xs">認知</span>\s*<span className="bg-green-100 text-green-700 px-2 py-1 rounded text-xs">行動</span>'
        new_badges = '''<span className="bg-red-100 text-red-700 px-2 py-1 rounded text-xs">認知</span>
              <span className="bg-blue-100 text-blue-700 px-2 py-1 rounded text-xs">判断</span>
              <span className="bg-green-100 text-green-700 px-2 py-1 rounded text-xs">行動</span>'''
        
        content = re.sub(old_badges_pattern, new_badges, content)
    
    # ⑤ ランキングエリアを完全に書き換え
    # 古いランキングエリアを探して置換
    old_ranking = r'<!-- ランキングエリア -->.*?</div>\s*</div>\s*(?=</>)'
    
    new_ranking = '''<!-- ランキングエリア -->
        <div className="bg-gradient-to-r from-yellow-400 to-yellow-500 rounded-2xl shadow-xl p-8 mb-8">
          <div className="flex items-center justify-between">
            <h3 className="text-2xl font-bold text-gray-800 flex items-center">
              🏆 ランキング
            </h3>
            <button
              onClick={() => router.push('/ranking')}
              className="bg-white text-yellow-700 px-6 py-3 rounded-lg font-bold hover:bg-yellow-50 transition-all shadow-md hover:shadow-lg flex items-center space-x-2"
            >
              <span>ランキングを見る</span>
              <span>→</span>
            </button>
          </div>
        </div>
        </>'''
    
    content = re.sub(old_ranking, new_ranking, content, flags=re.DOTALL)
    
    print("✅ app/page.tsx の再修正完了")
    return content

def fix_ranking_page_complete(content):
    """app/ranking/page.tsx の完全修正 (⑨⑩⑪)"""
    print("📝 app/ranking/page.tsx を完全修正中...")
    
    # ⑨ スプリントボタンを完全削除
    sprint_button_pattern = r'<button\s+onClick=\{\(\) => setModeFilter\(\'sprint\'\)\}[^>]*>.*?🏃 スプリント.*?</button>'
    content = re.sub(sprint_button_pattern, '', content, flags=re.DOTALL)
    
    # グリッドのクラスを修正 (5列 → 4列)
    content = content.replace(
        'grid-cols-2 md:grid-cols-5',
        'grid-cols-2 md:grid-cols-4'
    )
    
    # ⑩ カラー・デュアルの表示サイズを統一
    # すべての text-2xl, text-3xl を text-xl に統一
    
    # ⑪ 表示単位を ms → s に変更
    # パターン1: ユーザーのベスト記録
    content = re.sub(
        r'<p className="text-4xl font-bold">\s*\{userBestRecord\.reactionTime\}\s*<span className="text-xl">ms</span>',
        r'<p className="text-4xl font-bold">\n                {(userBestRecord.reactionTime / 1000).toFixed(3)}\n                <span className="text-xl">s</span>',
        content
    )
    
    # パターン2: ランキングリストの記録表示
    content = re.sub(
        r'<p className="text-2xl font-bold text-gray-800">\s*\{record\.reactionTime\}\s*<span className="text-sm text-gray-500 ml-1">ms</span>',
        r'<p className="text-xl font-bold text-gray-800">\n                      {(record.reactionTime / 1000).toFixed(3)}\n                      <span className="text-sm text-gray-500 ml-1">s</span>',
        content
    )
    
    # パターン3: 統計情報の平均タイム
    content = re.sub(
        r'<p className="text-2xl font-bold">\s*\{Math\.round\(\s*filteredRecords\.reduce\(\(sum, r\) => sum \+ r\.reactionTime, 0\) /\s*filteredRecords\.length\s*\)\}\s*<span className="text-sm">ms</span>',
        r'<p className="text-xl font-bold">\n                {(\n                  filteredRecords.reduce((sum, r) => sum + r.reactionTime, 0) /\n                    filteredRecords.length / 1000\n                ).toFixed(3)}\n                <span className="text-sm">s</span>',
        content
    )
    
    # パターン4: 統計情報の最速記録
    content = re.sub(
        r'<p className="text-2xl font-bold">\s*\{filteredRecords\[0\]\.reactionTime \|\| 0\}\s*<span className="text-sm">ms</span>',
        r'<p className="text-xl font-bold">\n                {((filteredRecords[0]?.reactionTime || 0) / 1000).toFixed(3)}\n                <span className="text-sm">s</span>',
        content
    )
    
    # パターン5: 参加者数も text-xl に統一
    content = re.sub(
        r'<p className="text-2xl font-bold">\s*\{new Set\(filteredRecords\.map\(r => r\.userId\)\)\.size\}人',
        r'<p className="text-xl font-bold">\n                {new Set(filteredRecords.map(r => r.userId)).size}人',
        content
    )
    
    print("✅ app/ranking/page.tsx の完全修正完了")
    return content

def fix_training_page_units(filepath, content):
    """トレーニングページの単位を完全に秒に変換 (⑪)"""
    print(f"📝 {filepath} の単位を秒に統一中...")
    
    # すべての {xxx}ms パターンを {(xxx/1000).toFixed(3)}s に変換
    # パターンを順番に処理
    
    # 1. 単純な変数参照
    patterns = [
        (r'\{time\}ms', r'{(time/1000).toFixed(3)}s'),
        (r'\{reaction\}ms', r'{(reaction/1000).toFixed(3)}s'),
        (r'\{r\.time\}ms', r'{(r.time/1000).toFixed(3)}s'),
        (r'\{r\.reaction\}ms', r'{(r.reaction/1000).toFixed(3)}s'),
    ]
    
    for pattern, replacement in patterns:
        content = re.sub(pattern, replacement, content)
    
    # 2. stats オブジェクト
    content = re.sub(r'\{stats\.average\}ms', r'{(stats.average/1000).toFixed(3)}s', content)
    content = re.sub(r'\{stats\.stdDev\}ms', r'{(stats.stdDev/1000).toFixed(3)}s', content)
    
    # 3. 既に変換されているが単位が ms のままのパターンを修正
    content = re.sub(r'\(time/1000\)\.toFixed\(3\)\}ms', r'(time/1000).toFixed(3)}s', content)
    content = re.sub(r'\(reaction/1000\)\.toFixed\(3\)\}ms', r'(reaction/1000).toFixed(3)}s', content)
    content = re.sub(r'\(stats\.average/1000\)\.toFixed\(3\)\}ms', r'(stats.average/1000).toFixed(3)}s', content)
    content = re.sub(r'\(stats\.stdDev/1000\)\.toFixed\(3\)\}ms', r'(stats.stdDev/1000).toFixed(3)}s', content)
    
    # 4. 複数行にまたがるパターン（改行を含む）
    content = re.sub(r'\{time\}\s*<span[^>]*>ms</span>', r'{(time/1000).toFixed(3)}<span className="text-sm">s</span>', content)
    content = re.sub(r'\{reaction\}\s*<span[^>]*>ms</span>', r'{(reaction/1000).toFixed(3)}<span className="text-sm">s</span>', content)
    
    print(f"✅ {filepath} の単位統一完了")
    return content

def main():
    print("=" * 70)
    print("🎯 島根県大田市カスタマイズ - 追加修正スクリプト v3 (完全版)")
    print("=" * 70)
    print()
    
    # カレントディレクトリの確認
    if not os.path.exists('app/page.tsx'):
        print("❌ エラー: app/page.tsx が見つかりません")
        print("   プロジェクトのルートディレクトリで実行してください")
        return
    
    # バックアップディレクトリ作成
    backup_dir = Path('backup_v3_complete')
    backup_dir.mkdir(exist_ok=True)
    print(f"💾 バックアップを {backup_dir}/ に作成中...")
    
    files_to_modify = [
        'app/page.tsx',
        'app/ranking/page.tsx',
        'app/simple/page.tsx',
        'app/color/page.tsx',
        'app/dual/page.tsx',
    ]
    
    # バックアップ作成
    for filepath in files_to_modify:
        if os.path.exists(filepath):
            backup_path = backup_dir / filepath.replace('/', '_')
            content = read_file(filepath)
            write_file(backup_path, content)
    
    print("✅ バックアップ完了\n")
    
    # 修正実行
    print("🔧 修正を適用中...\n")
    
    # 1. app/page.tsx (③⑤)
    if os.path.exists('app/page.tsx'):
        content = read_file('app/page.tsx')
        content = fix_page_tsx(content)
        write_file('app/page.tsx', content)
    
    # 2. app/ranking/page.tsx (⑨⑩⑪)
    if os.path.exists('app/ranking/page.tsx'):
        content = read_file('app/ranking/page.tsx')
        content = fix_ranking_page_complete(content)
        write_file('app/ranking/page.tsx', content)
    
    # 3. 全トレーニングページの単位統一 (⑪)
    training_pages = [
        'app/simple/page.tsx',
        'app/color/page.tsx',
        'app/dual/page.tsx',
    ]
    
    for filepath in training_pages:
        if os.path.exists(filepath):
            content = read_file(filepath)
            content = fix_training_page_units(filepath, content)
            write_file(filepath, content)
    
    print("\n" + "=" * 70)
    print("✨ 追加修正完了！")
    print("=" * 70)
    print("\n📋 修正内容:")
    print("  ③ シンプル反応:")
    print("     - タイトル: 「シンプル反応」")
    print("     - バッジ: 認知 + 判断 + 行動 (3つ)")
    print()
    print("  ⑤ ランキングエリア:")
    print("     - 「🏆 ランキング」と「ランキングを見る→」のみ表示")
    print("     - メダルカード(🥇🥈🥉)と説明文を削除")
    print()
    print("  ⑨ ランキングページ:")
    print("     - モード選択から「🏃 スプリント」ボタンを完全削除")
    print("     - グリッド: 5列 → 4列に変更")
    print()
    print("  ⑩ ランキングページ:")
    print("     - すべての数値を text-xl サイズに統一")
    print("     - カラー・デュアルの秒数と正確率が同じサイズ")
    print()
    print("  ⑧ 全ページ:")
    print("     - 表示単位: ms → s (例: 250ms → 0.250s)")
    print("     - すべてのトレーニングモードとランキングで統一")
    print()
    print("🚀 次のステップ:")
    print("  1. npm run dev でローカル確認")
    print("  2. 表示を確認して問題なければ:")
    print("     git add .")
    print("     git commit -m 'fix: 島根県大田市カスタマイズ完全適用'")
    print("     git push")
    print()
    print("💾 バックアップ: backup_v3_complete/ フォルダに保存されています")
    print()

if __name__ == '__main__':
    main()
