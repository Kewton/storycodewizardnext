# システム構成

StoryCodeWizardのシステム全体の構成とアーキテクチャについて説明します。

## システム概要

StoryCodeWizardは、LLM（大規模言語モデル）を活用したコード生成・プロジェクト管理デスクトップアプリケーションです。

### 主要コンポーネント

## UIコンポーネント構成

### メインウィンドウ (MainWindow)
- **位置**: `./ui/main_window.py`
- **機能**: アプリケーションのメインコンテナ、**アクティビティーサイドバー管理**
- **コンポーネント**: ActivitySidebar、メインコンテンツエリア、ウィンドウサイズ管理
- **改善点**: VS Code風ナビゲーション、最大化されたコンテンツ表示領域

### アクティビティーサイドバー (ActivitySidebar)
- **位置**: `./ui/widgets/activity_sidebar.py`
- **機能**: VS Code風のサイドバーナビゲーション、機能切り替え
- **コンポーネント**: アイコンボタン、アクティブ状態表示、コンテンツ切り替え
- **改善点**: 直感的なアイコンベースナビゲーション、視覚的フィードバック

### Story2Codeコンテンツ (ChatTab)
- **位置**: `./ui/chat_tab.py`
- **機能**: LLMとの対話インターフェース、ストリーミング応答表示
- **コンポーネント**: プロジェクト選択、モデル選択、Programming Type選択（プロジェクト連携）、入力エリア、チャット表示
- **改善点**: リアルタイムストリーミング表示、スクロール可能な設定パネル、プロジェクト選択時の自動Programming Type設定、**Markdown表示対応**

### MyHistoryコンテンツ (HistoryTab)
- **位置**: `./ui/history_tab.py`
- **機能**: 過去のチャット履歴管理
- **コンポーネント**: 履歴リスト、詳細表示、削除・ダウンロード機能
- **改善点**: 自動データ更新、フィルタリング機能強化、実行時刻とモデル名のみ表示（フォントサイズ拡大）、**Markdown表示対応**

### プロジェクト管理コンテンツ (ProjectTab)
- **位置**: `./ui/project_tab.py`
- **機能**: プロジェクトの作成・管理・編集（Programming Type管理含む）
- **コンポーネント**: プロジェクト一覧、新規作成フォーム（Programming Type選択付き）、プロジェクト編集機能
- **改善点**: スクロール可能な設定パネル、Programming Type管理、ラベルとフィールドの配置最適化、登録後の自動更新、プロジェクト説明管理

### カスタムウィジェット
- **ChatMessage**: `./ui/widgets/chat_message.py` - チャットメッセージ表示用（**Markdown対応**）
- **ProjectCard**: `./ui/widgets/project_card.py` - プロジェクト情報表示・編集用（Programming Type表示対応）
- **ProjectEditDialog**: `./ui/widgets/project_edit_dialog.py` - プロジェクト編集ダイアログ（Programming Type編集対応、可変サイズ対応）
- **FileUploader**: `./ui/widgets/file_uploader.py` - ファイルアップロード機能
- **StreamingChatMessage**: `./ui/widgets/streaming_chat_message.py` - ストリーミング対応チャットメッセージ表示（**Markdown対応**）
- **MarkdownRenderer**: `./ui/widgets/markdown_renderer.py` - **新規追加**: Markdown表示用ウィジェット
- **ActivitySidebar**: `./ui/widgets/activity_sidebar.py` - **新規追加**: VS Code風アクティビティーサイドバー

## アーキテクチャ

```
    ./
    ├── main.py                    # アプリケーションエントリーポイント
    ├── ui/                        # UIコンポーネント
    │   ├── main_window.py         # メインウィンドウ（アクティビティーサイドバー対応）
    │   ├── chat_tab.py           # チャット機能コンテンツ（ストリーミング対応、Programming Type連携）
    │   ├── history_tab.py        # 履歴管理コンテンツ
    │   ├── project_tab.py        # プロジェクト管理コンテンツ（Programming Type管理対応）
    │   ├── styles.py             # UI共通スタイル定義
    │   └── widgets/              # カスタムウィジェット
    │       ├── activity_sidebar.py # **新規**: VS Code風アクティビティーサイドバー
    │       ├── chat_message.py   # チャットメッセージ表示（Markdown対応）
    │       ├── streaming_chat_message.py # ストリーミングチャットメッセージ表示（Markdown対応）
    │       ├── markdown_renderer.py # Markdown表示ウィジェット
    │       ├── project_card.py   # プロジェクトカード（Programming Type表示対応）
    │       ├── project_edit_dialog.py # プロジェクト編集ダイアログ（Programming Type編集対応）
    │       └── file_uploader.py  # ファイルアップロード
    ├── app/                      # 既存のビジネスロジック
    │   ├── chat.py              # チャット処理（ストリーミング対応）
    │   ├── myjsondb/            # データベース処理（Programming Type管理対応）
    │   ├── util/                # ユーティリティ
    │   └── prompt/              # プロンプト生成
    └── requirements.txt          # 依存関係（Markdown処理ライブラリ追加）
```