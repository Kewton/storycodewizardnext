from openai import OpenAI
from secret_keys import openai_api_key, claude_api_key, gemini_api_key
import anthropic
from google import genai


chatgptapi_client = OpenAI(
  api_key=openai_api_key
)


claude_client = anthropic.Anthropic(
    api_key=claude_api_key,
)


gemini_client = genai.Client(
    api_key=gemini_api_key,
)


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
            _inpurt_messages = []
            _inpurt_messages.append(_messages[0])
            _inpurt_messages.append(
                {"role": "user", "content": [
                    {"type": "text", "text": _messages[1]["content"]},
                    {"type": "image_url", "image_url": {
                        "url": f"data:image/jpeg;base64,{encoded_file}"}}
                ]}
            )
            response = chatgptapi_client.chat.completions.create(
                model=_selected_model,
                messages=_inpurt_messages
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
        _inpurt_messages, _systemrole = buildInpurtMessages(_messages, encoded_file)

        response = gemini_client.models.generate_content(
            model=_selected_model,
            contents=_inpurt_messages[0]["content"]
        )

        return response.text, "assistant"

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


def execLlmApiStreaming(_selected_model, _messages, encoded_file, streaming_callback=None):
    """
    ストリーミング対応のLLM API実行関数
    
    Args:
        _selected_model (str): 選択されたモデル名
        _messages (list): メッセージリスト
        encoded_file (str): エンコードされたファイルデータ
        streaming_callback (callable): ストリーミングチャンク受信時のコールバック関数
    
    Returns:
        tuple: (完全なレスポンス内容, ロール)
    """
    if isChatGptAPI(_selected_model):
        if isChatGPTImageAPI(_selected_model) and len(encoded_file) > 0:
            _inpurt_messages = []
            _inpurt_messages.append(_messages[0])
            _inpurt_messages.append(
                {"role": "user", "content": [
                    {"type": "text", "text": _messages[1]["content"]},
                    {"type": "image_url", "image_url": {
                        "url": f"data:image/jpeg;base64,{encoded_file}"}}
                ]}
            )
            response = chatgptapi_client.chat.completions.create(
                model=_selected_model,
                messages=_inpurt_messages,
                stream=True
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

    elif isChatGPT_o1(_selected_model):
        _inpurt_messages, _systemrole = buildInpurtMessages(_messages, encoded_file)

        response = chatgptapi_client.chat.completions.create(
            model=_selected_model,
            messages=_inpurt_messages,
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
        _inpurt_messages, _systemrole = buildInpurtMessages(_messages, encoded_file)

        # Geminiの場合はストリーミング機能が制限されているため、通常の実行を行う
        response = gemini_client.models.generate_content(
            model=_selected_model,
            contents=_inpurt_messages[0]["content"]
        )
        
        # 一括でコールバックを呼び出し
        content = response.text
        if streaming_callback:
            streaming_callback(content)
        
        return content, "assistant"

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
            stream=True
        )

        # Claudeストリーミングレスポンス処理
        content = ""
        role = "assistant"
        for event in response:
            if hasattr(event, "delta") and hasattr(event.delta, "text"):
                chunk_content = event.delta.text
                content += chunk_content
                if streaming_callback:
                    streaming_callback(chunk_content)
            if hasattr(event, "role"):
                role = event.role

        return content, role
    else:
        return "", "assistant"