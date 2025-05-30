"""
StoryCodeWizard - CustomTkinter Desktop Application
メインアプリケーションエントリーポイント
"""
import customtkinter as ctk
import sys
import os
from ui.main_window import MainWindow
from ui.styles import AppStyles

def main():
    """
    アプリケーションのメインエントリーポイント
    CustomTkinterアプリケーションを初期化して起動
    """
    # CustomTkinterの外観設定
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")
    
    # アプリケーションスタイルを初期化
    AppStyles.initialize()
    
    try:
        # メインウィンドウを作成して起動
        app = MainWindow()
        app.mainloop()
    except KeyboardInterrupt:
        print("\nアプリケーションが中断されました")
        sys.exit(0)
    except Exception as e:
        print(f"アプリケーション実行中にエラーが発生しました: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()