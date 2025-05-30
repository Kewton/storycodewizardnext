"""
Project Card Widget
プロジェクト情報表示用カスタムウィジェット
"""
import customtkinter as ctk
from ui.styles import AppStyles
from ui.widgets.project_edit_dialog import ProjectEditDialog
from app.myjsondb.myProjectSettings import getValueByPjnm

class ProjectCard(ctk.CTkFrame):
    """プロジェクト情報表示カードウィジェット"""
    
    def __init__(self, parent, project_name, project_path, delete_callback=None, edit_callback=None, **kwargs):
        super().__init__(parent, **AppStyles.get_frame_style('card'), **kwargs)
        
        self.parent = parent
        self.project_name = project_name
        self.project_path = project_path
        self.delete_callback = delete_callback
        self.edit_callback = edit_callback
        
        # プロジェクト情報を取得
        self.project_description, self.programming_type = self.get_project_info()
        
        self.setup_ui()
    
    def get_project_info(self):
        """プロジェクト情報を取得"""
        try:
            value_data = getValueByPjnm(self.project_name)
            description = value_data.get('description', 'プロジェクトの説明がありません。')
            programming_type = value_data.get('programming_type', '未設定')
            return description, programming_type
        except:
            return 'プロジェクトの説明がありません。', '未設定'
    
    def setup_ui(self):
        """UIコンポーネントをセットアップ"""
        self.grid_columnconfigure(0, weight=1)
        
        # プロジェクト名
        name_label = ctk.CTkLabel(
            self,
            text=self.project_name,
            font=AppStyles.FONTS['subheading'],
            text_color=AppStyles.COLORS['text']
        )
        name_label.grid(
            row=0, 
            column=0, 
            columnspan=3,
            padx=AppStyles.SIZES['padding_medium'],
            pady=(AppStyles.SIZES['padding_medium'], AppStyles.SIZES['padding_small']),
            sticky="w"
        )
        
        # Programming Type
        programming_type_label = ctk.CTkLabel(
            self,
            text=f"Programming Type: {self.programming_type}",
            font=AppStyles.FONTS['small'],
            text_color=AppStyles.COLORS['accent']
        )
        programming_type_label.grid(
            row=1, 
            column=0, 
            columnspan=3,
            padx=AppStyles.SIZES['padding_medium'],
            pady=(0, AppStyles.SIZES['padding_small']),
            sticky="w"
        )
        
        # プロジェクトパス
        path_label = ctk.CTkLabel(
            self,
            text=f"ディレクトリパス: {self.project_path}",
            font=AppStyles.FONTS['small'],
            text_color=AppStyles.COLORS['text_secondary']
        )
        path_label.grid(
            row=2, 
            column=0, 
            columnspan=3,
            padx=AppStyles.SIZES['padding_medium'],
            pady=(0, AppStyles.SIZES['padding_small']),
            sticky="w"
        )
        
        # プロジェクト説明
        description_label = ctk.CTkLabel(
            self,
            text=f"説明: {self.project_description}",
            font=AppStyles.FONTS['small'],
            text_color=AppStyles.COLORS['text_secondary'],
            wraplength=400
        )
        description_label.grid(
            row=3, 
            column=0, 
            padx=AppStyles.SIZES['padding_medium'],
            pady=(0, AppStyles.SIZES['padding_medium']),
            sticky="w"
        )
        
        # ボタンフレーム
        button_frame = ctk.CTkFrame(self, fg_color="transparent")
        button_frame.grid(
            row=3,
            column=1,
            columnspan=2,
            padx=AppStyles.SIZES['padding_medium'],
            pady=(0, AppStyles.SIZES['padding_medium']),
            sticky="e"
        )
        
        # 編集ボタン
        edit_style = AppStyles.get_button_style('outline').copy()
        edit_style['text_color'] = AppStyles.COLORS['primary']
        edit_style['hover_color'] = AppStyles.COLORS['primary']
        edit_style['font'] = AppStyles.FONTS['small']
        edit_button = ctk.CTkButton(
            button_frame,
            text="編集",
            command=self.on_edit,
            width=60,
            **edit_style
        )
        edit_button.grid(row=0, column=0, padx=(0, 5), sticky="e")
        
        # 削除ボタン
        if self.delete_callback:
            delete_style = AppStyles.get_button_style('outline').copy()
            delete_style['text_color'] = AppStyles.COLORS['error']
            delete_style['hover_color'] = AppStyles.COLORS['error']
            delete_style['font'] = AppStyles.FONTS['small']
            delete_button = ctk.CTkButton(
                button_frame,
                text="削除",
                command=self.on_delete,
                width=60,
                **delete_style
            )
            delete_button.grid(row=0, column=1, sticky="e")
    
    def on_edit(self):
        """編集ボタンクリック時のハンドラ"""
        # プロジェクト編集ダイアログを開く
        dialog = ProjectEditDialog(
            self,
            project_name=self.project_name,
            project_path=self.project_path,
            project_description=self.project_description,
            programming_type=self.programming_type,
            save_callback=self.on_project_updated
        )
        dialog.grab_set()  # モーダルダイアログにする
    
    def on_delete(self):
        """削除ボタンクリック時のハンドラ"""
        if self.delete_callback:
            self.delete_callback(self.project_name)
    
    def on_project_updated(self, new_name, new_path, new_description, new_programming_type):
        """プロジェクト更新後のコールバック"""
        self.project_name = new_name
        self.project_path = new_path
        self.project_description = new_description
        self.programming_type = new_programming_type
        
        # UI更新のため、親にコールバック
        if self.edit_callback:
            self.edit_callback()