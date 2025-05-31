"""
Activity Sidebar Widget
VS Code風のアクティビティーサイドバー用カスタムウィジェット
"""
import customtkinter as ctk
from ui.styles import AppStyles

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
                'tooltip': 'Story2Code\nLLMとのチャット',
                'row': 0
            },
            {
                'id': 'history',
                'icon': '📚',
                'tooltip': 'MyHistory\nチャット履歴管理',
                'row': 1
            },
            {
                'id': 'projects',
                'icon': '📁',
                'tooltip': 'Project List\nプロジェクト管理',
                'row': 2
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
        
        # ツールチップ効果（簡易版）
        self.create_tooltip(button, activity['tooltip'])
        
        self.buttons[activity['id']] = button
    
    def create_tooltip(self, widget, text):
        """簡易ツールチップを作成"""
        def on_enter(event):
            # ツールチップ表示のロジック（簡易版）
            print(f"Tooltip: {text}")
        
        def on_leave(event):
            # ツールチップ非表示のロジック
            pass
        
        widget.bind("<Enter>", on_enter)
        widget.bind("<Leave>", on_leave)
    
    def on_button_click(self, activity_id):
        """ボタンクリック時のハンドラ"""
        self.set_active(activity_id)
        
        if self.on_activity_changed:
            self.on_activity_changed(activity_id)
    
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