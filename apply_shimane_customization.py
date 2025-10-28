#!/usr/bin/env python3
"""
島根県大田市カスタマイズ - 11項目修正スクリプト
実行方法: python3 apply_shimane_customization.py
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

def modify_layout_tsx(content):
    """app/layout.tsx の修正 (①②⑥⑦)"""
    print("📝 app/layout.tsx を修正中...")
    
    # ① タイトル変更
    content = content.replace(
        '⚡ リアクショントレーニングシステム',
        '⚡リアクショントレーニングシステム⚡<br />⛰️島根県大田市限定版⛰️'
    )
    
    # ② 説明文に改行追加
    content = content.replace(
        '本システムは2025年11月9日開催の島根県大田市と学校法人日本体育大学の自治体連携協定推進事業に際して作成されました。',
        '本システムは2025年11月9日開催の<br />島根県大田市と学校法人日本体育大学の<br />自治体連携協定推進事業に際して作成されました。'
    )
    
    # ⑥ フッターテキスト変更
    content = content.replace(
        '認知・判断・行動を科学的にトレーニング',
        '島根県大田市内の方々にご利用いただけます'
    )
    
    # ⑦ コピーライト変更
    content = content.replace(
        '© 2025 島根県大田市 × 学校法人日本体育大学 自治体連携協定推進事業',
        'Built by Kedo Bot and Yuzu Bot / NSSU'
    )
    
    print("✅ app/layout.tsx の修正完了")
    return content

def modify_page_tsx(content):
    """app/page.tsx の修正 (③④⑤)"""
    print("📝 app/page.tsx を修正中...")
    
    # ③ シンプル反応に「判断」追加
    content = content.replace(
        '<h3 className="text-xl font-bold text-gray-800 mb-2 group-hover:text-blue-600">\n              シンプル反応\n            </h3>\n            <p className="text-sm text-gray-600 mb-3">\n              シグナルに反応する速さを測定',
        '<h3 className="text-xl font-bold text-gray-800 mb-2 group-hover:text-blue-600">\n              シンプル反応・判断\n            </h3>\n            <p className="text-sm text-gray-600 mb-3">\n              シグナルに反応する速さを測定'
    )
    
    # ④ デュアルタスクから「NEW!」削除
    content = re.sub(
        r'<span className="bg-purple-100 text-purple-700 px-2 py-1 rounded text-xs font-bold">NEW!</span>',
        '',
        content
    )
    
    # ⑤ ランキングセクション簡略化
    content = content.replace(
        '<p className="text-sm text-gray-700 mt-1">\n                みんなの記録を見て、目標を立てよう！\n              </p>',
        ''
    )
    
    print("✅ app/page.tsx の修正完了")
    return content

def modify_simple_page(content):
    """app/simple/page.tsx の修正 (⑪)"""
    print("📝 app/simple/page.tsx を修正中...")
    
    # ⑪ 表示単位を ms → s に変更 (すべてのパターン)
    # パターン1: {time}ms
    content = re.sub(r'{time}ms', r'{(time/1000).toFixed(3)}s', content)
    content = re.sub(r'{reaction}ms', r'{(reaction/1000).toFixed(3)}s', content)
    
    # パターン2: 平均反応時間の表示
    content = re.sub(
        r'{stats\.average}ms',
        r'{(stats.average/1000).toFixed(3)}s',
        content
    )
    
    # パターン3: 標準偏差の表示（既に修正済みかもしれない）
    if '(stats.stdDev/1000).toFixed(3)' not in content:
        content = re.sub(
            r'{stats\.stdDev}ms',
            r'{(stats.stdDev/1000).toFixed(3)}s',
            content
        )
    
    print("✅ app/simple/page.tsx の修正完了")
    return content

def modify_color_page(content):
    """app/color/page.tsx の修正 (⑩⑪)"""
    print("📝 app/color/page.tsx を修正中...")
    
    # ⑩ 表示サイズをデュアルと統一
    # カラーページのシグナル表示を150px→200pxに変更
    content = re.sub(
        r'(className="w-\[)150(px\] h-\[)150(px\])',
        r'\g<1>200\g<2>200\g<3>',
        content
    )
    
    # ⑪ 表示単位を ms → s に変更
    content = re.sub(r'{time}ms', r'{(time/1000).toFixed(3)}s', content)
    content = re.sub(r'{reaction}ms', r'{(reaction/1000).toFixed(3)}s', content)
    content = re.sub(r'{stats\.average}ms', r'{(stats.average/1000).toFixed(3)}s', content)
    
    if '(stats.stdDev/1000).toFixed(3)' not in content:
        content = re.sub(r'{stats\.stdDev}ms', r'{(stats.stdDev/1000).toFixed(3)}s', content)
    
    print("✅ app/color/page.tsx の修正完了")
    return content

def modify_dual_page(content):
    """app/dual/page.tsx の修正 (⑩⑪)"""
    print("📝 app/dual/page.tsx を修正中...")
    
    # ⑩ 表示サイズは既に200pxのはずなので確認のみ
    # ⑪ 表示単位を ms → s に変更
    content = re.sub(r'{time}ms', r'{(time/1000).toFixed(3)}s', content)
    content = re.sub(r'{reaction}ms', r'{(reaction/1000).toFixed(3)}s', content)
    content = re.sub(r'{stats\.average}ms', r'{(stats.average/1000).toFixed(3)}s', content)
    
    if '(stats.stdDev/1000).toFixed(3)' not in content:
        content = re.sub(r'{stats\.stdDev}ms', r'{(stats.stdDev/1000).toFixed(3)}s', content)
    
    print("✅ app/dual/page.tsx の修正完了")
    return content

def modify_ranking_page(content):
    """app/ranking/page.tsx の修正 (⑧)"""
    print("📝 app/ranking/page.tsx を修正中...")
    
    # ⑧ 講座名の表示を削除
    # "参加講座" や "講座" という文字列を含む行を削除
    lines = content.split('\n')
    modified_lines = []
    skip_next = False
    
    for i, line in enumerate(lines):
        if skip_next:
            skip_next = False
            continue
        
        # "参加講座" や "講座" を含む行とその値の行をスキップ
        if '講座' in line or 'session' in line and 'className' in line:
            # この行とその値が表示される行をスキップ
            if i + 1 < len(lines) and ('record.session' in lines[i+1] or '{record.sessionName}' in lines[i+1]):
                skip_next = True
            continue
        
        modified_lines.append(line)
    
    content = '\n'.join(modified_lines)
    
    print("✅ app/ranking/page.tsx の修正完了")
    return content

def main():
    print("=" * 60)
    print("🎯 島根県大田市カスタマイズ - 11項目修正スクリプト")
    print("=" * 60)
    print()
    
    # カレントディレクトリの確認
    if not os.path.exists('app/layout.tsx'):
        print("❌ エラー: app/layout.tsx が見つかりません")
        print("   プロジェクトのルートディレクトリで実行してください")
        return
    
    # バックアップディレクトリ作成
    backup_dir = Path('backup_before_shimane')
    backup_dir.mkdir(exist_ok=True)
    print(f"💾 バックアップを {backup_dir}/ に作成中...")
    
    files_to_modify = [
        'app/layout.tsx',
        'app/page.tsx',
        'app/simple/page.tsx',
        'app/color/page.tsx',
        'app/dual/page.tsx',
        'app/ranking/page.tsx',
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
    
    # 1. app/layout.tsx (①②⑥⑦)
    if os.path.exists('app/layout.tsx'):
        content = read_file('app/layout.tsx')
        content = modify_layout_tsx(content)
        write_file('app/layout.tsx', content)
    
    # 2. app/page.tsx (③④⑤)
    if os.path.exists('app/page.tsx'):
        content = read_file('app/page.tsx')
        content = modify_page_tsx(content)
        write_file('app/page.tsx', content)
    
    # 3. app/simple/page.tsx (⑪)
    if os.path.exists('app/simple/page.tsx'):
        content = read_file('app/simple/page.tsx')
        content = modify_simple_page(content)
        write_file('app/simple/page.tsx', content)
    
    # 4. app/color/page.tsx (⑩⑪)
    if os.path.exists('app/color/page.tsx'):
        content = read_file('app/color/page.tsx')
        content = modify_color_page(content)
        write_file('app/color/page.tsx', content)
    
    # 5. app/dual/page.tsx (⑩⑪)
    if os.path.exists('app/dual/page.tsx'):
        content = read_file('app/dual/page.tsx')
        content = modify_dual_page(content)
        write_file('app/dual/page.tsx', content)
    
    # 6. app/ranking/page.tsx (⑧)
    if os.path.exists('app/ranking/page.tsx'):
        content = read_file('app/ranking/page.tsx')
        content = modify_ranking_page(content)
        write_file('app/ranking/page.tsx', content)
    
    # 7. スプリントモード削除 (⑨)
    print("\n📝 スプリントモード削除中...")
    sprint_dir = Path('app/sprint')
    if sprint_dir.exists():
        import shutil
        shutil.rmtree(sprint_dir)
        print("✅ app/sprint/ フォルダを削除しました")
    else:
        print("ℹ️  app/sprint/ は既に存在しません")
    
    print("\n" + "=" * 60)
    print("✨ 修正完了！")
    print("=" * 60)
    print("\n📋 修正内容:")
    print("  ① タイトルに「島根県大田市限定版」追加")
    print("  ② 説明文に改行追加")
    print("  ③ シンプル反応に「判断」追加")
    print("  ④ デュアルタスクから「NEW!」削除")
    print("  ⑤ ランキングセクション簡略化")
    print("  ⑥ フッターテキスト変更")
    print("  ⑦ コピーライト変更")
    print("  ⑧ ランキングページから講座名削除")
    print("  ⑨ スプリントモード削除")
    print("  ⑩ カラー・デュアルの表示サイズ統一")
    print("  ⑪ 表示単位を ms → s に変更")
    print("\n🚀 次のステップ:")
    print("  1. npm run dev でローカル確認")
    print("  2. git add .")
    print("  3. git commit -m 'feat: 島根県大田市カスタマイズ適用'")
    print("  4. git push")
    print("\n💾 バックアップ: backup_before_shimane/ フォルダに保存されています")
    print()

if __name__ == '__main__':
    main()
