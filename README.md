# StoryCodeWizardNext - CustomTkinter Desktop Application

StoryCodeWizardNextは、自然言語で記述した要求・要件からコード一式を生成しローカルの開発環境に反映する**Vibe Coding 支援ツール**です。

## 概要
Vibe Codingのコンセプトは

>バイブス（感覚）に完全に身を委ね、指数関数的な進化を受け入れ、コードの存在そのものを忘れてしまいます
> <br> [(MIT Technology Review)バイブコーディングとは何か？ AIに「委ねる」プログラミング新手法](https://www.technologyreview.jp/s/359884/what-is-vibe-coding-exactly/)

ですが、2025年現在、下記課題があると考えています。

- Chatインターフェース
   - 入出力時コードを大量にコピーする必要がある
- クラウドサービス
   - 個別に料金が発生する。無料の場合も制約がある。
   - 作業環境や実行環境に制約がある
   - ブラックボックスが多い
   - 独自の実行環境で始めようとすると大変

StoryCodeWizardNextは、自然言語での要件の記述からコンテナ化までの流れを支援します。
バグ修正はGithubCopilotの使用を想定しています。

１アプリ５ドルくらいくらいで作成可能な見込みです。

LLMへの入出力について「コードの存在を忘れる」ことが可能で、動作させるのに必要なコード一式を出力させることができ、クライアントで動作するツールです。

このプロジェクトは、要件からアプリケーションのコード一式を生成することを目的とした **Vibe Coding 支援ツール**です。大規模言語モデル（LLM）の進化に伴い、ソースコード全体をLLMに渡し、新しい要件と共に処理させることで、更新されたコードを効率的に出力できる可能性に着目しました。このツールは、そのアイデアを基に、特に出力フォーマットを工夫することで、要件からコードへの反映をよりシームレスに行うことを目指しています。

主な**ターゲットユーザー**は、「Vibe Coding」というアプローチで独自のアプリケーションを開発したいと考えているものの、現時点では技術的なリテラシーに不安があり、最初の一歩をスムーズに踏み出せない方々です。

このツールを利用することで、ユーザーは主にGUIを中心とした簡単なアプリケーションであれば、**1〜2時間程度**で開発を始めることができます。**ローカル環境で実行可能なコード一式**が出力され実際に動作を確認しながら機能改善を繰り返していくことが可能です。

### 背景
- 
### 目的
- Vibe Codingの民主化
### 主な機能
- コード"一式"の生成
- 履歴管理
### 使い方
- Step1: 本ツールを使用してコードを生成し
- Step2: VS Codeの作業ツリーで差分を確認。
- Step3: バグ修正は GitHubCopiloy を使用

### 使用方法
1. 要求・要件を整理
1. 要求・要件を入力
1. プロジェクトに反映
1. 動作確認

##  画面イメージ
### プロジェクト登録
<img src="./docs/images/プロジェクト管理.png" alt="プロジェクト管理" width="50%" height="50%">

### コード生成リクエスト
<img src="./docs/images/コード生成リクエスト.png" alt="コード生成リクエスト" width="50%" height="50%">

### コーディングエージェントとの会話履歴
<img src="./docs/images/コーディングエージェントとの会話履歴.png" alt="コーディングエージェントとの会話履歴" width="50%" height="50%">

### ヘルプ・ガイド
<img src="./docs/images/ヘルプ・ガイド.png" alt="ヘルプ・ガイド" width="50%" height="50%">


## 特徴
- **複数プロジェクトサポート**: プロジェクトごとに履歴を管理し、特定のプロジェクトに絞ったコード生成を行います。
- **選択可能なLLM（大規模言語モデル）**:
  - OpenAI GPTシリーズ
  - Claude (Anthropic)
  - Gemini
- **コード履歴管理**: 過去に生成したコードやプロンプトをいつでも参照履歴からダウンロード可能。
- **カスタムディレクトリと設定管理**: 各プロジェクトは異なるディレクトリ構造に対応可能。

## インストール

1. Gitリポジトリをクローンします:
   ```bash
   git clone https://github.com/Kewton/storycodewizardnext
   cd storycodewizardnext
   ```

2. Python環境のセットアップと必要なライブラリをインストールします:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate  # Windowsの場合: .venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. 機密情報を設定します:<br>
   以下の内容で`secret_keys.py`を作成します。
   ```python
   openai_api_key = "<Your OpenAI API Key>"
   claude_api_key = "<Your Claude API Key>"
   gemini_api_key = "<Your Gemini API Key>"
   ```

4. データベースを初期化します:
   ```bash
   python initdatabase.py
   ```

## アプリケーションの起動
**アプリケーションを起動**
```bash
source .venv/bin/activate  # Windowsの場合: .venv\Scripts\activate
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

このプロジェクトはMITライセンスのもとで公開されています。詳細については、[LICENSE](LICENSE.md)ファイルをご覧ください。