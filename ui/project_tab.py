"""
StoryCodeWizard Project Tab
プロジェクト管理のUIコンポーネント
"""
import customtkinter as ctk
import os
from tkinter import filedialog, messagebox
from ui.styles import AppStyles
from ui.widgets.project_card import ProjectCard
from app.chat import create_new_project, delete_project
from app.myjsondb.myHistories import getProjectList
from app.myjsondb.myProjectSettings import getPjdirByPjnm
from app.myjsondb.myStreamlit import getValueByFormnameAndKeyName

class ProjectTab:
    """プロジェクト管理タブのUIコンポーネント"""
    
    def __init__(self, parent, main_window=None):
        self.parent = parent
        self.main_window = main_window
        
        # レイアウト設定
        self.parent.grid_columnconfigure(0, weight=1)
        self.parent.grid_columnconfigure(1, weight=2)
        self.parent.grid_rowconfigure(0, weight=1)
        
        self.setup_ui()
        self.load_projects()
    
    def setup_ui(self):
        """UIコンポーネントをセットアップ"""
        # 左側パネル（新規作成） - スクロール可能に変更
        self.setup_left_panel()
        
        # 右側パネル（プロジェクト一覧）
        self.setup_right_panel()
    
    def setup_left_panel(self):
        """左側パネル（新規作成）をセットアップ（スクロール可能）"""
        # スクロール可能フレーム
        self.left_scrollable = ctk.CTkScrollableFrame(
            self.parent,
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
            text="新規プロジェクトの作成",
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
        
        # プロジェクト名入力
        current_row = self.setup_project_name_input(self.left_scrollable, current_row)
        
        # ディレクトリ選択
        current_row = self.setup_directory_selection(self.left_scrollable, current_row)
        
        # Programming Type選択
        current_row = self.setup_programming_type_selection(self.left_scrollable, current_row)
        
        # プロジェクト説明入力
        current_row = self.setup_description_input(self.left_scrollable, current_row)
        
        # 作成ボタン
        self.setup_create_button(self.left_scrollable, current_row)
    
    def setup_project_name_input(self, parent, start_row):
        """プロジェクト名入力をセットアップ"""
        label = ctk.CTkLabel(parent, text="プロジェクト名:", font=AppStyles.FONTS['default'])
        label.grid(
            row=start_row, 
            column=0, 
            padx=AppStyles.SIZES['padding_medium'], 
            pady=(AppStyles.SIZES['padding_small'], 4), 
            sticky="w"
        )
        
        self.project_name_entry = ctk.CTkEntry(
            parent,
            placeholder_text="プロジェクト名を入力...",
            **AppStyles.get_entry_style()
        )
        self.project_name_entry.grid(
            row=start_row + 1, 
            column=0, 
            padx=AppStyles.SIZES['padding_medium'],
            pady=(4, AppStyles.SIZES['padding_small']),
            sticky="ew"
        )
        
        return start_row + 2
    
    def setup_directory_selection(self, parent, start_row):
        """ディレクトリ選択をセットアップ"""
        label = ctk.CTkLabel(parent, text="ディレクトリのパス:", font=AppStyles.FONTS['default'])
        label.grid(
            row=start_row, 
            column=0, 
            padx=AppStyles.SIZES['padding_medium'], 
            pady=(AppStyles.SIZES['padding_small'], 4), 
            sticky="w"
        )
        
        # ディレクトリ入力とボタンのフレーム
        dir_frame = ctk.CTkFrame(parent, fg_color="transparent")
        dir_frame.grid(
            row=start_row + 1, 
            column=0, 
            padx=AppStyles.SIZES['padding_medium'],
            pady=(4, AppStyles.SIZES['padding_small']),
            sticky="ew"
        )
        dir_frame.grid_columnconfigure(0, weight=1)
        
        self.directory_entry = ctk.CTkEntry(
            dir_frame,
            placeholder_text="ディレクトリパスを選択...",
            **AppStyles.get_entry_style()
        )
        self.directory_entry.grid(row=0, column=0, padx=(0, 8), sticky="ew")
        
        browse_button = ctk.CTkButton(
            dir_frame,
            text="参照",
            command=self.browse_directory,
            width=80,
            height=AppStyles.SIZES['button_height'],
            **AppStyles.get_button_style('outline')
        )
        browse_button.grid(row=0, column=1, sticky="e")
        
        return start_row + 2
    
    def setup_programming_type_selection(self, parent, start_row):
        """Programming Type選択をセットアップ"""
        label = ctk.CTkLabel(parent, text="Programming Type:", font=AppStyles.FONTS['default'])
        label.grid(
            row=start_row, 
            column=0, 
            padx=AppStyles.SIZES['padding_medium'], 
            pady=(AppStyles.SIZES['padding_small'], 4), 
            sticky="w"
        )
        
        self.programming_type_var = ctk.StringVar()
        self.programming_type_combo = ctk.CTkComboBox(
            parent,
            variable=self.programming_type_var,
            **AppStyles.get_entry_style()
        )
        self.programming_type_combo.grid(
            row=start_row + 1, 
            column=0, 
            padx=AppStyles.SIZES['padding_medium'],
            pady=(4, AppStyles.SIZES['padding_small']),
            sticky="ew"
        )
        
        # Programming Type一覧を読み込み
        self.load_programming_types()
        
        return start_row + 2
    
    def setup_description_input(self, parent, start_row):
        """プロジェクト説明入力をセットアップ"""
        label = ctk.CTkLabel(parent, text="プロジェクト説明:", font=AppStyles.FONTS['default'])
        label.grid(
            row=start_row, 
            column=0, 
            padx=AppStyles.SIZES['padding_medium'], 
            pady=(AppStyles.SIZES['padding_small'], 4), 
            sticky="w"
        )
        
        self.description_text = ctk.CTkTextbox(
            parent,
            height=80,  # 高さを少し縮小
            font=AppStyles.FONTS['default'],
            corner_radius=AppStyles.SIZES['corner_radius']
        )
        self.description_text.grid(
            row=start_row + 1, 
            column=0, 
            padx=AppStyles.SIZES['padding_medium'],
            pady=(4, AppStyles.SIZES['padding_small']),
            sticky="ew"
        )
        
        return start_row + 2
    
    def setup_create_button(self, parent, start_row):
        """作成ボタンをセットアップ"""
        self.create_button = ctk.CTkButton(
            parent,
            text="プロジェクトを追加",
            command=self.create_project,
            height=AppStyles.SIZES['button_height'],
            **AppStyles.get_button_style('primary')
        )
        self.create_button.grid(
            row=start_row, 
            column=0, 
            padx=AppStyles.SIZES['padding_medium'],
            pady=(AppStyles.SIZES['padding_small'], AppStyles.SIZES['padding_large']),
            sticky="ew"
        )
    
    def setup_right_panel(self):
        """右側パネル（プロジェクト一覧）をセットアップ"""
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
            text="プロジェクト一覧",
            font=AppStyles.FONTS['heading']
        )
        title_label.grid(
            row=0, 
            column=0, 
            padx=AppStyles.SIZES['padding_medium'],
            pady=(AppStyles.SIZES['padding_medium'], AppStyles.SIZES['padding_small']),
            sticky="w"
        )
        
        # プロジェクト一覧スクロール可能フレーム
        self.projects_scrollable = ctk.CTkScrollableFrame(
            right_frame,
            **AppStyles.get_scrollable_frame_style()
        )
        self.projects_scrollable.grid(
            row=1, 
            column=0, 
            padx=AppStyles.SIZES['padding_medium'],
            pady=(0, AppStyles.SIZES['padding_medium']),
            sticky="nsew"
        )
        self.projects_scrollable.grid_columnconfigure(0, weight=1)
    
    def load_programming_types(self):
        """Programming Type一覧を読み込み"""
        languages = getValueByFormnameAndKeyName("chat", "systemrole", "プログラミング言語")
        if languages:
            self.programming_type_combo.configure(values=languages)
            if languages:
                self.programming_type_var.set(languages[0])
    
    def browse_directory(self):
        """ディレクトリ選択ダイアログ"""
        directory = filedialog.askdirectory()
        if directory:
            self.directory_entry.delete(0, 'end')
            self.directory_entry.insert(0, directory)
    
    def create_project(self):
        """プロジェクト作成"""
        project_name = self.project_name_entry.get().strip()
        directory_path = self.directory_entry.get().strip()
        programming_type = self.programming_type_var.get()
        description = self.description_text.get("1.0", "end-1c").strip()
        
        success, message = self.create_new_project_with_all_data(
            project_name, directory_path, programming_type, description
        )
        
        if success:
            # 入力欄をクリア
            self.project_name_entry.delete(0, 'end')
            self.directory_entry.delete(0, 'end')
            self.description_text.delete("1.0", "end")
            # Programming Typeは最初の選択肢にリセット
            languages = getValueByFormnameAndKeyName("chat", "systemrole", "プログラミング言語")
            if languages:
                self.programming_type_var.set(languages[0])
            
            # プロジェクト一覧を更新
            self.load_projects()
            
            # 全タブのデータを更新
            if self.main_window:
                self.main_window.refresh_all_tabs()
            
            messagebox.showinfo("Success", message)
        else:
            messagebox.showerror("Error", message)
    
    def create_new_project_with_all_data(self, project_name, directory_path, programming_type, description):
        """Programming Type対応のプロジェクト作成"""
        from app.myjsondb.myHistories import createProject, getAllProject
        from app.myjsondb.myProjectSettings import upsertPjdirAndValueByPjnm, getAllProject
        
        # 入力値検証
        if not project_name.strip():
            return False, "プロジェクト名を入力してください。"
        
        if not directory_path.strip():
            return False, "ディレクトリパスを入力してください。"
        
        if not os.path.isdir(directory_path):
            return False, "有効なディレクトリパスを入力してください。"
        
        if not programming_type.strip():
            return False, "Programming Typeを選択してください。"
        
        # 既存プロジェクト名チェック
        existing_projects = getAllProject()
        if project_name in existing_projects:
            return False, "このプロジェクト名は既に存在します。"
        
        try:
            createProject(project_name)
            value_data = {
                "test": "sss",
                "description": description if description else "プロジェクトの説明がありません。",
                "programming_type": programming_type
            }
            upsertPjdirAndValueByPjnm(project_name, directory_path, value_data)
            return True, f"プロジェクト '{project_name}' を追加しました。"
        except Exception as e:
            return False, f"プロジェクト作成中にエラーが発生しました: {str(e)}"
    
    def refresh_data(self):
        """データを更新"""
        self.load_programming_types()
        self.load_projects()
    
    def load_projects(self):
        """プロジェクト一覧を読み込み"""
        # 既存のウィジェットをクリア
        for widget in self.projects_scrollable.winfo_children():
            widget.destroy()
        
        # プロジェクト一覧取得
        projects = getProjectList()
        
        if not projects:
            # プロジェクトがない場合のメッセージ
            no_projects_label = ctk.CTkLabel(
                self.projects_scrollable,
                text="現在、プロジェクトはありません。\n最初のプロジェクトを作成しましょう！",
                font=AppStyles.FONTS['default'],
                text_color=AppStyles.COLORS['text_secondary']
            )
            no_projects_label.grid(
                row=0, 
                column=0, 
                padx=AppStyles.SIZES['padding_medium'],
                pady=AppStyles.SIZES['padding_large'],
                sticky="ew"
            )
            return
        
        # プロジェクトカードを作成
        for i, project_name in enumerate(projects):
            project_dir = getPjdirByPjnm(project_name)
            
            project_card = ProjectCard(
                self.projects_scrollable,
                project_name=project_name,
                project_path=project_dir,
                delete_callback=self.delete_project_callback,
                edit_callback=self.on_project_edited
            )
            project_card.grid(
                row=i, 
                column=0, 
                padx=AppStyles.SIZES['padding_small'],
                pady=AppStyles.SIZES['padding_small'],
                sticky="ew"
            )
    
    def delete_project_callback(self, project_name):
        """プロジェクト削除コールバック"""
        # 確認ダイアログ
        result = messagebox.askyesno(
            "削除確認",
            f"プロジェクト '{project_name}' を削除しますか？\nこの操作は取り消せません。"
        )
        
        if result:
            success, message = delete_project(project_name)
            
            if success:
                self.load_projects()
                # 全タブのデータを更新
                if self.main_window:
                    self.main_window.refresh_all_tabs()
                messagebox.showinfo("Success", message)
            else:
                messagebox.showerror("Error", message)
    
    def on_project_edited(self):
        """プロジェクト編集後のコールバック"""
        self.load_projects()
        # 全タブのデータを更新
        if self.main_window:
            self.main_window.refresh_all_tabs()