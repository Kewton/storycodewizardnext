"""
Streaming Chat Message Widget
ストリーミング対応チャットメッセージ表示用カスタムウィジェット（Markdown対応）
"""
import customtkinter as ctk
import tkinter as tk
from ui.styles import AppStyles
from ui.widgets.markdown_renderer import MarkdownRenderer

class StreamingChatMessage(ctk.CTkFrame):
    """ストリーミング対応チャットメッセージ表示ウィジェット"""
    
    def __init__(self, parent, speaker, is_user=False, enable_markdown=True, **kwargs):
        super().__init__(parent, **kwargs)
        
        self.speaker = speaker
        self.is_user = is_user
        self.content = ""
        self.enable_markdown = enable_markdown and not is_user  # ユーザーメッセージはMarkdown無効
        self.is_markdown_view = True
        
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
        
        current_row = 1
        
        # ストリーミング状態表示
        if not self.is_user:
            self.status_label = ctk.CTkLabel(
                self,
                text="🔄 応答中...",
                font=AppStyles.FONTS['small'],
                text_color=AppStyles.COLORS['accent']
            )
            self.status_label.grid(
                row=current_row, 
                column=0, 
                padx=AppStyles.SIZES['padding_medium'],
                pady=(0, AppStyles.SIZES['padding_small']),
                sticky="w"
            )
            current_row += 1
            
            # 表示切り替えボタン（エージェントメッセージのみ）
            if self.enable_markdown:
                self.setup_view_toggle(current_row)
                current_row += 1
        
        # コンテンツ表示
        self.setup_content_display(current_row)
        
        # ユーザーメッセージの場合は即座にコンテンツを設定
        if self.is_user:
            self.content_widget.configure(state="disabled")
    
    def setup_view_toggle(self, row):
        """表示切り替えボタンをセットアップ"""
        button_frame = ctk.CTkFrame(self, fg_color="transparent")
        button_frame.grid(
            row=row, 
            column=0, 
            padx=AppStyles.SIZES['padding_medium'],
            pady=(0, AppStyles.SIZES['padding_small']),
            sticky="w"
        )
        
        style = AppStyles.get_button_style('outline').copy()
        style['font'] = AppStyles.FONTS['small']
        style['height'] = 25
        
        self.toggle_view_button = ctk.CTkButton(
            button_frame,
            text="📝 Raw Text",
            command=self.toggle_view_mode,
            width=100,
            **style
        )
        self.toggle_view_button.grid(row=0, column=0, sticky="w")
    
    def toggle_view_mode(self):
        """表示モードを切り替え"""
        self.is_markdown_view = not self.is_markdown_view
        
        if self.is_markdown_view:
            self.toggle_view_button.configure(text="📝 Raw Text")
        else:
            self.toggle_view_button.configure(text="🎨 Markdown")
        
        # コンテンツウィジェットを再作成
        if hasattr(self, 'content_widget'):
            self.content_widget.destroy()
        
        self.setup_content_display(3 if not self.is_user else 1)
        
        # 現在のコンテンツを再設定
        if self.content:
            if self.enable_markdown and not self.is_user and self.is_markdown_view:
                self.content_widget.set_content(self.content)
            else:
                self.content_widget.configure(state="normal")
                self.content_widget.delete("1.0", "end")
                self.content_widget.insert("1.0", self.content)
                self.content_widget.configure(state="disabled")
    
    def setup_content_display(self, row):
        """コンテンツ表示をセットアップ"""
        if self.enable_markdown and not self.is_user and self.is_markdown_view:
            # Markdownレンダラーを使用
            self.content_widget = MarkdownRenderer(self)
        else:
            # 通常のテキストボックスを使用
            self.content_widget = ctk.CTkTextbox(
                self,
                height=100,
                font=AppStyles.FONTS['default'],
                corner_radius=AppStyles.SIZES['corner_radius'],
                wrap="word"
            )
        
        self.content_widget.grid(
            row=row, 
            column=0, 
            padx=AppStyles.SIZES['padding_medium'],
            pady=(0, AppStyles.SIZES['padding_medium']),
            sticky="ew"
        )
    
    def update_content(self, new_text):
        """コンテンツを更新（ストリーミング用）"""
        self.content += new_text
        
        if self.enable_markdown and not self.is_user and self.is_markdown_view:
            # Markdownレンダラーでの更新
            self.content_widget.update_content(new_text)
        else:
            # テキストボックスでの更新
            self.content_widget.configure(state="normal")
            self.content_widget.insert("end", new_text)
            self.content_widget.configure(state="disabled")
            
            # 自動スクロール
            self.content_widget.see("end")
        
        # 高さを調整（テキストボックスの場合のみ）
        if not (self.enable_markdown and not self.is_user and self.is_markdown_view):
            lines = self.content.count('\n') + 1
            height = min(max(lines * 20 + 50, 100), 400)
            self.content_widget.configure(height=height)
    
    def set_content(self, content):
        """コンテンツを一括設定（通常メッセージ用）"""
        self.content = content
        
        if self.enable_markdown and not self.is_user and self.is_markdown_view:
            # Markdownレンダラーでの設定
            self.content_widget.set_content(content)
        else:
            # テキストボックスでの設定
            self.content_widget.configure(state="normal")
            self.content_widget.delete("1.0", "end")
            self.content_widget.insert("1.0", content)
            self.content_widget.configure(state="disabled")
        
        # 高さを調整（テキストボックスの場合のみ）
        if not (self.enable_markdown and not self.is_user and self.is_markdown_view):
            lines = content.count('\n') + 1
            height = min(max(lines * 20 + 50, 100), 400)
            self.content_widget.configure(height=height)
    
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