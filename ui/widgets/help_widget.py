"""
Help Widget
ユーザーガイド表示用カスタムウィジェット
"""
import customtkinter as ctk
import tkinter as tk
from ui.styles import AppStyles

class HelpWidget(ctk.CTkFrame):
    """ヘルプ・ユーザーガイド表示ウィジェット"""
    
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        
        # レイアウト設定
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=3)
        self.grid_rowconfigure(0, weight=1)
        
        self.setup_ui()
    
    def setup_ui(self):
        """UIコンポーネントをセットアップ"""
        # 左側パネル（ナビゲーション）
        self.setup_navigation_panel()
        
        # 右側パネル（コンテンツ表示）
        self.setup_content_panel()
        
        # デフォルトで「はじめに」を表示
        self.show_getting_started()
    
    def setup_navigation_panel(self):
        """左側ナビゲーションパネルをセットアップ"""
        nav_frame = ctk.CTkFrame(
            self,
            **AppStyles.get_frame_style('default')
        )
        nav_frame.grid(
            row=0, 
            column=0, 
            padx=(0, AppStyles.SIZES['padding_medium']),
            pady=0,
            sticky="nsew"
        )
        nav_frame.grid_columnconfigure(0, weight=1)
        
        # タイトル
        title_label = ctk.CTkLabel(
            nav_frame,
            text="ヘルプ・ガイド",
            font=AppStyles.FONTS['heading']
        )
        title_label.grid(
            row=0, 
            column=0, 
            padx=AppStyles.SIZES['padding_medium'],
            pady=(AppStyles.SIZES['padding_medium'], AppStyles.SIZES['padding_large']),
            sticky="w"
        )
        
        # ナビゲーションボタン
        nav_items = [
            ("🚀 はじめに", self.show_getting_started),
            ("💬 コード生成リクエスト", self.show_chat_help),
            ("📁 プロジェクト管理", self.show_project_help),
            ("📚 コーディングエージェントとの会話履歴", self.show_history_help),
            ("🎨 UI操作ガイド", self.show_ui_help),
            ("❓ よくある質問", self.show_faq),
            ("📖 ドキュメント", self.show_documentation)
        ]
        
        self.nav_buttons = {}
        for i, (text, command) in enumerate(nav_items):
            button = ctk.CTkButton(
                nav_frame,
                text=text,
                command=command,
                anchor="w",
                **AppStyles.get_button_style('outline')
            )
            button.grid(
                row=i + 1,
                column=0,
                padx=AppStyles.SIZES['padding_medium'],
                pady=AppStyles.SIZES['padding_small'],
                sticky="ew"
            )
            self.nav_buttons[text] = button
    
    def setup_content_panel(self):
        """右側コンテンツパネルをセットアップ"""
        content_frame = ctk.CTkFrame(
            self,
            **AppStyles.get_frame_style('default')
        )
        content_frame.grid(
            row=0, 
            column=1, 
            padx=0,
            pady=0,
            sticky="nsew"
        )
        content_frame.grid_columnconfigure(0, weight=1)
        content_frame.grid_rowconfigure(1, weight=1)
        
        # コンテンツタイトル
        self.content_title = ctk.CTkLabel(
            content_frame,
            text="はじめに",
            font=AppStyles.FONTS['heading']
        )
        self.content_title.grid(
            row=0, 
            column=0, 
            padx=AppStyles.SIZES['padding_medium'],
            pady=(AppStyles.SIZES['padding_medium'], AppStyles.SIZES['padding_small']),
            sticky="w"
        )
        
        # スクロール可能なコンテンツエリア
        self.content_scrollable = ctk.CTkScrollableFrame(
            content_frame,
            **AppStyles.get_scrollable_frame_style()
        )
        self.content_scrollable.grid(
            row=1, 
            column=0, 
            padx=AppStyles.SIZES['padding_medium'],
            pady=(0, AppStyles.SIZES['padding_medium']),
            sticky="nsew"
        )
        self.content_scrollable.grid_columnconfigure(0, weight=1)
    
    def clear_content(self):
        """コンテンツエリアをクリア"""
        for widget in self.content_scrollable.winfo_children():
            widget.destroy()
    
    def set_active_nav(self, button_text):
        """アクティブなナビゲーションボタンを設定"""
        for text, button in self.nav_buttons.items():
            if text == button_text:
                button.configure(**AppStyles.get_button_style('primary'))
            else:
                button.configure(**AppStyles.get_button_style('outline'))
    
    def add_section(self, title, content, row):
        """セクションを追加"""
        # セクションタイトル
        section_title = ctk.CTkLabel(
            self.content_scrollable,
            text=title,
            font=AppStyles.FONTS['subheading'],
            text_color=AppStyles.COLORS['primary']
        )
        section_title.grid(
            row=row, 
            column=0, 
            padx=AppStyles.SIZES['padding_small'],
            pady=(AppStyles.SIZES['padding_medium'], AppStyles.SIZES['padding_small']),
            sticky="w"
        )
        
        # セクション内容
        section_content = ctk.CTkLabel(
            self.content_scrollable,
            text=content,
            font=AppStyles.FONTS['default'],
            wraplength=600,
            justify="left",
            anchor="w"
        )
        section_content.grid(
            row=row + 1, 
            column=0, 
            padx=AppStyles.SIZES['padding_small'],
            pady=(0, AppStyles.SIZES['padding_medium']),
            sticky="ew"
        )
    
    def show_getting_started(self):
        """はじめにページを表示"""
        self.content_title.configure(text="🚀 はじめに")
        self.set_active_nav("🚀 はじめに")
        self.clear_content()
        
        welcome_text = """StoryCodeWizardへようこそ！

このアプリケーションは、LLM（大規模言語モデル）を活用して、
あなたのアイデアを実際のコードに変換する強力なツールです。

初めての方でも簡単に使い始められるよう、
基本的な使い方をご案内します。"""
        
        self.add_section("StoryCodeWizardとは", welcome_text, 0)
        
        steps_text = """1. 左側のサイドバーから機能を選択
2. プロジェクトを作成（📁 プロジェクト管理）
3. コード生成リクエスト機能でコード生成を実施（💬 コード生成リクエスト）
4. 生成されたコードを確認しプロジェクトへの反映を実施（💬 コード生成リクエスト）
5. 履歴から過去の結果を参照（📚 コーディングエージェントとの会話履歴）"""
        
        self.add_section("基本的な使い方", steps_text, 2)
        
        features_text = """• 複数のLLMモデル対応（GPT、Claude、Gemini）
• リアルタイムストリーミング応答
• Markdown形式での美しい表示
• プロジェクトごとの履歴管理
• ファイルアップロード対応（JPEG画像とPNG画像）
• コード生成結果の自動プロジェクト反映"""
        
        self.add_section("主な機能", features_text, 4)
    
    def show_chat_help(self):
        """コード生成リクエスト機能ヘルプを表示"""
        self.content_title.configure(text="💬 コード生成リクエスト")
        self.set_active_nav("💬 コード生成リクエスト")
        self.clear_content()
        
        overview_text = """コード生成リクエスト機能では、コーディングエージェントにコード生成を依頼できます。
左側の設定パネルでプロジェクトやモデルを選択し、
右側でリアルタイムに応答を確認できます。
コーディングエージェントからの応答が完了するとプロジェクトへの反映が可能になります。
"""
        
        self.add_section("機能概要", overview_text, 0)
        
        config_text = """• プロジェクト: 作業対象のプロジェクトを選択
• LLMモデル: 使用するAIモデルを選択
• コーディングエージェント: プロジェクトの開発言語/フレームワーク
• ファイルアップロード: JPEG画像とPNG画像を添付可能
• 要求入力: 生成したいコードの要求を記述
• プロジェクトに範囲: 生成したコードをプロジェクトに反映するオプション"""
        
        self.add_section("設定項目", config_text, 2)
        
        tips_text = """• 具体的で明確な要求を記述する
• プロジェクトを事前に作成しておく
• コーディングエージェントはプロジェクト作成時に自動設定される
• ストリーミング中は他の操作を控える
• Markdown表示でコードを見やすく確認"""
        
        self.add_section("使用のコツ", tips_text, 4)
    
    def show_project_help(self):
        """プロジェクト管理ヘルプを表示"""
        self.content_title.configure(text="📁 プロジェクト管理")
        self.set_active_nav("📁 プロジェクト管理")
        self.clear_content()
        
        overview_text = """プロジェクト管理では、開発プロジェクトの作成・編集・削除を行います。
各プロジェクトにはディレクトリパス、コーディングエージェント、
説明などの情報を設定できます。"""
        
        self.add_section("機能概要", overview_text, 0)
        
        create_text = """1. 左側パネルの入力フォームに情報を入力
2. プロジェクト名: 識別用の一意な名前
3. ディレクトリパス: ソースコードの保存場所
4. コーディングエージェント: 開発言語/フレームワーク
5. プロジェクト説明: プロジェクトの詳細説明"""
        
        self.add_section("プロジェクト作成", create_text, 2)
        
        management_text = """• 編集: プロジェクトカードの「編集」ボタン
• 削除: プロジェクトカードの「削除」ボタン
• 一覧表示: 右側パネルで全プロジェクトを確認
• 自動更新: 変更後は自動的に一覧が更新"""
        
        self.add_section("プロジェクト管理", management_text, 4)
    
    def show_history_help(self):
        """コーディングエージェントとの会話履歴ヘルプを表示"""
        self.content_title.configure(text="📚 コーディングエージェントとの会話履歴")
        self.set_active_nav("📚 コーディングエージェントとの会話履歴")
        self.clear_content()
        
        overview_text = """コーディングエージェントとの会話履歴では、過去のコード作成履歴を確認・管理できます。
プロジェクトごとに整理された履歴から、
必要な情報を簡単に見つけることができます。"""
        
        self.add_section("機能概要", overview_text, 0)
        
        view_text = """• 左側: プロジェクト選択と履歴一覧
• 右側: 選択した履歴の詳細表示
• 実行時刻とモデル名で履歴を識別
• 4セクション形式: システムロール内容、入力、ユーザーコンテキスト、エージェントコンテキスト
• Markdown形式で美しく表示"""
        
        self.add_section("履歴表示", view_text, 2)
        
        actions_text = """• 削除: 不要な履歴を削除
• ダウンロード: Your Context/Agent Contextを保存
• プロジェクト反映: 生成されたコードをプロジェクトに適用
• 詳細表示: 会話内容の4セクション表示"""
        
        self.add_section("利用可能な操作", actions_text, 4)
    
    def show_ui_help(self):
        """UI操作ガイドを表示"""
        self.content_title.configure(text="🎨 UI操作ガイド")
        self.set_active_nav("🎨 UI操作ガイド")
        self.clear_content()
        
        overview_text = """StoryCodeWizardはモダンなUIを採用しています。
直感的な操作で各機能にアクセスできるよう設計されています。"""
        
        self.add_section("UI概要", overview_text, 0)
        
        sidebar_text = """• 💬 コード生成リクエスト: LLMとの対話によるコード生成
• 📚 コーディングエージェントとの会話履歴: 履歴管理
• 📁 プロジェクト管理: プロジェクト管理
• ❓ ヘルプ: このガイド
• アクティブ状態: 選択中の機能がハイライト表示"""
        
        self.add_section("アクティビティーサイドバー", sidebar_text, 2)
        
        tips_text = """• ツールチップ: アイコンにマウスオーバーで詳細表示
• レスポンシブデザイン: ウィンドウサイズに応じて調整
• ダークテーマ: 目に優しい配色
• キーボードショートカット: 効率的な操作"""
        
        self.add_section("UI操作のコツ", tips_text, 4)
    
    def show_faq(self):
        """よくある質問を表示"""
        self.content_title.configure(text="❓ よくある質問")
        self.set_active_nav("❓ よくある質問")
        self.clear_content()
        
        setup_text = """Q: アプリケーションが起動しない
A: Python 3.8以上がインストールされているか確認してください。

Q: APIキーエラーが表示される
A: secret_keys.pyファイルに正しいAPIキーを設定してください。

Q: データベースエラーが発生する
A: python initdatabase.py を実行してデータベースを初期化してください。"""
        
        self.add_section("セットアップ関連", setup_text, 0)
        
        usage_text = """Q: プロジェクトが作成できない
A: ディレクトリパスが正しく、アクセス権限があることを確認してください。

Q: コード作成の応答が表示されない
A: インターネット接続とAPIキーの設定を確認してください。

Q: ファイルアップロードができない
A: JPEG形式とPNG形式のファイルのみサポートしています。"""
        
        self.add_section("使用方法関連", usage_text, 2)
        
        performance_text = """Q: アプリケーションが重い
A: プロジェクト数を整理し、不要な履歴を削除してください。

Q: ストリーミングが止まる
A: ネットワーク接続を確認し、アプリケーションを再起動してください。"""
        
        self.add_section("パフォーマンス関連", performance_text, 4)
    
    def show_documentation(self):
        """ドキュメントページを表示"""
        self.content_title.configure(text="📖 ドキュメント")
        self.set_active_nav("📖 ドキュメント")
        self.clear_content()
        
        overview_text = """StoryCodeWizardの詳細なドキュメントは、
mkdocsを使用して生成・管理されています。
より詳しい情報が必要な場合は、以下をご参照ください。"""
        
        self.add_section("ドキュメント概要", overview_text, 0)
        
        docs_text = """• インストールガイド: セットアップ手順
• ユーザーガイド: 各機能の詳細説明
• アーキテクチャ: システム構成の詳細
• API リファレンス: 開発者向け情報
• 開発ガイド: カスタマイズ・拡張方法"""
        
        self.add_section("利用可能なドキュメント", docs_text, 2)
        
        access_text = """ドキュメントサーバーを起動するには:

1. ターミナルでプロジェクトディレクトリに移動
2. 以下のコマンドを実行:
   mkdocs serve
3. ブラウザで http://localhost:8000 にアクセス

詳細な技術情報や開発者向けの情報は、
Webドキュメントをご確認ください。"""
        
        self.add_section("ドキュメントへのアクセス", access_text, 4)