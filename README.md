# StoryCodeWizard - CustomTkinter Desktop Application

StreamlitからCustomTkinterに変換されたデスクトップチャットアプリケーション

## 機能概要
- LLMとのチャット機能（GPT、Claude、Gemini対応）
- プロジェクト管理機能
- チャット履歴の保存・検索・ダウンロード
- ファイルアップロード対応（JPEG）
- コード自動生成とプロジェクトへの反映
- モダンなCustomTkinter UI
- リアルタイムデータ更新機能

## セットアップ手順

### 1. 環境構築
```bash
python3 -m venv .venv
source .venv/bin/activate  # Windowsの場合: .venv\Scripts\activate
pip install -r requirements.txt
```

### 2. APIキー設定
`secret_keys.py`ファイルを作成し、以下の内容を設定：
```python
openai_api_key = "<your OpenAI API key>"
claude_api_key = "<your Claude API key>"
gemini_api_key = "<your Gemini API key>"
```

### 3. データベース初期化
```bash
python initdatabase.py
```

### 4. アプリケーション起動
```bash
python main.py
```

## UIコンポーネント構成

### メインウィンドウ (MainWindow)
- **位置**: `./ui/main_window.py`
- **機能**: アプリケーションのメインコンテナ、タブ管理
- **コンポーネント**: CTkTabview、ウィンドウサイズ管理
- **改善点**: レスポンシブレイアウト、タブ間データ同期

### Story2Codeタブ (ChatTab)
- **位置**: `./ui/chat_tab.py`
- **機能**: LLMとの対話インターフェース
- **コンポーネント**: プロジェクト選択、モデル選択、入力エリア、チャット表示
- **改善点**: ラベルとドロップダウンの適切な間隔調整、リアルタイムデータ更新

### MyHistoryタブ (HistoryTab)
- **位置**: `./ui/history_tab.py`
- **機能**: 過去のチャット履歴管理
- **コンポーネント**: 履歴リスト、詳細表示、削除・ダウンロード機能
- **改善点**: 自動データ更新、フィルタリング機能強化

### Project Listタブ (ProjectTab)
- **位置**: `./ui/project_tab.py`
- **機能**: プロジェクトの作成・管理
- **コンポーネント**: プロジェクト一覧、新規作成フォーム
- **改善点**: ラベルとフィールドの配置最適化、登録後の自動更新

### カスタムウィジェット
- **ChatMessage**: `./ui/widgets/chat_message.py` - チャットメッセージ表示用
- **ProjectCard**: `./ui/widgets/project_card.py` - プロジェクト情報表示用
- **FileUploader**: `./ui/widgets/file_uploader.py` - ファイルアップロード機能

## アーキテクチャ

```
./
├── main.py                    # アプリケーションエントリーポイント
├── ui/                        # UIコンポーネント
│   ├── main_window.py         # メインウィンドウ
│   ├── chat_tab.py           # チャット機能タブ
│   ├── history_tab.py        # 履歴管理タブ
│   ├── project_tab.py        # プロジェクト管理タブ
│   ├── styles.py             # UI共通スタイル定義
│   └── widgets/              # カスタムウィジェット
│       ├── chat_message.py   # チャットメッセージ表示
│       ├── project_card.py   # プロジェクトカード
│       └── file_uploader.py  # ファイルアップロード
├── app/                      # 既存のビジネスロジック
│   ├── chat.py              # チャット処理（CustomTkinter対応）
│   ├── myjsondb/            # データベース処理
│   ├── util/                # ユーティリティ
│   └── prompt/              # プロンプト生成
└── requirements.txt          # 依存関係
```

## 技術仕様
- **UI Framework**: CustomTkinter 5.2.0+
- **Python**: 3.8+
- **Database**: JSONベースローカルDB
- **LLM API**: OpenAI, Anthropic, Google Gemini

## 開発者向け情報

### カスタムテーマ
CustomTkinterのダークテーマをベースにカスタムカラーパレットを適用：
- プライマリ: #1f538d (ブルー)
- セカンダリ: #14375e (ダークブルー)
- アクセント: #1f538d (ライトブルー)
- 背景: #212121 (ダークグレー)

### レイアウト設計指針
- **間隔統一**: 全てのコンポーネント間で一貫した間隔を使用
- **視覚的階層**: ラベル、入力フィールド、ボタンの明確な配置
- **レスポンシブ対応**: ウィンドウサイズ変更に対応した柔軟なレイアウト
- **データ同期**: タブ間でのリアルタイムデータ更新

### イベントハンドリング
- 非同期LLM API呼び出し
- リアルタイムUI更新
- ファイルドラッグ&ドロップ対応
- 自動データリフレッシュ機能

## トラブルシューティング

### よくある問題
1. **APIキーエラー**: `secret_keys.py`の設定を確認
2. **データベースエラー**: `python initdatabase.py`を再実行
3. **UI表示問題**: CustomTkinterの最新版を確認
4. **レイアウト崩れ**: ウィンドウサイズを調整し、最小サイズ以上で使用

### ログ出力
アプリケーションログは標準出力に表示されます。

## 従来のStreamlit版からの変更点

### 主な改善点
- **ネイティブデスクトップアプリ**: ブラウザ不要で直接実行
- **レスポンシブUI**: より高速で滑らかな操作感
- **カスタマイズ性向上**: テーマ・レイアウトの柔軟な調整
- **ファイル管理**: ドラッグ&ドロップによる直感的なファイル操作
- **リアルタイム更新**: データベース変更の即座な反映

### 機能移行対応表
| Streamlit機能 | CustomTkinter対応 |
|--------------|------------------|
| st.tabs() | CTkTabview |
| st.selectbox() | CTkComboBox |
| st.text_area() | CTkTextbox |
| st.button() | CTkButton |
| st.file_uploader() | カスタムFileUploader |
| st.dataframe() | Tkinter Listbox + カスタム表示 |
| st.download_button() | ファイルダイアログ + 保存処理 |