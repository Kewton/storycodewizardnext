from app.util.codeopen import fetch_libraryfiles_and_contents, fetch_files_and_contents


def nextjstemplate1(_prerequisites, _input, _libraryFileList, _src_root_path_List, _ignorelist):
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
- 要求文書を適切な表現にブラッシュアップすること
- アウトプットはmarkdown形式とし、出力フォーマットに従うこと
- 変更が発生するファイルは全て出力すること
- 変更が発生しないファイルは出力しないこと
- README.mdには変更を加えないこと
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
- 削除するファイルがある場合は、削除するファイル名と理由を明確にし、内容が空のファイルを出力すること
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
    <変更後のREADME.md ・・・README.md内のコードブロックはインデントすること。>
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
    ## ./src/fff.tsx
    ### 変更内容
    <削除理由>
    ### ./src/fff.tsx
    ```css
    <削除する場合は内容が空のファイルを出力すること>
    ```
    ---
    ```

# 要求仕様書
{_input}

# 現在の管理ファイル
{fetch_libraryfiles_and_contents(_libraryFileList)}

# 現在のソースコード
{fetch_files_and_contents(_src_root_path_List, _ignorelist)}

    """
    return _content