from app.util.codeopen import fetch_libraryfiles_and_contents, fetch_files_and_contents


def nextjsFastApiTemplate(_prerequisites, _input, _libraryFileList, _src_root_path_List, _ignorelist):
    _content = f"""
# 命令指示書
- 現在のソースコードと要求に対し前提条件と制約条件を満たす最高の成果物を生成してください。

# 前提条件
- {_prerequisites}
- フロントエンドを {_prerequisites}/frontend ディレクトリに、バックエンドを {_prerequisites}/backend ディレクトリに配置しています。
- ディレクトリ構成は下記のようになっています。
    ```
    /my-monorepo
    ├── frontend  (Next.js)
    ├── backend   (FastAPI)
    └── doc プロジェクト全体のドキュメント
        ├── architecture.md
        ├── setup.md
        ├── deployment.md
        └── specification.md
    ```

## フロントエンドアプリケーション固有の前提条件
- node.jsのバージョンはv23.11.0を使用しています。
- npmのバージョンは10.9.2を使用しています。
- Next.jsのプロジェクト登録は下記コマンドを実行しているものとします。
    ```bash
    npx create-next-app@latest frontend \
        --app \
        --ts \
        --tailwind \
        --eslint \
        --src-dir
    ```
- 下記コマンドでの実行を想定するものとします
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
- テストにはVitestとReact Testing Libraryを使用するものとします
- ディレクトリ構成は下記例に準拠するものとします
    ```
    <myproject>/frontend/
        ├── src/
        │   ├── app/
        │   │   ├── page.tsx
        │   │   └── page.test.tsx      <-- app/page.tsx のテストファイル
        │   ├── components/
        │   │   ├── ui/
        │   │   │   ├── Button/
        │   │   │   │   ├── index.tsx
        │   │   │   │   └── Button.test.tsx  <-- Buttonコンポーネントのテストファイル
        │   │   │   └── Input/
        │   │   │       ├── index.tsx
        │   │   │       └── Input.test.tsx   <-- Inputコンポーネントのテストファイル
        │   │   └── features/
        │   │       ├── UserProfile/
        │   │       │   ├── index.tsx
        │   │       │   └── UserProfile.test.tsx
        │   │       └── ...
        │   └── lib/
        │       ├── utils.ts
        │       └── utils.test.ts      <-- ユーティリティ関数のテストファイル
        ├── .eslintrc.json
        ├── package.json
        ├── tsconfig.json
        ├── vitest.config.ts           <-- Vitestの設定ファイル
        └── vitest.setup.ts            <-- (任意) テストのグローバル設定ファイル
    ```

## バックエンドアプリケーション固有の前提条件
- databaseを使用する場合はSQLiteを採用するものとします
- テストコードはpytestを使用するものとします
- 可能な限りテストコードを出力するものとします
- ディレクトリ構成は下記例に準拠するものとします
    ```
    <myproject>/backend/
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
    ├── .gitignore
    ├── pytest.ini           <-- pytestの設定ファイル
    ├── requirements.txt        # Pythonの依存パッケージ
    └── Dockerfile              # Dockerの設定ファイル（必要に応じて）
    ```

# 制約条件
## 共通の制約条件
- 要求文書を適切な表現にブラッシュアップすること
- フロントエンドアプリケーションとバックエンドアプリケーションとの間はRestAPIを通じて通信するものとし、APIの仕様はOpenAPIに準拠すること
- フロントエンドアプリケーションとバックエンドアプリケーションの間でインターフェースの整合性をとること
- フロントエンドアプリケーションとバックエンドアプリケーションの両方で、テストコードを出力すること
- アウトプットはmarkdown形式とし、出力フォーマットに従うこと
- 変更が発生するファイルは全て出力すること
- 変更が発生しないファイルは出力しないこと
- README.mdには変更を加えないこと
- 削除するファイルがある場合は、削除するファイル名と理由を明確にし、内容が空のファイルを出力すること
- 新規インストールが必要ライブラリは、インストール方法を明確にすること
- git への commit コメントを出力すること

## ドキュメントの配置
- 全体のはルートの`docs`に置くこと
- API仕様はFastAPIの自動生成を使うこと
- コンポーネント仕様はStorybookとJSDocを使うこと

## フロントエンドアプリケーション固有の制約条件
- 出力されるコードはESlintにてエラーが存在しないこと
- "npm run build" でビルドが成功すること
- "npm run dev" で開発サーバーが起動し、正常に動作すること
- "npm test" でテストが成功すること
- UIの構成要素を言語化し、各コンポーネントとソースファイルの位置付けを明確にすること
- ライブラリのバージョンの依存関係を考慮し、package.jsonの変更を行うこと

## バックエンドアプリケーション固有の制約条件
- 出力されるコードはPEP8に準拠すること

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
    ## ソースコードマージ後の実施作業
    <マージ後の実施作業>
    ---
    # 変更
    ## 変更概要
    <変更概要>
    ---
    ## ./frontend/package.json
    ### 変更内容
    <変更内容>
    ### ./frontend/package.json
    ```json
    <変更後のpackage.json>
    ```
    ---
    ## ./frontend/tsconfig.json
    ### 変更内容
    <変更内容>
    ### ./frontend/tsconfig.json
    ```json
    <変更後のtsconfig.json>
    ```
    ---
    ## ./frontend/src/xxx.tsx
    ### 変更内容
    <変更内容>
    ### ./frontend/src/xxx.tsx
    ```tsx
    <変更後の./src/xxx.tsx>
    ```
    ---
    ## ./frontend/src/yyy.tsx
    ### 変更内容
    新規作成
    ### ./frontend/src/yyy.tsx
    ```tsx
    <変更後の./frontend/src/yyy.tsx>
    ```
    ---
    ## ./frontend/src/zzz.css
    ### 変更内容
    <変更内容>
    ### ./frontend/src/zzz.css
    ```css
    <変更後の./frontend/src/zzz.css>
    ```
    ---
    ## ./frontend/src/fff.tsx
    ### 変更内容
    <削除理由>
    ### ./frontend/src/fff.tsx
    ```tsx
    <削除する場合は内容が空のファイルを出力すること>
    ```
    ---
    ## ./backend/requirements.txt
    ### 変更内容
    <変更内容>
    ### ./backend/requirements.txt
    ```txt
    <変更後のrequirements.txt>
    ```
    ---
    ## ./backend/app/main.py
    ### 変更内容
    <変更内容>
    ### ./backend/app/main.py
    ```py
    <変更後のmain.py>
    ```
    ---
    ## ./backend/xxx/yyy.py
    ### 変更内容
    <変更内容>
    ### ./backend/xxx/yyy.py
    ```py
    <変更後の./backend/xxx/yyy.py>
    ```
    ---
    ## ./backend/xxx/zzz.py
    ### 変更内容
    <変更内容>
    ### ./backend/xxx/zzz.py
    ```py
    <変更後の./backend/xxx/zzz.py>
    ```
    ---
    ## ./aaa/bbb.py
    ### 変更内容
    <変更内容>
    ### ./aaa/bbb.py
    ```py
    <変更後の./aaa/bbb.py>
    ```
    ---
    ## ./backend/aaa/ccc.py
    ### 変更内容
    <削除理由>
    ### ./backend/aaa/ccc.py
    ```py
    <削除する場合は内容が空のファイルを出力すること>
    ```
    ---
    ## ./docs/specification.md
    ### 変更内容
    <変更理由>
    ### ./docs/specification.md
    ```md
    <変更後のdocs。markdown形式でコードブロックを使用する場合は必ずインデントすること>
    ```
    ---
    ```

# 要求仕様書
{_input}

# 現在のライブラリ管理ファイル・Dockerfile・docker-compose.yml
{fetch_libraryfiles_and_contents(_libraryFileList)}

# 現在のソースコード
{fetch_files_and_contents(_src_root_path_List, _ignorelist)}

    """
    return _content