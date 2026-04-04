# agents

エージェントとスキルを管理するリポジトリ。Claude Codeセッションのメイン作業ディレクトリとして使う。

## 構成

```
agents/       エージェント定義（coach, secretary等）
context/      共通原則・情報ソース定義
personas/     ペルソナ定義（将来移行）
skills/       スキル定義（将来移行）
frameworks/   思考フレームワーク（将来移行）
templates/    テンプレート（将来移行）
```

## 使い方

```bash
cd ~/.ghq/github.com/mitsu9/agents
claude
```

デフォルトでコーチ（参謀）モードで起動する。

## データソース

データはこのリポジトリに置かない。Obsidian vault（work-cockpit）や外部サービス（Linear, Notion, Slack等）から取得する。
