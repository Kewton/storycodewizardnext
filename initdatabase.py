from app.myjsondb.myStreamlit import upsertValueByFormnameAndKeyName


def initdata():
    upsertValueByFormnameAndKeyName(
        "chat",
        "gpt",
        {
            "gpt_model": [
                "claude-sonnet-4-20250514",
                "gpt-4.1",
                "gpt-4.1-mini",
                "o4-mini",
                "o3",
                "gemini-2.5-flash-preview-05-20",
                "gemini-2.5-pro-preview-05-06"
            ]
        }
    )

    upsertValueByFormnameAndKeyName(
        "chat",
        "systemrole",
        {
            "プログラミング言語": ["Next.js_1", "FastAPI", "Next.js_2", "streamlit2CustomTkinter"],
            "Next.js_1": {
                "srcdire": "src",
                "libraryFileList": [
                    "eslint.config.mjs",
                    "next-env.d.ts",
                    "next.config.ts",
                    "postcss.config.mjs",
                    "package.json",
                    "tsconfig.json"
                ],
                "prerequisites": " ディレクトリにてNext.jsのフロントエンドを開発しています。利用者に最高のチャット体験を提供します。",
                "system_role": "あなたは世界一優秀なNext.jsのフロントエンドエンジニアです。入力された情報を元に最高のコードをアウトプットします。",
                "ignorelist": [
                    "*.ico",
                    ".DS_Store"
                ],
                "prompt": "nextjstemplate1"
            },
            "Next.js_2": {
                "srcdire": "src",
                "libraryFileList": [
                    "eslint.config.mjs",
                    "next-env.d.ts",
                    "next.config.ts",
                    "postcss.config.mjs",
                    "package.json",
                    "tsconfig.json"
                ],
                "prerequisites": "ディレクトリにてNext.jsのフロントエンドを開発しています。利用者に最高のユーザー体験を提供します。",
                "system_role": "あなたは優秀なNext.jsのフロントエンドエンジニアです。入力された情報を元に最高のコードをアウトプットします。",
                "ignorelist": [
                    "public/",
                    ".DS_Store",
                    "*.ico"
                    ""
                ],
                "prompt": "nextjstemplate2"
            },
            "FastAPI": {
                "srcdire": "../test",
                "libraryFileList": [
                    "requirements.txt"
                ],
                "prerequisites": "./docs/requiredSpecifications.md に記載された要求仕様書に従ったFastAPIのバックエンドエンドAPIを開発しています。利用者に最高のユーザー体験を提供します。",
                "system_role": "あなたは優秀なFastAPIのバックエンドエンジニアです。入力された情報を元に最高のコードをアウトプットします。",
                "ignorelist": [
                    "__pycache__/",
                    "venv/",
                    "*.db",
                    "*.DS_Store",
                    "*.log"
                ],
                "prompt": "fastAPItemplate"
            },
            "streamlit2CustomTkinter": {
                "srcdire": "",
                "libraryFileList": [
                    "requirements.txt"
                ],
                "prerequisites": "/ ディレクトリにてStreamlitのフロントエンドを開発しています。利用者に最高のチャット体験を提供します。",
                "system_role": "あなたは優秀なPythonのフロントエンドエンジニアです。入力された情報を元にStreamlitで開発されたフロントエンドアプリケーションをCustomTkinterに変換します。",
                "ignorelist": [
                    "__pycache__/",
                    ".venv/",
                    "venv/",
                    "*.db",
                    "*.DS_Store",
                    "*.log",
                    "__pycache__/",
                    ".venv/",
                    "secret_keys.py",
                    "mydb/",
                    "myproject/",
                    "old/",
                    "escape/",
                    "output.txt",
                    "temp/",
                    ".git/"
                ],
                "prompt": "streamlit2CustomTkinter"
            }
        }
    )


if __name__ == '__main__':
    initdata()
