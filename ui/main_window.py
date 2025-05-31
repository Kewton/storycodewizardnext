"""
StoryCodeWizard Main Window
メインアプリケーションウィンドウとアクティビティーサイドバー管理
"""
import customtkinter as ctk
from ui.chat_tab import ChatTab
from ui.history_tab import HistoryTab
from ui.project_tab import ProjectTab
from ui.widgets.activity_sidebar import ActivitySidebar
from ui.styles import AppStyles

class MainWindow(ctk.CTk):
    """メインアプリケーションウィンドウ"""
    
    def __init__(self):
        super().__init__()
        
        # ウィンドウ設定
        self.title("StoryCodeWizard")
        self.geometry("1400x900")
        self.minsize(1200, 700)
        
        # アイコン設定（オプション）
        try:
            self.iconbitmap("assets/icon.ico")
        except:
            pass  # アイコンファイルがない場合は無視
        
        # レイアウト設定
        self.grid_columnconfigure(0, weight=0)  # サイドバー（固定幅）
        self.grid_columnconfigure(1, weight=1)  # メインコンテンツ（可変）
        self.grid_rowconfigure(0, weight=1)
        
        # 現在のアクティブなコンテンツ
        self.current_content = None
        self.content_components = {}
        
        # UI初期化
        self.setup_ui()
        
        # デフォルトでStory2Codeを表示
        self.show_content("story2code")
        
        # ウィンドウ閉じるイベント
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
    
    def setup_ui(self):
        """UIコンポーネントをセットアップ"""
        # アクティビティーサイドバー
        self.activity_sidebar = ActivitySidebar(
            self,
            on_activity_changed=self.on_activity_changed
        )
        self.activity_sidebar.grid(
            row=0, 
            column=0, 
            sticky="nsew"
        )
        
        # メインコンテンツエリア（フレーム）
        self.content_frame = ctk.CTkFrame(
            self,
            **AppStyles.get_frame_style('default')
        )
        self.content_frame.grid(
            row=0, 
            column=1, 
            padx=(0, AppStyles.SIZES['padding_medium']),
            pady=AppStyles.SIZES['padding_medium'],
            sticky="nsew"
        )
        self.content_frame.grid_columnconfigure(0, weight=1)
        self.content_frame.grid_rowconfigure(0, weight=1)
    
    def on_activity_changed(self, activity_id):
        """アクティビティー変更時のハンドラ"""
        self.show_content(activity_id)
    
    def show_content(self, activity_id):
        """指定されたコンテンツを表示"""
        # 現在のコンテンツを非表示
        if self.current_content:
            self.current_content.grid_remove()
        
        # 新しいコンテンツを作成または取得
        if activity_id not in self.content_components:
            self.create_content_component(activity_id)
        
        # 新しいコンテンツを表示
        self.current_content = self.content_components[activity_id]
        self.current_content.grid(
            row=0, 
            column=0, 
            sticky="nsew"
        )
        
        # データを更新
        if hasattr(self.current_content, 'refresh_data'):
            self.current_content.refresh_data()
        
        # サイドバーのアクティブ状態を更新
        self.activity_sidebar.set_active(activity_id)
    
    def create_content_component(self, activity_id):
        """コンテンツコンポーネントを作成"""
        if activity_id == "story2code":
            self.content_components[activity_id] = ChatTab(self.content_frame, main_window=self)
        elif activity_id == "history":
            self.content_components[activity_id] = HistoryTab(self.content_frame, main_window=self)
        elif activity_id == "projects":
            self.content_components[activity_id] = ProjectTab(self.content_frame, main_window=self)
    
    def refresh_all_content(self):
        """全コンテンツのデータを更新"""
        for component in self.content_components.values():
            if hasattr(component, 'refresh_data'):
                component.refresh_data()
    
    def on_closing(self):
        """アプリケーション終了時の処理"""
        # 必要に応じてクリーンアップ処理を追加
        self.quit()
        self.destroy()