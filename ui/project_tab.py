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

class ProjectTab:
    """プロジェクト管理タブのUIコンポーネント"""
    
    def __init__(self, parent):
        self.parent = parent
        
        # レイアウト設定
        self.parent.grid_columnconfigure(0, weight=1)
        self.parent.grid_columnconfigure(1, weight=2)
        self.parent.grid_rowconfigure(0, weight=1)
        
        self.setup_ui()
        self.load_projects()
    
    def setup_ui(self):
        """UIコンポーネントをセットアップ"""
        # 左側パネル（新規作成）
        self.setup_left_panel()
        
        # 右側パネル（プロジェクト一覧）
        self.setup_right_panel()
    
    def setup_left_panel(self):
        """左側パネル（新規作成）をセットアップ"""
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
        
        # プロジェクト名入力
        self.setup_project_name_input(left_frame, 1)
        
        # ディレクトリ選択
        self.setup_directory_selection(left_frame, 2)
        
        # 作成ボタン
        self.setup_create_button(left_frame, 3)
    
    def setup_project_name_input(self, parent, row):
        """プロジェクト名入力をセットアップ"""
        label = ctk.CTkLabel(parent, text="プロジェクト名:", font=AppStyles.FONTS['default'])
        label.grid(
            row=row, 
            column=0, 
            padx=AppStyles.SIZES['padding_medium'], 
            pady=(AppStyles.SIZES['padding_small'], 2), 
            sticky="w"
        )
        
        self.project_name_entry = ctk.CTkEntry(
            parent,
            placeholder_text="プロジェクト名を入力...",
            **AppStyles.get_entry_style()
        )
        self.project_name_entry.grid(
            row=row+1, 
            column=0, 
            padx=AppStyles.SIZES['padding_medium'],
            pady=(2, AppStyles.SIZES['padding_medium']),
            sticky="ew"
        )
    
    def setup_directory_selection(self, parent, row):
        """ディレクトリ選択をセットアップ"""
        label = ctk.CTkLabel(parent, text="ディレクトリのパス:", font=AppStyles.FONTS['default'])
        label.grid(
            row=row, 
            column=0, 
            padx=AppStyles.SIZES['padding_medium'], 
            pady=(AppStyles.SIZES['padding_small'], 2), 
            sticky="w"
        )
        
        # ディレクトリ入力とボタンのフレーム
        dir_frame = ctk.CTkFrame(parent, fg_color="transparent")
        dir_frame.grid(
            row=row+1, 
            column=0, 
            padx=AppStyles.SIZES['padding_medium'],
            pady=(2, AppStyles.SIZES['padding_medium']),
            sticky="ew"
        )
        dir_frame.grid_columnconfigure(0, weight=1)
        
        self.directory_entry = ctk.CTkEntry(
            dir_frame,
            placeholder_text="ディレクトリパスを選択...",
            **AppStyles.get_entry_style()
        )
        self.directory_entry.grid(row=0, column=0, padx=(0, 5), sticky="ew")
        
        browse_button = ctk.CTkButton(
            dir_frame,
            text="参照",
            command=self.browse_directory,
            width=80,
            **AppStyles.get_button_style('outline')
        )
        browse_button.grid(row=0, column=1, sticky="e")
    
    def setup_create_button(self, parent, row):
        """作成ボタンをセットアップ"""
        self.create_button = ctk.CTkButton(
            parent,
            text="プロジェクトを追加",
            command=self.create_project,
            **AppStyles.get_button_style('primary')
        )
        self.create_button.grid(
            row=row, 
            column=0, 
            padx=AppStyles.SIZES['padding_medium'],
            pady=AppStyles.SIZES['padding_medium'],
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
        
        success, message = create_new_project(project_name, directory_path)
        
        if success:
            # 入力欄をクリア
            self.project_name_entry.delete(0, 'end')
            self.directory_entry.delete(0, 'end')
            
            # プロジェクト一覧を更新
            self.load_projects()
            
            messagebox.showinfo("Success", message)
        else:
            messagebox.showerror("Error", message)
    
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
                delete_callback=self.delete_project_callback
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
                messagebox.showinfo("Success", message)
            else:
                messagebox.showerror("Error", message)