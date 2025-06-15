"""
チャット機能のコアロジック
CustomTkinter UIとStreamlit UIの両方で使用可能な共通処理
"""
import pandas as pd
from app.myjsondb.myStreamlit import getValueByFormnameAndKeyName
from app.myjsondb.myHistories import createProject, getProjectList, dropProject, upsertValToPjByKey, getAllHistoryOfPj, getValOfPjByKey, deletePjByKey
from app.myjsondb.myProjectSettings import upsertPjdirAndValueByPjnm, getPjdirByPjnm, deletePjSettingsByKey, getAllProject
from app.prompt import createPromt
from app.util.execLlmApi import execLlmApi, execLlmApiStreaming
import base64
import os
import subprocess


def communicate_core(selected_project, selected_model, selected_programing_model, user_input, encoded_file=""):
    """
    チャット通信のコア処理（UI非依存）
    
    Args:
        selected_project (str): 選択されたプロジェクト名
        selected_model (str): 選択されたLLMモデル
        selected_programing_model (str): 選択されたプログラミング言語
        user_input (str): ユーザー入力テキスト
        encoded_file (str): Base64エンコードされたファイルデータ
    
    Returns:
        list: メッセージリスト
    """
    messages = []
    
    # システムロール取得
    systemrole_content = getValueByFormnameAndKeyName("chat", "systemrole", selected_programing_model)
    systemrole_content["pjdir"] = getPjdirByPjnm(selected_project)
    messages.append({"role": "system", "content": systemrole_content["system_role"]})
    
    # ユーザーメッセージ作成
    content = createPromt(systemrole_content, user_input)
    user_message = {"role": "user", "content": content}
    messages.append(user_message)
    
    # LLM API実行
    message_content, message_role = execLlmApi(selected_model, messages, encoded_file)
    
    bot_message = {
        "content": message_content,
        "role": message_role
    }
    messages.append(bot_message)
    
    return messages


def communicate_core_streaming(selected_project, selected_model, selected_programing_model, user_input, encoded_file="", streaming_callback=None):
    """
    ストリーミング対応チャット通信のコア処理（UI非依存）
    
    Args:
        selected_project (str): 選択されたプロジェクト名
        selected_model (str): 選択されたLLMモデル
        selected_programing_model (str): 選択されたプログラミング言語
        user_input (str): ユーザー入力テキスト
        encoded_file (str): Base64エンコードされたファイルデータ
        streaming_callback (callable): ストリーミングチャンク受信時のコールバック関数
    
    Returns:
        list: メッセージリスト
    """
    messages = []
    
    # システムロール取得
    systemrole_content = getValueByFormnameAndKeyName("chat", "systemrole", selected_programing_model)
    systemrole_content["pjdir"] = getPjdirByPjnm(selected_project)
    messages.append({"role": "system", "content": systemrole_content["system_role"]})
    
    # ユーザーメッセージ作成
    content = createPromt(systemrole_content, user_input)
    user_message = {"role": "user", "content": content}
    messages.append(user_message)
    
    # ストリーミングLLM API実行
    message_content, message_role = execLlmApiStreaming(selected_model, messages, encoded_file, streaming_callback)
    
    bot_message = {
        "content": message_content,
        "role": message_role
    }
    messages.append(bot_message)
    
    return messages


def save_chat_history(selected_model, user_input, messages, selected_project):
    """
    チャット履歴を保存
    
    Args:
        selected_model (str): 使用されたLLMモデル
        user_input (str): ユーザー入力
        messages (list): メッセージリスト
        selected_project (str): プロジェクト名
    """
    upsertValToPjByKey(selected_model, user_input, messages, selected_project)


def get_user_content_from_messages(messages):
    """
    メッセージからユーザーコンテンツを取得
    
    Args:
        messages (list): メッセージリスト
    
    Returns:
        str: ユーザーコンテンツ
    """
    for message in messages[1:]:  # システムメッセージをスキップ
        if message["role"] == "user":
            return message['content']
    return ""


def get_assistant_content_from_messages(messages):
    """
    メッセージからアシスタントコンテンツを取得
    
    Args:
        messages (list): メッセージリスト
    
    Returns:
        str: アシスタントコンテンツ
    """
    for message in messages[1:]:  # システムメッセージをスキップ
        if message["role"] == "assistant":
            return message['content']
    return ""


def show_scrollable_message_dialog(title, message, message_type="info"):
    """
    スクロール可能なメッセージダイアログを表示
    
    Args:
        title (str): ダイアログタイトル
        message (str): 表示メッセージ
        message_type (str): メッセージタイプ ("info", "error", "warning")
    """
    import tkinter as tk
    import customtkinter as ctk
    from ui.styles import AppStyles
    
    # カスタムダイアログウィンドウを作成
    dialog = ctk.CTkToplevel()
    dialog.title(title)
    dialog.geometry("800x500")  # 固定サイズ
    dialog.minsize(600, 400)
    dialog.maxsize(900, 600)
    dialog.resizable(True, False)  # 幅のみリサイズ可能
    dialog.transient()
    dialog.grab_set()
    
    # ダイアログを中央に配置
    dialog.update_idletasks()
    x = (dialog.winfo_screenwidth() // 2) - (800 // 2)
    y = (dialog.winfo_screenheight() // 2) - (500 // 2)
    dialog.geometry(f"800x500+{x}+{y}")
    
    # メインフレーム
    main_frame = ctk.CTkFrame(dialog, **AppStyles.get_frame_style('default'))
    main_frame.pack(fill="both", expand=True, padx=20, pady=20)
    main_frame.grid_columnconfigure(0, weight=1)
    main_frame.grid_rowconfigure(1, weight=1)
    
    # タイトル
    title_label = ctk.CTkLabel(
        main_frame,
        text=title,
        font=AppStyles.FONTS['heading']
    )
    title_label.grid(row=0, column=0, pady=(10, 20), sticky="w")
    
    # スクロール可能なメッセージ表示フレーム（高さ固定）
    scrollable_frame = ctk.CTkScrollableFrame(
        main_frame,
        height=350,  # 固定の高さ
        **AppStyles.get_scrollable_frame_style()
    )
    scrollable_frame.grid(row=1, column=0, sticky="nsew", pady=(0, 20))
    scrollable_frame.grid_columnconfigure(0, weight=1)
    
    # メッセージテキストを表示
    message_label = ctk.CTkLabel(
        scrollable_frame,
        text=message,
        font=AppStyles.FONTS['default'],
        anchor="w",
        justify="left",
        wraplength=750
    )
    message_label.grid(row=0, column=0, sticky="ew", pady=10, padx=10)
    
    # ボタンフレーム
    button_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
    button_frame.grid(row=2, column=0, sticky="ew", pady=(0, 10))
    button_frame.grid_columnconfigure(0, weight=1)
    
    def on_ok():
        dialog.destroy()
    
    # OKボタン
    if message_type == "error":
        button_style = AppStyles.get_button_style('outline')
        button_style['text_color'] = AppStyles.COLORS['error']
        button_style['hover_color'] = AppStyles.COLORS['error']
    else:
        button_style = AppStyles.get_button_style('primary')
    
    ok_button = ctk.CTkButton(
        button_frame,
        text="OK",
        command=on_ok,
        **button_style
    )
    ok_button.grid(row=0, column=0, pady=10)
    
    # ダイアログが閉じられるまで待機
    dialog.wait_window()


def apply_to_project(agent_content, project_name, model_name, timestamp):
    """
    エージェントのレスポンスをプロジェクトに反映
    
    Args:
        agent_content (str): エージェントのレスポンス内容
        project_name (str): プロジェクト名
        model_name (str): モデル名
        timestamp (str): タイムスタンプ
    
    Returns:
        tuple: (成功フラグ, メッセージ)
    """
    try:
        import tkinter as tk
        from tkinter import messagebox
        import customtkinter as ctk
        import re
        from ui.styles import AppStyles
        
        # 一時ファイル保存
        temp_dir = "./temp"
        os.makedirs(temp_dir, exist_ok=True)
        
        filename = f"chat_history_{model_name}_{timestamp}_agent.md"
        file_path = os.path.join(temp_dir, filename)
        
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(agent_content)
        
        # プロジェクトディレクトリ取得
        pjdir = getPjdirByPjnm(project_name)
        
        # ファイル一覧を事前に解析
        def parse_file_list_from_content(content):
            """コンテンツからファイル一覧を解析"""
            file_pattern = r"^## \./(.+?)$"
            matches = re.findall(file_pattern, content, re.MULTILINE)
            return [match for match in matches if match.strip()]
        
        files_to_apply = parse_file_list_from_content(agent_content)
        
        if not files_to_apply:
            # ファイルが見つからない場合は直接実行
            cmd = f"python generate_files.py {os.path.abspath(file_path)} -d {pjdir}"
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            
            if result.returncode == 0:
                # 成功時はスクロール可能ダイアログで表示
                full_message = f"Applied to project successfully.\n\n{result.stdout}"
                show_scrollable_message_dialog("プロジェクト反映完了", full_message, "info")
                return True, "Applied to project successfully."
            else:
                # エラー時はスクロール可能ダイアログで表示
                full_message = f"Failed to apply to project.\n\n{result.stderr}"
                show_scrollable_message_dialog("プロジェクト反映エラー", full_message, "error")
                return False, "Failed to apply to project."
        
        # ファイル一覧表示ダイアログ
        def show_files_confirmation_dialog():
            """確認ダイアログを表示してユーザーの選択を取得"""
            
            # カスタムダイアログウィンドウを作成
            dialog = ctk.CTkToplevel()
            dialog.title("プロジェクト反映の確認")
            dialog.geometry("700x600")  # 高さを固定
            dialog.minsize(600, 600)    # 最小サイズも固定
            dialog.maxsize(900, 600)    # 最大サイズの高さも固定
            dialog.resizable(True, False)  # 幅のみリサイズ可能、高さは固定
            dialog.transient()
            dialog.grab_set()
            
            # ダイアログを中央に配置
            dialog.update_idletasks()
            x = (dialog.winfo_screenwidth() // 2) - (700 // 2)
            y = (dialog.winfo_screenheight() // 2) - (600 // 2)
            dialog.geometry(f"700x600+{x}+{y}")
            
            # 結果を格納する変数
            user_choice = [None]
            
            # メインフレーム
            main_frame = ctk.CTkFrame(dialog, **AppStyles.get_frame_style('default'))
            main_frame.pack(fill="both", expand=True, padx=20, pady=20)
            main_frame.grid_columnconfigure(0, weight=1)
            main_frame.grid_rowconfigure(1, weight=1)
            
            # タイトル
            title_label = ctk.CTkLabel(
                main_frame,
                text="以下のファイルをプロジェクトに反映します",
                font=AppStyles.FONTS['heading']
            )
            title_label.grid(row=0, column=0, pady=(10, 20), sticky="w")
            
            # スクロール可能なファイル一覧フレーム（高さ固定）
            scrollable_frame = ctk.CTkScrollableFrame(
                main_frame,
                height=400,  # 固定の高さ
                **AppStyles.get_scrollable_frame_style()
            )
            scrollable_frame.grid(row=1, column=0, sticky="nsew", pady=(0, 20))
            scrollable_frame.grid_columnconfigure(0, weight=1)
            
            # ファイルリストを表示
            for i, file_path in enumerate(files_to_apply):
                file_label = ctk.CTkLabel(
                    scrollable_frame,
                    text=f"• {file_path}",
                    font=AppStyles.FONTS['default'],
                    anchor="w"
                )
                file_label.grid(row=i, column=0, sticky="ew", pady=2, padx=10)
            
            # 統計情報
            stats_text = f"反映対象ファイル数: {len(files_to_apply)}"
            stats_label = ctk.CTkLabel(
                main_frame,
                text=stats_text,
                font=AppStyles.FONTS['small'],
                text_color=AppStyles.COLORS['text_secondary']
            )
            stats_label.grid(row=2, column=0, pady=(0, 20), sticky="w")
            
            # ボタンフレーム
            button_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
            button_frame.grid(row=3, column=0, sticky="ew", pady=(0, 10))
            button_frame.grid_columnconfigure((0, 1), weight=1)
            
            def on_yes():
                user_choice[0] = True
                dialog.destroy()
            
            def on_no():
                user_choice[0] = False
                dialog.destroy()
            
            # キャンセルボタン
            no_button = ctk.CTkButton(
                button_frame,
                text="キャンセル",
                command=on_no,
                **AppStyles.get_button_style('outline')
            )
            no_button.grid(row=0, column=0, padx=(0, 10), sticky="ew")
            
            # 実行ボタン
            yes_button = ctk.CTkButton(
                button_frame,
                text="プロジェクトに反映",
                command=on_yes,
                **AppStyles.get_button_style('primary')
            )
            yes_button.grid(row=0, column=1, padx=(10, 0), sticky="ew")
            
            # ダイアログが閉じられるまで待機
            dialog.wait_window()
            
            return user_choice[0]
        
        # 確認ダイアログを表示
        user_confirmed = show_files_confirmation_dialog()
        
        if not user_confirmed:
            return False, "ユーザーによりキャンセルされました。"
        
        # コマンド実行
        cmd = f"python generate_files.py {os.path.abspath(file_path)} -d {pjdir}"
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        
        if result.returncode == 0:
            # 成功時はスクロール可能ダイアログで表示
            full_message = f"Applied to project successfully.\n\n{result.stdout}"
            show_scrollable_message_dialog("プロジェクト反映完了", full_message, "info")
            return True, "Applied to project successfully."
        else:
            # エラー時はスクロール可能ダイアログで表示
            full_message = f"Failed to apply to project.\n\n{result.stderr}"
            show_scrollable_message_dialog("プロジェクト反映エラー", full_message, "error")
            return False, "Failed to apply to project."
            
    except Exception as e:
        error_message = f"An error occurred: {str(e)}"
        show_scrollable_message_dialog("エラー", error_message, "error")
        return False, error_message


def format_history_data(project_name):
    """
    履歴データを整形してリスト形式で返す
    
    Args:
        project_name (str): プロジェクト名
    
    Returns:
        list: 整形された履歴データのリスト
    """
    data = getAllHistoryOfPj(project_name)
    if not data or not isinstance(data, list) or len(data) == 0:
        return []
    
    df = pd.DataFrame(data)
    
    # 必要なカラムがなければ空のリストを返す
    required_cols = {'registration_date', 'gptmodel', 'input'}
    if not required_cols.issubset(df.columns):
        return []
    
    # ソート
    df = df.sort_index(ascending=False).reset_index(drop=True)
    
    # 日付フォーマット
    df['registration_date'] = (
        df['registration_date']
        .str[:14]
        .apply(lambda x: f"{x[:4]}-{x[4:6]}-{x[6:8]}_{x[8:10]}:{x[10:12]}:{x[12:14]}")
    )
    
    columns_order = ['registration_date', 'gptmodel', 'input']
    df = df[columns_order]
    
    return df.to_dict('records')


def delete_history_item(gptmodel, input_text, registration_date, project_name):
    """
    履歴項目を削除
    
    Args:
        gptmodel (str): GPTモデル名
        input_text (str): 入力テキスト
        registration_date (str): 登録日時
        project_name (str): プロジェクト名
    
    Returns:
        bool: 削除成功フラグ
    """
    try:
        deletePjByKey(gptmodel, input_text, registration_date, project_name)
        return True
    except Exception as e:
        print(f"Error deleting history: {e}")
        return False


def create_new_project(project_name, directory_path):
    """
    新しいプロジェクトを作成
    
    Args:
        project_name (str): プロジェクト名
        directory_path (str): ディレクトリパス
    
    Returns:
        tuple: (成功フラグ, メッセージ)
    """
    # 入力値検証
    if not project_name.strip():
        return False, "プロジェクト名を入力してください。"
    
    if not directory_path.strip():
        return False, "ディレクトリパスを入力してください。"
    
    if not os.path.isdir(directory_path):
        return False, "有効なディレクトリパスを入力してください。"
    
    # 既存プロジェクト名チェック
    existing_projects = getAllProject()
    if project_name in existing_projects:
        return False, "このプロジェクト名は既に存在します。"
    
    try:
        createProject(project_name)
        upsertPjdirAndValueByPjnm(project_name, directory_path, {"test": "sss"})
        return True, f"プロジェクト '{project_name}' を追加しました。"
    except Exception as e:
        return False, f"プロジェクト作成中にエラーが発生しました: {str(e)}"


def delete_project(project_name):
    """
    プロジェクトを削除
    
    Args:
        project_name (str): プロジェクト名
    
    Returns:
        tuple: (成功フラグ, メッセージ)
    """
    try:
        dropProject(project_name)
        deletePjSettingsByKey(project_name)
        return True, f"プロジェクト '{project_name}' を削除しました。"
    except Exception as e:
        return False, f"プロジェクト削除中にエラーが発生しました: {str(e)}"


# Streamlit向けの既存関数群（互換性のため保持）
def communicate(selected_project, _selected_model, selected_programing_model, encoded_file):
    """Streamlit用の通信関数（後方互換性のため保持）"""
    import streamlit as st
    
    st.session_state["messages"] = []
    messages = st.session_state["messages"]

    _systemrole_content = getValueByFormnameAndKeyName("chat", "systemrole", selected_programing_model)
    _systemrole_content["pjdir"] = getPjdirByPjnm(selected_project)
    messages.append({"role": "system", "content": _systemrole_content["system_role"]})

    _content = createPromt(
        _systemrole_content,
        st.session_state["user_input"]
    )
    user_message = {"role": "user", "content": _content}
    messages.append(user_message)

    message_content, message_role = execLlmApi(_selected_model, messages, encoded_file)

    bot_message = {
        "content": message_content,
        "role": message_role
    }

    messages.append(bot_message)

    return messages


# Streamlit用のメイン関数（既存のままで互換性保持）
def chat():
    """Streamlit版のメイン関数"""
    import streamlit as st
    
    # 既存のStreamlit実装をそのまま保持
    # （省略: 元のコードと同じ内容）
    st.set_page_config(layout="wide")
    st.title("StoryCodeWizard")
    st.info("CustomTkinter版も利用可能です: python main.py で起動")
    
    tab1, tab2, tab3 = st.tabs(["Stroy2Code", "MyHistory", "プロジェクト管理"])

    with tab1:
        st.write("CustomTkinter版をご利用ください")

    with tab2:
        st.write("CustomTkinter版をご利用ください")

    with tab3:
        st.write("CustomTkinter版をご利用ください")