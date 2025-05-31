"""
StoryCodeWizard Help Tab
ヘルプ・ユーザーガイドのUIコンポーネント
"""
import customtkinter as ctk
from ui.styles import AppStyles
from ui.widgets.help_widget import HelpWidget

class HelpTab(ctk.CTkFrame):
    """ヘルプタブのUIコンポーネント"""
    
    def __init__(self, parent, main_window=None):
        super().__init__(parent)
        self.main_window = main_window
        
        # レイアウト設定
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        self.setup_ui()
    
    def setup_ui(self):
        """UIコンポーネントをセットアップ"""
        # ヘルプウィジェットを作成
        self.help_widget = HelpWidget(self)
        self.help_widget.grid(
            row=0, 
            column=0, 
            padx=0,
            pady=0,
            sticky="nsew"
        )
    
    def refresh_data(self):
        """データを更新（ヘルプタブは静的コンテンツのため実装なし）"""
        pass
    
    def cleanup(self):
        """クリーンアップ処理"""
        pass