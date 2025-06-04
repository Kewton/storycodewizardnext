from app.myjsondb.myStreamlit import upsertValueByFormnameAndKeyName


def initdata():
    upsertValueByFormnameAndKeyName(
        "chat",
        "gpt",
        {
            "gpt_model": [
                "claude-sonnet-4-20250514",
                "gemini-2.5-pro-preview-05-06",
                "gemini-2.5-flash-preview-05-20",
                "gpt-4.1",
                "gpt-4.1-mini",
                "o4-mini",
                "o3"
            ]
        }
    )

    upsertValueByFormnameAndKeyName(
        "chat",
        "systemrole",
        {
            "プログラミング言語": ["Next.js_Agent", "FastAPI_Agent", "NextJS_FastAPI_Agent", "CustomTkinter_Agent"],
            "Next.js_Agent": {
                "srcdire": ["src"],
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
            "FastAPI_Agent": {
                "srcdire": [""],
                "libraryFileList": [
                    "requirements.txt"
                ],
                "prerequisites": "/ ディレクトリにてFastAPIのバックエンドアプリケーションを開発しています。利用者に最高のユーザー体験を提供します。",
                "system_role": "あなたは優秀なFastAPIのバックエンドエンジニアです。入力された情報を元に最高のコードをアウトプットします。",
                "ignorelist": [
                    "__pycache__/",
                    ".venv/",
                    "venv/",
                    "*.db",
                    "*.DS_Store",
                    "*.log",
                    ".git/"
                ],
                "prompt": "fastAPItemplate"
            },
            "CustomTkinter_Agent": {
                "srcdire": [""],
                "libraryFileList": [
                    "requirements.txt"
                ],
                "prerequisites": "/ ディレクトリにてCustomTkinterのクライアントアプリケーションを開発しています。利用者に最高のユーザー体験を提供します。",
                "system_role": "あなたは優秀なPythonのCustomTkinterエンジニアです。入力された情報を元に最高のコードをアウトプットします。",
                "ignorelist": [
                    ".git/",
                    "__pycache__/",
                    ".github/",
                    ".venv/",
                    "venv/",
                    "docs/",
                    "init/",
                    "mydb/",
                    "temp/",
                    "secret_keys.py",
                    "*.db",
                    "*.DS_Store",
                    "*.log"
                ],
                "prompt": "CustomTkinter"
            },
            "NextJS_FastAPI_Agent": {
                "srcdire": ["/backend", "/frontend/src"],
                "libraryFileList": [
                    "backend/Dockerfile",
                    "frontend/Dockerfile",
                    "docker-compose.yml",
                    "backend/requirements.txt",
                    "frontend/eslint.config.mjs",
                    "frontend/next-env.d.ts",
                    "frontend/next.config.ts",
                    "frontend/postcss.config.mjs",
                    "frontend/package.json",
                    "frontend/tsconfig.json"
                ],
                "prerequisites": "/ ディレクトリにてNext.JSでフロントエンドを、FastAPIでバックエンドを開発しています。利用者に最高のユーザー体験を提供します。",
                "system_role": "あなたは優秀なフルスタックエンジニアです。入力された情報を元に最高のコードをアウトプットします。",
                "ignorelist": [
                    ".git/",
                    "__pycache__/",
                    ".github/",
                    ".venv/",
                    "venv/",
                    "docs/",
                    ".env",
                    "*.db",
                    "*.DS_Store",
                    "*.log",
                    "*.ico",
                ],
                "prompt": "nextjsFastApiTemplate"
            }
        }
    )


if __name__ == '__main__':
    initdata()
