"""
StoryCodeWizard History Tab
コーディングエージェントとの会話履歴管理のUIコンポーネント
"""
import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox, filedialog
from ui.styles import AppStyles
from ui.widgets.chat_message import ChatMessage
from app.myjsondb.myProjectSettings import getAllProject
from app.chat import (
    format_history_data, 
    get_user_content_from_messages, 
    get_assistant_content_from_messages,
    delete_history_item,
    apply_to_project
)
from app.myjsondb.myHistories import getValOfPjByKey

class HistoryTab(ctk.CTkFrame):
    """コーディングエージェントとの会話履歴管理タブのUIコンポーネント"""
    
    def __init__(self, parent, main_window=None):
        super().__init__(parent)
        self.main_window = main_window
        self.current_history_data = []
        self.selected_index = 0
        self.current_messages = []
        
        # レイアウト設定
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=2)
        self.grid_rowconfigure(0, weight=1)
        
        self.setup_ui()
        self.load_initial_data()
    
    def setup_ui(self):
        """UIコンポーネントをセットアップ"""
        # 左側パネル（履歴一覧）
        self.setup_left_panel()
        
        # 右側パネル（詳細表示）
        self.setup_right_panel()
    
    def setup_left_panel(self):
        """左側パネル（履歴一覧）をセットアップ"""
        left_frame = ctk.CTkFrame(
            self,
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
        left_frame.grid_rowconfigure(3, weight=1)
        
        # タイトル
        title_label = ctk.CTkLabel(
            left_frame,
            text="コーディングエージェントとの会話履歴",
            font=AppStyles.FONTS['heading']
        )
        title_label.grid(
            row=0, 
            column=0, 
            padx=AppStyles.SIZES['padding_medium'],
            pady=(AppStyles.SIZES['padding_medium'], AppStyles.SIZES['padding_large']),
            sticky="w"
        )
        
        # プロジェクト選択
        self.setup_project_selection(left_frame, 1)
        
        # 履歴リスト
        self.setup_history_list(left_frame, 3)
    
    def setup_project_selection(self, parent, start_row):
        """プロジェクト選択UIをセットアップ"""
        label = ctk.CTkLabel(parent, text="Project:", font=AppStyles.FONTS['default'])
        label.grid(
            row=start_row, 
            column=0, 
            padx=AppStyles.SIZES['padding_medium'], 
            pady=(AppStyles.SIZES['padding_medium'], 4), 
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
            pady=(4, AppStyles.SIZES['padding_large']),
            sticky="ew"
        )
    
    def setup_history_list(self, parent, row):
        """履歴リストをセットアップ"""
        # リストボックスとスクロールバーのフレーム
        list_frame = ctk.CTkFrame(parent, fg_color="transparent")
        list_frame.grid(
            row=row, 
            column=0, 
            padx=AppStyles.SIZES['padding_medium'],
            pady=(0, AppStyles.SIZES['padding_medium']),
            sticky="nsew"
        )
        list_frame.grid_columnconfigure(0, weight=1)
        list_frame.grid_rowconfigure(0, weight=1)
        
        # 履歴リストボックス - フォントサイズを大きく設定
        history_font = ('Helvetica', 14)  # フォントサイズを大きく
        self.history_listbox = tk.Listbox(
            list_frame,
            font=history_font,
            bg=AppStyles.COLORS['surface'],
            fg=AppStyles.COLORS['text'],
            selectbackground=AppStyles.COLORS['primary'],
            selectforeground=AppStyles.COLORS['text'],
            borderwidth=0,
            highlightthickness=0
        )
        self.history_listbox.grid(row=0, column=0, sticky="nsew")
        self.history_listbox.bind('<<ListboxSelect>>', self.on_history_select)
        
        # スクロールバー
        scrollbar = ctk.CTkScrollbar(list_frame, command=self.history_listbox.yview)
        scrollbar.grid(row=0, column=1, sticky="ns")
        self.history_listbox.configure(yscrollcommand=scrollbar.set)
    
    def setup_right_panel(self):
        """右側パネル（詳細表示）をセットアップ"""
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
        right_frame.grid_rowconfigure(2, weight=1)
        
        # タイトル
        title_label = ctk.CTkLabel(
            right_frame,
            text="会話詳細",
            font=AppStyles.FONTS['heading']
        )
        title_label.grid(
            row=0, 
            column=0, 
            padx=AppStyles.SIZES['padding_medium'],
            pady=(AppStyles.SIZES['padding_medium'], AppStyles.SIZES['padding_small']),
            sticky="w"
        )
        
        # アクションボタン
        self.setup_action_buttons(right_frame, 1)
        
        # 会話詳細表示
        self.setup_chat_detail(right_frame, 2)
    
    def setup_action_buttons(self, parent, row):
        """アクションボタンをセットアップ"""
        button_frame = ctk.CTkFrame(parent, fg_color="transparent")
        button_frame.grid(
            row=row, 
            column=0, 
            padx=AppStyles.SIZES['padding_medium'],
            pady=(0, AppStyles.SIZES['padding_medium']),
            sticky="ew"
        )
        button_frame.grid_columnconfigure((0, 1, 2, 3), weight=1)
        
        # 削除ボタン
        style = AppStyles.get_button_style('outline').copy()
        style.pop('text_color', None)
        style.pop('hover_color', None)
        style['text_color'] = AppStyles.COLORS['error']
        style['hover_color'] = AppStyles.COLORS['error']
        style['height'] = AppStyles.SIZES['button_height']
        self.delete_button = ctk.CTkButton(
            button_frame,
            text="Delete History",
            command=self.delete_history,
            **style
        )
        self.delete_button.grid(row=0, column=0, padx=(0, 5), sticky="ew")
        
        # ユーザーコンテキストダウンロード
        button_style = AppStyles.get_button_style('secondary').copy()
        button_style['height'] = AppStyles.SIZES['button_height']
        self.download_user_button = ctk.CTkButton(
            button_frame,
            text="Download Your Context",
            command=self.download_user_context,
            **button_style
        )
        self.download_user_button.grid(row=0, column=1, padx=5, sticky="ew")
        
        # エージェントコンテキストダウンロード
        self.download_agent_button = ctk.CTkButton(
            button_frame,
            text="Download Agent Context",
            command=self.download_agent_context,
            **button_style
        )
        self.download_agent_button.grid(row=0, column=2, padx=5, sticky="ew")
        
        # プロジェクトに反映ボタン
        primary_style = AppStyles.get_button_style('primary').copy()
        primary_style['height'] = AppStyles.SIZES['button_height']
        self.apply_button = ctk.CTkButton(
            button_frame,
            text="プロジェクトに反映",
            command=self.apply_to_project,
            **primary_style
        )
        self.apply_button.grid(row=0, column=3, padx=(5, 0), sticky="ew")
    
    def setup_chat_detail(self, parent, row):
        """会話詳細表示をセットアップ"""
        self.detail_scrollable = ctk.CTkScrollableFrame(
            parent,
            **AppStyles.get_scrollable_frame_style()
        )
        self.detail_scrollable.grid(
            row=row, 
            column=0, 
            padx=AppStyles.SIZES['padding_medium'],
            pady=(0, AppStyles.SIZES['padding_medium']),
            sticky="nsew"
        )
        self.detail_scrollable.grid_columnconfigure(0, weight=1)
    
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
                self.load_history_data()
            elif projects:
                self.project_var.set(projects[0])
                self.load_history_data()
    
    def on_project_changed(self, value):
        """プロジェクト変更時のハンドラ"""
        self.load_history_data()
    
    def load_history_data(self):
        """履歴データを読み込み"""
        if not self.project_var.get():
            return
        
        # 履歴データ取得
        self.current_history_data = format_history_data(self.project_var.get())
        self.update_history_list()
        
        # 最初の項目を選択
        if self.current_history_data:
            self.history_listbox.selection_set(0)
            self.selected_index = 0
            self.load_detail_display()
        else:
            self.clear_detail_display()
    
    def update_history_list(self):
        """履歴リストを更新（実行時刻とモデル名のみ表示）"""
        self.history_listbox.delete(0, tk.END)
        
        for i, item in enumerate(self.current_history_data):
            # 実行時刻とモデル名のみを表示
            display_text = f"{item['registration_date']} | {item['gptmodel']}"
            self.history_listbox.insert(tk.END, display_text)
    
    def on_history_select(self, event):
        """履歴選択時のハンドラ"""
        selection = self.history_listbox.curselection()
        if selection:
            self.selected_index = selection[0]
            self.load_detail_display()
    
    def load_detail_display(self):
        """詳細表示を読み込み"""
        if not self.current_history_data or self.selected_index >= len(self.current_history_data):
            return
        
        item = self.current_history_data[self.selected_index]
        
        # メッセージ取得
        self.current_messages = getValOfPjByKey(
            item['gptmodel'],
            item['input'],
            self.project_var.get()
        )
        
        if not self.current_messages:
            self.clear_detail_display()
            return
        
        # 詳細表示更新（4セクション形式）
        self.update_detail_display_enhanced(self.current_messages, input_text=item['input'])
    
    def update_detail_display_enhanced(self, messages, input_text=None):
        """詳細表示を更新（4セクション形式：system role content、input、your context、agent context）"""
        self.clear_detail_display()
        
        current_row = 0
        
        # ①System Role Content
        if messages and len(messages) > 0 and messages[0]["role"] == "system":
            system_content = messages[0]["content"]
            section_header = ctk.CTkLabel(
                self.detail_scrollable,
                text="① System Role Content",
                font=AppStyles.FONTS['subheading'],
                text_color=AppStyles.COLORS['accent']
            )
            section_header.grid(
                row=current_row, 
                column=0, 
                padx=AppStyles.SIZES['padding_small'],
                pady=(AppStyles.SIZES['padding_small'], 4),
                sticky="w"
            )
            current_row += 1
            
            system_msg = ChatMessage(
                self.detail_scrollable,
                speaker="System",
                content=system_content,
                is_user=False
            )
            system_msg.grid(
                row=current_row, 
                column=0, 
                padx=AppStyles.SIZES['padding_small'],
                pady=(0, AppStyles.SIZES['padding_medium']),
                sticky="ew"
            )
            current_row += 1
        
        # ②Input        
        if input_text:
            section_header = ctk.CTkLabel(
                self.detail_scrollable,
                text="② Input",
                font=AppStyles.FONTS['subheading'],
                text_color=AppStyles.COLORS['accent']
            )
            section_header.grid(
                row=current_row, 
                column=0, 
                padx=AppStyles.SIZES['padding_small'],
                pady=(AppStyles.SIZES['padding_small'], 4),
                sticky="w"
            )
            current_row += 1
            
            input_msg = ChatMessage(
                self.detail_scrollable,
                speaker="Input",
                content=input_text,
                is_user=False
            )
            input_msg.grid(
                row=current_row, 
                column=0, 
                padx=AppStyles.SIZES['padding_small'],
                pady=(0, AppStyles.SIZES['padding_medium']),
                sticky="ew"
            )
            current_row += 1
        
        # ③Your Context & ④Agent Context
        for i, message in enumerate(messages[1:], 1):  # システムメッセージをスキップ
            if message["role"] == "user":
                section_label = "③ Your Context"
                speaker = "You"
            elif message["role"] == "assistant":
                section_label = "④ Agent Context"
                speaker = "Coding Agent"
            else:
                continue
            
            section_header = ctk.CTkLabel(
                self.detail_scrollable,
                text=section_label,
                font=AppStyles.FONTS['subheading'],
                text_color=AppStyles.COLORS['accent']
            )
            section_header.grid(
                row=current_row, 
                column=0, 
                padx=AppStyles.SIZES['padding_small'],
                pady=(AppStyles.SIZES['padding_small'], 4),
                sticky="w"
            )
            current_row += 1
            
            chat_msg = ChatMessage(
                self.detail_scrollable,
                speaker=speaker,
                content=message["content"],
                is_user=(message["role"] == "user")
            )
            chat_msg.grid(
                row=current_row, 
                column=0, 
                padx=AppStyles.SIZES['padding_small'],
                pady=(0, AppStyles.SIZES['padding_medium']),
                sticky="ew"
            )
            current_row += 1
    
    def clear_detail_display(self):
        """詳細表示をクリア"""
        for widget in self.detail_scrollable.winfo_children():
            widget.destroy()
    
    def delete_history(self):
        """履歴削除"""
        if not self.current_history_data or self.selected_index >= len(self.current_history_data):
            messagebox.showwarning("Warning", "履歴項目が選択されていません。")
            return
        
        # 確認ダイアログ
        result = messagebox.askyesno(
            "削除確認",
            "この履歴項目を削除しますか？"
        )
        
        if result:
            item = self.current_history_data[self.selected_index]
            success = delete_history_item(
                item['gptmodel'],
                item['input'],
                item['registration_date'],
                self.project_var.get()
            )
            
            if success:
                messagebox.showinfo("Success", "履歴項目を削除しました。")
                self.load_history_data()
                # 全タブのデータを更新
                if self.main_window:
                    self.main_window.refresh_all_content()
            else:
                messagebox.showerror("Error", "履歴項目の削除に失敗しました。")
    
    def download_user_context(self):
        """ユーザーコンテキストをダウンロード"""
        if not self.current_messages:
            messagebox.showwarning("Warning", "ダウンロードするコンテンツがありません。")
            return
        
        content = get_user_content_from_messages(self.current_messages)
        if content:
            self._save_file_dialog(content, "user")
    
    def download_agent_context(self):
        """エージェントコンテキストをダウンロード"""
        if not self.current_messages:
            messagebox.showwarning("Warning", "ダウンロードするコンテンツがありません。")
            return
        
        content = get_assistant_content_from_messages(self.current_messages)
        if content:
            self._save_file_dialog(content, "agent")
    
    def _save_file_dialog(self, content, context_type):
        """ファイル保存ダイアログ"""
        if not content:
            messagebox.showwarning("Warning", "保存するコンテンツがありません。")
            return
        
        item = self.current_history_data[self.selected_index]
        filename = f"chat_history_{item['gptmodel']}_{item['registration_date']}_{context_type}.md"
        
        file_path = filedialog.asksaveasfilename(
            initialfile=filename,
            defaultextension=".md",
            filetypes=[("Markdown files", "*.md"), ("All files", "*.*")]
        )
        
        if file_path:
            try:
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(content)
                messagebox.showinfo("Success", f"ファイルを保存しました: {file_path}")
            except Exception as e:
                messagebox.showerror("Error", f"ファイル保存に失敗しました: {str(e)}")
    
    def apply_to_project(self):
        """プロジェクトに反映"""
        if not self.current_messages:
            messagebox.showwarning("Warning", "反映するコンテンツがありません。")
            return
        
        content = get_assistant_content_from_messages(self.current_messages)
        if not content:
            messagebox.showwarning("Warning", "エージェントのコンテンツがありません。")
            return
        
        item = self.current_history_data[self.selected_index]
        success, message = apply_to_project(
            content,
            self.project_var.get(),
            item['gptmodel'],
            item['registration_date']
        )
        
        if success:
            messagebox.showinfo("Success", message)
        else:
            messagebox.showerror("Error", message)