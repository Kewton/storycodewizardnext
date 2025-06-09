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
## ./frontend/vitest.config.ts
### ./frontend/vitest.config.ts
```ts
import { defineConfig } from 'vitest/config';
import react from '@vitejs/plugin-react';
import path from 'path';

export default defineConfig({
  plugins: [react()],
  test: {
    // Node.js環境でブラウザAPIをシミュレートする
    environment: 'jsdom',
    // 各テストファイルの実行前にグローバルな設定を読み込む
    setupFiles: './vitest.setup.ts',
    // CSS Modulesを正しく扱えるようにする設定
    css: true, 
  },
  // src/を@/でインポートするエイリアス設定（任意ですが推奨）
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src'),
    },
  },
});
```

---
## ./frontend/vitest.setup.ts
### ./frontend/vitest.setup.ts
```ts
import '@testing-library/jest-dom';
```

---
## ./frontend/package.json
### ./frontend/package.json
```json
{
  "name": "frontend",
  "version": "0.1.0",
  "private": true,
  "scripts": {
    "dev": "next dev",
    "build": "next build",
    "start": "next start",
    "lint": "next lint",
    "test": "vitest",
    "test:watch": "vitest --watch"
  },
  "dependencies": {
    "lucide-react": "^0.513.0",
    "next": "15.3.3",
    "react": "^19.0.0",
    "react-dom": "^19.0.0"
  },
  "devDependencies": {
    "@eslint/eslintrc": "^3",
    "@tailwindcss/postcss": "^4.1.8",
    "@testing-library/jest-dom": "^6.6.3",
    "@testing-library/react": "^16.3.0",
    "@types/node": "^20",
    "@types/react": "^19",
    "@types/react-dom": "^19",
    "@vitejs/plugin-react": "^4.5.1",
    "eslint": "^9",
    "eslint-config-next": "15.3.3",
    "jsdom": "^26.1.0",
    "tailwindcss": "^4.1.8",
    "typescript": "^5",
    "vitest": "^3.2.2"
  }
}
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
# テストの実行方法
    ```
    # すべてのテストを実行する
    pytest

    # 詳細な情報を表示して実行する
    pytest -v

    # テストカバレッジを計測する
    pip install pytest-cov
    pytest --cov=myapi -v
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