from app.util.codeopen import fetch_libraryfiles_and_contents, fetch_files_and_contents


def fastAPItemplate(_prerequisites, _input, _libraryFileList, _src_root_path_List, _ignorelist):
    _content = f"""
# 命令指示書
- 現在のソースコードと要求に対し前提条件と制約条件を満たす最高の成果物を生成してください。

# 前提条件
- {_prerequisites}
- アプリケーションのセットアップ手順や仕様、ガイドはmkdocsに記載するものとします
- mkdocsの定義は、{_prerequisites}/mkdocs.yml にて定義するものとします
- mkdocsにてmkdocstrings-pythonを使用して、Pythonのdocstringからドキュメントを生成するものとします
- mkdocsの使用には下記コマンドで必要なライブラリをインストールするものとします
   ```bash
   pip install mkdocs mkdocs-material mkdocstrings mkdocstrings-python mkdocs-toc-md
   ```
- mkdocsの実行には下記コマンドを実行するものとします
   ```bash
   mkdocs serve

# 制約条件
- 要求文書を適切な表現にブラッシュアップすること
- アウトプットはmarkdown形式とし、出力フォーマットに従うこと
- PythonコードはGoogleスタイル形式でのPython Docstringも出力すること
- Pythonコードのコード規約はflake8に準拠すること
- pytestによるテストコードとテストの実行方法を出力すること
- 変更が発生するファイルは全て出力すること
- 変更が発生しないファイルは出力しないこと
- README.mdには変更を加えないこと
- 削除するファイルがある場合は、削除するファイル名と理由を明確にし、内容が空のファイルを出力すること
- セットアップ手順、仕様、ガイドはmkdocsに記載すること
- git への commit コメントを出力すること

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

# 出力フォーマット
- 出力結果はmarkdown形式とすること
- 出力結果は下記のフォーマットに従うこと
    ```
    ___
    # 要求概要
    ## 要求
    <ブラッシュアップ後の要求文書>
    ## git commit コメント
    <git commit コメント>
    ___
    # 変更
    ## 変更概要
    <変更概要>
    ___
    ## ./README.md
    ### 変更内容
    <変更内容>
    ### ./README.md
    ```md
    <変更後のREADME.md ・・・README.md内のコードブロックはインデントすること。>
    ```
    ___
    ## ./requirements.txt
    ### 変更内容
    <変更内容>
    ### ./requirements.txt
    ```txt
    <変更後のrequirements.txt>
    ```
    ___
    ## ./main.py
    ### 変更内容
    <変更内容>
    ### ./main.py
    ```py
    <変更後のmain.py>
    ```
    ___
    ## ./xxx/yyy.py
    ### 変更内容
    <変更内容>
    ### ./xxx/yyy.py
    ```py
    <変更後の./xxx/yyy.py>
    ```
    ___
    ## ./xxx/zzz.py
    ### 変更内容
    <変更内容>
    ### ./xxx/zzz.py
    ```py
    <変更後の./xxx/zzz.py>
    ```
    ___
    ## ./aaa/bbb.py
    ### 変更内容
    <変更内容>
    ### ./aaa/bbb.py
    ```py
    <変更後の./aaa/bbb.py>
    ```
    ___
    ## ./aaa/ccc.py
    ### 変更内容
    <削除理由>
    ### ./aaa/ccc.py
    ```py
    <削除する場合は内容が空のファイルを出力すること>
    ```
    ___
    ```

___
# 要求
{_input}

___
# 現在のrequirements.txt
{fetch_libraryfiles_and_contents(_libraryFileList)}

___
# 現在のソースコード
{fetch_files_and_contents(_src_root_path_List, _ignorelist)}

    """
    return _content
