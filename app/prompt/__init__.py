from app.util.codeopen import fetch_libraryfiles_and_contents, fetch_files_and_contents


def createPromt(_systemrole_content, _input):
    _prerequisites = _systemrole_content["pjdir"] + _systemrole_content["prerequisites"]

    _libraryFileList = []
    for a in _systemrole_content["libraryFileList"]:
        _libraryFileList.append(_systemrole_content["pjdir"] + "/" + a)
    _src_root_path = _systemrole_content["pjdir"] + "/" + _systemrole_content["srcdire"]
    _ignorelist = _systemrole_content["ignorelist"]

    if "nextjstemplate1" == _systemrole_content["prompt"]:
        return nextjstemplate1(_prerequisites, _input, _libraryFileList, _src_root_path, _ignorelist)
    elif "nextjstemplate2" == _systemrole_content["prompt"]:
        return nextjstemplate2(_prerequisites, _input, _libraryFileList, _src_root_path, _ignorelist)
    elif "fastAPItemplate" == _systemrole_content["prompt"]:
        return fastAPItemplate(_prerequisites, _input, _libraryFileList, _src_root_path, _ignorelist)
    elif "streamlit2CustomTkinter" == _systemrole_content["prompt"]:
        return streamlit2CustomTkinter(_prerequisites, _input, _libraryFileList, _src_root_path, _ignorelist)
    else:
        _content = f"""
# 命令指示書
- 現在のソースコードと要求に対し前提条件と制約条件を満たす最高の成果物を生成してください。

### 前提条件
{_prerequisites}

### 制約条件
- アウトプットはmarkdown形式とすること
- 要求文書を適切な表現に変換すること
- UIの構成要素を言語化し、各コンポーネントとソースファイルの位置付けを明確にすること
- 新規にインストールが必要な場合、ライブラリのインストール方法を明確にすること
- 新規にファイル作成が必要な場合、名称と拡張子も明確にしソースコードをフルで出力すること
- git への commit コメントを出力すること

### 要求
{_input}

### 現在のpackage.json
{fetch_libraryfiles_and_contents(_libraryFileList)}

### 現在のソースコード
{fetch_files_and_contents(_src_root_path, _ignorelist)}

    """
        return _content


def nextjstemplate1(_prerequisites, _input, _libraryFileList, _src_root_path, _ignorelist):
    _content = f"""
# 命令指示書
- 現在のソースコードと要求に対し前提条件と制約条件を満たす最高の成果物を生成してください。

# 前提条件
- {_prerequisites}
- node.jsのバージョンはv23.11.0を使用しています。
- npmのバージョンは10.9.2を使用しています。
- Next.jsのプロジェクト登録は下記コマンドを実行しているものとします。
    ```bash
    npx create-next-app@latest myux \
        --app \
        --ts \
        --tailwind \
        --eslint \
        --src-dir
    ```

# 制約条件
- アウトプットはmarkdown形式とすること
- 出力フォーマットに従うこと
- セットアップ手順はREADME.mdに記載すること
- 下記コマンドにより実行可能であること
    ```bash
    # 依存関係のインストール
    npm install

    # 開発サーバーの起動
    npm run dev

    # ビルド
    npm run build

    # 本番サーバーの起動
    npm start
    ```
- 変更が発生するファイルは全て出力すること
- 要求文書を適切な表現にブラッシュアップすること
- UIの構成要素を言語化し、各コンポーネントとソースファイルの位置付けを明確にすること
- 新規インストールが必要ライブラリは、インストール方法を明確にすること
- git への commit コメントを出力すること

# 出力フォーマット
- 出力結果はmarkdown形式とすること
- 出力結果は下記のフォーマットに従うこと
    ```
    ---
    # 要求概要
    ## 要求
    <ブラッシュアップ後の要求文書>
    ## git commit コメント
    <git commit コメント>
    ---
    # 変更
    ## 変更概要
    <変更概要>
    ---
    ## ./README.md
    ### 変更内容
    <変更内容>
    ### ./README.md
    ```md
    <変更後のREADME.md ・・・README.mdのみ全体をインデントしたものを出力すること。また、README.md内のコードブロックはインデントすること。>
    ```
    ---
    ## ./package.json
    ### 変更内容
    <変更内容>
    ### ./package.json
    ```json
    <変更後のpackage.json>
    ```
    ---
    ## ./tsconfig.json
    ### 変更内容
    <変更内容>
    ### ./tsconfig.json
    ```json
    <変更後のtsconfig.json>
    ```
    ---
    ## ./src/xxx.tsx
    ### 変更内容
    <変更内容>
    ### ./src/xxx.tsx
    ```tsx
    <変更後の./src/xxx.tsx>
    ```
    ---
    ## ./src/yyy.tsx
    ### 変更内容
    新規作成
    ### ./src/yyy.tsx
    ```tsx
    <変更後の./src/xxx.tsx>
    ```
    ---
    ## ./src/zzz.css
    ### 変更内容
    <変更内容>
    ### ./src/zzz.css
    ```css
    <変更後の./src/zzz.css>
    ```
    ---
    ```

# 要求仕様書
{_input}

# 現在の管理ファイル
{fetch_libraryfiles_and_contents(_libraryFileList)}

# 現在のソースコード
{fetch_files_and_contents(_src_root_path, _ignorelist)}

    """
    return _content


def nextjstemplate2(_prerequisites, _input, _libraryFileList, _src_root_path, _ignorelist):
    _content = f"""
# 命令指示書
- 現在のソースコードと要求に対し前提条件と制約条件を満たす最高の成果物を生成してください。
- 必要に応じて改善案を提案して下さい。

### 前提条件
{_prerequisites}

### 制約条件
- アウトプットはmarkdown形式とすること
- 要求文書を適切な表現に変換すること
- UIの構成要素を言語化し、各コンポーネントとソースファイルの位置付けを明確にすること
- 新規にインストールが必要な場合、ライブラリのインストール方法を明確にすること
- 新規にファイル作成が必要な場合、名称と拡張子も明確にしソースコードをフルで出力すること
- git への commit コメントを出力すること

### 要求
{_input}

### 現在のpackage.json
{fetch_libraryfiles_and_contents(_libraryFileList)}

### 現在のソースコード
{fetch_files_and_contents(_src_root_path, _ignorelist)}

    """
    return _content


def fastAPItemplate(_prerequisites, _input, _libraryFileList, _src_root_path, _ignorelist):
    _content = f"""
# 命令指示書
- 現在のソースコードと要求に対し、クリティカルシンキングを活用し、下記手順に従って前提条件と制約条件と技術制約を満たす最高の成果物を生成してください。
    1. 要求を解析し必要に応じて情報を補完してユーザーが本当にやりたいことを言語化する。
    2. 出力結果への評価方法及び前提条件と制約条件と技術制約を満たした合格条件を定義する。
    3. ソースコードが存在する場合、下記に注目して現状認識する
        - databaseのテーブル構造を理解する
        - ディレクトリ構造を整理しアーキテクチャを理解する
        - モジュール間のインターフェースを整理する
        - 各モジュールの処理フローを理解する
    4. ユーザーがやりたいことが障害調査かつエラーログが付与されている場合、3の結果をふまえたうえで下記に注目して原因調査と対策を具体化する
        - エラーが発生している箇所を特定する
        - 特定のモジュールに閉じたエラーなのか他のモジュールに影響するエラーなのか、またdatabaseにも影響を及ぼすのかを判断する
        - 他のモジュールに影響する場合、その影響範囲を特定する
        - クリティカルシンキングを活用し根本原因を特定する
        - 根本原因を取り除く抜本的な解決方針を立案する
        - 解決策を適用すべき範囲を明確にする
    5. 合格条件に合うコードもしくはテキストを出力する
    6. 2の評価方法に従って評価する
    7. 評価結果が合格の場合終了する。不合格の場合は8に進む。
    8. 不合格の事象を事実に基づいて言語化する
    9. 不合格の原因箇所を特定する
    10. 原因を調査し、調査結果に基づいて下記に従う
        - 現状認識誤りの場合は、誤り箇所に注意し認識を修正し、3に戻る
        - ユーザーが付与したエラーログの解釈誤りの場合は誤り内容を明確ご、4に戻る
        - 出力したコードもしくはテキストが誤っている場合は修正し、5に戻る

# 前提条件
- {_prerequisites}
- 開発環境は「macbook air m3」です

# 制約条件
- 出力結果はmarkdown形式とすること
- ユーザーが本当にやりたいことを言語化したものを出力すること
- PythonコードはGoogleスタイル形式でのPython Docstringも出力すること
- Pythonコードのコード規約はflake8に準拠すること
- pytestによるテストコードとテストの実行方法を出力すること
- ソースコードとテキスト共に途中を省略せずに全てを出力すること
- 新規にライブラリのインストールが必要な場合、ライブラリのインストール方法を明確にすること
- 新規にファイル作成が必要な場合、ファイル名と拡張子を明確にしソースコードをフルで出力すること
- 修正が必要な場合は、類似の修正であっても全ての対象箇所を出力すること
- 修正時は、修正後の全てのコードに加えdiff形式で変更箇所が明らかになるように出力すること
- ./docs/requiredSpecifications.md（要求仕様書）の変更が発生する場合は修正内容を出力すること
- git への commit コメントを出力すること
- 出力結果の妥当性の評価方法及び評価結果を出力すること
- 出力結果に問題が残る場合は再度検討しブラッシュアップすること

# 技術制約
- databaseはSQLiteを使用すること
- ディレクトリ構成は下記例に準拠こと
    ```
    <myproject>/
    ├── app/
    │   ├── api/                # エンドポイント（ルーター）のディレクトリ
    │   │   ├── v1/
    │   │   │   ├── endpoints/  # 個別のエンドポイントファイル
    │   │   │   │   ├── user.py # 例: ユーザー関連のエンドポイント
    │   │   │   │   ├── item.py # 例: アイテム関連のエンドポイント
    │   │   │   └── __init__.py
    │   ├── core/               # 設定や重要なロジック（例: 認証設定）
    │   │   ├── config.py       # 設定ファイル
    │   │   ├── security.py     # セキュリティ関連の設定や認証処理
    │   │   └── __init__.py
    │   ├── models/             # データベースモデル（SQLAlchemyなど）
    │   │   ├── user.py         # 例: ユーザーモデル
    │   │   ├── item.py         # 例: アイテムモデル
    │   │   └── __init__.py
    │   ├── schemas/            # データバリデーションやリクエスト/レスポンスのスキーマ
    │   │   ├── user.py         # 例: ユーザー関連のスキーマ
    │   │   ├── item.py         # 例: アイテム関連のスキーマ
    │   │   └── __init__.py
    │   ├── services/           # ビジネスロジック（アプリケーションのサービス層）
    │   │   ├── user_service.py # 例: ユーザー関連のビジネスロジック
    │   │   ├── item_service.py # 例: アイテム関連のビジネスロジック
    │   │   └── __init__.py
    │   ├── db/                 # データベース接続や設定
    │   │   ├── base.py         # モデルのベース設定
    │   │   ├── session.py      # DBセッションの設定
    │   │   └── __init__.py
    │   ├── utils/              # ヘルパー関数やユーティリティ関数
    │   │   ├── helpers.py
    │   │   └── __init__.py
    │   ├── main.py             # アプリケーションのエントリーポイント
    │   └── __init__.py
    ├── .env                    # 環境変数ファイル
    ├── tests                   # pytestによるテストコード
    │   ├── test_user.py        # 例: ユーザー関連のテスト
    │   └── test_item.py        # 例: アイテム関連のテスト
    ├── docs                    # mkdocsによるドキュメント
    │   ├── index.md            # mkddocsのhome画面
    │   ├── reference.md        # appディレクトリのコードから自動生成下ドキュメント
    │   └── requiredSpecifications.md # 要求仕様書
    ├── requirements.txt        # Pythonの依存パッケージ
    └── Dockerfile              # Dockerの設定ファイル（必要に応じて）
    ```

---
# 要求
{_input}

---
# 現在のrequirements.txt
{fetch_libraryfiles_and_contents(_libraryFileList)}

---
# 現在のソースコード
{fetch_files_and_contents(_src_root_path, _ignorelist)}

    """
    return _content


def streamlit2CustomTkinter(_prerequisites, _input, _libraryFileList, _src_root_path, _ignorelist):
    _content = f"""
# 命令指示書
- 現在のソースコードと要求に対し前提条件と制約条件を満たす最高の成果物を生成してください。

# 前提条件
- {_prerequisites}

# 制約条件
- 要求文書を適切な表現にブラッシュアップすること
- アウトプットはmarkdown形式とし、出力フォーマットに従うこと
- 変更が発生するファイルは全て出力すること
- セットアップ手順はREADME.mdに記載すること
- UIの構成要素を言語化し、各コンポーネントとソースファイルの位置付けを明確にすること
- 新規インストールが必要ライブラリは、インストール方法を明確にすること
- git への commit コメントを出力すること

# 出力フォーマット
- 出力結果はmarkdown形式とすること
- 出力結果は下記のフォーマットに従うこと
    ```
    ---
    # 要求概要
    ## 要求
    <ブラッシュアップ後の要求文書>
    ## git commit コメント
    <git commit コメント>
    ---
    # 変更
    ## 変更概要
    <変更概要>
    ---
    ## ./README.md
    ### 変更内容
    <変更内容>
    ### ./README.md
    ```md
    <変更後のREADME.md ・・・README.mdのみ全体をインデントしたものを出力すること。また、README.md内のコードブロックはインデントすること。>
    ```
    ---
    ## ./requirements.txt
    ### 変更内容
    <変更内容>
    ### ./requirements.txt
    ```txt
    <変更後のrequirements.txt>
    ```
    ---
    ## ./main.py
    ### 変更内容
    <変更内容>
    ### ./main.py
    ```py
    <変更後のmain.py>
    ```
    ---
    ## ./xxx/yyy.py
    ### 変更内容
    新規作成
    ### ./xxx/yyy.py
    ```py
    <変更後の./xxx/yyy.py>
    ```
    ---
    ## ./xxx/zzz.py
    ### 変更内容
    新規作成
    ### ./xxx/zzz.py
    ```py
    <変更後の./xxx/zzz.py>
    ```
    ---
    ## ./aaa/bbb.py
    ### 変更内容
    新規作成
    ### ./aaa/bbb.py
    ```py
    <変更後の./aaa/bbb.py>
    ```
    ---
    ```

# 要求仕様書
{_input}

# 現在の管理ファイル
{fetch_libraryfiles_and_contents(_libraryFileList)}

# 現在のソースコード
{fetch_files_and_contents(_src_root_path, _ignorelist)}

    """
    return _content