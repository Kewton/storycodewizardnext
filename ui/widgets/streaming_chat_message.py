"""
Streaming Chat Message Widget
ストリーミング対応チャットメッセージ表示用カスタムウィジェット
"""
import customtkinter as ctk
import tkinter as tk
from ui.styles import AppStyles

class StreamingChatMessage(ctk.CTkFrame):
    """ストリーミング対応チャットメッセージ表示ウィジェット"""
    
    def __init__(self, parent, speaker, is_user=False, **kwargs):
        super().__init__(parent, **kwargs)
        
        self.speaker = speaker
        self.is_user = is_user
        self.content = ""
        
        # フレームスタイル設定
        if is_user:
            self.configure(**AppStyles.get_frame_style('card'))
        else:
            self.configure(
                fg_color=AppStyles.COLORS['surface_light'],
                corner_radius=AppStyles.SIZES['corner_radius'],
                border_width=1,
                border_color=AppStyles.COLORS['primary']
            )
        
        self.setup_ui()
    
    def setup_ui(self):
        """UIコンポーネントをセットアップ"""
        self.grid_columnconfigure(0, weight=1)
        
        # スピーカーラベル
        speaker_icon = "🙂" if self.is_user else "🤖"
        speaker_text = f"{speaker_icon} {self.speaker}"
        
        self.speaker_label = ctk.CTkLabel(
            self,
            text=speaker_text,
            font=AppStyles.FONTS['subheading'],
            text_color=AppStyles.COLORS['primary'] if not self.is_user else AppStyles.COLORS['text']
        )
        self.speaker_label.grid(
            row=0, 
            column=0, 
            padx=AppStyles.SIZES['padding_medium'],
            pady=(AppStyles.SIZES['padding_medium'], AppStyles.SIZES['padding_small']),
            sticky="w"
        )
        
        # ストリーミング状態表示
        if not self.is_user:
            self.status_label = ctk.CTkLabel(
                self,
                text="🔄 応答中...",
                font=AppStyles.FONTS['small'],
                text_color=AppStyles.COLORS['accent']
            )
            self.status_label.grid(
                row=1, 
                column=0, 
                padx=AppStyles.SIZES['padding_medium'],
                pady=(0, AppStyles.SIZES['padding_small']),
                sticky="w"
            )
        
        # コンテンツテキスト
        self.content_text = ctk.CTkTextbox(
            self,
            height=100,
            font=AppStyles.FONTS['default'],
            corner_radius=AppStyles.SIZES['corner_radius'],
            wrap="word"
        )
        self.content_text.grid(
            row=2, 
            column=0, 
            padx=AppStyles.SIZES['padding_medium'],
            pady=(0, AppStyles.SIZES['padding_medium']),
            sticky="ew"
        )
        
        # ユーザーメッセージの場合は即座にコンテンツを設定
        if self.is_user:
            self.content_text.configure(state="disabled")
    
    def update_content(self, new_text):
        """コンテンツを更新（ストリーミング用）"""
        self.content += new_text
        
        # テキストボックスを更新
        self.content_text.configure(state="normal")
        self.content_text.insert("end", new_text)
        self.content_text.configure(state="disabled")
        
        # 自動スクロール
        self.content_text.see("end")
        
        # 高さを調整
        lines = self.content.count('\n') + 1
        height = min(max(lines * 20 + 50, 100), 400)
        self.content_text.configure(height=height)
    
    def set_content(self, content):
        """コンテンツを一括設定（通常メッセージ用）"""
        self.content = content
        self.content_text.configure(state="normal")
        self.content_text.delete("1.0", "end")
        self.content_text.insert("1.0", content)
        self.content_text.configure(state="disabled")
        
        # 高さを調整
        lines = content.count('\n') + 1
        height = min(max(lines * 20 + 50, 100), 400)
        self.content_text.configure(height=height)
    
    def finish_streaming(self):
        """ストリーミング完了時の処理"""
        if not self.is_user and hasattr(self, 'status_label'):
            self.status_label.configure(
                text="✅ 完了",
                text_color=AppStyles.COLORS['success']
            )
    
    def get_content(self):
        """現在のコンテンツを取得"""
        return self.content