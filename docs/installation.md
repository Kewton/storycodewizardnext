# Installation Guide

Follow the steps to set up the StoryCodeWizard project on your local machine.

## Prerequisites

- Python >= 3.9
- Git

## Steps

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