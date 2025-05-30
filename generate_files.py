"""

# input.md からファイルを生成するスクリプト
```bash
python generate_files.py [input.mdのパス] -d [出力ディレクトリ名]

python generate_files.py ./temp/chat_history_claude-sonnet-4-20250514_2025-05-23_23_43_34_agent.md -d ./temp
```
# input.md がカレントディレクトリにあり、出力先をデフォルトの generated_files にする場合は、単に以下のように実行します。
```bash
python generate_files.py
```
"""
import os
import re
import argparse

def parse_input_md_sections(md_content):
    """
    input.md の内容を解析し、ファイル情報を抽出します。

    Args:
        md_content (str): input.md ファイルの内容。

    Returns:
        list: 各要素が以下のキーを持つ辞書のリスト:
              'filepath': str, 作成/更新するファイルのパス。
              'content': str, ファイルの内容。
              'change_description': str, 変更内容の説明（オプション）。
    """
    files_to_create = []
    # --- が行頭に来る場合も考慮し、改行を含めてスプリット
    sections = re.split(r'\n---\n', md_content)

    for section_content in sections:
        section_content = section_content.strip()
        if not section_content:
            continue

        # セクションの主要なファイルパスを検索 (例: ## ./README.md)
        filepath_match = re.search(r"^## \./(.+?)$", section_content, re.MULTILINE)
        if not filepath_match:
            # このセクションは期待される形式のファイル定義ではない
            continue

        current_filepath = filepath_match.group(1).strip()

        # 変更内容を検索 (オプション) (例: ### 変更内容)
        change_desc = ""
        # 変更内容は ### 変更内容 から始まり、次の ### ./filepath か ``` の前まで
        change_desc_match = re.search(
            r"### 変更内容\n(.*?)(?=\n### \./|\n```|$)",
            section_content,
            re.DOTALL
        )
        if change_desc_match:
            change_desc = change_desc_match.group(1).strip()

        # コンテンツブロックを検索
        # コンテンツブロックは ### ./<filepath_check> の後に ```...``` で囲まれる
        # filepath_check が current_filepath と一致することを確認
        # re.escape を使用して current_filepath 内の特殊文字をエスケープ
        content_block_regex = re.compile(
            r"### \./" + re.escape(current_filepath) +
            r"\s*```(?:[a-zA-Z0-9_.-]+)?\n(.*?)\n```",
            re.DOTALL | re.MULTILINE
        )
        content_match = content_block_regex.search(section_content)

        if content_match:
            content = content_match.group(1)  # キャプチャされたコンテンツ
            files_to_create.append({
                "filepath": current_filepath,
                "content": content,
                "change_description": change_desc
            })
        # else:
            # print(f"警告: ファイル '{current_filepath}' のコンテンツブロックが見つからないか、形式が不正です。")

    return files_to_create

def create_files_from_parsed_data(parsed_data, base_dir="."):
    """
    解析されたデータに基づいてファイルとディレクトリを作成します。

    Args:
        parsed_data (list): parse_input_md_sections からのファイル情報辞書のリスト。
        base_dir (str): ファイルが作成されるベースディレクトリ。
    """
    if not parsed_data:
        print("作成するファイルがありません。")
        return

    for file_info in parsed_data:
        relative_filepath = file_info['filepath']
        # os.path.join は "./" で始まるパスを正しく処理する
        filepath = os.path.join(base_dir, relative_filepath)
        content = file_info['content']

        # 必要に応じてディレクトリを作成
        dir_name = os.path.dirname(filepath)
        if dir_name:  # dir_nameが空でないことを確認 (base_dirのルートにあるファイルの場合)
            os.makedirs(dir_name, exist_ok=True)

        try:
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(content)
            print(f"ファイルを作成/更新しました: {filepath}")
            if file_info.get("change_description"):
                 print(f"  '{file_info['filepath']}' の変更内容: {file_info['change_description']}")
        except IOError as e:
            print(f"ファイル '{filepath}' の書き込み中にエラーが発生しました: {e}")

def main():
    """
    メイン関数。input.md を読み込み、解析し、ファイルを作成します。
    """
    parser = argparse.ArgumentParser(description="input.md からファイルを生成します。")
    parser.add_argument(
        "input_file",
        nargs="?",
        default="input.md",
        help="入力マークダウンファイルへのパス (デフォルト: input.md)"
    )
    parser.add_argument(
        "-d", "--directory",
        default="generated_files",
        help="ファイルの出力先ディレクトリ (デフォルト: generated_files)"
    )
    args = parser.parse_args()

    input_md_path = args.input_file
    output_directory = args.directory

    try:
        with open(input_md_path, "r", encoding="utf-8") as f:
            md_content = f.read()
    except FileNotFoundError:
        print(f"エラー: 入力ファイル '{input_md_path}' が見つかりません。")
        return
    except IOError as e:
        print(f"エラー: ファイル '{input_md_path}' の読み込み中にエラーが発生しました: {e}")
        return

    # 出力ディレクトリが存在しない場合は作成
    if not os.path.exists(output_directory):
        os.makedirs(output_directory, exist_ok=True)
        print(f"出力ディレクトリを作成しました: {output_directory}")
    else:
        print(f"出力ディレクトリ '{output_directory}' は既に存在します。ファイルはここに作成/上書きされます。")

    parsed_files = parse_input_md_sections(md_content)

    if not parsed_files:
        print(f"'{input_md_path}' からファイル情報が正常に解析されませんでした。")
        return

    create_files_from_parsed_data(parsed_files, base_dir=output_directory)
    print("\nファイル作成プロセスが完了しました。")


if __name__ == "__main__":
    main()
