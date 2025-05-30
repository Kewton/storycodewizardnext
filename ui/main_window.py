"""
StoryCodeWizard Main Window
メインアプリケーションウィンドウとタブ管理
"""
import customtkinter as ctk
from ui.chat_tab import ChatTab
from ui.history_tab import HistoryTab
from ui.project_tab import ProjectTab
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
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        # UI初期化
        self.setup_ui()
        
        # ウィンドウ閉じるイベント
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
    
    def setup_ui(self):
        """UIコンポーネントをセットアップ"""
        # メインタブビュー
        self.tabview = ctk.CTkTabview(
            self,
            corner_radius=AppStyles.SIZES['corner_radius']
        )
        self.tabview.grid(
            row=0, 
            column=0, 
            padx=AppStyles.SIZES['padding_medium'],
            pady=AppStyles.SIZES['padding_medium'],
            sticky="nsew"
        )
        
        # タブ作成
        self.create_tabs()
        
        # タブ変更イベントを監視
        self.tabview.configure(command=self.on_tab_changed)
    
    def create_tabs(self):
        """各タブを作成"""
        # Story2Code タブ
        chat_tab = self.tabview.add("Story2Code")
        self.chat_component = ChatTab(chat_tab, main_window=self)
        
        # MyHistory タブ
        history_tab = self.tabview.add("MyHistory")
        self.history_component = HistoryTab(history_tab, main_window=self)
        
        # Project List タブ
        project_tab = self.tabview.add("Project List")
        self.project_component = ProjectTab(project_tab, main_window=self)
        
        # デフォルトタブを設定
        self.tabview.set("Story2Code")
    
    def on_tab_changed(self):
        """タブ変更時のハンドラ - データの自動更新"""
        current_tab = self.tabview.get()
        
        if current_tab == "Story2Code":
            self.chat_component.refresh_data()
        elif current_tab == "MyHistory":
            self.history_component.refresh_data()
        elif current_tab == "Project List":
            self.project_component.refresh_data()
    
    def refresh_all_tabs(self):
        """全タブのデータを更新"""
        self.chat_component.refresh_data()
        self.history_component.refresh_data()
        self.project_component.refresh_data()
    
    def on_closing(self):
        """アプリケーション終了時の処理"""
        # 必要に応じてクリーンアップ処理を追加
        self.quit()
        self.destroy()