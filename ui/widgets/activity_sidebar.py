"""
Activity Sidebar Widget
VS Code風のアクティビティーサイドバー用カスタムウィジェット
"""
import customtkinter as ctk
import tkinter as tk
from ui.styles import AppStyles

class ToolTip:
    """ツールチップウィジェット"""
    
    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.tooltip_window = None
        self.show_delay = 500  # 表示遅延（ミリ秒）
        self.hide_delay = 100   # 非表示遅延（ミリ秒）
        self.show_timer = None
        self.hide_timer = None
        
        # イベントバインド
        self.widget.bind("<Enter>", self.on_enter)
        self.widget.bind("<Leave>", self.on_leave)
        self.widget.bind("<Motion>", self.on_motion)
    
    def on_enter(self, event):
        """マウスエンター時の処理"""
        self.cancel_hide_timer()
        self.show_timer = self.widget.after(self.show_delay, self.show_tooltip)
    
    def on_leave(self, event):
        """マウスリーブ時の処理"""
        self.cancel_show_timer()
        if self.tooltip_window:
            self.hide_timer = self.widget.after(self.hide_delay, self.hide_tooltip)
    
    def on_motion(self, event):
        """マウス移動時の処理"""
        if self.tooltip_window:
            self.update_tooltip_position(event)
    
    def cancel_show_timer(self):
        """表示タイマーをキャンセル"""
        if self.show_timer:
            self.widget.after_cancel(self.show_timer)
            self.show_timer = None
    
    def cancel_hide_timer(self):
        """非表示タイマーをキャンセル"""
        if self.hide_timer:
            self.widget.after_cancel(self.hide_timer)
            self.hide_timer = None
    
    def show_tooltip(self):
        """ツールチップを表示"""
        if self.tooltip_window:
            return
        
        self.tooltip_window = tk.Toplevel(self.widget)
        self.tooltip_window.wm_overrideredirect(True)
        self.tooltip_window.wm_attributes("-topmost", True)
        
        # スタイリング
        label = tk.Label(
            self.tooltip_window,
            text=self.text,
            background="#2d2d2d",
            foreground="#ffffff",
            font=("Arial", 10),
            relief="solid",
            borderwidth=1,
            padx=8,
            pady=4
        )
        label.pack()
        
        # 位置を更新
        self.update_tooltip_position()
    
    def update_tooltip_position(self, event=None):
        """ツールチップの位置を更新"""
        if not self.tooltip_window:
            return
        
        # ウィジェットの位置を取得
        x = self.widget.winfo_rootx() + self.widget.winfo_width() + 10
        y = self.widget.winfo_rooty() + self.widget.winfo_height() // 2
        
        # 画面外に出ないよう調整
        screen_width = self.widget.winfo_screenwidth()
        screen_height = self.widget.winfo_screenheight()
        
        tooltip_width = self.tooltip_window.winfo_reqwidth()
        tooltip_height = self.tooltip_window.winfo_reqheight()
        
        if x + tooltip_width > screen_width:
            x = self.widget.winfo_rootx() - tooltip_width - 10
        
        if y + tooltip_height > screen_height:
            y = screen_height - tooltip_height - 10
        
        if y < 0:
            y = 0
        
        self.tooltip_window.wm_geometry(f"+{x}+{y}")
    
    def hide_tooltip(self):
        """ツールチップを非表示"""
        if self.tooltip_window:
            self.tooltip_window.destroy()
            self.tooltip_window = None
    
    def destroy(self):
        """ツールチップを完全に破棄"""
        self.cancel_show_timer()
        self.cancel_hide_timer()
        self.hide_tooltip()


class ActivitySidebar(ctk.CTkFrame):
    """VS Code風アクティビティーサイドバーウィジェット"""
    
    def __init__(self, parent, on_activity_changed=None, **kwargs):
        # サイドバー専用のスタイル
        sidebar_style = {
            'fg_color': '#2d2d2d',  # VS Code風ダークグレー
            'corner_radius': 0,
            'border_width': 0
        }
        super().__init__(parent, **sidebar_style, **kwargs)
        
        self.on_activity_changed = on_activity_changed
        self.active_button = None
        self.buttons = {}
        self.tooltips = {}  # ツールチップ管理
        self._click_debounce = False  # クリック重複防止
        
        # 固定幅の設定
        self.configure(width=70)
        self.grid_propagate(False)
        
        self.setup_ui()
    
    def setup_ui(self):
        """UIコンポーネントをセットアップ"""
        self.grid_rowconfigure(10, weight=1)  # 下部に余白を作る
        
        # アクティビティーボタンを作成
        activities = [
            {
                'id': 'story2code',
                'icon': '💬',
                'tooltip': 'Story2Code\n\nLLMとのチャット機能\n• 複数LLM対応\n• ストリーミング表示\n• Markdown対応',
                'row': 0
            },
            {
                'id': 'history',
                'icon': '📚',
                'tooltip': 'MyHistory\n\nチャット履歴管理\n• プロジェクト別履歴\n• エクスポート機能\n• 詳細表示',
                'row': 1
            },
            {
                'id': 'projects',
                'icon': '📁',
                'tooltip': 'Project List\n\nプロジェクト管理\n• 新規作成・編集\n• Programming Type管理\n• ディレクトリ連携',
                'row': 2
            },
            {
                'id': 'help',
                'icon': '❓',
                'tooltip': 'ヘルプ\n\nユーザーガイド\n• 機能説明\n• 使い方ガイド\n• よくある質問',
                'row': 3
            }
        ]
        
        for activity in activities:
            self.create_activity_button(activity)
    
    def create_activity_button(self, activity):
        """アクティビティーボタンを作成"""
        button = ctk.CTkButton(
            self,
            text=activity['icon'],
            width=50,
            height=50,
            font=('Arial', 20),
            fg_color='transparent',
            hover_color='#404040',
            text_color='#cccccc',
            corner_radius=8,
            command=lambda: self.on_button_click(activity['id'])
        )
        button.grid(
            row=activity['row'],
            column=0,
            padx=10,
            pady=(15, 5),
            sticky="n"
        )
        
        # ツールチップを作成
        tooltip = ToolTip(button, activity['tooltip'])
        self.tooltips[activity['id']] = tooltip
        
        self.buttons[activity['id']] = button
    
    def on_button_click(self, activity_id):
        """ボタンクリック時のハンドラ（デバウンス付き）"""
        # 重複クリック防止
        if self._click_debounce:
            return
        
        self._click_debounce = True
        
        try:
            # 即座にアクティブ状態を更新（視覚的フィードバック）
            self.set_active(activity_id)
            
            # コールバック実行
            if self.on_activity_changed:
                self.on_activity_changed(activity_id)
        finally:
            # 短時間後にデバウンスフラグをリセット
            self.after(100, self._reset_debounce)
    
    def _reset_debounce(self):
        """デバウンスフラグをリセット"""
        self._click_debounce = False
    
    def set_active(self, activity_id):
        """アクティブなボタンを設定"""
        # 前のアクティブボタンをリセット
        if self.active_button:
            self.active_button.configure(
                fg_color='transparent',
                text_color='#cccccc'
            )
        
        # 新しいアクティブボタンを設定
        if activity_id in self.buttons:
            self.active_button = self.buttons[activity_id]
            self.active_button.configure(
                fg_color=AppStyles.COLORS['primary'],
                text_color='#ffffff'
            )
    
    def get_active(self):
        """現在アクティブなアクティビティーIDを取得"""
        for activity_id, button in self.buttons.items():
            if button == self.active_button:
                return activity_id
        return None
    
    def destroy(self):
        """ウィジェット破棄時のクリーンアップ"""
        # ツールチップを破棄
        for tooltip in self.tooltips.values():
            tooltip.destroy()
        
        super().destroy()