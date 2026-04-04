---
name: slide
description: マークダウンからMarpスライドを生成し、PDF/PPTXでエクスポートする。チーム共有用のプレゼン資料を素早く作りたいときに使う。
---

# スライド生成スキル

マークダウンの内容をMarpスライドに変換し、チームにすぐ展開できるプレゼン資料を生成する。

## 使い方

```
/slide [対象]
```

対象の指定方法:
- **テーマを伝える**: 「来週のチーム共有用に〇〇のスライドを作って」→ 対話しながら構成を決める
- **ファイルパスを渡す**: `/slide {sessions}/2026/2026-03-28_xxx.md` → 既存ファイルの内容をスライド化
- **引数なし**: 何についてスライドを作るか聞く

## 実行手順

### 1. スライドの目的と構成を確認

ユーザーに以下を確認する（わかっている部分はスキップ）:

- **目的**: 誰に、何を伝えるスライドか
- **ソース**: 既存ファイルの内容をスライド化するか、新規に作るか
- **ボリューム**: 何枚程度を想定しているか（デフォルト: 5〜10枚）

### 2. コンテンツの構成設計

スライドの構成を箇条書きで設計し、ユーザーに確認する。**各スライドにレイアウトパターン名を付与**して構成を見せる:

```
1. [cover] タイトル — FY27 プロダクトデザインチーム方針
2. [agenda] 今日お話しすること
3. [section] FY26の振り返り
4. [kpi-cards] FY26は4人→12人へ拡大しながら120%成長を達成した
5. [good-next] 一方、個人の馬力に依存する構造が残っている
6. [section] FY27の環境変化
7. [timeline-insight] 人の入れ替わりは今後も続く
8. [section] デザイナーの本来の価値
9. [role-cards] デザイナーの貢献は3つの領域がある
10. [section] 現状の課題
11. [cause-effect] 「作ること」に時間を取られ上流に入れていない
12. [root-cause] 根本原因はチームの基盤がなく「個人戦」になっていること
13. [section] FY27テーマ
14. [message] 価値を届けるチームをつくる
15. [pillar-cards] テーマ実現のために3つの柱で取り組む
16. [three-col-list] 各柱で取り組むこと
17. [as-is-to-be] FY27末の目指す姿
18. [closing] クロージング
```

**構成設計の原則（コンサル流）**:
- **アクションタイトル**: h2は「トピック名」ではなく「このスライドで言いたいこと（結論）」にする（例: ✕「FY26の振り返り」→ ○「FY26は4人→12人へ拡大しながら120%成長を達成した」）
- **ボディはタイトルの根拠**: 下の内容がタイトルの主張を裏付ける構造にする
- **1スライド1メッセージ**: 情報を詰め込むくらいならスライドを増やす
- **So What?を常に問う**: 事実の列挙ではなく「だから何が言えるか」を明示する
- **聞き手が知りたい順序**: 結論ファースト、根拠は後

### 3. Marpスライドの生成

確認が取れたら、Marpフォーマットのマークダウンファイルを生成する。

**保存先**: `Documents/slides/YYYY-MM-DD_[スライド名].md`（`Documents/slides/` ディレクトリがなければ作成）

**デフォルトのフロントマター**（全スライドに適用）:

```markdown
---
marp: true
theme: default
paginate: true
style: |
  /* === Base === */
  section {
    font-family: 'Noto Sans JP', 'Hiragino Kaku Gothic ProN', sans-serif;
    font-size: 22px;
    padding: 0;
    background: #f8fafc;
    color: #1e293b;
    line-height: 1.6;
    display: flex;
    flex-direction: column;
    justify-content: flex-start !important;
    align-items: stretch !important;
  }

  /* === Fixed Header Bar === */
  section h2 {
    background: linear-gradient(to right, #006199, #0082C2);
    color: #fff;
    font-size: 1.1em;
    margin: 0;
    padding: 16px 50px;
    border-bottom: none;
    flex-shrink: 0;
  }

  /* === Content area below header === */
  section > :not(h2) {
    margin-left: 50px;
    margin-right: 50px;
  }
  section > :nth-child(2) {
    margin-top: 28px;
  }

  /* === Typography === */
  h1 { font-size: 1.6em; color: #0d7fa5; margin-bottom: 0.4em; }
  h3 { font-size: 1.0em; color: #0d7fa5; margin-bottom: 0.3em; }
  ul, ol { font-size: 0.92em; margin-top: 0.3em; }
  li { margin-bottom: 0.2em; }
  pre { font-size: 0.78em; background: #e8f7fc; border: 1px solid #a3d9ed; border-radius: 6px; }
  code { background: #e8f7fc; color: #0a4f6b; padding: 0.1em 0.3em; border-radius: 3px; }
  strong { color: #0d7fa5; }
  table { font-size: 0.82em; border-collapse: collapse; width: 100%; }
  table th { background: #0a4f6b; color: #fff; padding: 10px 14px; text-align: left; }
  table td { padding: 10px 14px; border-bottom: 1px solid #d4eef7; }
  table tr:nth-child(even) td { background: #f0f9fc; }

  /* === Lead (cover / section divider) === */
  section.lead {
    background: linear-gradient(to top right, #0082C2 0%, #3EB4DF 50%, #AFFFF7 100%);
    color: #fff;
    text-align: center;
    justify-content: center !important;
    align-items: center !important;
    padding: 60px;
  }
  section.lead h1 { color: #fff; font-size: 2.0em; border: none; margin-bottom: 0.2em; }
  section.lead h2 { color: #a3d9ed; border: none; font-weight: normal; font-size: 1.1em; background: none; padding: 0; margin: 0; }
  section.lead blockquote { border-left-color: #3EB4DF; background: rgba(255,255,255,0.06); color: #d4eef7; }
  section.lead blockquote strong { color: #fff; }
  section.lead strong { color: #ffffff; }
  section.lead > :not(h2) { margin-left: 0; margin-right: 0; }

  /* === Accent elements === */
  blockquote { border-left: 4px solid #3EB4DF; padding: 0.5em 1.2em; background: #e8f7fc; font-size: 0.92em; border-radius: 0 6px 6px 0; margin: 0.8em 0; }
  .dark-box strong { color: #fff; }
  .card { background: #fff; border-radius: 8px; padding: 1.2em; border-left: 4px solid #3EB4DF; box-shadow: 0 2px 8px rgba(0,0,0,0.06); }
  .card-red { border-left-color: #ef4444; }
  .card-green { border-left-color: #15803d; }
  .card-amber { border-left-color: #b45309; }
  .muted { font-size: 0.75em; color: #64748b; }

  /* === Page number === */
  section::after { color: #94a3b8; font-size: 0.65em; }
---
```

### 4. プレビューとエクスポート

ファイル生成後、エクスポートコマンドを提示する:

```bash
# HTMLプレビュー
npx @marp-team/marp-cli Documents/slides/YYYY-MM-DD_xxx.md --html -o Documents/slides/YYYY-MM-DD_xxx.html

# PDF出力
npx @marp-team/marp-cli Documents/slides/YYYY-MM-DD_xxx.md --html --pdf -o Documents/slides/YYYY-MM-DD_xxx.pdf

# PPTX出力
npx @marp-team/marp-cli Documents/slides/YYYY-MM-DD_xxx.md --html --pptx -o Documents/slides/YYYY-MM-DD_xxx.pptx
```

**ユーザーに確認してからエクスポートを実行する**。

### 5. 完了報告

保存先パス・エクスポート結果・スライド枚数を報告し、「内容の修正があれば言ってください」と伝える。

---

## レイアウトパターン集

各スライドは以下のパターンから選んで構成する。コンテンツに最も合うパターンを選ぶこと。
**アクションタイトル**: 通常スライド（非lead）のh2は必ず「このスライドの結論」を一文で書く。

### cover — タイトルスライド

プレゼンの表紙。グラデーション背景で中央揃え。

```markdown
<!-- _class: lead -->
<!-- _paginate: false -->

# プレゼンタイトル

## サブタイトル・文脈

発表者名 / YYYY-MM-DD
```

### section — セクション区切り

トピックの切り替わりを示す。間（ま）を作る。

```markdown
<!-- _class: lead -->

# セクションタイトル

> 一行でこのセクションの要点を伝える
```

### agenda — アジェンダ

全体の流れをナンバーバッジで見せる。

```markdown
## 今日お話しすること

<div style="display: grid; grid-template-columns: 40px 1fr; gap: 12px 16px; margin-top: 1.2em; font-size: 0.95em;">
<div style="background: #0082C2; color: #fff; width: 36px; height: 36px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-weight: bold;">1</div>
<div style="padding-top: 6px;"><strong>トピック1</strong> — 補足説明</div>
<div style="background: #0082C2; color: #fff; width: 36px; height: 36px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-weight: bold;">2</div>
<div style="padding-top: 6px;"><strong>トピック2</strong> — 補足説明</div>
</div>
```

### message — キーメッセージ

最も伝えたい一文を大きく見せる。テーマ発表・結論・ミッションに使う。

```markdown
<!-- _class: lead -->

<style scoped>
h1 { font-size: 2.4em; margin-bottom: 0.5em; }
</style>

# キーメッセージをここに

補足のサブテキスト
```

### kpi-cards — 数値カード

インパクトのある数字を3枚のカードで見せる。実績・成果の提示に最適。

```markdown
## アクションタイトル（結論を一文で）

<div style="display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 1.2rem; margin-top: 0.8em;">
<div class="card">
<div style="font-size: 2.2em; font-weight: bold; color: #0082C2; line-height: 1.2;">数値</div>
<div style="margin-top: 0.3em;">説明テキスト</div>
</div>
<div class="card">
<div style="font-size: 2.2em; font-weight: bold; color: #0082C2; line-height: 1.2;">数値</div>
<div style="margin-top: 0.3em;">説明テキスト</div>
</div>
<div class="card">
<div style="font-size: 2.2em; font-weight: bold; color: #0082C2; line-height: 1.2;">数値</div>
<div style="margin-top: 0.3em;">説明テキスト</div>
</div>
</div>
```

### good-next — GOOD/NEXT対比

成果と残課題を左右で対比し、下部にSo What?のバナーを置く。

```markdown
## アクションタイトル（結論を一文で）

<div style="display: grid; grid-template-columns: 1fr 1fr; gap: 2rem; margin-top: 0.8em;">
<div>

<div style="font-size: 0.8em; font-weight: bold; color: #0082C2; margin-bottom: 0.5em;">GOOD（できたこと）</div>

- 箇条書き1
- 箇条書き2

</div>
<div>

<div style="font-size: 0.8em; font-weight: bold; color: #ef4444; margin-bottom: 0.5em;">NEXT（残った課題）</div>

- 箇条書き1
- 箇条書き2

</div>
</div>

<div style="margin-top: 1.5em; text-align: center; padding: 0.7em; background: #0082C2; color: #fff; border-radius: 6px; font-size: 0.95em;">
<strong>So What? — ここから言えること</strong>
</div>
```

### timeline-insight — タイムライン＋示唆

左にタイムライン（バッジ＋テキスト）、右に示唆ボックス。

```markdown
## アクションタイトル（結論を一文で）

<div style="display: grid; grid-template-columns: 3fr 2fr; gap: 2.5rem; margin-top: 0.8em;">
<div>

<div style="display: grid; grid-template-columns: 80px 1fr; gap: 8px 16px; font-size: 0.9em;">
<div style="background: #0082C2; color: white; padding: 6px 0; border-radius: 6px; text-align: center; font-weight: bold;">時期</div>
<div style="padding-top: 4px;">イベント内容</div>
<div style="background: #3EB4DF; color: white; padding: 6px 0; border-radius: 6px; text-align: center; font-weight: bold;">時期</div>
<div style="padding-top: 4px;">イベント内容</div>
</div>

</div>
<div>

<div style="background: #e8f7fc; border-radius: 8px; padding: 1.2em; margin-top: 0.5em;">

**示唆**

ここにタイムラインから読み取れるインサイトを書く

</div>
</div>
</div>
```

### role-cards — 役割カード

3つの役割・機能を、ラベル付きカードで構造化する。

```markdown
## アクションタイトル（結論を一文で）

<div style="display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 1rem; margin-top: 0.8em;">
<div style="background: #fff; border-radius: 8px; padding: 1em; box-shadow: 0 2px 8px rgba(0,0,0,0.06);">
<div style="background: #0082C2; color: #fff; display: inline-block; padding: 2px 12px; border-radius: 4px; font-size: 0.75em; font-weight: bold;">ラベル 1</div>
<div style="font-size: 1.05em; font-weight: bold; color: #0d7fa5; margin: 0.5em 0 0.3em;">タイトル</div>
<div style="font-size: 0.85em;">説明テキスト</div>
<div style="font-size: 0.78em; color: #64748b; margin-top: 0.8em; border-top: 1px solid #e2e8f0; padding-top: 0.5em;">→ 効果・成果</div>
</div>
<!-- 2枚目・3枚目も同様 -->
</div>
```

### cause-effect — 原因→結果の2カラム

左に原因群、右に結果群を配置し、それぞれの下部に結論ボックスを置く。

```markdown
## アクションタイトル（結論を一文で）

<div style="display: grid; grid-template-columns: 1fr 1fr; gap: 2rem; margin-top: 0.5em;">
<div>

<div style="font-size: 0.8em; font-weight: bold; color: #ef4444; margin-bottom: 0.5em; letter-spacing: 0.05em;">原因側ラベル</div>

- 原因1
- 原因2

<div style="text-align: center; font-size: 1.2em; color: #94a3b8; margin: 0.3em 0;">↓</div>
<div style="text-align: center; font-size: 0.85em; background: #fef2f2; padding: 0.5em; border-radius: 6px; color: #991b1b;"><strong>結論</strong></div>

</div>
<div>

<div style="font-size: 0.8em; font-weight: bold; color: #ef4444; margin-bottom: 0.5em; letter-spacing: 0.05em;">結果側ラベル</div>

- 結果1
- 結果2

<div style="text-align: center; font-size: 1.2em; color: #94a3b8; margin: 0.3em 0;">↓</div>
<div style="text-align: center; font-size: 0.85em; background: #fef2f2; padding: 0.5em; border-radius: 6px; color: #991b1b;"><strong>結論</strong></div>

</div>
</div>
```

### root-cause — 根本原因の構造図

上部に根本原因ボックス、下部に影響カードを並べ、最後にアクションを示す。

```markdown
## アクションタイトル（結論を一文で）

<div style="text-align: center; margin-top: 1em;">

<div style="display: inline-block; background: #fef2f2; border: 2px solid #ef4444; border-radius: 8px; padding: 0.6em 2em; font-weight: bold; color: #991b1b;">根本原因</div>

<div style="display: grid; grid-template-columns: 1fr 1fr; gap: 2rem; margin-top: 1em; text-align: left;">
<div style="background: #fff; border-radius: 8px; padding: 1em; box-shadow: 0 2px 8px rgba(0,0,0,0.06);">
<div style="font-size: 0.8em; font-weight: bold; color: #64748b; margin-bottom: 0.4em;">影響 1</div>
<div style="font-weight: bold; color: #0d7fa5; margin-bottom: 0.3em;">タイトル</div>
<div style="font-size: 0.85em;">説明</div>
</div>
<div style="background: #fff; border-radius: 8px; padding: 1em; box-shadow: 0 2px 8px rgba(0,0,0,0.06);">
<div style="font-size: 0.8em; font-weight: bold; color: #64748b; margin-bottom: 0.4em;">影響 2</div>
<div style="font-weight: bold; color: #0d7fa5; margin-bottom: 0.3em;">タイトル</div>
<div style="font-size: 0.85em;">説明</div>
</div>
</div>

<div style="margin-top: 1.5em; font-size: 1.1em; font-weight: bold; color: #0082C2;">だから、○○する</div>

</div>
```

### pillar-cards — 柱カード

3つの戦略柱をカード形式で。上部にPILLARラベル、色分けされたトップボーダー。

```markdown
## アクションタイトル（結論を一文で）

<div style="display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 1rem; margin-top: 0.8em;">
<div style="background: #fff; border-radius: 8px; padding: 1.2em; box-shadow: 0 2px 8px rgba(0,0,0,0.06); border-top: 4px solid #0082C2;">
<div style="font-size: 0.75em; font-weight: bold; color: #0082C2; letter-spacing: 0.1em;">PILLAR 01</div>
<div style="font-size: 1.1em; font-weight: bold; color: #1e293b; margin: 0.4em 0;">タイトル</div>
<div style="font-size: 0.85em; color: #475569;">説明テキスト</div>
<div style="font-size: 0.78em; color: #64748b; margin-top: 1em; border-top: 1px solid #e2e8f0; padding-top: 0.5em;">具体例</div>
</div>
<div style="background: #fff; border-radius: 8px; padding: 1.2em; box-shadow: 0 2px 8px rgba(0,0,0,0.06); border-top: 4px solid #3EB4DF;">
<div style="font-size: 0.75em; font-weight: bold; color: #3EB4DF; letter-spacing: 0.1em;">PILLAR 02</div>
<!-- 同様 -->
</div>
<div style="background: #fff; border-radius: 8px; padding: 1.2em; box-shadow: 0 2px 8px rgba(0,0,0,0.06); border-top: 4px solid #AFFFF7;">
<div style="font-size: 0.75em; font-weight: bold; color: #0d7fa5; letter-spacing: 0.1em;">PILLAR 03</div>
<!-- 同様 -->
</div>
</div>
```

### three-col-list — 3カラムリスト

3つの柱・カテゴリに沿った箇条書きを並列表示。下部にまとめバナー。

```markdown
## アクションタイトル（結論を一文で）

<div style="display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 1rem; margin-top: 0.8em; font-size: 0.9em;">
<div>

<div style="font-weight: bold; color: #0082C2; border-bottom: 2px solid #0082C2; padding-bottom: 4px; margin-bottom: 0.6em;">01 カテゴリ名</div>

- 項目1
- 項目2

</div>
<div>

<div style="font-weight: bold; color: #3EB4DF; border-bottom: 2px solid #3EB4DF; padding-bottom: 4px; margin-bottom: 0.6em;">02 カテゴリ名</div>

- 項目1
- 項目2

</div>
<div>

<div style="font-weight: bold; color: #0d7fa5; border-bottom: 2px solid #0d7fa5; padding-bottom: 4px; margin-bottom: 0.6em;">03 カテゴリ名</div>

- 項目1

</div>
</div>

<div style="margin-top: 2em; text-align: center; padding: 0.7em; background: #e8f7fc; border-radius: 6px; font-size: 0.92em;">
まとめ・補足メッセージ
</div>
```

### as-is-to-be — 現状→目指す姿の対比

左にAS-IS、右にTO-BEを配置し、変革の方向を示す。

```markdown
## アクションタイトル（結論を一文で）

<div style="display: grid; grid-template-columns: 1fr 1fr; gap: 2rem; margin-top: 0.8em;">
<div>

<div style="font-size: 0.8em; font-weight: bold; color: #ef4444; margin-bottom: 0.5em; letter-spacing: 0.05em;">AS-IS（今）</div>

<div style="font-size: 0.88em;">

- 現状の課題1
- 現状の課題2

</div>
</div>
<div>

<div style="font-size: 0.8em; font-weight: bold; color: #0082C2; margin-bottom: 0.5em; letter-spacing: 0.05em;">TO-BE（目指す姿）</div>

<div style="font-size: 0.88em;">

- 目標状態1
- 目標状態2

</div>
</div>
</div>
```

### table — テーブル

構造化されたデータの比較。役割定義・機能比較・ステータス一覧に。

```markdown
## アクションタイトル（結論を一文で）

| 列1 | 列2 | 列3 |
|------|------|------|
| **項目** | 内容 | 効果 |
```

### closing — クロージング

プレゼンの締め。lead背景でメッセージを大きく。

```markdown
<!-- _class: lead -->

<style scoped>
h1 { font-size: 1.6em; line-height: 1.8; }
</style>

# メッセージ1行目
# メッセージ2行目
```

---

## カラーパレット

| 用途 | カラー |
|------|--------|
| プライマリ（アクセント） | `#3EB4DF` |
| プライマリダーク（ヘッダー・テーブルヘッダ） | `#0082C2` / `#006199` |
| 見出し・strong | `#0d7fa5` |
| leadグラデーション | `#0082C2` → `#3EB4DF` → `#AFFFF7`（左下→右上） |
| ヘッダーバーグラデーション | `#006199` → `#0082C2`（左→右） |
| 薄い背景（blockquote・示唆ボックス） | `#e8f7fc` |
| 警告・課題 | `#ef4444` / `#fef2f2` |
| 成功・達成 | `#15803d` |
| ミュートテキスト | `#64748b` |

---

## 重要な原則

- **アクションタイトル**: h2は「トピック名」ではなく「結論」。読むだけでストーリーが分かる状態にする
- **ボディはタイトルの根拠**: コンテンツがタイトルの主張を証明する構造
- **1スライド1メッセージ**: 情報を詰め込むくらいならスライドを増やす
- **速さ優先**: チームにすぐ展開できることが最大の価値。完璧を目指さない
- **エクスポートはユーザー確認後**: 形式（HTML/PDF/PPTX）を確認してから実行する
- **コントラストに注意**: 白文字の背景は十分暗くする。薄い色（#3EB4DF等）に白文字を乗せない
