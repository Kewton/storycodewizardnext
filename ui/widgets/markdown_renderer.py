"""
Markdown Renderer Widget
Markdown記法対応テキスト表示用カスタムウィジェット
"""
import customtkinter as ctk
import tkinter as tk
from tkinter import font
import markdown
from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatters import get_formatter_by_name
from pygments.util import ClassNotFound
import re
from ui.styles import AppStyles

class MarkdownRenderer(ctk.CTkFrame):
    """Markdown記法対応テキスト表示ウィジェット"""
    
    def __init__(self, parent, content="", **kwargs):
        super().__init__(parent, fg_color="transparent", **kwargs)
        
        self.content = content
        self.text_widget = None
        
        self.setup_ui()
        if content:
            self.set_content(content)
    
    def setup_ui(self):
        """UIコンポーネントをセットアップ"""
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        # スクロール可能なテキストウィジェット
        self.text_widget = tk.Text(
            self,
            wrap=tk.WORD,
            state=tk.DISABLED,
            bg=AppStyles.COLORS['surface'],
            fg=AppStyles.COLORS['text'],
            font=AppStyles.FONTS['default'],
            selectbackground=AppStyles.COLORS['primary'],
            selectforeground=AppStyles.COLORS['text'],
            borderwidth=0,
            highlightthickness=0,
            padx=AppStyles.SIZES['padding_medium'],
            pady=AppStyles.SIZES['padding_medium']
        )
        self.text_widget.grid(row=0, column=0, sticky="nsew")
        
        # スクロールバー
        scrollbar = ctk.CTkScrollbar(self, command=self.text_widget.yview)
        scrollbar.grid(row=0, column=1, sticky="ns")
        self.text_widget.configure(yscrollcommand=scrollbar.set)
        
        # テキストスタイルを設定
        self.setup_text_styles()
    
    def setup_text_styles(self):
        """テキストスタイルを設定"""
        # フォント設定
        default_font = font.Font(family="Helvetica", size=13)
        heading_font = font.Font(family="Helvetica", size=18, weight="bold")
        subheading_font = font.Font(family="Helvetica", size=16, weight="bold")
        small_heading_font = font.Font(family="Helvetica", size=14, weight="bold")
        code_font = font.Font(family="Courier New", size=12)
        bold_font = font.Font(family="Helvetica", size=13, weight="bold")
        italic_font = font.Font(family="Helvetica", size=13, slant="italic")
        
        # スタイルタグを設定
        self.text_widget.tag_configure("h1", font=heading_font, foreground=AppStyles.COLORS['accent'], spacing1=10, spacing3=5)
        self.text_widget.tag_configure("h2", font=subheading_font, foreground=AppStyles.COLORS['accent'], spacing1=8, spacing3=4)
        self.text_widget.tag_configure("h3", font=small_heading_font, foreground=AppStyles.COLORS['accent'], spacing1=6, spacing3=3)
        self.text_widget.tag_configure("h4", font=small_heading_font, foreground=AppStyles.COLORS['text'], spacing1=4, spacing3=2)
        self.text_widget.tag_configure("h5", font=bold_font, foreground=AppStyles.COLORS['text'], spacing1=3, spacing3=2)
        self.text_widget.tag_configure("h6", font=bold_font, foreground=AppStyles.COLORS['text_secondary'], spacing1=2, spacing3=1)
        
        self.text_widget.tag_configure("bold", font=bold_font)
        self.text_widget.tag_configure("italic", font=italic_font)
        self.text_widget.tag_configure("code", font=code_font, background=AppStyles.COLORS['surface_light'], foreground=AppStyles.COLORS['accent'])
        self.text_widget.tag_configure("code_block", font=code_font, background=AppStyles.COLORS['surface_light'], foreground=AppStyles.COLORS['text'], lmargin1=20, lmargin2=20, spacing1=5, spacing3=5)
        
        self.text_widget.tag_configure("blockquote", foreground=AppStyles.COLORS['text_secondary'], lmargin1=20, lmargin2=20, borderwidth=2, relief="solid")
        self.text_widget.tag_configure("list_item", lmargin1=20, lmargin2=30)
        self.text_widget.tag_configure("link", foreground=AppStyles.COLORS['primary'], underline=True)
        self.text_widget.tag_configure("hr", background=AppStyles.COLORS['border'])
    
    def set_content(self, content):
        """Markdownコンテンツを設定"""
        self.content = content
        self.render_markdown()
    
    def update_content(self, additional_content):
        """コンテンツを追加（ストリーミング用）"""
        self.content += additional_content
        self.render_markdown()
    
    def render_markdown(self):
        """Markdownをレンダリング"""
        self.text_widget.config(state=tk.NORMAL)
        self.text_widget.delete(1.0, tk.END)
        
        if not self.content.strip():
            self.text_widget.config(state=tk.DISABLED)
            return
        
        # Markdownを解析して表示
        self.parse_and_render_markdown(self.content)
        
        self.text_widget.config(state=tk.DISABLED)
        self.text_widget.see(tk.END)
    
    def parse_and_render_markdown(self, content):
        """Markdownを解析してレンダリング"""
        lines = content.split('\n')
        i = 0
        
        while i < len(lines):
            line = lines[i]
            
            # 見出し
            if line.startswith('#'):
                level = len(line) - len(line.lstrip('#'))
                if level <= 6:
                    text = line[level:].strip()
                    self.insert_with_tag(text + '\n', f"h{level}")
                    i += 1
                    continue
            
            # コードブロック
            if line.strip().startswith('```'):
                language = line.strip()[3:].strip()
                i += 1
                code_lines = []
                
                while i < len(lines) and not lines[i].strip().startswith('```'):
                    code_lines.append(lines[i])
                    i += 1
                
                if i < len(lines):  # 終了の```をスキップ
                    i += 1
                
                code_content = '\n'.join(code_lines)
                if code_content.strip():
                    self.insert_code_block(code_content, language)
                continue
            
            # 引用
            if line.strip().startswith('>'):
                quote_text = line[1:].strip()
                self.insert_with_tag(quote_text + '\n', "blockquote")
                i += 1
                continue
            
            # 水平線
            if line.strip() in ['---', '***', '___']:
                self.insert_with_tag('─' * 50 + '\n', "hr")
                i += 1
                continue
            
            # リスト項目
            if re.match(r'^[\s]*[-*+]\s', line) or re.match(r'^[\s]*\d+\.\s', line):
                list_text = re.sub(r'^[\s]*[-*+\d\.]\s*', '• ', line)
                self.insert_with_tag(list_text + '\n', "list_item")
                i += 1
                continue
            
            # 通常のテキスト（インライン記法を処理）
            if line.strip():
                self.parse_inline_markdown(line + '\n')
            else:
                self.text_widget.insert(tk.END, '\n')
            
            i += 1
    
    def parse_inline_markdown(self, text):
        """インライン記法を解析"""
        # **太字**
        text = re.sub(r'\*\*([^*]+)\*\*', lambda m: self.insert_styled_text(m.group(1), "bold"), text)
        
        # *斜体*
        text = re.sub(r'\*([^*]+)\*', lambda m: self.insert_styled_text(m.group(1), "italic"), text)
        
        # `コード`
        text = re.sub(r'`([^`]+)`', lambda m: self.insert_styled_text(m.group(1), "code"), text)
        
        # [リンク](URL)
        text = re.sub(r'\[([^\]]+)\]\([^)]+\)', lambda m: self.insert_styled_text(m.group(1), "link"), text)
        
        # 残りのテキストを挿入
        if isinstance(text, str):
            self.text_widget.insert(tk.END, text)
    
    def insert_styled_text(self, text, style):
        """スタイル付きテキストを挿入"""
        start_pos = self.text_widget.index(tk.END)
        self.text_widget.insert(tk.END, text)
        end_pos = self.text_widget.index(tk.END)
        self.text_widget.tag_add(style, start_pos, end_pos)
        return ""  # 正規表現の置換用
    
    def insert_with_tag(self, text, tag):
        """タグ付きテキストを挿入"""
        start_pos = self.text_widget.index(tk.END)
        self.text_widget.insert(tk.END, text)
        end_pos = self.text_widget.index(tk.END)
        self.text_widget.tag_add(tag, start_pos, end_pos)
    
    def insert_code_block(self, code, language=""):
        """コードブロックを挿入"""
        if language:
            try:
                # Pygmentsを使用してシンタックスハイライト
                lexer = get_lexer_by_name(language, stripall=True)
                formatter = get_formatter_by_name('text')
                highlighted_code = highlight(code, lexer, formatter)
                self.insert_with_tag(highlighted_code + '\n', "code_block")
            except ClassNotFound:
                # 言語が見つからない場合は通常のコードブロックとして表示
                self.insert_with_tag(code + '\n', "code_block")
        else:
            self.insert_with_tag(code + '\n', "code_block")
    
    def get_content(self):
        """現在のコンテンツを取得"""
        return self.content
    
    def clear(self):
        """コンテンツをクリア"""
        self.content = ""
        self.text_widget.config(state=tk.NORMAL)
        self.text_widget.delete(1.0, tk.END)
        self.text_widget.config(state=tk.DISABLED)