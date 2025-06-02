"""
StoryCodeWizard History Tab
コーディングエージェントとの会話履歴管理のUIコンポーネント
"""
import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox, filedialog
from ui.styles import AppStyles
from ui.widgets.chat_message import ChatMessage
from app.myjsondb.myProjectSettings import getAllProject, getValueByPjnm
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
        left_frame.grid_rowconfigure(4, weight=1) # history_list のrowを1つ下げるので、weightをかけるrowも変更
        
        # タイトル（履歴件数表示対応）
        self.title_label = ctk.CTkLabel(
            left_frame,
            text="コーディングエージェントとの会話履歴",
            font=AppStyles.FONTS['heading']
        )
        self.title_label.grid(
            row=0, 
            column=0, 
            padx=AppStyles.SIZES['padding_medium'],
            pady=(AppStyles.SIZES['padding_medium'], AppStyles.SIZES['padding_large']),
            sticky="w"
        )
        
        # プロジェクト選択
        self.setup_project_selection(left_frame, 1)
        
        # 履歴リスト
        self.setup_history_list(left_frame, 4) # プロジェクト説明ラベルを追加したので1行下げる
    
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

        # プロジェクト説明表示ラベル
        self.project_description_label = ctk.CTkLabel(
            parent,
            text="プロジェクトを選択してください。",
            font=AppStyles.FONTS['small'],
            text_color=AppStyles.COLORS['text_secondary'],
            wraplength=380, # 左パネルの幅に応じて調整
            justify="left"
        )
        self.project_description_label.grid(
            row=start_row + 2,
            column=0,
            padx=AppStyles.SIZES['padding_medium'],
            pady=(AppStyles.SIZES['padding_small'], AppStyles.SIZES['padding_medium']),
            sticky="w"
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
        current_project_before_refresh = self.project_var.get() # 更新前のプロジェクトを保持

        if projects and projects != [""]:
            self.project_combo.configure(values=projects)
            if current_project_before_refresh in projects:
                self.project_var.set(current_project_before_refresh)
                self.load_history_data() # 既存プロジェクト選択時は履歴もロード
            elif projects:
                self.project_var.set(projects[0])
                self.load_history_data() # 新規プロジェクト選択時は履歴もロード
            # プロジェクト変更イベントを手動でトリガーして説明を更新
            self.on_project_changed(self.project_var.get())
        else:
            self.project_combo.configure(values=[])
            self.project_var.set("")
            self.project_description_label.configure(text="プロジェクトがありません。")
            self.current_history_data = [] # プロジェクトがない場合は履歴もクリア
            self.update_history_list()
            self.clear_detail_display()
            self.update_title_with_count(0)  # 履歴件数を0で更新
    
    def on_project_changed(self, project_name):
        """プロジェクト変更時のハンドラ"""
        if project_name:
            project_data = getValueByPjnm(project_name)
            if project_data and 'description' in project_data:
                description = project_data['description']
                self.project_description_label.configure(text=f"説明: {description if description else '説明がありません。'}")
            else:
                self.project_description_label.configure(text="説明: プロジェクト情報が見つかりません。")
            
            self.load_history_data()
        else:
            self.project_description_label.configure(text="プロジェクトを選択してください。")
            self.current_history_data = []
            self.update_history_list()
            self.clear_detail_display()
            self.update_title_with_count(0)  # 履歴件数を0で更新
    
    def load_history_data(self):
        """履歴データを読み込み"""
        project_name = self.project_var.get()
        if not project_name:
            self.project_description_label.configure(text="プロジェクトを選択してください。")
            self.current_history_data = []
            self.update_history_list()
            self.clear_detail_display()
            self.update_title_with_count(0)  # 履歴件数を0で更新
            return

        # プロジェクト説明の表示（プロジェクト名が有効な場合のみ）
        project_data = getValueByPjnm(project_name)
        if project_data and 'description' in project_data:
            description = project_data['description']
            self.project_description_label.configure(text=f"説明: {description if description else '説明がありません。'}")
        else:
            self.project_description_label.configure(text="説明: プロジェクト情報が見つかりません。")
        
        # 履歴データ取得
        self.current_history_data = format_history_data(project_name)
        self.update_history_list()
        
        # タイトルに履歴件数を表示
        self.update_title_with_count(len(self.current_history_data))
        
        # 最初の項目を選択
        if self.current_history_data:
            self.history_listbox.selection_set(0)
            self.selected_index = 0
            self.load_detail_display()
        else:
            self.clear_detail_display()
    
    def update_title_with_count(self, count):
        """タイトルに履歴件数を表示"""
        title_text = f"コーディングエージェントとの会話履歴 ({count}件)"
        self.title_label.configure(text=title_text)
    
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
        
        # ①System Role Content - 高さを1/5に縮小（従来の400→80）
        if messages and len(messages) > 0 and messages[0]["role"] == "system":
            system_content = messages[0]["content"]
            section_header = ctk.CTkLabel(
                self.detail_scrollable,
                text="① Coding Agent Role",
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
                speaker="Coding Agent",
                content=system_content,
                is_user=True,
                max_height=80  # 従来の400の1/5
            )
            system_msg.grid(
                row=current_row, 
                column=0, 
                padx=AppStyles.SIZES['padding_small'],
                pady=(0, AppStyles.SIZES['padding_medium']),
                sticky="ew"
            )
            current_row += 1
        
        # ②Input - 高さを1/2に縮小（従来の200→100）
        if input_text:
            section_header = ctk.CTkLabel(
                self.detail_scrollable,
                text="② Your Request",
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
                speaker="You",
                content=input_text,
                is_user=True,
                max_height=200
            )
            input_msg.grid(
                row=current_row, 
                column=0, 
                padx=AppStyles.SIZES['padding_small'],
                pady=(0, AppStyles.SIZES['padding_medium']),
                sticky="ew"
            )
            current_row += 1
        
        # ③Your Context & ④Agent Context - 高さ制限なし（従来通り）
        for i, message in enumerate(messages[1:], 1):  # システムメッセージをスキップ
            if message["role"] == "user":
                section_label = "③ Your Context"
                speaker = "You"
                max_height = 600  # 高さ制限なし
                default_markdown_view = True  # ユーザーコンテキストはMarkdownデフォルト
            elif message["role"] == "assistant":
                section_label = "④ Agent Context"
                speaker = "Coding Agent"
                max_height = 600  # 高さ制限なし
                default_markdown_view = False  # エージェントコンテキストはRaw Textデフォルト
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
                is_user=(message["role"] == "user"),
                max_height=max_height,
                default_markdown_view=default_markdown_view
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
        
        # 確認ダイアログを表示
        item = self.current_history_data[self.selected_index]
        confirmation_message = (
            "選択した履歴のコードをプロジェクトに反映しますか？\n\n"
            f"対象プロジェクト: {self.project_var.get()}\n"
            f"生成モデル: {item['gptmodel']}\n"
            f"実行時刻: {item['registration_date']}\n\n"
            "この操作により、プロジェクト内のファイルが変更される可能性があります。\n"
            "続行しますか？"
        )
        
        result = messagebox.askyesno(
            "プロジェクト反映の確認",
            confirmation_message
        )
        
        if not result:
            return  # ユーザーがキャンセルした場合は処理を中止
        
        # 元の日時フォーマット（YYYYMMDDHHMMSS）に変換
        # registration_dateは既にYYYY-MM-DD_HH:MM:SS形式のため、数字のみ抽出
        timestamp = item['registration_date'].replace('-', '').replace('_', '').replace(':', '')
        
        success, message = apply_to_project(
            content,
            self.project_var.get(),
            item['gptmodel'],
            timestamp
        )
        
        if success:
            messagebox.showinfo("Success", message)
        else:
            messagebox.showerror("Error", message)