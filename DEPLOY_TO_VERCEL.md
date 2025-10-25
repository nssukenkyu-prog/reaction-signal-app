# Vercelへのデプロイ手順

## 方法1: GitHubを経由してデプロイ（推奨）

### 1. GitHubにコードをアップロード

GitHubで新しいリポジトリを作成したら、以下のコマンドを実行：

```bash
# リモートリポジトリを追加（YOUR_USERNAMEを自分のGitHubユーザー名に変更）
git remote add origin https://github.com/YOUR_USERNAME/reaction-signal-app.git

# mainブランチにリネーム
git branch -M main

# GitHubにプッシュ
git push -u origin main
```

### 2. Vercelでデプロイ

1. [Vercel](https://vercel.com)にアクセス
2. 「Sign Up」→「Continue with GitHub」でGitHubアカウントで登録
3. ダッシュボードで「Add New...」→「Project」をクリック
4. GitHubリポジトリから`reaction-signal-app`を選択
5. 「Import」をクリック
6. Framework Preset: **Next.js** が自動選択されます
7. 「Deploy」をクリック

### 3. デプロイ完了！

数分後、以下のようなURLでアクセス可能になります：
- `https://reaction-signal-app-xxx.vercel.app`

---

## 方法2: Vercel CLIで直接デプロイ

GitHubを使わずに直接デプロイする方法：

### 1. Vercel CLIをインストール

```bash
npm install -g vercel
```

### 2. ログイン

```bash
vercel login
```

### 3. デプロイ

```bash
cd reaction-signal-app
vercel
```

プロンプトに従って設定を進めると、自動的にデプロイされます。

---

## 修正済みの内容

このバージョンでは以下のTypeScriptエラーを修正済みです：

1. `lib/storage.ts`: ModeType型のインポート追加
2. `app/dual/page.tsx`: number型の null を undefined に変換

すぐにデプロイ可能な状態になっています！

---

## カスタムドメインの設定（オプション）

Vercelダッシュボードから独自ドメインを設定できます：

1. プロジェクトの「Settings」→「Domains」
2. 独自ドメインを入力
3. DNSレコードを設定（指示に従う）

---

## 環境変数の設定（必要に応じて）

Vercelダッシュボードの「Settings」→「Environment Variables」から設定可能

---

## サポート

- Vercel公式ドキュメント: https://vercel.com/docs
- Next.js公式ドキュメント: https://nextjs.org/docs
