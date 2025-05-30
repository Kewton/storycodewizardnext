"""
Project Card Widget
プロジェクト情報表示用カスタムウィジェット
"""
import customtkinter as ctk
from ui.styles import AppStyles

class ProjectCard(ctk.CTkFrame):
    """プロジェクト情報表示カードウィジェット"""
    
    def __init__(self, parent, project_name, project_path, delete_callback=None, **kwargs):
        super().__init__(parent, **AppStyles.get_frame_style('card'), **kwargs)
        
        self.project_name = project_name
        self.project_path = project_path
        self.delete_callback = delete_callback
        
        self.setup_ui()
    
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
            columnspan=2,
            padx=AppStyles.SIZES['padding_medium'],
            pady=(AppStyles.SIZES['padding_medium'], AppStyles.SIZES['padding_small']),
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
            row=1, 
            column=0, 
            padx=AppStyles.SIZES['padding_medium'],
            pady=(0, AppStyles.SIZES['padding_medium']),
            sticky="w"
        )
        
        # 削除ボタン
        if self.delete_callback:
            style = AppStyles.get_button_style('outline').copy()
            # style 中の重複定義を排除
            style.pop('text_color', None)
            style.pop('hover_color', None)
            style['text_color'] = AppStyles.COLORS['error']
            style['hover_color'] = AppStyles.COLORS['error']
            style['font'] = AppStyles.FONTS['small']  # fontをスタイル辞書で指定
            delete_button = ctk.CTkButton(
                self,
                text="削除",
                command=self.on_delete,
                width=80,
                # font=AppStyles.FONTS['small'],  # 直接指定を削除
                **style
            )
            delete_button.grid(
                row=1,
                column=1,
                padx=AppStyles.SIZES['padding_medium'],
                pady=(0, AppStyles.SIZES['padding_medium']),
                sticky="e"
            )
    
    def on_delete(self):
        """削除ボタンクリック時のハンドラ"""
        if self.delete_callback:
            self.delete_callback(self.project_name)