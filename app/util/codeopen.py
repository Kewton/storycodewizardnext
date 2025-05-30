import os
from pathspec import PathSpec


def escape(_instr):
    return _instr.replace('"', '\\"').replace('`', '\\`')


def fetch_libraryfiles_and_contents(_file_list):
    # ファイルを開き、内容を読み込む
    all_files = []
    outstr = ""
    print(_file_list)
    for file_path in _file_list:
        try:
            # 拡張子を取得
            print(file_path)
            _, file_extension = os.path.splitext(file_path)
            file_extension = file_extension.lstrip('.')
            if os.path.exists(file_path):
                with open(file_path, 'r', encoding='utf-8') as file:
                    content = file.read()
                    all_files.append(f" - filename:{file_path}")
                    all_files.append(f"```{file_extension}")
                    all_files.append(content)
                    all_files.append("```")
                    all_files.append("")
        except (UnicodeDecodeError, IOError):
            print(f"Error reading {file_path}. It may not be a text file or might have encoding issues.")
    if len(all_files) > 0:
        outstr = '\n'.join(str(elem) for elem in all_files)
    else:
        outstr = "既存のソースコードは特にありません。新規です。"
    return outstr


def fetch_files_and_contents(directory, ignorelist):
    all_files = []
    outstr = ""

    # PathSpec を初期化
    spec = PathSpec.from_lines('gitwildmatch', ignorelist)

    # os.walk() を使用してディレクトリを再帰的に走査
    for root, dirs, files in os.walk(directory):
        # ディレクトリを除外リストに基づきフィルタリング
        dirs[:] = [d for d in dirs if not spec.match_file(os.path.join(root, d))]
        for filename in files:
            file_path = os.path.join(root, filename)

            # ファイルが ignorelist に該当する場合はスキップ
            if spec.match_file(file_path):
                continue

            # ファイルを開き、内容を読み込む
            try:
                _, file_extension = os.path.splitext(file_path)
                file_extension = file_extension.lstrip('.')
                with open(file_path, 'r', encoding='utf-8') as file:
                    content = file.read()
                    all_files.append(f" - filename:{file_path}")
                    all_files.append(f"```{file_extension}")
                    all_files.append(content)
                    all_files.append("```")
                    all_files.append("")
            except (UnicodeDecodeError, IOError):
                print(f"Error reading {file_path}. It may not be a text file or might have encoding issues.")

    if len(all_files) > 0:
        outstr = '\n'.join(str(elem) for elem in all_files)
    else:
        outstr = "既存のソースコードは特にありません。新規です。"

    return outstr


def fetch_files_and_contents_old(directory, ignorelist):
    all_files = []
    outstr = ""
    # os.walk()を使用してディレクトリを再帰的に走査
    for root, dirs, files in os.walk(directory):
        for filename in files:
            if filename not in ignorelist:
                # ファイルの完全なパスを取得
                file_path = os.path.join(root, filename)

                # ファイルを開き、内容を読み込む
                try:
                    # 拡張子を取得
                    _, file_extension = os.path.splitext(file_path)
                    file_extension = file_extension.lstrip('.')
                    with open(file_path, 'r', encoding='utf-8') as file:
                        content = file.read()
                        all_files.append(f" - filename:{file_path}")
                        all_files.append(f"```{file_extension}")
                        all_files.append(content)
                        all_files.append("```")
                        all_files.append("")
                except (UnicodeDecodeError, IOError):
                    print(f"Error reading {file_path}. It may not be a text file or might have encoding issues.")
    if len(all_files) > 0:
        outstr = '\n'.join(str(elem) for elem in all_files)
    else:
        outstr = "既存のソースコードは特にありません。新規です。"
    return outstr
