# 初期セットアップ指示書
## Step0. git 初期化
```bash
git init
```

## Step1. 基本的なTurborepoプロジェクトを作成する
### 1. プロジェクトを作成
pnpmでインストール
```bash
npx create-turbo@latest .
```

### 2. 依存関係をインストール
```bash
pnpm install
```

## Step2. 不要なアプリケーションを削除する
### `apps/docs` ディレクトリを削除
```bash
rm -rf apps/docs
```

## Step3. NestJSアプリケーションを新規作成する
### 1. `apps` ディレクトリに移動
```bash
cd apps
```

### 2. NestJSのCLIを使って 'api' プロジェクトを作成
```bash
npx @nestjs/cli new api
```

### 3. NestJSが作成したGitリポジトリは不要なので削除
```bash
rm -rf api/.git
```

### 4. ルートディレクトリに戻る
```bash
cd ..
```

## Step4. ESlint 初期設定
### 1. ESLintのセキュリティブラグインをインストールする
```bash
pnpm add -D -w eslint-plugin-security
```
### 2. ./packages/eslint-config/base.js にてeslint-plugin-securityを有効化

## Step5. フロントエンドとバックエンドのIPアドレスの競合の解消 
### ./apps/api/src/main.ts
ポート番号を3001に変更する
```ts
import { NestFactory } from '@nestjs/core';
import { ValidationPipe } from '@nestjs/common';
import { AppModule } from './app.module';

async function bootstrap() {
  const app = await NestFactory.create(AppModule);

  // CORS設定
  app.enableCors({
    origin: ['http://localhost:3000'],
    methods: ['GET', 'POST', 'PUT', 'DELETE'],
    credentials: true,
  });

  // バリデーションパイプの設定
  app.useGlobalPipes(new ValidationPipe());

  await app.listen(process.env.PORT ?? 3001);
}

void bootstrap();
```

## Step5. 各種コマンドを実行可能にする
### ./packages.json
```
{
  "name": "my-monorepo-project",
  "private": true,
  "scripts": {
    "build": "turbo run build",
    "dev": "turbo run dev",
    "lint": "turbo run lint",
    "test": "turbo run test",
    "format": "prettier --write \"**/*.{ts,tsx,md}\"",
    "audit": "pnpm audit --audit-level=high",
    "check-types": "turbo run check-types",
    "check:all": "pnpm format && pnpm lint -- --fix && pnpm check-types && pnpm test && pnpm audit"
  },
  "devDependencies": {
    "eslint-plugin-security": "^3.0.1",
    "prettier": "^3.5.3",
    "turbo": "^2.5.4",
    "typescript": "5.8.2"
  },
  "packageManager": "pnpm@9.0.0",
  "engines": {
    "node": ">=18"
  }
}
```

## Step6. 確認
以下のコマンドが成功するようにしてください。
- `pnpm run dev`: 開発サーバーの起動。webとapiが起動すること
- `pnpm run build`: プロジェクトのビルド
- `pnpm run lint`: リント実行
- `pnpm run test`: テスト実行
- `pnpm run check:all`: 全体チェック（フォーマット、リント、型チェック、テスト、監査）

## Step7. commit
現在の状態をコミットし、v0.0.1としてタグを打ってください