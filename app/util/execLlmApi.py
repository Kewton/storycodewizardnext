import anthropic
import google.generativeai as genai  # New import
from google.generativeai.types import BlockedPromptException
from openai import OpenAI
from secret_keys import claude_api_key, gemini_api_key, openai_api_key


chatgptapi_client = OpenAI(
  api_key=openai_api_key
)


claude_client = anthropic.Anthropic(
    api_key=claude_api_key,
)


# gemini_client = genai.Client( # 古いクライアント初期化
#     api_key=gemini_api_key,
# )
genai.configure(api_key=gemini_api_key)  # New API key configuration


def isChatGptAPI(_selected_model):
    if "gpt" in _selected_model:
        return True
    else:
        return False


def isChatGPT_o1(_selected_model):
    if "o1" in _selected_model:
        return True
    else:
        return False


def isChatGPTImageAPI(_selected_model):
    if "gpt-4o" in _selected_model:
        return True
    elif "o1" in _selected_model:
        return True
    elif "o2" in _selected_model:
        return True
    elif "o3" in _selected_model:
        return True
    else:
        return False


def isGemini(_selected_model):
    if "gemini" in _selected_model:
        return True
    else:
        return False


def isClaude(_selected_model):
    if "claude" in _selected_model:
        return True
    else:
        return False


def buildInpurtMessages(_messages, encoded_file):
    _inpurt_messages = []
    _systemrole = ""
    for _rec in _messages:
        if _rec["role"] == "system":
            _systemrole = _rec["content"]
        elif _rec["role"] == "user":
            if len(encoded_file) > 0:
                print("append image")
                _content = []
                _content.append({
                    "type": "image",
                    "source": {
                        "type": "base64",
                        "media_type": "image/jpeg",
                        "data": encoded_file
                    }
                })
                _content.append({
                    "type": "text",
                    "text": _rec["content"]
                })
                
                _inpurt_messages.append(
                    {
                        "role": _rec["role"],
                        "content": _content
                    }
                )
            else:
                _inpurt_messages.append(_rec)

    return _inpurt_messages, _systemrole


def execLlmApi(_selected_model, _messages, encoded_file):
    if isChatGptAPI(_selected_model):
        if isChatGPTImageAPI(_selected_model) and len(encoded_file) > 0:
            processed_messages_non_streaming = []
            # メッセージ履歴を処理し、最後のユーザーメッセージに画像を追加
            for msg in _messages:
                if msg["role"] == "system":
                    processed_messages_non_streaming.append(msg)
                elif msg["role"] == "user":
                    # contentがリスト形式（例：他の画像やテキストパートを含む）か文字列かをチェック
                    if isinstance(msg["content"], list):
                        processed_messages_non_streaming.append(msg) 
                    else:  # 文字列の場合
                        processed_messages_non_streaming.append({"role": "user", "content": msg["content"]})
                else:  # assistant messages
                    processed_messages_non_streaming.append(msg)

            if encoded_file and processed_messages_non_streaming:
                last_user_msg_index = -1
                for i in range(len(processed_messages_non_streaming) - 1, -1, -1):
                    if processed_messages_non_streaming[i]["role"] == "user":
                        last_user_msg_index = i
                        break

                if last_user_msg_index != -1:
                    original_content = processed_messages_non_streaming[
                        last_user_msg_index
                    ]["content"]
                    new_content_parts = []
                    if isinstance(original_content, str):
                        new_content_parts.append(
                            {"type": "text", "text": original_content}
                        )
                    elif isinstance(original_content, list):  # 既にリストの場合
                        new_content_parts.extend(original_content)

                    new_content_parts.append(
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{encoded_file}"
                            },
                        }
                    )
                    processed_messages_non_streaming[last_user_msg_index][
                        "content"
                    ] = new_content_parts

            _inpurt_messages = processed_messages_non_streaming
            response = chatgptapi_client.chat.completions.create(
                model=_selected_model, messages=_inpurt_messages
            )
        else:
            response = chatgptapi_client.chat.completions.create(
                model=_selected_model,
                messages=_messages
            )
        return response.choices[0].message.content, response.choices[0].message.role

    elif isChatGPT_o1(_selected_model):
        _inpurt_messages, _systemrole = buildInpurtMessages(_messages, encoded_file)

        response = chatgptapi_client.chat.completions.create(
            model=_selected_model,
            messages=_inpurt_messages
        )

        return response.choices[0].message.content, response.choices[0].message.role

    elif isGemini(_selected_model):
        gemini_formatted_contents_for_non_streaming = []
        system_prompt_for_non_streaming = None

        temp_messages = []
        for m in _messages:
            if m["role"] == "system":
                system_prompt_for_non_streaming = m["content"]
            else:
                # Geminiは 'assistant' ではなく 'model' ロールを期待
                role_for_gemini = "user" if m["role"] == "user" else "model"
                temp_messages.append(
                    {"role": role_for_gemini, "content": m["content"]}
                )

        for i, msg in enumerate(temp_messages):
            parts = []
            if isinstance(msg["content"], str):
                parts.append({"text": msg["content"]})
            elif isinstance(msg["content"], list):  # GPT-4oのようなコンテンツリストの場合
                for item_content in msg["content"]:  # itemだとループ変数と被る可能性があるので変更
                    if item_content["type"] == "text":
                        parts.append({"text": item_content["text"]})

            # 最後のユーザーメッセージの場合に画像を追加
            if (
                msg["role"] == "user"
                and i == len(temp_messages) - 1
                and encoded_file
            ):
                parts.append(
                    {
                        "inline_data": {
                            "mime_type": "image/jpeg",
                            "data": encoded_file,
                        }
                    }
                )

            if parts:  # partsが空の場合は追加しない
                gemini_formatted_contents_for_non_streaming.append(
                    {"role": msg["role"], "parts": parts}
                )

        # parts が空の content をフィルタリング
        gemini_formatted_contents_for_non_streaming = [
            c for c in gemini_formatted_contents_for_non_streaming if c["parts"]
        ]

        if not gemini_formatted_contents_for_non_streaming:
            print("Gemini (non-streaming): No content to send.")
            return "", "assistant"

        actual_model_name = _selected_model
        if "gemini-1.5-pro" in _selected_model:
            actual_model_name = "gemini-1.5-pro-latest"
        elif (
            _selected_model == "gemini-pro" or _selected_model == "gemini-1.0-pro"
        ):  # "gemini-pro" も "gemini-1.0-pro" を指すように
            actual_model_name = "gemini-1.0-pro"
        # 他のGeminiモデルも同様にマッピングが必要な場合がある

        model_instance = genai.GenerativeModel(
            model_name=actual_model_name,
            system_instruction=system_prompt_for_non_streaming
            if system_prompt_for_non_streaming
            else None,
        )

        try:
            response = model_instance.generate_content(
                gemini_formatted_contents_for_non_streaming
            )
            # response.text だと、候補が複数ある場合に最初のものしか取れない可能性がある
            # response.candidates[0].content.parts[0].text を使うのがより安全
            full_text = "".join(
                part.text
                for part in response.candidates[0].content.parts
                if hasattr(part, "text")
            )
            return full_text, "assistant"
        except BlockedPromptException as e:  # インポートした例外を使用
            error_message = (
                f"Error: Gemini API call failed due to blocked prompt. {e}"
            )
            print(error_message)
            return error_message, "assistant"
        except Exception as e:
            print(f"Error during Gemini non-streaming API call: {e}")
            return f"Error: {e}", "assistant"

    elif isClaude(_selected_model):
        _inpurt_messages, _systemrole = buildInpurtMessages(_messages, encoded_file)

        _max_tokens = 4096

        if "claude-sonnet-4" in _selected_model or "claude-3-7-sonnet" in _selected_model:
            _max_tokens = 64000
        elif "claude-opus-4" in _selected_model:
            _max_tokens = 32000

        response = claude_client.messages.create(
            max_tokens=_max_tokens,
            system=_systemrole,
            model=_selected_model,
            messages=_inpurt_messages,
            stream=True  # Anthropic Claude API で10分以上かかるリクエストはストリーミングモードで実行することが推奨されている
        )

        # ストリーミングレスポンスを結合
        content = ""
        role = "assistant"
        for event in response:
            # Claudeのストリーミングはdelta.textにテキストが入る
            if hasattr(event, "delta") and hasattr(event.delta, "text"):
                content += event.delta.text
                print(event.delta.text, end="", flush=True)
            if hasattr(event, "role"):
                role = event.role

        return content, role
    else:
        return {}, ""


def execLlmApiStreaming(
    _selected_model, _messages, encoded_file, streaming_callback=None
):
    """
    Streaming-enabled LLM API execution function

    Args:
        _selected_model (str): Selected model name
        _messages (list): Message list
        encoded_file (str): Encoded file data
        streaming_callback (callable): Callback function for receiving streaming chunks

    Returns:
        tuple: (Full response content, role)
    """
    if isChatGptAPI(_selected_model):
        if isChatGPTImageAPI(_selected_model) and len(encoded_file) > 0:
            processed_messages_streaming = []
            # メッセージ履歴を処理し、最後のユーザーメッセージに画像を追加
            for msg in _messages:
                if msg["role"] == "system":
                    processed_messages_streaming.append(msg)
                elif msg["role"] == "user":
                    if isinstance(msg["content"], list):
                        processed_messages_streaming.append(msg)
                    else:
                        processed_messages_streaming.append(
                            {"role": "user", "content": msg["content"]}
                        )
                else:
                    processed_messages_streaming.append(msg)

            if encoded_file and processed_messages_streaming:
                last_user_msg_index = -1
                for i in range(len(processed_messages_streaming) - 1, -1, -1):
                    if processed_messages_streaming[i]["role"] == "user":
                        last_user_msg_index = i
                        break

                if last_user_msg_index != -1:
                    original_content = processed_messages_streaming[
                        last_user_msg_index
                    ]["content"]
                    new_content_parts = []
                    if isinstance(original_content, str):
                        new_content_parts.append(
                            {"type": "text", "text": original_content}
                        )
                    elif isinstance(original_content, list):
                        new_content_parts.extend(original_content)

                    new_content_parts.append(
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{encoded_file}"
                            },
                        }
                    )
                    processed_messages_streaming[last_user_msg_index][
                        "content"
                    ] = new_content_parts

            _inpurt_messages = processed_messages_streaming
            response = chatgptapi_client.chat.completions.create(
                model=_selected_model,
                messages=_inpurt_messages,  # 修正されたメッセージ
                stream=True,
            )
        else:
            response = chatgptapi_client.chat.completions.create(
                model=_selected_model,
                messages=_messages,
                stream=True
            )
        
        # GPTストリーミングレスポンス処理
        content = ""
        role = "assistant"
        for chunk in response:
            if chunk.choices[0].delta.content is not None:
                chunk_content = chunk.choices[0].delta.content
                content += chunk_content
                if streaming_callback:
                    streaming_callback(chunk_content)
            if chunk.choices[0].delta.role:
                role = chunk.choices[0].delta.role
        
        return content, role

    elif isChatGPT_o1(_selected_model):  # This block seems redundant if isChatGptAPI covers "o1" models.
                                        # Assuming it's a distinct logic path as per original code.
        _inpurt_messages, _systemrole = buildInpurtMessages(_messages, encoded_file)

        response = chatgptapi_client.chat.completions.create(
            model=_selected_model,
            messages=_inpurt_messages, # buildInpurtMessages might not be ideal for plain OpenAI if it's Claude-specific for images
            stream=True
        )
        
        # o1モデルストリーミングレスポンス処理
        content = ""
        role = "assistant"
        for chunk in response:
            if chunk.choices[0].delta.content is not None:
                chunk_content = chunk.choices[0].delta.content
                content += chunk_content
                if streaming_callback:
                    streaming_callback(chunk_content)
            if chunk.choices[0].delta.role:
                role = chunk.choices[0].delta.role
        
        return content, role

    elif isGemini(_selected_model):
        gemini_formatted_contents = []
        system_instruction = None 

        temp_messages_for_gemini_streaming = []
        for m in _messages:
            if m["role"] == "system":
                system_instruction = m["content"]
            else:
                role_for_gemini = "user" if m["role"] == "user" else "model"
                temp_messages_for_gemini_streaming.append(
                    {"role": role_for_gemini, "content": m["content"]}
                )

        for i, msg in enumerate(temp_messages_for_gemini_streaming):
            parts = []
            if isinstance(msg["content"], str):
                parts.append({"text": msg["content"]})
            elif isinstance(msg["content"], list):
                for item_content_streaming in msg["content"]:  # ループ変数名を変更
                    if item_content_streaming["type"] == "text":
                        parts.append({"text": item_content_streaming["text"]})

            if (
                msg["role"] == "user"
                and i == len(temp_messages_for_gemini_streaming) - 1
                and encoded_file
            ):
                parts.append(
                    {
                        "inline_data": {
                            "mime_type": "image/jpeg",
                            "data": encoded_file,
                        }
                    }
                )

            if parts:
                gemini_formatted_contents.append(
                    {"role": msg["role"], "parts": parts}
                )

        gemini_formatted_contents = [
            c for c in gemini_formatted_contents if c["parts"]
        ]

        if not gemini_formatted_contents:
            if streaming_callback:
                streaming_callback("Error: No content to send to Gemini.")
            return "Error: No content to send to Gemini.", "assistant"

        actual_model_name_streaming = _selected_model
        if "gemini-1.5-pro" in _selected_model:
            actual_model_name_streaming = "gemini-1.5-pro-latest"
        elif _selected_model in ("gemini-pro", "gemini-1.0-pro"):
            actual_model_name_streaming = "gemini-1.0-pro"

        model = genai.GenerativeModel(
            model_name=actual_model_name_streaming,
            system_instruction=system_instruction if system_instruction else None,
        )

        full_response_text = ""
        try:
            response_stream = model.generate_content(
                gemini_formatted_contents, stream=True
            )
            for chunk in response_stream:
                chunk_text = ""
                if hasattr(chunk, "text") and chunk.text:
                    chunk_text = chunk.text
                elif hasattr(chunk, "parts") and chunk.parts:
                    for part_in_chunk in chunk.parts:
                        if hasattr(part_in_chunk, "text") and \
                           part_in_chunk.text:
                            chunk_text += part_in_chunk.text

                if chunk_text:
                    full_response_text += chunk_text
                    if streaming_callback:
                        streaming_callback(chunk_text)

            return full_response_text, "assistant"

        except BlockedPromptException as e:  # インポートした例外を使用
            error_message = (
                f"Error: Gemini API call failed due to blocked prompt. {e}"
            )
            print(error_message)
            if streaming_callback:
                streaming_callback(error_message)
            return error_message, "assistant"
        except Exception as e:
            error_message = f"Error during Gemini streaming API call: {e}"
            print(error_message)
            if streaming_callback:
                streaming_callback(error_message)
            return error_message, "assistant"

    elif isClaude(_selected_model):
        _inpurt_messages, _systemrole = buildInpurtMessages(
            _messages, encoded_file
        )

        _max_tokens = 4096
        # User's existing model name checks for max_tokens
        if "claude-sonnet-4" in _selected_model or "claude-3-7-sonnet" in _selected_model:
            _max_tokens = 64000
        elif "claude-opus-4" in _selected_model:
            _max_tokens = 32000

        response = claude_client.messages.create(
            max_tokens=_max_tokens,
            system=_systemrole,
            model=_selected_model,
            messages=_inpurt_messages,
            stream=True
        )

        # Claude streaming response processing
        content = ""
        role = "assistant"  # Default role
        for event in response:
            if event.type == "message_start":
                if hasattr(event.message, "role"):
                    role = event.message.role
            elif event.type == "content_block_delta":
                if event.delta.type == "text_delta":
                    chunk_content = event.delta.text
                    content += chunk_content
                    if streaming_callback:
                        streaming_callback(chunk_content)
            # 他のイベントタイプ (e.g., message_delta, content_block_start, content_block_stop, message_stop)
            # も必要に応じて処理できますが、テキスト抽出には上記で十分な場合が多いです。

        return content, role
    else:
        return "", "assistant"