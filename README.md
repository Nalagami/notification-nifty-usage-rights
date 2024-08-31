# notification-nifty-usage-rights

## 概要
ニフティ使用権をslackに通知するスクリプトです。

## インストール
インストール手順を以下に示します。

```bash
# クローンリポジトリ
git clone https://github.com/ユーザー名/リポジトリ名.git

# ディレクトリに移動
cd notification-nifty-usage-rights

# .envファイルを作成
cp .env.example .env
vi .env

# 3つの環境変数を設定
# SLACK_WEBHOOK_URL: SlackのWebhook URL
# USER_ID: ニフティ使用権を取得したいユーザーID
# PASSWORD: ニフティ使用権を取得したいユーザーのパスワード

# docker imageをビルド
docker build -t notification-nifty-usage-rights .

# docker containerを起動
docker run notification-nifty-usage-rights
```
