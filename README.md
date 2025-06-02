# StoryCodeWizard - CustomTkinter Desktop Application

StoryCodeWizardは、ストーリーベースの要件記述から最高のコード生成を支援するツールです。
現在のプロジェクトはFastAPIやCustomTkinterやNext.jsを使用して開発されているシステム向けのコードテンプレート生成や改善案を提供します。

## 使用方法

## 特徴
- **複数プロジェクトサポート**: プロジェクトごとに履歴を管理し、特定のプロジェクトに絞ったコード生成を行います。
- **選択可能なLLM（大規模言語モデル）**:
  - OpenAI GPTシリーズ
  - Claude (Anthropic)
  - Gemini
- **コード履歴管理**: 過去に生成したコードやプロンプトをいつでも参照履歴からダウンロード可能。
- **カスタムディレクトリと設定管理**: 各プロジェクトは異なるディレクトリ構造に対応可能。

## セットアップ手順

### 1. ソースコードの取得
Gitリポジトリをクローンします。
```bash
git clone https://github.com/Kewton/storycodewizardnext
cd storycodewizardnext
```

### 2. Python環境のセットアップ
```bash
python3 -m venv .venv
source .venv/bin/activate  # Windowsの場合: .venv\Scripts\activate
pip install -r requirements.txt
```

### 3. 機密情報の設定
以下の内容で`secret_keys.py`を作成します。
```python
openai_api_key = "<Your OpenAI API Key>"
claude_api_key = "<Your Claude API Key>"
gemini_api_key = "<Your Gemini API Key>"
```

### 4. データベースの初期化
```bash
python initdatabase.py
```

### 5. アプリケーション起動
```bash
python main.py
```

## ドキュメントの参照

アプリケーションのAPIや仕様についての詳細な説明は MkDocs で確認可能です。

1. **必要なツールのインストール**
   ```bash
   pip install mkdocs mkdocs-material mkdocstrings mkdocstrings-python mkdocs-toc-md
   ```

2. **ローカルサーバーでドキュメントを表示**
   ```bash
   mkdocs serve
   ```

   デフォルトで `http://localhost:8000` で閲覧可能です。

## ライセンス

このプロジェクトはMITライセンスのもとで公開されています。詳細については、[LICENSE](LICENSE)ファイルをご覧ください。