"""
Chat Message Widget
チャットメッセージ表示用カスタムウィジェット（Markdown対応）
"""
import customtkinter as ctk
import tkinter as tk
from ui.styles import AppStyles
from ui.widgets.markdown_renderer import MarkdownRenderer

class ChatMessage(ctk.CTkFrame):
    """チャットメッセージ表示ウィジェット"""
    
    def __init__(self, parent, speaker, content, is_user=False, enable_markdown=True, **kwargs):
        super().__init__(parent, **kwargs)
        
        self.speaker = speaker
        self.content = content
        self.is_user = is_user
        self.enable_markdown = enable_markdown and not is_user  # ユーザーメッセージはMarkdown無効
        
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
        
        # 表示切り替えボタン（エージェントメッセージのみ）
        if not self.is_user and self.enable_markdown:
            self.setup_view_toggle()
            current_row = 2
        else:
            current_row = 1
        
        # コンテンツ表示
        if self.is_user:
            # ユーザーメッセージは折りたたみ可能
            self.setup_collapsible_content(current_row)
        else:
            # エージェントメッセージは常に表示
            self.setup_regular_content(current_row)
    
    def setup_view_toggle(self):
        """表示切り替えボタンをセットアップ"""
        self.is_markdown_view = True
        
        button_frame = ctk.CTkFrame(self, fg_color="transparent")
        button_frame.grid(
            row=1, 
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
        
        # コンテンツを再作成
        if hasattr(self, 'content_widget'):
            self.content_widget.destroy()
        
        self.setup_regular_content(2)
    
    def setup_collapsible_content(self, start_row):
        """折りたたみ可能なコンテンツをセットアップ"""
        self.is_expanded = False
        
        # 折りたたみボタン
        style = AppStyles.get_button_style('outline').copy()
        style['font'] = AppStyles.FONTS['small']
        style['height'] = 25
        self.collapse_button = ctk.CTkButton(
            self,
            text="▶ Show Content",
            command=self.toggle_content,
            **style
        )
        self.collapse_button.grid(
            row=start_row, 
            column=0, 
            padx=AppStyles.SIZES['padding_medium'],
            pady=(0, AppStyles.SIZES['padding_small']),
            sticky="w"
        )
        
        # コンテンツフレーム（初期は非表示）
        self.content_frame = ctk.CTkFrame(self, fg_color="transparent")
    
    def setup_regular_content(self, start_row):
        """通常のコンテンツをセットアップ"""
        if self.enable_markdown and not self.is_user and hasattr(self, 'is_markdown_view') and self.is_markdown_view:
            # Markdownレンダラーを使用
            self.content_widget = MarkdownRenderer(
                self,
                content=self.content
            )
        else:
            # 通常のテキストボックスを使用
            self.content_widget = ctk.CTkTextbox(
                self,
                height=min(max(self.content.count('\n') * 20 + 50, 100), 400),
                font=AppStyles.FONTS['default'],
                corner_radius=AppStyles.SIZES['corner_radius'],
                wrap="word"
            )
            # コンテンツを挿入（編集不可）
            self.content_widget.insert("1.0", self.content)
            self.content_widget.configure(state="disabled")
        
        self.content_widget.grid(
            row=start_row, 
            column=0, 
            padx=AppStyles.SIZES['padding_medium'],
            pady=(0, AppStyles.SIZES['padding_medium']),
            sticky="ew"
        )
    
    def toggle_content(self):
        """コンテンツの表示/非表示を切り替え"""
        if self.is_expanded:
            # 折りたたむ
            self.content_frame.grid_remove()
            self.collapse_button.configure(text="▶ Show Content")
            self.is_expanded = False
        else:
            # 展開する
            if not hasattr(self, '_content_created'):
                self.create_collapsible_content()
                self._content_created = True
            
            self.content_frame.grid(
                row=3, 
                column=0, 
                padx=AppStyles.SIZES['padding_medium'],
                pady=(0, AppStyles.SIZES['padding_medium']),
                sticky="ew"
            )
            self.collapse_button.configure(text="▼ Hide Content")
            self.is_expanded = True
    
    def create_collapsible_content(self):
        """折りたたみ可能なコンテンツを作成"""
        self.content_frame.grid_columnconfigure(0, weight=1)
        
        # コンテンツテキスト
        content_text = ctk.CTkTextbox(
            self.content_frame,
            height=min(max(self.content.count('\n') * 20 + 50, 100), 300),
            font=AppStyles.FONTS['default'],
            corner_radius=AppStyles.SIZES['corner_radius'],
            wrap="word"
        )
        content_text.grid(row=0, column=0, sticky="ew")
        
        # コンテンツを挿入（編集不可）
        content_text.insert("1.0", self.content)
        content_text.configure(state="disabled")