"""
StoryCodeWizard Project Tab
プロジェクト管理のUIコンポーネント
"""
import customtkinter as ctk
import os
import subprocess
import sys
from tkinter import filedialog, messagebox
from ui.styles import AppStyles
from ui.widgets.project_card import ProjectCard
from app.chat import create_new_project, delete_project
from app.myjsondb.myHistories import getProjectList
from app.myjsondb.myProjectSettings import getPjdirByPjnm
from app.myjsondb.myStreamlit import getValueByFormnameAndKeyName

class ProjectTab(ctk.CTkFrame):
    """プロジェクト管理タブのUIコンポーネント"""
    
    def __init__(self, parent, main_window=None):
        super().__init__(parent)
        self.main_window = main_window
        
        # レイアウト設定
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=2)
        self.grid_rowconfigure(0, weight=1)
        
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
        
        # コーディングエージェント選択
        current_row = self.setup_coding_agent_selection(self.left_scrollable, current_row)
        
        # プロジェクト説明入力
        current_row = self.setup_description_input(self.left_scrollable, current_row)
        
        # ファイル作成オプション
        current_row = self.setup_file_creation_option(self.left_scrollable, current_row)
        
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
    
    def setup_coding_agent_selection(self, parent, start_row):
        """コーディングエージェント選択をセットアップ"""
        label = ctk.CTkLabel(parent, text="コーディングエージェント:", font=AppStyles.FONTS['default'])
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
        
        # コーディングエージェント一覧を読み込み
        self.load_coding_agents()
        
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
    
    def setup_file_creation_option(self, parent, start_row):
        """ファイル作成オプションをセットアップ"""
        label = ctk.CTkLabel(parent, text="初期ファイル作成:", font=AppStyles.FONTS['default'])
        label.grid(
            row=start_row, 
            column=0, 
            padx=AppStyles.SIZES['padding_medium'], 
            pady=(AppStyles.SIZES['padding_small'], 4), 
            sticky="w"
        )
        
        # チェックボックスとラベルのフレーム
        option_frame = ctk.CTkFrame(parent, fg_color="transparent")
        option_frame.grid(
            row=start_row + 1, 
            column=0, 
            padx=AppStyles.SIZES['padding_medium'],
            pady=(4, AppStyles.SIZES['padding_small']),
            sticky="ew"
        )
        option_frame.grid_columnconfigure(1, weight=1)
        
        # チェックボックス
        self.create_files_var = ctk.BooleanVar(value=True)  # デフォルトは有効
        self.create_files_checkbox = ctk.CTkCheckBox(
            option_frame,
            text="",
            variable=self.create_files_var,
            width=20
        )
        self.create_files_checkbox.grid(row=0, column=0, padx=(0, 8), sticky="w")
        
        # 説明ラベル
        description_label = ctk.CTkLabel(
            option_frame,
            text="プロジェクト作成時に初期ファイルを自動作成する",
            font=AppStyles.FONTS['small'],
            text_color=AppStyles.COLORS['text_secondary'],
            anchor="w"
        )
        description_label.grid(row=0, column=1, sticky="w")
        
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
    
    def load_coding_agents(self):
        """コーディングエージェント一覧を読み込み"""
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
        create_files = self.create_files_var.get()
        
        success, message = self.create_new_project_with_all_data(
            project_name, directory_path, programming_type, description
        )
        
        if success:
            # プロジェクト作成成功後、初期化スクリプト実行の確認（チェックボックスが有効な場合のみ）
            if create_files:
                self.prompt_for_initialization(project_name, directory_path, programming_type)
            
            # 入力欄をクリア
            self.project_name_entry.delete(0, 'end')
            self.directory_entry.delete(0, 'end')
            self.description_text.delete("1.0", "end")
            self.create_files_var.set(True)  # チェックボックスをデフォルト状態に戻す
            # コーディングエージェントは最初の選択肢にリセット
            languages = getValueByFormnameAndKeyName("chat", "systemrole", "プログラミング言語")
            if languages:
                self.programming_type_var.set(languages[0])
            
            # プロジェクト一覧を更新
            self.load_projects()
            
            # 全タブのデータを更新
            if self.main_window:
                self.main_window.refresh_all_content()
            
            messagebox.showinfo("Success", message)
        else:
            messagebox.showerror("Error", message)
    
    def prompt_for_initialization(self, project_name, directory_path, programming_type):
        """プロジェクト初期化スクリプト実行の確認ダイアログ"""
        # 確認メッセージを表示
        confirmation_message = (
            f"プロジェクト '{project_name}' の初期化を実行しますか？\n\n"
            f"実行される処理:\n"
            f"• コーディングエージェント: {programming_type}\n"
            f"• 対象ディレクトリ: {directory_path}\n"
            f"• 初期化ファイル: ./init/{programming_type}.md\n\n"
            "この操作により、プロジェクトディレクトリに初期ファイルが作成される可能性があります。\n"
            "続行しますか？"
        )
        
        result = messagebox.askyesno(
            "プロジェクト初期化の確認",
            confirmation_message
        )
        
        if result:
            self.execute_initialization_script(project_name, directory_path, programming_type)
        else:
            messagebox.showinfo(
                "初期化スキップ",
                f"プロジェクト '{project_name}' は作成されましたが、初期化はスキップされました。\n"
                "後で手動で初期化を実行することも可能です。"
            )
    
    def execute_initialization_script(self, project_name, directory_path, programming_type):
        """プロジェクト初期化スクリプトを実行"""
        try:
            # 初期化ファイルのパスを構築
            init_file_path = f"./init/{programming_type}.md"
            
            # 初期化ファイルの存在確認
            if not os.path.exists(init_file_path):
                messagebox.showwarning(
                    "初期化ファイルなし",
                    f"初期化ファイル '{init_file_path}' が見つかりません。\n"
                    "プロジェクトは作成されましたが、初期化はスキップされました。"
                )
                return
            
            # generate_files.pyの存在確認
            generate_script = "./generate_files.py"
            if not os.path.exists(generate_script):
                messagebox.showerror(
                    "スクリプトエラー",
                    f"初期化スクリプト '{generate_script}' が見つかりません。"
                )
                return
            
            # コマンドを構築して実行
            cmd = [
                sys.executable, 
                "generate_files.py", 
                os.path.abspath(init_file_path), 
                "-d", 
                directory_path
            ]
            
            # プログレスダイアログの表示（実装は簡易版）
            progress_dialog = messagebox.showinfo(
                "初期化実行中",
                f"プロジェクト '{project_name}' の初期化を実行中です...\n"
                "しばらくお待ちください。",
                type='ok'
            )
            
            # コマンド実行
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                cwd="."
            )
            
            # 実行結果の処理
            if result.returncode == 0:
                messagebox.showinfo(
                    "初期化完了",
                    f"プロジェクト '{project_name}' の初期化が正常に完了しました。\n\n"
                    f"出力:\n{result.stdout[:500]}{'...' if len(result.stdout) > 500 else ''}"
                )
            else:
                messagebox.showerror(
                    "初期化エラー",
                    f"プロジェクト初期化中にエラーが発生しました。\n\n"
                    f"エラー内容:\n{result.stderr[:500]}{'...' if len(result.stderr) > 500 else ''}"
                )
                
        except subprocess.TimeoutExpired:
            messagebox.showerror(
                "初期化タイムアウト",
                "初期化処理がタイムアウトしました。\n"
                "プロジェクトディレクトリを確認してください。"
            )
        except Exception as e:
            messagebox.showerror(
                "初期化エラー",
                f"予期しないエラーが発生しました:\n{str(e)}"
            )
    
    def create_new_project_with_all_data(self, project_name, directory_path, programming_type, description):
        """コーディングエージェント対応のプロジェクト作成"""
        from app.myjsondb.myHistories import createProject, getProjectList
        from app.myjsondb.myProjectSettings import upsertPjdirAndValueByPjnm, getAllProject
        
        # 入力値検証
        if not project_name.strip():
            return False, "プロジェクト名を入力してください。"
        
        if not directory_path.strip():
            return False, "ディレクトリパスを入力してください。"
        
        if not os.path.isdir(directory_path):
            return False, "有効なディレクトリパスを入力してください。"
        
        if not programming_type.strip():
            return False, "コーディングエージェントを選択してください。"
        
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
        self.load_coding_agents()
        self.load_projects()
    
    def load_projects(self):
        """プロジェクト一覧を読み込み（昇順ソート）"""
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
        
        # プロジェクト名で昇順ソート
        projects.sort()
        
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
                    self.main_window.refresh_all_content()
                messagebox.showinfo("Success", message)
            else:
                messagebox.showerror("Error", message)
    
    def on_project_edited(self):
        """プロジェクト編集後のコールバック"""
        self.load_projects()
        # 全タブのデータを更新
        if self.main_window:
            self.main_window.refresh_all_content()