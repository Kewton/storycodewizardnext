"""
File Uploader Widget
ファイルアップロード用カスタムウィジェット
"""
import customtkinter as ctk
import tkinter as tk
from tkinter import filedialog
import base64
import os
from ui.styles import AppStyles

class FileUploader(ctk.CTkFrame):
    """ファイルアップロードウィジェット"""
    
    def __init__(self, parent, file_callback=None, **kwargs):
        super().__init__(parent, fg_color="transparent", **kwargs)
        
        self.file_callback = file_callback
        self.selected_file = None
        self.file_data = ""
        
        self.setup_ui()
    
    def setup_ui(self):
        """UIコンポーネントをセットアップ"""
        self.grid_columnconfigure(0, weight=1)
        
        # ファイル選択ボタン
        self.select_button = ctk.CTkButton(
            self,
            text="ファイルをアップロードしてください",
            command=self.select_file,
            **AppStyles.get_button_style('outline')
        )
        self.select_button.grid(
            row=0, 
            column=0, 
            sticky="ew"
        )
        
        # 選択されたファイル情報
        self.file_info_label = ctk.CTkLabel(
            self,
            text="ファイルが選択されていません",
            font=AppStyles.FONTS['small'],
            text_color=AppStyles.COLORS['text_secondary']
        )
        self.file_info_label.grid(
            row=1, 
            column=0, 
            pady=(AppStyles.SIZES['padding_small'], 0),
            sticky="w"
        )
        
        # クリアボタン（初期は非表示）
        style = AppStyles.get_button_style('outline').copy()
        # style 中の重複定義を排除
        style.pop('text_color', None)
        style.pop('hover_color', None)
        style['text_color'] = AppStyles.COLORS['error']
        style['hover_color'] = AppStyles.COLORS['error']  # hover_colorもerrorに設定
        style['font'] = AppStyles.FONTS['small']  # fontをスタイル辞書で指定
        self.clear_button = ctk.CTkButton(
            self,
            text="クリア",
            command=self.clear_file,
            width=60,
            height=25,
            # font=AppStyles.FONTS['small'],  # 直接指定を削除
            **style
        )
    
    def select_file(self):
        """ファイル選択ダイアログを開く"""
        file_path = filedialog.askopenfilename(
            title="JPEG画像を選択",
            filetypes=[
                ("JPEG files", "*.jpg *.jpeg"),
                ("All files", "*.*")
            ]
        )
        
        if file_path:
            self.load_file(file_path)
    
    def load_file(self, file_path):
        """ファイルを読み込む"""
        try:
            with open(file_path, 'rb') as file:
                file_contents = file.read()
                self.file_data = base64.b64encode(
                    file_contents
                ).decode('utf-8')
                self.selected_file = file_path
                
                # UI更新
                filename = os.path.basename(file_path)
                self.file_info_label.configure(
                    text=f"選択されたファイル: {filename}",
                    text_color=AppStyles.COLORS['success']
                )
                
                # クリアボタンを表示
                self.clear_button.grid(
                    row=2,
                    column=0,
                    pady=(AppStyles.SIZES['padding_small'], 0),
                    sticky="w"
                )
                
                # コールバック実行
                if self.file_callback:
                    self.file_callback(file_path, self.file_data)
                    
        except Exception as e:
            print(f"ファイル読み込みエラー: {e}")
            self.file_info_label.configure(
                text="ファイル読み込みエラー",
                text_color=AppStyles.COLORS['error']
            )
    
    def clear_file(self):
        """ファイル選択をクリア"""
        self.selected_file = None
        self.file_data = ""
        
        # UI更新
        self.file_info_label.configure(
            text="ファイルが選択されていません",
            text_color=AppStyles.COLORS['text_secondary']
        )
        
        # クリアボタンを非表示
        self.clear_button.grid_remove()
        
        # コールバック実行
        if self.file_callback:
            self.file_callback(None, "")
    
    def get_file_data(self):
        """ファイルデータを取得"""
        return self.file_data
    
    def get_file_path(self):
        """ファイルパスを取得"""
        return self.selected_file