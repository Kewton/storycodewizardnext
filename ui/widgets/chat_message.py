"""
Chat Message Widget
チャットメッセージ表示用カスタムウィジェット
"""
import customtkinter as ctk
import tkinter as tk
from ui.styles import AppStyles

class ChatMessage(ctk.CTkFrame):
    """チャットメッセージ表示ウィジェット"""
    
    def __init__(self, parent, speaker, content, is_user=False, **kwargs):
        super().__init__(parent, **kwargs)
        
        self.speaker = speaker
        self.content = content
        self.is_user = is_user
        
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
        
        # コンテンツ表示
        if self.is_user:
            # ユーザーメッセージは折りたたみ可能
            self.setup_collapsible_content()
        else:
            # エージェントメッセージは常に表示
            self.setup_regular_content()
    
    def setup_collapsible_content(self):
        """折りたたみ可能なコンテンツをセットアップ"""
        self.is_expanded = False
        
        # 折りたたみボタン
        style = AppStyles.get_button_style('outline').copy()
        style['font'] = AppStyles.FONTS['small'] # fontをスタイル辞書で指定
        self.toggle_button = ctk.CTkButton(
            self,
            text="▶ Show Content",
            command=self.toggle_content,
            height=25,
            # font=AppStyles.FONTS['small'], # 直接指定を削除
            **style
        )
        self.toggle_button.grid(
            row=1, 
            column=0, 
            padx=AppStyles.SIZES['padding_medium'],
            pady=(0, AppStyles.SIZES['padding_small']),
            sticky="w"
        )
        
        # コンテンツフレーム（初期は非表示）
        self.content_frame = ctk.CTkFrame(self, fg_color="transparent")
    
    def setup_regular_content(self):
        """通常のコンテンツをセットアップ"""
        # コンテンツテキスト
        self.content_text = ctk.CTkTextbox(
            self,
            height=min(max(self.content.count('\n') * 20 + 50, 100), 400),
            font=AppStyles.FONTS['default'],
            corner_radius=AppStyles.SIZES['corner_radius'],
            wrap="word"
        )
        self.content_text.grid(
            row=1, 
            column=0, 
            padx=AppStyles.SIZES['padding_medium'],
            pady=(0, AppStyles.SIZES['padding_medium']),
            sticky="ew"
        )
        
        # コンテンツを挿入（編集不可）
        self.content_text.insert("1.0", self.content)
        self.content_text.configure(state="disabled")
    
    def toggle_content(self):
        """コンテンツの表示/非表示を切り替え"""
        if self.is_expanded:
            # 折りたたむ
            self.content_frame.grid_remove()
            self.toggle_button.configure(text="▶ Show Content")
            self.is_expanded = False
        else:
            # 展開する
            if not hasattr(self, '_content_created'):
                self.create_collapsible_content()
                self._content_created = True
            
            self.content_frame.grid(
                row=2, 
                column=0, 
                padx=AppStyles.SIZES['padding_medium'],
                pady=(0, AppStyles.SIZES['padding_medium']),
                sticky="ew"
            )
            self.toggle_button.configure(text="▼ Hide Content")
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