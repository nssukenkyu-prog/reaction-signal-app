#!/usr/bin/env python3
"""
島根県大田市カスタマイズ - 追加修正スクリプト v2
実行方法: python3 apply_shimane_fixes_v2.py
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
    # まず、タイトルを「シンプル反応」に修正
    content = re.sub(
        r'シンプル反応・判断',
        'シンプル反応',
        content
    )
    
    # バッジ部分を修正：「認知」「判断」「行動」の3つに
    old_badges = '''<div className="flex items-center space-x-2">
              <span className="bg-red-100 text-red-700 px-2 py-1 rounded text-xs">認知</span>
              <span className="bg-green-100 text-green-700 px-2 py-1 rounded text-xs">行動</span>
            </div>'''
    
    new_badges = '''<div className="flex items-center space-x-2">
              <span className="bg-red-100 text-red-700 px-2 py-1 rounded text-xs">認知</span>
              <span className="bg-blue-100 text-blue-700 px-2 py-1 rounded text-xs">判断</span>
              <span className="bg-green-100 text-green-700 px-2 py-1 rounded text-xs">行動</span>
            </div>'''
    
    content = content.replace(old_badges, new_badges)
    
    # ⑤ ランキングエリア全体を簡略化
    # 古いランキングエリアのパターンを探す
    ranking_pattern = r'(<!-- ランキングエリア -->.*?<div className="bg-gradient-to-r from-yellow-400 to-yellow-500 rounded-2xl shadow-xl p-8 mb-8">)(.*?)(</div>\s*</div>)'
    
    new_ranking_section = '''<!-- ランキングエリア -->
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
        </div>'''
    
    # ランキングエリア全体を置き換え
    content = re.sub(
        r'<!-- ランキングエリア -->.*?<div className="bg-gradient-to-r from-yellow-400 to-yellow-500 rounded-2xl shadow-xl p-8 mb-8">.*?</div>\s*</div>',
        new_ranking_section,
        content,
        flags=re.DOTALL
    )
    
    print("✅ app/page.tsx の再修正完了")
    return content

def fix_ranking_page(content):
    """app/ranking/page.tsx の追加修正 (⑨⑩⑪)"""
    print("📝 app/ranking/page.tsx を再修正中...")
    
    # ⑨ スプリントモードの選択肢を削除
    content = re.sub(
        r'<button[^>]*onClick=\{\(\) => setMode\(\'sprint\'\)\}[^>]*>.*?スプリント.*?</button>',
        '',
        content,
        flags=re.DOTALL
    )
    
    # ⑩ カラーとデュアルの表示を統一（秒数と正確率を同じサイズで）
    # "text-3xl" → "text-xl" に変更して統一
    # カラーモードの結果表示部分
    content = re.sub(
        r'(<div className="bg-white rounded-lg p-4">.*?カラー判断.*?<p className="text-xs text-gray-500 mb-2">平均反応時間</p>.*?<p className=")(text-3xl|text-2xl)(.*?font-bold text-blue-600">)',
        r'\1text-xl\3',
        content,
        flags=re.DOTALL
    )
    
    content = re.sub(
        r'(<p className="text-xs text-gray-500 mb-2">正確率</p>.*?<p className=")(text-3xl|text-2xl)(.*?font-bold text-green-600">)',
        r'\1text-xl\3',
        content,
        flags=re.DOTALL
    )
    
    # デュアルタスクの結果表示部分
    content = re.sub(
        r'(<div className="bg-white rounded-lg p-4">.*?デュアルタスク.*?<p className="text-xs text-gray-500 mb-2">平均反応時間</p>.*?<p className=")(text-3xl|text-2xl)(.*?font-bold text-purple-600">)',
        r'\1text-xl\3',
        content,
        flags=re.DOTALL
    )
    
    content = re.sub(
        r'(<p className="text-xs text-gray-500 mb-2">正確率</p>.*?<p className=")(text-3xl|text-2xl)(.*?font-bold text-green-600">)',
        r'\1text-xl\3',
        content,
        flags=re.DOTALL
    )
    
    # ⑪ ランキングページの表示単位を ms → s に変更
    # 既に toFixed(3) がある場合はスキップ
    if '.toFixed(3)' not in content:
        # record.avgTimeをミリ秒から秒に変換
        content = re.sub(
            r'{record\.avgTime}ms',
            r'{(record.avgTime / 1000).toFixed(3)}s',
            content
        )
        
        content = re.sub(
            r'{record\.avgTime}',
            r'{(record.avgTime / 1000).toFixed(3)}',
            content
        )
    
    # すでに変換されているパターンも確認
    # パターン: (record.avgTime/1000).toFixed(3) があれば、単位が s になっているか確認
    content = re.sub(
        r'\(record\.avgTime/1000\)\.toFixed\(3\)\}ms',
        r'(record.avgTime/1000).toFixed(3)}s',
        content
    )
    
    print("✅ app/ranking/page.tsx の再修正完了")
    return content

def fix_all_training_pages(filepath, content):
    """全トレーニングページの表示単位を秒に統一 (⑪)"""
    print(f"📝 {filepath} の単位を秒に統一中...")
    
    # 既に toFixed(3) が含まれている場合はスキップのパターンもある
    # すべての {time}ms, {reaction}ms パターンを変換
    
    # パターン1: 直接的な time 変数
    content = re.sub(r'{time}ms\b', r'{(time/1000).toFixed(3)}s', content)
    content = re.sub(r'{reaction}ms\b', r'{(reaction/1000).toFixed(3)}s', content)
    
    # パターン2: stats.average
    content = re.sub(r'{stats\.average}ms\b', r'{(stats.average/1000).toFixed(3)}s', content)
    
    # パターン3: stats.stdDev
    if '(stats.stdDev/1000).toFixed(3)' not in content:
        content = re.sub(r'{stats\.stdDev}ms\b', r'{(stats.stdDev/1000).toFixed(3)}s', content)
    
    # パターン4: 個別の試行結果 (配列内)
    content = re.sub(r'{r\.time}ms\b', r'{(r.time/1000).toFixed(3)}s', content)
    content = re.sub(r'{r\.reaction}ms\b', r'{(r.reaction/1000).toFixed(3)}s', content)
    
    # パターン5: result.time や result.avgTime
    content = re.sub(r'{result\.time}ms\b', r'{(result.time/1000).toFixed(3)}s', content)
    content = re.sub(r'{result\.avgTime}ms\b', r'{(result.avgTime/1000).toFixed(3)}s', content)
    
    # 既に変換されているが、単位が ms のままのパターンを修正
    content = re.sub(
        r'\(time/1000\)\.toFixed\(3\)\}ms',
        r'(time/1000).toFixed(3)}s',
        content
    )
    
    content = re.sub(
        r'\(reaction/1000\)\.toFixed\(3\)\}ms',
        r'(reaction/1000).toFixed(3)}s',
        content
    )
    
    content = re.sub(
        r'\(stats\.average/1000\)\.toFixed\(3\)\}ms',
        r'(stats.average/1000).toFixed(3)}s',
        content
    )
    
    print(f"✅ {filepath} の単位統一完了")
    return content

def main():
    print("=" * 60)
    print("🎯 島根県大田市カスタマイズ - 追加修正スクリプト v2")
    print("=" * 60)
    print()
    
    # カレントディレクトリの確認
    if not os.path.exists('app/page.tsx'):
        print("❌ エラー: app/page.tsx が見つかりません")
        print("   プロジェクトのルートディレクトリで実行してください")
        return
    
    # バックアップディレクトリ作成
    backup_dir = Path('backup_v2')
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
        content = fix_ranking_page(content)
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
            content = fix_all_training_pages(filepath, content)
            write_file(filepath, content)
    
    print("\n" + "=" * 60)
    print("✨ 追加修正完了！")
    print("=" * 60)
    print("\n📋 修正内容:")
    print("  ③ シンプル反応: タイトルを「シンプル反応」に戻し、バッジに「判断」追加")
    print("  ⑤ ランキングエリア: 「ランキングを見る→」のみのシンプル表示")
    print("  ⑨ ランキングページ: スプリントモード選択肢を削除")
    print("  ⑩ ランキングページ: カラー・デュアルの秒数と正確率を同じサイズで表示")
    print("  ⑪ 全ページ: 表示単位を ms → s に統一（0.3224s 形式）")
    print("\n🚀 次のステップ:")
    print("  1. npm run dev でローカル確認")
    print("  2. git add .")
    print("  3. git commit -m 'fix: 島根県大田市カスタマイズ追加修正'")
    print("  4. git push")
    print("\n💾 バックアップ: backup_v2/ フォルダに保存されています")
    print()

if __name__ == '__main__':
    main()
