# StoryCodeWizardNext

StoryCodeWizardNextは、自然言語で要件を記述するだけで、アプリ一式を生成しローカルの開発環境に即時反映可能な**Vibe Coding 支援ツール**です。

## 📌 What is StoryCodeWizardNext?
>[(MIT Technology Review)バイブコーディングとは何か？ AIに「委ねる」プログラミング新手法](https://www.technologyreview.jp/s/359884/what-is-vibe-coding-exactly/)<br>
>バイブス（感覚）に完全に身を委ね、指数関数的な進化を受け入れ、コードの存在そのものを忘れてしまいます

StoryCodeWizardNext は、この「Vibe Coding」を実践するために設計されたツールです。VS Code 上で Git と GitHub Copilot を組み合わせた使用を前提としています。本ツールは、直感的に思いついたアイデアを即座にコードとして実現し、変化への対応速度を飛躍的に高めます。

StoryCodeWizardNext は OODAループ（Observe→Orient→Decide→Act）という意思決定の高速化サイクルと融合することで、その真価を発揮します。
- Observe（観察）・Orient（判断）・Decide（決断）フェーズでは、直感やアイデアを即座にコード生成に反映。
- Act（行動）フェーズでは GitHub Copilot を活用し迅速なバグ対応を支援。
- さらに Git を活用し、1サイクルごとにコミットして変更を管理することで、いつでも変更の差し戻しや再検討を容易にします。

これらが一体となることで、指数関数的な改善速度と環境変化への圧倒的な適応力を備えた、新しい開発スタイルを実現します。

## 📌 特徴

StoryCodeWizardNext は、Vibe Coding をプロジェクト単位で実践し、高速かつ柔軟な開発を可能にするための以下の特徴を備えています。

1. プロジェクト単位でのVibe Coding管理
	- 複数のプロジェクトを明確に区分けし、それぞれの作業ディレクトリとコーディングエージェントを独立して管理。
	- Next.js や FastAPI といった現代的で人気のフレームワークに対応し、即座に本格的なプロトタイプを生成可能。
	- プロジェクトごとに生成したコードやプロンプトの履歴を保存・管理しているため、過去のアイデアや試作品をいつでも簡単に参照・再利用できます。

2. 自然言語による直感的なコード生成（Vibe Codingの実践）
	- 自然言語で要件を記述するだけで、プロジェクトに最適化されたコード一式が瞬時に生成されます。
	- 現在の作業ディレクトリのコードを事前にLLMが分析するため、既存コードとの整合性を保ちながら最新の状況を反映したコードが生成されます。
	- 生成時に意味のあるGitコミットコメントも自動生成され、変更履歴の管理が容易になります。

3. コード生成後の即時反映・変更管理
	- 生成されたコードはワンクリックで即座に作業ディレクトリへ反映されます。
	- Gitを使用しているため、コードが想定通りでない場合でも即座に元の状態に戻せる安心設計です。

4. 柔軟なLLM選択による最適な開発支援
	- 用途や好みに合わせて以下の主要な大規模言語モデル（LLM）から自由に選択できます。
	- OpenAI GPTシリーズ（汎用性の高い業界標準）
	- Claude (Anthropic)（品質と安全性に優れた推奨モデル）
	- Gemini（柔軟で高速な処理性能）

## 📌 なぜ StoryCodeWizardNext？

StoryCodeWizardNext は、従来のAIを活用したコード生成ツールの抱える課題を明確に解決し、開発者がより直感的で柔軟にコーディングを進められる環境を提供します。

| 🧩 従来の課題        | 🔧 StoryCodeWizardNext の解決策                                                                                                                                 |
| --------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **コピペ地獄**       | 従来のAI生成ツールではコードをコピー＆ペーストする手間が発生し、人的ミスや効率低下の原因になっていました。StoryCodeWizardNext はソースコードを自動でLLMに提供し、生成されたコードも自動的に指定したファイルやディレクトリに保存されるため、手間なく即時に開発作業に反映できます。       |
| **クラウド依存 & 制約** | クラウドベースのサービスでは利用にあたり制約やコストが伴い、環境構築やリソース管理が困難なことがありました。StoryCodeWizardNext は完全にローカルで動作可能なため、インターネット接続や外部サービスへの依存が不要で、プロジェクトのソースコード一式を自由かつ柔軟に管理可能です。          |
| **ブラックボックス化**   | AIによるコード生成のプロセスがブラックボックスとなり、なぜそのコードが生成されたのか理解が難しいケースがありました。StoryCodeWizardNext はプロンプトから生成されるコードまでのプロセスをすべて可視化し、開発者が自由に調整や再生成を行えるようにします。                     |
| **高コスト・経済性の問題** | AIを用いた開発がクラウドサービス依存である場合、費用がかさみ、小規模プロジェクトには経済的な負担となります。StoryCodeWizardNext はローカル環境と効率的なモデル選択により、1つのアプリケーション開発を数ドルという低コストで実現し、小規模なプロトタイプや個人開発でも現実的に活用可能にします。 |


# Getting Started
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

   **「ModuleNotFoundError: No module named '_tkinter'」** が出力された場合<br>
   
   エラーの原因は、PythonがTkinter（_tkinterモジュール）を利用できないためです。これはPythonがTkサポート付きでインストールされていない場合に発生します。

   macOSでは、HomebrewなどでPythonをインストールした場合、Tkサポートが含まれていないことがあります。
   Pythonの再インストール時にTkサポートを有効にする必要があります。
   対処手順:

   1. Homebrewでtkをインストールします。
   1. pyenvを使っている場合は、環境変数を設定してPythonを再インストールします。
      ```bash
      brew install tcl-tk
      env PATH="/opt/homebrew/opt/tcl-tk/bin:$PATH" \
         LDFLAGS="-L/opt/homebrew/opt/tcl-tk/lib" \
         CPPFLAGS="-I/opt/homebrew/opt/tcl-tk/include" \
         PKG_CONFIG_PATH="/opt/homebrew/opt/tcl-tk/lib/pkgconfig" \
         pyenv install 3.12.3
      ```
   1. 仮想環境を作り直し、再度依存パッケージをインストールしてください。

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
1. アプリケーションを起動
   ```bash
   source .venv/bin/activate  # Windowsの場合: .venv\Scripts\activate
   python main.py
   ```

## チュートリアル
フロントエンドをNext.JSでバックエンドをFastAPIでフルスタックアプリを開発します
### 1. プロジェクト登録
<img src="./docs/images/プロジェクト管理.png" alt="プロジェクト管理" width="50%" height="50%">

### 2.コード生成リクエスト
<img src="./docs/images/コード生成リクエスト.png" alt="コード生成リクエスト" width="50%" height="50%">

### 3.コーディングエージェントとの会話履歴
<img src="./docs/images/コーディングエージェントとの会話履歴.png" alt="コーディングエージェントとの会話履歴" width="50%" height="50%">

### その他.ヘルプ・ガイド
<img src="./docs/images/ヘルプ・ガイド.png" alt="ヘルプ・ガイド" width="50%" height="50%">


# ドキュメントの参照

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

# 補足
## 📌 OODAループ × Vibe Coding
StoryCodeWizardNextは、Vibe Codingを実践的に支援するツールであり、<br>
さらに、OODAループを高速かつ効率よく回すための基盤となります。

|フェーズ|Vibe Coding視点|StoryCodeWizardNextが支援すること|
|-|-|-|
|Observe（観察）|ユーザーの感覚・違和感に気づく|プロンプトによる要件入力で課題を言語化|
|Orient（状況判断）|直感で仮説を立てる|自然言語をコードに即座に変換（生成）|
|Decide（意思決定）|「とりあえず動かす」方向へ|変換されたコードをボタン１つで反映。判断を加速|
|Act（実行）|手を動かして検証|ローカル環境で動作確認後、Dockerコンテナを活用して即時デプロイ|

→ このサイクルを数分で回すことが可能になります。

### 重要な追加観点:
- 🛠 GitHub Copilot：バグ対応を迅速化（Actフェーズを支援）
- 🔄 Git：1サイクル毎にコミット（変更の容易な差し戻しが可能。安心してコード反映が可能）

### 🛠 GitHub CopilotがOODAループを加速する理由

GitHub CopilotはAIによるコード補完・バグ修正支援ツールで、特に **「Act」フェーズ** を飛躍的に高速化します。

|項目|具体的な活用方法|効果|
|-|-|-|
|🐞 バグの迅速検知|エディタ内で即座にバグを指摘・修正候補を提案|問題箇所を即座に発見可能|
|🚀 修正の高速化|Copilotの提案を受け入れるだけで素早く修正完了|開発者の負荷を軽減し、反復を促進|
|🎯 仮説検証の効率化|バグの修正を迅速化することで、検証の高速反復を支援|反復速度向上で学習サイクルが短縮|

#### 実際のサイクル例：
   1.	StoryCodeWizardNextでコードを生成
   1.	VS Codeで即時実行、バグ発見
   1.	Copilotを活用してエディタ内でバグ修正
   1.	即時再検証（1へ戻る）

この迅速なバグ対応ループにより、改善サイクルをさらに短縮します。

### 🔄 Gitを活用したコミットベースのOODA反復

Gitを利用することで、各反復ごとにコミットを行い、変更を簡単に管理できます。

|項目|具体的なGit活用方法|効果|
|-|-|-|
|📆 1反復1コミット|各OODAサイクルを細かくコミット|状況変化に応じて即座に差し戻し可能|
|⏪ 変更の迅速な差し戻し|問題が起きたら即座に元に戻す|変更コストを低減し、心理的負担も軽減|
|🔍 差分の明確化|コミットごとに差分が明確化される|改善の履歴が明確になり学習が促進|

### 📌 Copilot × Git × StoryCodeWizardNext の相乗効果

|ツール|主な役割|相乗効果|
|-|-|-|
|StoryCodeWizardNext|コード生成と即座の実行環境構築|Vibeベースでの即時仮説検証を支援|
|GitHub Copilot|高速なバグ検知と修正を支援|仮説検証時の修正コストを最小化|
|Git|変更履歴管理と差し戻しの容易化|迅速な試行錯誤を心理的・技術的に支援|

→ この三位一体により、OODAループが最大限加速されます。

### 📌 従来型の開発との比較（整理）

|項目|従来型開発|OODA×Vibe Coding|
|-|-|-|
|バグ修正速度|遅い（コードの調査・修正に時間がかかる）|非常に速い（Copilotの迅速な修正提案を活用）|
|変更管理|変更が複雑で元に戻しにくい|コミット単位で細かく管理、即座に戻せる|
|開発スタイル|設計・論理主導|直感・仮説主導|
|変化対応力|低い|非常に高い（コード再生成可能）|

## ライセンス

このプロジェクトはMITライセンスのもとで公開されています。詳細については、[LICENSE](LICENSE.md)ファイルをご覧ください。