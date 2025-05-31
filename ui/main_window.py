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
        self._cached_content = {}  # コンテンツキャッシュ
        self._is_switching = False  # 切り替え中フラグ
        
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
        """アクティビティー変更時のハンドラ（パフォーマンス最適化済み）"""
        # 切り替え中の重複実行を防止
        if self._is_switching:
            return
        
        self._is_switching = True
        
        try:
            # 即座にサイドバーのアクティブ状態を更新（視覚的フィードバック）
            self.activity_sidebar.set_active(activity_id)
            
            # 非同期でコンテンツを表示（UIブロッキングを回避）
            self.after_idle(lambda: self._show_content_async(activity_id))
        finally:
            self._is_switching = False
    
    def _show_content_async(self, activity_id):
        """非同期コンテンツ表示（レスポンス改善）"""
        try:
            self.show_content(activity_id)
        except Exception as e:
            print(f"Error showing content: {e}")
        finally:
            self._is_switching = False
    
    def show_content(self, activity_id):
        """指定されたコンテンツを表示（最適化済み）"""
        # 同じコンテンツの場合は何もしない
        if (self.current_content and 
            activity_id in self.content_components and 
            self.current_content == self.content_components[activity_id]):
            return
        
        # 現在のコンテンツを非表示
        if self.current_content:
            self.current_content.grid_remove()
        
        # キャッシュされたコンテンツを取得または新規作成
        if activity_id not in self.content_components:
            self._create_content_component(activity_id)
        
        # 新しいコンテンツを表示
        self.current_content = self.content_components[activity_id]
        self.current_content.grid(
            row=0, 
            column=0, 
            sticky="nsew"
        )
        
        # データを更新（必要時のみ）
        self._refresh_content_if_needed(activity_id)
    
    def _create_content_component(self, activity_id):
        """コンテンツコンポーネントを作成（遅延初期化）"""
        if activity_id == "story2code":
            self.content_components[activity_id] = ChatTab(self.content_frame, main_window=self)
        elif activity_id == "history":
            self.content_components[activity_id] = HistoryTab(self.content_frame, main_window=self)
        elif activity_id == "projects":
            self.content_components[activity_id] = ProjectTab(self.content_frame, main_window=self)
        
        # 作成時刻を記録（キャッシュ管理用）
        import time
        self._cached_content[activity_id] = time.time()
    
    def _refresh_content_if_needed(self, activity_id):
        """必要な場合のみコンテンツを更新"""
        content = self.content_components.get(activity_id)
        if content and hasattr(content, 'refresh_data'):
            # キャッシュの有効期限をチェック（30秒）
            import time
            last_update = self._cached_content.get(activity_id, 0)
            if time.time() - last_update > 30:
                content.refresh_data()
                self._cached_content[activity_id] = time.time()
    
    def refresh_all_content(self):
        """全コンテンツのデータを更新"""
        for activity_id, component in self.content_components.items():
            if hasattr(component, 'refresh_data'):
                component.refresh_data()
                # キャッシュタイムスタンプを更新
                import time
                self._cached_content[activity_id] = time.time()
    
    def force_refresh_content(self, activity_id=None):
        """強制的にコンテンツを更新"""
        if activity_id:
            if activity_id in self.content_components:
                component = self.content_components[activity_id]
                if hasattr(component, 'refresh_data'):
                    component.refresh_data()
                import time
                self._cached_content[activity_id] = time.time()
        else:
            self.refresh_all_content()
    
    def on_closing(self):
        """アプリケーション終了時の処理"""
        # コンテンツのクリーンアップ
        for component in self.content_components.values():
            if hasattr(component, 'cleanup'):
                try:
                    component.cleanup()
                except:
                    pass
        
        # 必要に応じてクリーンアップ処理を追加
        self.quit()
        self.destroy()