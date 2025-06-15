from app.util.codeopen import fetch_libraryfiles_and_contents, fetch_files_and_contents


def nextjsNestJsTemplate(_prerequisites, _input, _libraryFileList, _src_root_path_List, _ignorelist):
    _content = f"""
# 命令指示書
- 現在のソースコードと要求に対し前提条件と制約条件を満たす最高の成果物を生成してください。

# 前提条件
- {_prerequisites}
- 下記スクリプトを実行して環境構築しているものとします
    ```
    # Step1. 基本的なTurborepoプロジェクトを作成する
    ## 1. プロジェクトを作成
    npx create-turbo@latest <my-monorepo-project>

    ## 2. プロジェクトのディレクトリに移動
    cd <my-monorepo-project>

    ## 3. 依存関係をインストール
    pnpm install

    ___
    # Step2. 不要なアプリケーションを削除する
    rm -rf apps/docs

    ___
    # Step3. NestJSアプリケーションを新規作成する
    cd apps

    ## NestJSのCLIを使って 'api' プロジェクトを作成
    npx @nestjs/cli new api

    ## NestJSが作成したGitリポジトリは不要なので削除
    rm -rf api/.git

    ## ルートディレクトリに戻る
    cd ..
    ```
- ディレクトリ構成は下記のようになっています。フロントエンドを {_prerequisites}/apps/web ディレクトリに、バックエンドを {_prerequisites}/apps/api ディレクトリに配置しています。
    ```
    my-monorepo-project/
    ├── apps/
    │   ├── api/          # NestJS バックエンド
    │   │   ├── src/
    │   │   │   ├── app.controller.ts
    │   │   │   ├── app.module.ts
    │   │   │   └── main.ts
    │   │   ├── test/
    │   │   ├── eslint.config.mjs
    │   │   ├── nest-cli.json
    │   │   ├── package.json
    │   │   └── tsconfig.json
    │   │
    │   └── web/          # Next.js フロントエンド
    │       ├── app/
    │       ├── components/
    │       ├── public/
    │       ├── eslint.config.js
    │       ├── next.config.js
    │       ├── package.json
    │       └── tsconfig.json
    │
    ├── packages/
    │   ├── config-eslint/ # ESLintの共通設定
    │   │   └── package.json
    │   │
    │   └── tsconfig/      # TypeScriptの共通設定
    │       └── package.json
    │
    ├── .gitignore
    ├── package.json       # 全体を管理するpackage.json (pnpm-workspace.yamlも生成される)
    ├── pnpm-workspace.yaml
    ├── turbo.json         # Turborepoの設定ファイル
    └── docs               # プロジェクト全体のドキュメント
        ├── architecture.md
        ├── apiSpecification.md
        ├── datamodel.md
        ├── envlist.md
        ├── overview.md
        └── uiSpecification.md
    ```
- ビルド方法、実行方法、テスト自動化方法、静的解析方法は下記スクリプトを実行するものとします
    ```bash
    # 依存関係のインストール
    pnpm install

    # 開発サーバーの起動
    pnpm dev

    # 全てのアプリケーションのビルド
    pnpm build

    # Next.js (web) のみビルド
    pnpm turbo build --filter=web

    # NestJS (api) のみビルド
    pnpm turbo build --filter=api

    # 本番サーバーの起動
    pnpm start

    # 全てのテストを実行
    pnpm test

    # コードの静的解析を実行
    pnpm lint
    ```

# 制約条件
- databaseを使用する場合はSQLiteを採用するものとします
- 可能な限りテストコードを出力するものとします

# コード生成ルール
- 要求文書を適切な表現にブラッシュアップすること
- /docs ディレクトリにあるドキュメントを更新すること
- フロントエンドアプリケーションとバックエンドアプリケーションの両方で、API仕様を整合性をとること
- フロントエンドアプリケーションとバックエンドアプリケーションの両方で、テストコードを出力すること
- アウトプットはmarkdown形式とし、出力フォーマットに従うこと
- 変更が発生するファイルはファイル内容を全て出力すること
- 変更が発生しないファイルは出力しないこと
- README.mdには変更を加えないこと
- 外部仕様を uiSpecification.md にユースケース（Use Case）ベースで記載すること
- apiSpecification.md にAPI仕様を記載すること
- データモデルを datamodel.md に Mermaid で記載すること
- アーキテクチャを architecture.md に Mermaid で記載すること
- 環境変数の一覧を envlist.md に記載すること
- サービスの全体概要を overview.md に marp で記載すること。スライドの構成は以下のようにすること。
    ```
    1.  **はじめに**： 私たちは誰で、何を目指しているのか
    2.  **解決したい課題 (The Problem)**： なぜこのサービスが必要なのか
    3.  **私たちの解決策 (Our Solution)**： このサービスは何をするものか
    4.  **ターゲットユーザー**： 誰のためのサービスか
    5.  **主要な機能**： 具体的に何ができるのか
    6.  **技術スタックとアーキテクチャ**： どうやって作られているのか
    7.  **競合とポジショニング**： 市場における我々の立ち位置
    8.  **今後のロードマップ**： これからどこへ向かうのか
    9.  **まとめ**
    ```
- 削除するファイルがある場合は、削除するファイル名と理由を明確にし、内容が空のファイルを出力すること
- 新規インストールが必要ライブラリは、インストール方法を明確にすること
- git への commit コメントを出力すること
- "pnpm lint" で静的解析が成功すること
- "pnpm dev" で開発サーバーが起動し、正常に動作すること
- "pnpm test" で全てのテストが成功すること
- "pnpm build" でビルドが成功すること
- UIの構成要素を言語化し、各コンポーネントとソースファイルの位置付けを明確にすること
- ライブラリのバージョンの依存関係を考慮し、package.jsonの変更を行うこと

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
    ## ソースコードマージ後の実施作業
    <マージ後の実施作業>
    ___
    # 変更
    ## 変更概要
    <変更概要>
    ___
    ## ./apps/api/package.json
    ### 変更内容
    <変更内容>
    ### ./apps/web/package.json
    ```json
    <変更後のpackage.json>
    ```
    ___
    ## ./apps/web/tsconfig.json
    ### 変更内容
    <変更内容>
    ### ./apps/web/tsconfig.json
    ```json
    <変更後のtsconfig.json>
    ```
    ___
    ## ./apps/web/src/xxx.tsx
    ### 変更内容
    <変更内容>
    ### ./apps/web/src/xxx.tsx
    ```tsx
    <変更後の./src/xxx.tsx>
    ```
    ___
    ## ./apps/web/src/yyy.tsx
    ### 変更内容
    新規作成
    ### ./apps/web/src/yyy.tsx
    ```tsx
    <変更後の./apps/web/src/yyy.tsx>
    ```
    ___
    ## ./apps/web/src/zzz.css
    ### 変更内容
    <変更内容>
    ### ./apps/web/src/zzz.css
    ```css
    <変更後の./apps/web/src/zzz.css>
    ```
    ___
    ## ./apps/web/src/fff.tsx
    ### 変更内容
    <削除理由>
    ### ./apps/web/src/fff.tsx
    ```tsx
    <削除する場合は内容が空のファイルを出力すること>
    ```
    ___
    ## ./docs/specification.md
    ### 変更内容
    <変更理由>
    ### ./docs/specification.md
    ```md
    <変更後のdocs。markdown形式でコードブロックを使用する場合は必ずインデントすること>
    ```
    ___
    ```

# 要求仕様書
{_input}

# 現在のライブラリ管理ファイル・Dockerfile・docker-compose.yml
{fetch_libraryfiles_and_contents(_libraryFileList)}

# 現在のソースコード
{fetch_files_and_contents(_src_root_path_List, _ignorelist)}

    """
    return _content