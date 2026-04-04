---
name: github-member-activity-summary
description: GitHubを参照して、指定メンバー（1人）の活動サマリー（件数だけでなく価値行動と成長を含む）を今期（半期）で作成する。評価面談、1on1準備、フィードバック設計、チーム状況の棚卸しで使う。
---

# GitHubメンバー活動サマリー

指定したメンバーのGitHub活動を、複数リポジトリ横断で集計して要約する。
このスキルの目的は「開発実績から、価値ある行動とその成長を根拠付きで評価できる状態を作ること」。
主な出力は `{peoples}/{人名}/` 配下のMarkdownファイルで、以下の3部構成を必須とする。

1. 活動件数サマリー（PR / Review / Issue / Commit）
2. 価値行動シグナルの分析（難易度、品質、協働、成果影響）
3. 期間内の成長分析（前半/後半比較 + 具体エピソード）

## 役割分担

- **スクリプト**: GitHub APIからのデータ収集のみを行う
- **LLM**: マッピングファイルの読み取り、期間計算、データの加工・分析・レポート生成・保存を行う

## 基盤の読み込み

最初に以下を読む:

- `{thinking}/Documents/general/GitHubチームメンバー.md`
- `{thinking}/Documents/general/GitHubリポジトリ.md`
- `{thinking}/Documents/general/GitHubメンバー別監視リポジトリ.md`

`GitHubメンバー別監視リポジトリ.md` を正として扱う。
メンバー名、GitHubユーザー名、対象リポジトリの対応が欠けている場合は、先にこのファイルを更新してから集計する。

## 入力ルール

ユーザーに以下を確認する:

1. 対象メンバー: 人名（1人のみ。例: `宮本`）

期間は常に `今期`（半期: 4-9月 / 10-3月）として算出する。当日が期間終了前なら当日で打ち切り。

## 実行手順

### 1. 集計対象の展開（LLM）

`{thinking}/Documents/general/GitHubメンバー別監視リポジトリ.md` から対象メンバーの:

- 表示名
- GitHubユーザー名
- 監視対象リポジトリ（`org/repo`）

を特定する。該当行がないメンバーは「未定義」としてレポートに残し、集計対象から除外する。

### 2. 期間の算出（LLM）

以下を算出する:

- **全期間**: `start_date` 〜 `end_date`（半期: 4/1〜9/30 または 10/1〜3/31。当日が期間終了前なら当日で打ち切り）
- **前半**: `start_date` 〜 中間日
- **後半**: 中間日翌日 〜 `end_date`

### 3. データ収集（スクリプト）

以下のスクリプトを1回だけ実行してデータを収集する。
前半/後半の件数はスクリプト出力 `half_counts` を使用し、追加API呼び出しは行わない。

#### 全期間データ（PR詳細・レビュー深度あり）

```bash
python3 skills/github-member-activity-summary/scripts/collect_activity_data.py \
  --github-user "$GITHUB_USER" \
  --repos "$REPOS" \
  --start-date "$START_DATE" \
  --end-date "$END_DATE" \
  --include-pr-details \
  --include-review-depth
```

引数の説明:

| 引数 | 説明 |
|------|------|
| `--github-user` | GitHubユーザー名（LLMがマッピングファイルから取得） |
| `--repos` | カンマ区切りの `org/repo` リスト（LLMがマッピングファイルから取得） |
| `--start-date` | 開始日 YYYY-MM-DD（LLMが算出） |
| `--end-date` | 終了日 YYYY-MM-DD（LLMが算出） |
| `--include-pr-details` | PR詳細（mergedAt, additions, deletions, changedFiles）を取得 |
| `--include-review-depth` | GraphQLでレビューコメント深度を取得 |
| `--max-pr` | 代表PR件数上限（デフォルト: 10） |
| `--max-review` | 代表Review件数上限（デフォルト: 10） |
| `--max-issue` | 代表Issue件数上限（デフォルト: 10） |
| `--max-commit` | 代表Commit件数上限（デフォルト: 20） |

スクリプトの出力（JSON）:

```json
{
  "github_user": "username",
  "repos": ["org/repo1", "org/repo2"],
  "period": { "start": "2026-01-01", "end": "2026-03-04" },
  "half_periods": {
    "first": { "start": "2026-01-01", "end": "2026-02-01" },
    "second": { "start": "2026-02-02", "end": "2026-03-04" }
  },
  "half_counts": {
    "first": { "pr": 6, "review": 4, "issue": 2, "commit": 20 },
    "second": { "pr": 6, "review": 4, "issue": 1, "commit": 25 }
  },
  "counts": { "pr": 12, "review": 8, "issue": 3, "commit": 45 },
  "metrics": {
    "merged_pr_count": 10,
    "issue_closed_count": 2,
    "review_with_comment_count": 5
  },
  "representatives": {
    "prs": [{ "number": 123, "title": "...", "url": "...", "createdAt": "...", "mergedAt": "...", "additions": 50, "deletions": 20, "changedFiles": 3, "repo": "org/repo1", ... }],
    "reviews": [{ "number": 456, "title": "...", "url": "...", "repo": "org/repo1", ... }],
    "issues": [{ "number": 789, "title": "...", "url": "...", "state": "closed", "repo": "org/repo1", ... }],
    "commits": [{ "short_sha": "abc12345", "message": "...", "url": "...", "date": "...", "repo": "org/repo1" }]
  },
  "errors": []
}
```

認証エラー時は `{"error": "gh auth failed: ..."}` が返る。この場合は中断して認証を依頼する。

### 4. データの加工・分析（LLM）

スクリプトの出力JSONから、以下を算出する。

#### 基本指標

| 指標 | 算出方法 |
|------|---------|
| PR件数 | `counts.pr` |
| Review件数 | `counts.review` |
| Issue件数 | `counts.issue` |
| Commit件数 | `counts.commit` |

#### 補助メトリクス（価値行動の裏付け）

| 指標 | 算出方法 |
|------|---------|
| Merge率 | `metrics.merged_pr_count / counts.pr` |
| PRリードタイム中央値 | 代表PRの `createdAt` → `mergedAt` の差（時間単位）の中央値 |
| PR難易度（変更行数中央値） | 代表PRの `additions + deletions` の中央値 |
| PR難易度（変更ファイル数中央値） | 代表PRの `changedFiles` の中央値 |
| レビュー関与深度 | `metrics.review_with_comment_count` |
| Issueクローズ率 | `metrics.issue_closed_count / counts.issue` |
| 活動日数 | 代表PR/Review/Issue/Commitの日付からユニーク日数を算出 |
| 活動継続性（週変動係数） | 週ごとの活動日数のばらつき |

#### 成長分析（前半/後半比較）

`half_counts` と代表データから以下を比較:

1. 活動量の変化（PR/Review/Issue/Commit）
2. 難易度の変化（PRサイズ、担当テーマの複雑度）
3. 品質の変化（レビュー指摘の具体性、再修正の減少傾向）
4. 協働の変化（他者支援レビュー、横断調整の増減）

成長は必ず「証跡リンク + 変化の説明 + 解釈の確度（高/中/低）」の3点セットで記述する。
観測できない場合は「GitHub上では判定不可」と明記する。

#### 価値行動シグナルの分析

代表PR/Review/Issue/Commitのタイトル・内容から以下を分析:

- 難易度の高い貢献（変更規模、横断影響、技術的不確実性）
- 品質への貢献（テスト、バグ予防、保守性改善）
- 協働への貢献（レビュー、設計議論、他者支援）
- 成果影響（ユーザー価値、開発効率、運用安定）

### 5. レポート生成（LLM）

保存先:

- `{peoples}/{人名}/YYYY-MM-DD_GitHub活動サマリー_今期_{表示名}.md`

出力テンプレート:

```markdown
# GitHub活動サマリー（今期）- [表示名]

- 対象: [表示名]（@github_user）
- 対象リポジトリ: org/repo-a, org/repo-b
- 期間: YYYY-MM-DD〜YYYY-MM-DD
- 生成日: YYYY-MM-DD

## サマリー

- PR: N
- Review: N
- Issue: N
- Commit: N
- 価値行動ハイライト: [価値ある行動を1-2行]
- 成長ハイライト: [前半/後半で伸びた点を1行]

## 1. 期間中の主な作業内容
- 主要テーマ:
- 主な変更対象（機能/画面/モジュール）:
- 代表PR:
	- [#123 タイトル](URL) - 何をどう改善したかを1行で要約
	- [#456 タイトル](URL) - 何をどう改善したかを1行で要約
- 代表Issue:
	- [#789 タイトル](URL) - 課題定義と対応内容を1行で要約
- 代表Commit:
	- SHA(短縮): 変更意図を1行で要約

## 2. 価値行動シグナル（根拠付き）
- 難易度の高い貢献（例: 変更規模、横断影響、技術的不確実性）:
- 品質への貢献（テスト、バグ予防、保守性改善）:
- 協働への貢献（レビュー、設計議論、他者支援）:
- 成果影響（ユーザー価値、開発効率、運用安定）:

## 3. 協働・レビュー貢献
- 実施Reviewの傾向（設計観点 / 品質観点 / リスク指摘）:
- 他メンバーへの具体的な貢献例:
- チームへの波及（知見共有、再発防止、ガイド整備など）:

## 4. 成長分析（前半/後半比較）
- 活動量の変化:
- 貢献の質の変化:
- 新たにできるようになったこと:
- 次期に伸ばすべき点:

## 5. 実行特性（評価の参考）
- オーナーシップ: 自走して前進させた内容
- 複雑課題対応: 難易度の高い変更・調整への対応
- 品質志向: 不具合予防、テスト、保守性向上の取り組み
- 連携力: 関係者との調整、レビュー往復の質
- 継続性: 期間内の活動リズムと安定性

## 6. 成果と影響
- ユーザー/事業/開発効率への影響:
- 定量的成果（あれば）:
- 残課題と次アクション:

## 7. 評価メモ（根拠ベース）
- 強み:
- 改善余地:
- 根拠リンク一覧:
	- PR:
	- Issue:
	- Commit:
	- Review:

## 注意事項
- 取得失敗リポジトリ:
- 補足:
```

評価メモは断定ではなく、必ず根拠リンクとセットで記述する。
「行動」ではなく「価値ある行動」を評価対象にする。
観測できない事実は推測で埋めず、「情報不足」または「GitHub上では判定不可」と明記する。

### 6. 端末向け要約

ファイル保存後、端末には1-3行で要点のみ返す。
件数に加えて「主な作業テーマ」と「評価観点の一言」を含める。

例:

- `宮本`: PR 12 / Review 9 / Issue 1 / Commit 41。主要テーマはオンボーディング改善。難易度高いPR対応が増え、後半はレビューの質が向上。

## 失敗時の扱い

- 認証失敗（スクリプトが `error` フィールドを返した場合）: 中断して認証を依頼する。
- 一部repo取得失敗（`errors` 配列に内容がある場合）: 取得できた範囲で継続し、失敗repoを明記する。
- 対応表不備: 不備箇所を明示し、`{thinking}/Documents/general/GitHubメンバー別監視リポジトリ.md` の更新を優先する。
