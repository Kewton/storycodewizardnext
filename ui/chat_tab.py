"""
StoryCodeWizard Chat Tab
チャット機能のUIコンポーネント
"""
import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox
import threading
from ui.styles import AppStyles
from ui.widgets.chat_message import ChatMessage
from ui.widgets.file_uploader import FileUploader
from app.myjsondb.myStreamlit import getValueByFormnameAndKeyName
from app.myjsondb.myProjectSettings import getAllProject
from app.chat import communicate_core, save_chat_history

class ChatTab:
    """チャット機能タブのUIコンポーネント"""
    
    def __init__(self, parent):
        self.parent = parent
        self.current_messages = []
        self.current_file_data = ""
        
        # レイアウト設定
        self.parent.grid_columnconfigure(0, weight=2)
        self.parent.grid_columnconfigure(1, weight=3)
        self.parent.grid_rowconfigure(0, weight=1)
        
        self.setup_ui()
        self.load_initial_data()
    
    def setup_ui(self):
        """UIコンポーネントをセットアップ"""
        # 左側パネル（設定・入力）
        self.setup_left_panel()
        
        # 右側パネル（チャット表示）
        self.setup_right_panel()
    
    def setup_left_panel(self):
        """左側パネルをセットアップ"""
        left_frame = ctk.CTkFrame(
            self.parent,
            **AppStyles.get_frame_style('default')
        )
        left_frame.grid(
            row=0, 
            column=0, 
            padx=(0, AppStyles.SIZES['padding_medium']),
            pady=0,
            sticky="nsew"
        )
        left_frame.grid_columnconfigure(0, weight=1)
        
        # タイトル
        title_label = ctk.CTkLabel(
            left_frame,
            text="Chat Configuration",
            font=AppStyles.FONTS['heading']
        )
        title_label.grid(
            row=0, 
            column=0, 
            padx=AppStyles.SIZES['padding_medium'],
            pady=(AppStyles.SIZES['padding_medium'], AppStyles.SIZES['padding_small']),
            sticky="w"
        )
        
        # プロジェクト選択
        self.setup_project_selection(left_frame, 1)
        
        # モデル選択
        self.setup_model_selection(left_frame, 2)
        
        # 言語選択
        self.setup_language_selection(left_frame, 3)
        
        # ファイルアップロード
        self.setup_file_upload(left_frame, 4)
        
        # 入力テキストエリア
        self.setup_input_area(left_frame, 5)
        
        # 実行ボタン
        self.setup_execute_button(left_frame, 6)
    
    def setup_project_selection(self, parent, row):
        """プロジェクト選択UIをセットアップ"""
        label = ctk.CTkLabel(parent, text="Project:", font=AppStyles.FONTS['default'])
        label.grid(row=row, column=0, padx=AppStyles.SIZES['padding_medium'], pady=(AppStyles.SIZES['padding_small'], 2), sticky="w")
        
        self.project_var = ctk.StringVar()
        self.project_combo = ctk.CTkComboBox(
            parent,
            variable=self.project_var,
            **AppStyles.get_entry_style()
        )
        self.project_combo.grid(
            row=row+1, 
            column=0, 
            padx=AppStyles.SIZES['padding_medium'],
            pady=(2, AppStyles.SIZES['padding_small']),
            sticky="ew"
        )
    
    def setup_model_selection(self, parent, row):
        """モデル選択UIをセットアップ"""
        label = ctk.CTkLabel(parent, text="GPT Model:", font=AppStyles.FONTS['default'])
        label.grid(row=row, column=0, padx=AppStyles.SIZES['padding_medium'], pady=(AppStyles.SIZES['padding_small'], 2), sticky="w")
        
        self.model_var = ctk.StringVar()
        self.model_combo = ctk.CTkComboBox(
            parent,
            variable=self.model_var,
            **AppStyles.get_entry_style()
        )
        self.model_combo.grid(
            row=row+1, 
            column=0, 
            padx=AppStyles.SIZES['padding_medium'],
            pady=(2, AppStyles.SIZES['padding_small']),
            sticky="ew"
        )
    
    def setup_language_selection(self, parent, row):
        """プログラミング言語選択UIをセットアップ"""
        label = ctk.CTkLabel(parent, text="Programming Language:", font=AppStyles.FONTS['default'])
        label.grid(row=row, column=0, padx=AppStyles.SIZES['padding_medium'], pady=(AppStyles.SIZES['padding_small'], 2), sticky="w")
        
        self.language_var = ctk.StringVar()
        self.language_combo = ctk.CTkComboBox(
            parent,
            variable=self.language_var,
            **AppStyles.get_entry_style()
        )
        self.language_combo.grid(
            row=row+1, 
            column=0, 
            padx=AppStyles.SIZES['padding_medium'],
            pady=(2, AppStyles.SIZES['padding_small']),
            sticky="ew"
        )
    
    def setup_file_upload(self, parent, row):
        """ファイルアップロードUIをセットアップ"""
        label = ctk.CTkLabel(parent, text="File Upload (JPEG):", font=AppStyles.FONTS['default'])
        label.grid(row=row, column=0, padx=AppStyles.SIZES['padding_medium'], pady=(AppStyles.SIZES['padding_small'], 2), sticky="w")
        
        self.file_uploader = FileUploader(parent, self.on_file_selected)
        self.file_uploader.grid(
            row=row+1, 
            column=0, 
            padx=AppStyles.SIZES['padding_medium'],
            pady=(2, AppStyles.SIZES['padding_small']),
            sticky="ew"
        )
    
    def setup_input_area(self, parent, row):
        """入力テキストエリアをセットアップ"""
        label = ctk.CTkLabel(parent, text="要求を入力してください:", font=AppStyles.FONTS['default'])
        label.grid(row=row, column=0, padx=AppStyles.SIZES['padding_medium'], pady=(AppStyles.SIZES['padding_small'], 2), sticky="w")
        
        self.input_text = ctk.CTkTextbox(
            parent,
            height=200,
            font=AppStyles.FONTS['default'],
            corner_radius=AppStyles.SIZES['corner_radius']
        )
        self.input_text.grid(
            row=row+1, 
            column=0, 
            padx=AppStyles.SIZES['padding_medium'],
            pady=(2, AppStyles.SIZES['padding_small']),
            sticky="ew"
        )
    
    def setup_execute_button(self, parent, row):
        """実行ボタンをセットアップ"""
        self.execute_button = ctk.CTkButton(
            parent,
            text="実行",
            command=self.execute_chat,
            **AppStyles.get_button_style('primary')
        )
        self.execute_button.grid(
            row=row, 
            column=0, 
            padx=AppStyles.SIZES['padding_medium'],
            pady=AppStyles.SIZES['padding_medium'],
            sticky="ew"
        )
    
    def setup_right_panel(self):
        """右側パネル（チャット表示）をセットアップ"""
        right_frame = ctk.CTkFrame(
            self.parent,
            **AppStyles.get_frame_style('default')
        )
        right_frame.grid(
            row=0, 
            column=1, 
            padx=0,
            pady=0,
            sticky="nsew"
        )
        right_frame.grid_columnconfigure(0, weight=1)
        right_frame.grid_rowconfigure(1, weight=1)
        
        # タイトル
        title_label = ctk.CTkLabel(
            right_frame,
            text="Chat Messages",
            font=AppStyles.FONTS['heading']
        )
        title_label.grid(
            row=0, 
            column=0, 
            padx=AppStyles.SIZES['padding_medium'],
            pady=(AppStyles.SIZES['padding_medium'], AppStyles.SIZES['padding_small']),
            sticky="w"
        )
        
        # チャットメッセージ表示エリア
        self.chat_scrollable = ctk.CTkScrollableFrame(
            right_frame,
            **AppStyles.get_scrollable_frame_style()
        )
        self.chat_scrollable.grid(
            row=1, 
            column=0, 
            padx=AppStyles.SIZES['padding_medium'],
            pady=(0, AppStyles.SIZES['padding_medium']),
            sticky="nsew"
        )
        self.chat_scrollable.grid_columnconfigure(0, weight=1)
    
    def load_initial_data(self):
        """初期データを読み込み"""
        # プロジェクト一覧を読み込み
        projects = getAllProject()
        if projects and projects != [""]:
            self.project_combo.configure(values=projects)
            if projects:
                self.project_var.set(projects[0])
        
        # モデル一覧を読み込み
        models = getValueByFormnameAndKeyName("chat", "gpt", "gpt_model")
        if models:
            self.model_combo.configure(values=models)
            if models:
                self.model_var.set(models[0])
        
        # プログラミング言語一覧を読み込み
        languages = getValueByFormnameAndKeyName("chat", "systemrole", "プログラミング言語")
        if languages:
            self.language_combo.configure(values=languages)
            if languages:
                self.language_var.set(languages[0])
    
    def on_file_selected(self, file_path, file_data):
        """ファイル選択時のコールバック"""
        self.current_file_data = file_data
        print(f"File selected: {file_path}")
    
    def execute_chat(self):
        """チャット実行"""
        # 入力値検証
        user_input = self.input_text.get("1.0", "end-1c").strip()
        if not user_input:
            messagebox.showwarning("Warning", "要求を入力してください。")
            return
        
        if not self.project_var.get():
            messagebox.showwarning("Warning", "プロジェクトを選択してください。")
            return
        
        # ボタンを無効化
        self.execute_button.configure(state="disabled", text="処理中...")
        
        # 非同期でチャット処理を実行
        thread = threading.Thread(target=self._execute_chat_async)
        thread.daemon = True
        thread.start()
    
    def _execute_chat_async(self):
        """非同期チャット処理"""
        try:
            # チャット履歴をクリア
            self.clear_chat_display()
            
            # ユーザー入力を取得
            user_input = self.input_text.get("1.0", "end-1c").strip()
            
            # チャット処理実行
            messages = communicate_core(
                self.project_var.get(),
                self.model_var.get(),
                self.language_var.get(),
                user_input,
                self.current_file_data
            )
            
            # UI更新（メインスレッドで実行）
            self.parent.after(0, lambda: self._update_chat_display(messages))
            
            # 履歴保存
            save_chat_history(
                self.model_var.get(),
                user_input,
                messages,
                self.project_var.get()
            )
            
            # 入力欄をクリア
            self.parent.after(0, lambda: self.input_text.delete("1.0", "end"))
            
        except Exception as e:
            error_msg = f"チャット実行中にエラーが発生しました: {str(e)}"
            print(error_msg)
            self.parent.after(0, lambda: messagebox.showerror("Error", error_msg))
        finally:
            # ボタンを有効化
            self.parent.after(0, lambda: self.execute_button.configure(state="normal", text="実行"))
    
    def clear_chat_display(self):
        """チャット表示をクリア"""
        for widget in self.chat_scrollable.winfo_children():
            widget.destroy()
    
    def _update_chat_display(self, messages):
        """チャット表示を更新"""
        self.current_messages = messages
        
        for i, message in enumerate(messages[1:], 1):  # システムメッセージをスキップ
            speaker = "You" if message["role"] == "user" else "Agent"
            chat_msg = ChatMessage(
                self.chat_scrollable,
                speaker=speaker,
                content=message["content"],
                is_user=(message["role"] == "user")
            )
            chat_msg.grid(
                row=i-1, 
                column=0, 
                padx=AppStyles.SIZES['padding_small'],
                pady=AppStyles.SIZES['padding_small'],
                sticky="ew"
            )