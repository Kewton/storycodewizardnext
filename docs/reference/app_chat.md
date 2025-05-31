# Chat API

Streamlitアプリにおけるチャットインターフェースの実装。

## Functions

### communicate
Handles interaction with the selected LLM, managing inputs and responses.

#### Parameters
- `selected_project` *(str)*: The project name selected by the user.
- `selected_model` *(str)*: GPT model name.
- `selected_programing_model` *(str)*: Programming language type.
- `encoded_file` *(str)*: An optional file in base64.

#### Returns
*(list)*: Processed messages for chatbot interaction.

---

### story2code
Facilitates converting user stories into code outputs.

#### Parameters
Similar to `communicate`.

#### Returns
None.