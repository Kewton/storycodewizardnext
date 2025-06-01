"""
Activity Sidebar Widget
VS Code風のアクティビティーサイドバー用カスタムウィジェット
"""
import customtkinter as ctk
import tkinter as tk
import sys
from ui.styles import AppStyles

class ToolTip:
    """ツールチップウィジェット"""
    
    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.tooltip_window = None
        self.show_delay = 500  # 表示遅延（ミリ秒）
        self.hide_delay = 300   # 非表示遅延を増加（ミリ秒）
        self.show_timer = None
        self.hide_timer = None
        self.is_mouse_over = False  # マウスオーバー状態を追跡
        
        # イベントバインド
        self.widget.bind("<Enter>", self.on_enter)
        self.widget.bind("<Leave>", self.on_leave)
        self.widget.bind("<Motion>", self.on_motion)
    
    def on_enter(self, event):
        """マウスエンター時の処理"""
        self.is_mouse_over = True
        self.cancel_hide_timer()
        if not self.tooltip_window:  # ツールチップが表示されていない場合のみ表示タイマーを開始
            self.show_timer = self.widget.after(self.show_delay, self.show_tooltip)
    
    def on_leave(self, event):
        """マウスリーブ時の処理"""
        self.is_mouse_over = False
        self.cancel_show_timer()
        if self.tooltip_window:
            # マウスが離れた時にすぐに非表示タイマーを開始
            self.hide_timer = self.widget.after(self.hide_delay, self.check_and_hide_tooltip)
    
    def on_motion(self, event):
        """マウス移動時の処理"""
        self.is_mouse_over = True
        # マウスが動いている間は非表示タイマーをキャンセル
        self.cancel_hide_timer()
        
        if self.tooltip_window:
            self.update_tooltip_position(event)
        elif not self.show_timer:  # 表示タイマーが動いていない場合のみ新規開始
            self.show_timer = self.widget.after(self.show_delay, self.show_tooltip)
    
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
    
    def check_and_hide_tooltip(self):
        """マウス状態を確認してツールチップを非表示"""
        if not self.is_mouse_over and self.tooltip_window:
            self.hide_tooltip()
    
    def show_tooltip(self):
        """ツールチップを表示"""
        if self.tooltip_window or not self.is_mouse_over:
            return
        
        self.tooltip_window = tk.Toplevel(self.widget)
        self.tooltip_window.wm_overrideredirect(True)
        self.tooltip_window.wm_attributes("-topmost", True)
        
        # スタイリング改善
        label = tk.Label(
            self.tooltip_window,
            text=self.text,
            background=AppStyles.COLORS.get('surface_light', "#383838"),
            foreground=AppStyles.COLORS.get('text', "#ffffff"),
            font=AppStyles.FONTS.get('small', ("Arial", 10)),
            relief="solid",
            borderwidth=1,
            padx=12,  # パディング調整
            pady=8,   # パディング調整
            justify=tk.LEFT
        )
        label.pack()
        
        # 位置を更新
        self.update_tooltip_position()
        
        # ツールチップウィンドウにもマウスイベントをバインド
        self.tooltip_window.bind("<Enter>", self.on_tooltip_enter)
        self.tooltip_window.bind("<Leave>", self.on_tooltip_leave)
    
    def on_tooltip_enter(self, event):
        """ツールチップウィンドウにマウスが入った時"""
        self.cancel_hide_timer()
    
    def on_tooltip_leave(self, event):
        """ツールチップウィンドウからマウスが出た時"""
        self.hide_timer = self.widget.after(self.hide_delay, self.check_and_hide_tooltip)
    
    def update_tooltip_position(self, event=None):
        """ツールチップの位置を更新"""
        if not self.tooltip_window:
            return
        
        # ウィジェットの位置を取得
        x = self.widget.winfo_rootx() + self.widget.winfo_width() + 15
        y = self.widget.winfo_rooty() + (self.widget.winfo_height() // 2)
        
        # 画面外に出ないよう調整
        screen_width = self.widget.winfo_screenwidth()
        screen_height = self.widget.winfo_screenheight()
        
        self.tooltip_window.update_idletasks()
        tooltip_width = self.tooltip_window.winfo_reqwidth()
        tooltip_height = self.tooltip_window.winfo_reqheight()
        
        # 右端からはみ出る場合は左側に表示
        if x + tooltip_width > screen_width:
            x = self.widget.winfo_rootx() - tooltip_width - 15
        
        # 下端からはみ出る場合は上に調整
        if y + tooltip_height > screen_height:
            y = screen_height - tooltip_height - 10
        
        # 上端からはみ出る場合は下に調整
        if y < 0:
            y = 10
        
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
            'fg_color': AppStyles.COLORS.get('sidebar', '#2d2d2d'),
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
        self.configure(width=AppStyles.SIZES.get('sidebar_width', 70))
        self.grid_propagate(False)
        
        self.setup_ui()
    
    def setup_ui(self):
        """UIコンポーネントをセットアップ"""
        self.grid_rowconfigure(10, weight=1)  # 中間に余白を作る
        
        # アクティビティーボタンを作成
        activities = [
            {
                'id': 'story2code',
                'icon': '💬',
                'tooltip': (
                    'コード生成リクエスト\n\n'
                    '複数LLM対応のコード生成機能\n'
                    '• ストリーミング表示\n'
                    '• Markdown対応\n'
                    '• ファイルアップロード対応'
                ),
                'row': 0
            },
            {
                'id': 'history',
                'icon': '📚',
                'tooltip': (
                    'コーディングエージェントとの会話履歴\n\n'
                    'プロジェクト別の会話履歴管理\n'
                    '• エクスポート機能\n'
                    '• 詳細表示\n'
                    '• プロジェクト反映'
                ),
                'row': 1
            },
            {
                'id': 'projects',
                'icon': '📁',
                'tooltip': (
                    'プロジェクト管理\n\n'
                    'プロジェクト管理\n'
                    '• 新規作成・編集\n'
                    '• コーディングエージェント管理\n'
                    '• ディレクトリ連携'
                ),
                'row': 2
            },
            {
                'id': 'help',
                'icon': '❓',
                'tooltip': (
                    'ヘルプ\n\n'
                    'ユーザーガイド\n'
                    '• 機能説明\n'
                    '• 使い方ガイド\n'
                    '• よくある質問'
                ),
                'row': 3
            }
        ]
        
        for activity in activities:
            self.create_activity_button(activity)
        
        # 再起動ボタンを最下部に追加
        self.create_restart_button()
    
    def create_activity_button(self, activity):
        """アクティビティーボタンを作成"""
        button_style = AppStyles.get_sidebar_style()['button']
        button = ctk.CTkButton(
            self,
            text=activity['icon'],
            command=lambda: self.on_button_click(activity['id']),
            **button_style # スタイルを適用
        )
        button.grid(
            row=activity['row'],
            column=0,
            padx= (self.cget('width') - button_style['width']) // 2, # 中央揃え
            pady=(15, 5),
            sticky="n"
        )
        
        # ツールチップを作成
        tooltip = ToolTip(button, activity['tooltip'])
        self.tooltips[activity['id']] = tooltip
        
        self.buttons[activity['id']] = button
    
    def create_restart_button(self):
        """再起動ボタンを作成"""
        button_style = AppStyles.get_sidebar_style()['button'].copy()
        # 再起動ボタンは少し異なるスタイルを適用
        button_style['text_color'] = AppStyles.COLORS.get('warning', '#ff9800')
        
        restart_button = ctk.CTkButton(
            self,
            text='🔄',
            command=self.restart_application,
            **button_style
        )
        restart_button.grid(
            row=11,  # 最下部に配置
            column=0,
            padx=(self.cget('width') - button_style['width']) // 2,
            pady=(15, 15),
            sticky="s"
        )
        
        # ツールチップを作成（改善されたツールチップを使用）
        restart_tooltip = ToolTip(restart_button, 
                                 'アプリケーション再起動\n\n'
                                 'アプリケーションを完全に再起動します\n'
                                 '• 設定の再読み込み\n'
                                 '• メモリクリア\n'
                                 '• トラブル解決に効果的')
        self.tooltips['restart'] = restart_tooltip
    
    def restart_application(self):
        """アプリケーションを再起動"""
        try:
            # 確認ダイアログを表示
            from tkinter import messagebox
            result = messagebox.askyesno(
                "アプリケーション再起動",
                "アプリケーションを再起動しますか？\n\n"
                "現在の作業内容は保存済みであることを確認してください。"
            )
            
            if result:
                # ウィンドウを閉じる前にクリーンアップ
                self.master.on_closing()
                
                # Pythonスクリプトを再起動
                import subprocess
                subprocess.Popen([sys.executable] + sys.argv)
                
                # 現在のプロセスを終了
                sys.exit(0)
        except Exception as e:
            print(f"Restart failed: {e}")
            from tkinter import messagebox
            messagebox.showerror("再起動エラー", f"再起動に失敗しました: {str(e)}")
    
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
        sidebar_colors = AppStyles.get_sidebar_style()['colors']
        # 前のアクティブボタンをリセット
        if self.active_button:
            self.active_button.configure(
                fg_color='transparent', # 通常時の色
                text_color=sidebar_colors['text']
            )
        
        # 新しいアクティブボタンを設定
        if activity_id in self.buttons:
            self.active_button = self.buttons[activity_id]
            self.active_button.configure(
                fg_color=sidebar_colors['active'], # アクティブ時の色
                text_color='#ffffff' # アクティブ時のテキスト色
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