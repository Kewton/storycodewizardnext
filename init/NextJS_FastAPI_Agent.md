## ./frontend/Dockerfile
### ./frontend/Dockerfile
```txt
FROM node:23.11.0-alpine

WORKDIR /app

COPY . .

RUN npm install
RUN npm run build

CMD ["npm", "start"]
```

---
## ./backend/README.md
### ./backend/README.md
```txt
# Python環境のセットアップ
    ```bash
    python3 -m venv .venv
    source .venv/bin/activate  # Windowsの場合: .venv\Scripts\activate
    pip install -r requirements.txt
    ```
# ./.gitignore
    ```txt
    __pycache__/
    .venv/
    ```
```

---
## ./backend/.gitignore
### ./backend/.gitignore
```txt
__pycache__/
.venv/
```

---
## ./backend/requirements.txt
### ./backend/requirements.txt
```txt
git+https://github.com/Kewton/jsonDB
customtkinter>=5.2.0
pillow>=9.0.0
openai
anthropic
PathSpec
google-genai
google-generativeai
beautifulsoup4
```