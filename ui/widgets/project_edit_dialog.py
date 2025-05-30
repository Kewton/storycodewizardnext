"""
Project Edit Dialog Widget
プロジェクト編集ダイアログ用カスタムウィジェット
"""
import customtkinter as ctk
import os
from tkinter import filedialog, messagebox
from ui.styles import AppStyles
from app.myjsondb.myProjectSettings import upsertPjdirAndValueByPjnm, getValueByPjnm, getAllProject

class ProjectEditDialog(ctk.CTkToplevel):
    """プロジェクト編集ダイアログウィンドウ"""
    
    def __init__(self, parent, project_name, project_path, project_description, save_callback=None):
        super().__init__(parent)
        
        self.project_name = project_name
        self.original_project_name = project_name  # 元の名前を保持
        self.project_path = project_path
        self.project_description = project_description
        self.save_callback = save_callback
        
        # ウィンドウ設定（可変サイズ対応）
        self.title(f"プロジェクト編集: {project_name}")
        self.geometry("700x500")
        self.minsize(600, 400)  # 最小サイズを設定
        self.resizable(True, True)  # リサイズ可能に変更
        
        # ウィンドウを中央に配置
        self.transient(parent)
        self.center_window()
        
        self.setup_ui()
    
    def center_window(self):
        """ウィンドウを親ウィンドウの中央に配置"""
        self.update_idletasks()
        parent = self.master
        parent_x = parent.winfo_rootx()
        parent_y = parent.winfo_rooty()
        parent_width = parent.winfo_width()
        parent_height = parent.winfo_height()
        
        x = parent_x + (parent_width // 2) - (700 // 2)
        y = parent_y + (parent_height // 2) - (500 // 2)
        
        self.geometry(f"700x500+{x}+{y}")
    
    def setup_ui(self):
        """UIコンポーネントをセットアップ"""
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)  # フォームフレームを拡張可能に
        
        # タイトル
        title_label = ctk.CTkLabel(
            self,
            text="プロジェクト情報を編集",
            font=AppStyles.FONTS['heading']
        )
        title_label.grid(
            row=0,
            column=0,
            padx=AppStyles.SIZES['padding_large'],
            pady=(AppStyles.SIZES['padding_large'], AppStyles.SIZES['padding_medium']),
            sticky="w"
        )
        
        # フォームフレーム（拡張可能）
        form_frame = ctk.CTkFrame(self, **AppStyles.get_frame_style('default'))
        form_frame.grid(
            row=1,
            column=0,
            padx=AppStyles.SIZES['padding_large'],
            pady=(0, AppStyles.SIZES['padding_medium']),
            sticky="nsew"
        )
        form_frame.grid_columnconfigure(0, weight=1)
        form_frame.grid_rowconfigure(5, weight=1)  # 説明欄を拡張可能に
        
        # プロジェクト名表示（編集不可）
        self.setup_project_name_display(form_frame, 0)
        
        # ディレクトリパス入力
        self.setup_directory_input(form_frame, 2)
        
        # プロジェクト説明入力（拡張可能）
        self.setup_description_input(form_frame, 4)
        
        # ボタンフレーム
        self.setup_buttons()
    
    def setup_project_name_display(self, parent, start_row):
        """プロジェクト名表示をセットアップ（編集不可）"""
        label = ctk.CTkLabel(
            parent,
            text="プロジェクト名:",
            font=AppStyles.FONTS['default']
        )
        label.grid(
            row=start_row,
            column=0,
            padx=AppStyles.SIZES['padding_medium'],
            pady=(AppStyles.SIZES['padding_medium'], 4),
            sticky="w"
        )
        
        # 編集不可のラベル表示
        self.name_display = ctk.CTkLabel(
            parent,
            text=self.project_name,
            font=AppStyles.FONTS['default'],
            text_color=AppStyles.COLORS['text_secondary'],
            anchor="w"
        )
        self.name_display.grid(
            row=start_row + 1,
            column=0,
            padx=AppStyles.SIZES['padding_medium'],
            pady=(4, AppStyles.SIZES['padding_medium']),
            sticky="ew"
        )
        
        # 注意メッセージ
        note_label = ctk.CTkLabel(
            parent,
            text="※ プロジェクト名は変更できません",
            font=AppStyles.FONTS['small'],
            text_color=AppStyles.COLORS['warning']
        )
        note_label.grid(
            row=start_row + 1,
            column=0,
            padx=AppStyles.SIZES['padding_medium'],
            pady=(0, AppStyles.SIZES['padding_small']),
            sticky="e"
        )
    
    def setup_directory_input(self, parent, start_row):
        """ディレクトリパス入力をセットアップ"""
        label = ctk.CTkLabel(
            parent,
            text="ディレクトリパス:",
            font=AppStyles.FONTS['default']
        )
        label.grid(
            row=start_row,
            column=0,
            padx=AppStyles.SIZES['padding_medium'],
            pady=(AppStyles.SIZES['padding_medium'], 4),
            sticky="w"
        )
        
        # ディレクトリ入力とボタンのフレーム
        dir_frame = ctk.CTkFrame(parent, fg_color="transparent")
        dir_frame.grid(
            row=start_row + 1,
            column=0,
            padx=AppStyles.SIZES['padding_medium'],
            pady=(4, AppStyles.SIZES['padding_medium']),
            sticky="ew"
        )
        dir_frame.grid_columnconfigure(0, weight=1)
        
        self.path_entry = ctk.CTkEntry(
            dir_frame,
            **AppStyles.get_entry_style()
        )
        self.path_entry.grid(row=0, column=0, padx=(0, 8), sticky="ew")
        self.path_entry.insert(0, self.project_path)
        
        browse_button = ctk.CTkButton(
            dir_frame,
            text="参照",
            command=self.browse_directory,
            width=80,
            height=AppStyles.SIZES['button_height'],
            **AppStyles.get_button_style('outline')
        )
        browse_button.grid(row=0, column=1, sticky="e")
    
    def setup_description_input(self, parent, start_row):
        """プロジェクト説明入力をセットアップ（拡張可能）"""
        label = ctk.CTkLabel(
            parent,
            text="プロジェクト説明:",
            font=AppStyles.FONTS['default']
        )
        label.grid(
            row=start_row,
            column=0,
            padx=AppStyles.SIZES['padding_medium'],
            pady=(AppStyles.SIZES['padding_medium'], 4),
            sticky="w"
        )
        
        self.description_text = ctk.CTkTextbox(
            parent,
            height=150,
            font=AppStyles.FONTS['default'],
            corner_radius=AppStyles.SIZES['corner_radius']
        )
        self.description_text.grid(
            row=start_row + 1,
            column=0,
            padx=AppStyles.SIZES['padding_medium'],
            pady=(4, AppStyles.SIZES['padding_medium']),
            sticky="nsew"  # 縦横に拡張
        )
        self.description_text.insert("1.0", self.project_description)
    
    def setup_buttons(self):
        """ボタンをセットアップ"""
        button_frame = ctk.CTkFrame(self, fg_color="transparent")
        button_frame.grid(
            row=2,
            column=0,
            padx=AppStyles.SIZES['padding_large'],
            pady=(0, AppStyles.SIZES['padding_large']),
            sticky="ew"
        )
        button_frame.grid_columnconfigure((0, 1), weight=1)
        
        # キャンセルボタン
        cancel_button = ctk.CTkButton(
            button_frame,
            text="キャンセル",
            command=self.on_cancel,
            **AppStyles.get_button_style('outline')
        )
        cancel_button.grid(
            row=0,
            column=0,
            padx=(0, 10),
            sticky="ew"
        )
        
        # 保存ボタン
        save_button = ctk.CTkButton(
            button_frame,
            text="保存",
            command=self.on_save,
            **AppStyles.get_button_style('primary')
        )
        save_button.grid(
            row=0,
            column=1,
            padx=(10, 0),
            sticky="ew"
        )
    
    def browse_directory(self):
        """ディレクトリ選択ダイアログ"""
        directory = filedialog.askdirectory(initialdir=self.path_entry.get())
        if directory:
            self.path_entry.delete(0, 'end')
            self.path_entry.insert(0, directory)
    
    def on_cancel(self):
        """キャンセルボタンクリック"""
        self.destroy()
    
    def on_save(self):
        """保存ボタンクリック"""
        # 入力値取得（プロジェクト名は変更不可なので元の名前を使用）
        new_path = self.path_entry.get().strip()
        new_description = self.description_text.get("1.0", "end-1c").strip()
        
        # 入力検証
        if not new_path:
            messagebox.showerror("エラー", "ディレクトリパスを入力してください。")
            return
        
        if not os.path.isdir(new_path):
            messagebox.showerror("エラー", "有効なディレクトリパスを入力してください。")
            return
        
        try:
            # 既存の値データを取得
            existing_value = getValueByPjnm(self.original_project_name)
            if not existing_value:
                existing_value = {}
            
            # 説明を更新
            existing_value['description'] = new_description
            
            # プロジェクト情報を保存（名前は変更されないので同じ名前を使用）
            upsertPjdirAndValueByPjnm(self.original_project_name, new_path, existing_value)
            
            # コールバック実行
            if self.save_callback:
                self.save_callback(self.original_project_name, new_path, new_description)
            
            messagebox.showinfo("成功", "プロジェクト情報を保存しました。")
            self.destroy()
            
        except Exception as e:
            messagebox.showerror("エラー", f"保存中にエラーが発生しました: {str(e)}")