"""
StoryCodeWizard Chat Tab
コード作成をリクエスト機能のUIコンポーネント（ストリーミング対応）
"""
import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox
import threading
from ui.styles import AppStyles
from ui.widgets.chat_message import ChatMessage
from ui.widgets.streaming_chat_message import StreamingChatMessage
from ui.widgets.file_uploader import FileUploader
from app.myjsondb.myStreamlit import getValueByFormnameAndKeyName
from app.myjsondb.myProjectSettings import getAllProject, getValueByPjnm
from app.chat import communicate_core_streaming, save_chat_history

class ChatTab(ctk.CTkFrame):
    """コード作成をリクエスト機能タブのUIコンポーネント"""
    
    def __init__(self, parent, main_window=None):
        super().__init__(parent)
        self.main_window = main_window
        self.current_messages = []
        self.current_file_data = ""
        self.current_streaming_message = None
        self.is_streaming = False
        
        # レイアウト設定
        self.grid_columnconfigure(0, weight=2)
        self.grid_columnconfigure(1, weight=3)
        self.grid_rowconfigure(0, weight=1)
        
        self.setup_ui()
        self.load_initial_data()
    
    def setup_ui(self):
        """UIコンポーネントをセットアップ"""
        # 左側パネル（設定・入力） - スクロール可能に変更
        self.setup_left_panel()
        
        # 右側パネル（コード表示）
        self.setup_right_panel()
    
    def setup_left_panel(self):
        """左側パネルをセットアップ（スクロール可能）"""
        # スクロール可能フレーム
        self.left_scrollable = ctk.CTkScrollableFrame(
            self,
            **AppStyles.get_scrollable_frame_style()
        )
        self.left_scrollable.grid(
            row=0, 
            column=0, 
            padx=(0, AppStyles.SIZES['padding_medium']),
            pady=0,
            sticky="nsew"
        )
        self.left_scrollable.grid_columnconfigure(0, weight=1)
        
        # タイトル
        title_label = ctk.CTkLabel(
            self.left_scrollable,
            text="コード作成設定",
            font=AppStyles.FONTS['heading']
        )
        title_label.grid(
            row=0, 
            column=0, 
            padx=AppStyles.SIZES['padding_medium'],
            pady=(AppStyles.SIZES['padding_medium'], AppStyles.SIZES['padding_large']),
            sticky="w"
        )
        
        # 設定項目を縦に配置（間隔を調整）
        current_row = 1
        
        # プロジェクト選択
        current_row = self.setup_project_selection(self.left_scrollable, current_row)
        
        # モデル選択
        current_row = self.setup_model_selection(self.left_scrollable, current_row)
        
        # コーディングエージェント選択
        current_row = self.setup_coding_agent_selection(self.left_scrollable, current_row)
        
        # ファイルアップロード
        current_row = self.setup_file_upload(self.left_scrollable, current_row)
        
        # 入力テキストエリア
        current_row = self.setup_input_area(self.left_scrollable, current_row)
        
        # 実行ボタン
        self.setup_execute_button(self.left_scrollable, current_row)
    
    def setup_project_selection(self, parent, start_row):
        """プロジェクト選択UIをセットアップ"""
        label = ctk.CTkLabel(parent, text="Project:", font=AppStyles.FONTS['default'])
        label.grid(
            row=start_row, 
            column=0, 
            padx=AppStyles.SIZES['padding_medium'], 
            pady=(AppStyles.SIZES['padding_small'], 4), 
            sticky="w"
        )
        
        self.project_var = ctk.StringVar()
        self.project_combo = ctk.CTkComboBox(
            parent,
            variable=self.project_var,
            command=self.on_project_changed,
            **AppStyles.get_entry_style()
        )
        self.project_combo.grid(
            row=start_row + 1, 
            column=0, 
            padx=AppStyles.SIZES['padding_medium'],
            pady=(4, AppStyles.SIZES['padding_small']),
            sticky="ew"
        )
        
        return start_row + 2
    
    def setup_model_selection(self, parent, start_row):
        """モデル選択UIをセットアップ"""
        label = ctk.CTkLabel(parent, text="LLM Model:", font=AppStyles.FONTS['default'])
        label.grid(
            row=start_row, 
            column=0, 
            padx=AppStyles.SIZES['padding_medium'], 
            pady=(AppStyles.SIZES['padding_small'], 4), 
            sticky="w"
        )
        
        self.model_var = ctk.StringVar()
        self.model_combo = ctk.CTkComboBox(
            parent,
            variable=self.model_var,
            **AppStyles.get_entry_style()
        )
        self.model_combo.grid(
            row=start_row + 1, 
            column=0, 
            padx=AppStyles.SIZES['padding_medium'],
            pady=(4, AppStyles.SIZES['padding_small']),
            sticky="ew"
        )
        
        return start_row + 2
    
    def setup_coding_agent_selection(self, parent, start_row):
        """コーディングエージェント選択UIをセットアップ"""
        label = ctk.CTkLabel(parent, text="コーディングエージェント:", font=AppStyles.FONTS['default'])
        label.grid(
            row=start_row, 
            column=0, 
            padx=AppStyles.SIZES['padding_medium'], 
            pady=(AppStyles.SIZES['padding_small'], 4), 
            sticky="w"
        )
        
        self.language_var = ctk.StringVar()
        self.language_combo = ctk.CTkComboBox(
            parent,
            variable=self.language_var,
            **AppStyles.get_entry_style()
        )
        self.language_combo.grid(
            row=start_row + 1, 
            column=0, 
            padx=AppStyles.SIZES['padding_medium'],
            pady=(4, AppStyles.SIZES['padding_small']),
            sticky="ew"
        )
        
        return start_row + 2
    
    def setup_file_upload(self, parent, start_row):
        """ファイルアップロードUIをセットアップ"""
        label = ctk.CTkLabel(parent, text="File Upload (JPEG):", font=AppStyles.FONTS['default'])
        label.grid(
            row=start_row, 
            column=0, 
            padx=AppStyles.SIZES['padding_medium'], 
            pady=(AppStyles.SIZES['padding_small'], 4), 
            sticky="w"
        )
        
        self.file_uploader = FileUploader(parent, self.on_file_selected)
        self.file_uploader.grid(
            row=start_row + 1, 
            column=0, 
            padx=AppStyles.SIZES['padding_medium'],
            pady=(4, AppStyles.SIZES['padding_small']),
            sticky="ew"
        )
        
        return start_row + 2
    
    def setup_input_area(self, parent, start_row):
        """入力テキストエリアをセットアップ"""
        label = ctk.CTkLabel(parent, text="要求を入力してください:", font=AppStyles.FONTS['default'])
        label.grid(
            row=start_row, 
            column=0, 
            padx=AppStyles.SIZES['padding_medium'], 
            pady=(AppStyles.SIZES['padding_small'], 4), 
            sticky="w"
        )
        
        self.input_text = ctk.CTkTextbox(
            parent,
            height=150,  # 高さを少し縮小
            font=AppStyles.FONTS['default'],
            corner_radius=AppStyles.SIZES['corner_radius']
        )
        self.input_text.grid(
            row=start_row + 1, 
            column=0, 
            padx=AppStyles.SIZES['padding_medium'],
            pady=(4, AppStyles.SIZES['padding_small']),
            sticky="ew"
        )
        
        return start_row + 2
    
    def setup_execute_button(self, parent, start_row):
        """実行ボタンをセットアップ"""
        self.execute_button = ctk.CTkButton(
            parent,
            text="コード生成をリクエスト",
            command=self.execute_chat,
            height=AppStyles.SIZES['button_height'],
            **AppStyles.get_button_style('primary')
        )
        self.execute_button.grid(
            row=start_row, 
            column=0, 
            padx=AppStyles.SIZES['padding_medium'],
            pady=(AppStyles.SIZES['padding_small'], AppStyles.SIZES['padding_large']),
            sticky="ew"
        )
    
    def setup_right_panel(self):
        """右側パネル（コード表示）をセットアップ"""
        right_frame = ctk.CTkFrame(
            self,
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
            text="生成されたコード",
            font=AppStyles.FONTS['heading']
        )
        title_label.grid(
            row=0, 
            column=0, 
            padx=AppStyles.SIZES['padding_medium'],
            pady=(AppStyles.SIZES['padding_medium'], AppStyles.SIZES['padding_small']),
            sticky="w"
        )
        
        # コードメッセージ表示エリア
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
        self.refresh_data()
    
    def refresh_data(self):
        """データを更新"""
        # プロジェクト一覧を読み込み
        projects = getAllProject()
        if projects and projects != [""]:
            current_project = self.project_var.get()
            self.project_combo.configure(values=projects)
            if current_project in projects:
                self.project_var.set(current_project)
            elif projects:
                self.project_var.set(projects[0])
        
        # モデル一覧を読み込み
        models = getValueByFormnameAndKeyName("chat", "gpt", "gpt_model")
        if models:
            current_model = self.model_var.get()
            self.model_combo.configure(values=models)
            if current_model in models:
                self.model_var.set(current_model)
            elif models:
                self.model_var.set(models[0])
        
        # コーディングエージェント一覧を読み込み
        languages = getValueByFormnameAndKeyName("chat", "systemrole", "プログラミング言語")
        if languages:
            current_language = self.language_var.get()
            self.language_combo.configure(values=languages)
            if current_language in languages:
                self.language_var.set(current_language)
            elif languages:
                self.language_var.set(languages[0])
        
        # 初期プロジェクトが設定されている場合、コーディングエージェントを自動設定
        if self.project_var.get():
            self.auto_set_coding_agent()
    
    def on_project_changed(self, value):
        """プロジェクト変更時のハンドラ - コーディングエージェントを自動設定"""
        self.auto_set_coding_agent()
    
    def auto_set_coding_agent(self):
        """プロジェクトのコーディングエージェントを自動設定"""
        project_name = self.project_var.get()
        if not project_name:
            return
        
        # プロジェクトの設定からコーディングエージェントを取得
        project_data = getValueByPjnm(project_name)
        if project_data and 'programming_type' in project_data:
            programming_type = project_data['programming_type']
            
            # コーディングエージェントが有効な選択肢に含まれているかチェック
            available_languages = getValueByFormnameAndKeyName("chat", "systemrole", "プログラミング言語")
            if available_languages and programming_type in available_languages:
                self.language_var.set(programming_type)
    
    def on_file_selected(self, file_path, file_data):
        """ファイル選択時のコールバック"""
        self.current_file_data = file_data
        print(f"File selected: {file_path}")
    
    def execute_chat(self):
        """コード作成実行"""
        # 既にストリーミング中の場合は処理しない
        if self.is_streaming:
            messagebox.showwarning("Warning", "現在処理中です。しばらくお待ちください。")
            return
        
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
        self.is_streaming = True
        
        # コード履歴をクリア
        self.clear_chat_display()
        
        # ユーザーメッセージを表示
        user_msg = StreamingChatMessage(
            self.chat_scrollable,
            speaker="You",
            is_user=True
        )
        user_msg.set_content(user_input)
        user_msg.grid(
            row=0, 
            column=0, 
            padx=AppStyles.SIZES['padding_small'],
            pady=AppStyles.SIZES['padding_small'],
            sticky="ew"
        )
        
        # エージェントメッセージ（ストリーミング用）を準備
        self.current_streaming_message = StreamingChatMessage(
            self.chat_scrollable,
            speaker="Coding Agent",
            is_user=False
        )
        self.current_streaming_message.grid(
            row=1, 
            column=0, 
            padx=AppStyles.SIZES['padding_small'],
            pady=AppStyles.SIZES['padding_small'],
            sticky="ew"
        )
        
        # 非同期でコード作成処理を実行
        thread = threading.Thread(target=self._execute_chat_async)
        thread.daemon = True
        thread.start()
    
    def _execute_chat_async(self):
        """非同期コード作成処理"""
        try:
            # ユーザー入力を取得
            user_input = self.input_text.get("1.0", "end-1c").strip()
            
            # ストリーミングコード作成処理実行
            messages = communicate_core_streaming(
                self.project_var.get(),
                self.model_var.get(),
                self.language_var.get(),
                user_input,
                self.current_file_data,
                self._on_streaming_chunk
            )
            
            # ストリーミング完了
            self.after(0, lambda: self.current_streaming_message.finish_streaming())
            
            # 履歴保存
            save_chat_history(
                self.model_var.get(),
                user_input,
                messages,
                self.project_var.get()
            )
            
            # 入力欄をクリア
            self.after(0, lambda: self.input_text.delete("1.0", "end"))
            
            # 全タブのデータを更新
            if self.main_window:
                self.after(0, self.main_window.refresh_all_content)
            
        except Exception as e:
            error_msg = f"コード作成実行中にエラーが発生しました: {str(e)}"
            print(error_msg)
            self.after(0, lambda: messagebox.showerror("Error", error_msg))
        finally:
            # ボタンを有効化
            self.is_streaming = False
            self.after(0, lambda: self.execute_button.configure(state="normal", text="実行"))
    
    def _on_streaming_chunk(self, chunk):
        """ストリーミングチャンク受信時のコールバック"""
        if self.current_streaming_message:
            self.after(0, lambda: self.current_streaming_message.update_content(chunk))
    
    def clear_chat_display(self):
        """コード表示をクリア"""
        for widget in self.chat_scrollable.winfo_children():
            widget.destroy()
        self.current_streaming_message = None