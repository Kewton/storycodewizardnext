"""
StoryCodeWizard - CustomTkinter Desktop Application
メインアプリケーションエントリーポイント
"""
import customtkinter as ctk
import sys
import os
import subprocess
from ui.main_window import MainWindow
from ui.styles import AppStyles

def check_and_initialize_database():
    """
    データベースディレクトリの存在確認と自動初期化
    mydbディレクトリが存在しない場合、initdatabase.pyを実行する
    
    Returns:
        bool: 初期化成功時True、失敗時False
    """
    mydb_path = "./mydb"
    
    # mydbディレクトリが存在するかチェック
    if not os.path.exists(mydb_path):
        print("データベースディレクトリが見つかりません。初期セットアップを開始します...")
        
        try:
            # initdatabase.pyの存在確認
            init_script = "./initdatabase.py"
            if not os.path.exists(init_script):
                print(f"エラー: {init_script} が見つかりません。")
                return False
            
            # initdatabase.pyを実行
            print("python initdatabase.py を実行中...")
            result = subprocess.run(
                [sys.executable, "initdatabase.py"],
                capture_output=True,
                text=True,
                cwd="."
            )
            
            if result.returncode == 0:
                print("データベースの初期化が完了しました。")
                
                # mydbディレクトリが正常に作成されたか確認
                if os.path.exists(mydb_path):
                    print("データベースディレクトリの作成を確認しました。")
                    return True
                else:
                    print("警告: データベース初期化は成功しましたが、mydbディレクトリが見つかりません。")
                    return False
            else:
                print(f"データベース初期化中にエラーが発生しました:")
                print(f"stdout: {result.stdout}")
                print(f"stderr: {result.stderr}")
                return False
                
        except subprocess.CalledProcessError as e:
            print(f"データベース初期化の実行中にエラーが発生しました: {e}")
            return False
        except Exception as e:
            print(f"予期しないエラーが発生しました: {e}")
            return False
    else:
        print("データベースディレクトリが見つかりました。")
        return True

def main():
    """
    アプリケーションのメインエントリーポイント
    CustomTkinterアプリケーションを初期化して起動
    """
    # データベースの初期化チェック
    if not check_and_initialize_database():
        print("データベースの初期化に失敗しました。アプリケーションを終了します。")
        print("\n手動でデータベースを初期化するには以下のコマンドを実行してください:")
        print("python initdatabase.py")
        sys.exit(1)
    
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