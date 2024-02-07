import time
from threading import Thread
from taipy.gui import Gui, State, invoke_callback, get_state_id
conversation = {"Conversation": []}
state_id_list = []
selected_row = [1]
status = "Idle"

def on_init(state: State) -> None:
    state_id = get_state_id(state)
    state_id_list.append(state_id)


def client_handler(gui: Gui, state_id_list: list) -> None:
    while True:
        time.sleep(0.5)
        if len(state_id_list) > 0:
            invoke_callback(gui, state_id_list[0], update_conv, [])

def update_conv(state: State) -> None:
    with open("status.txt", "r") as f:
        status = f.read()
    state.status = status
    with open("conv.txt", "r") as f:
        conv = f.read()
    conversation["Conversation"] = conv.split("\n")
    if conversation == state.conversation:
        return
    state.conversation = conversation
    state.selected_row = [len(state.conversation["Conversation"]) - 1]

def erase_conv(state: State) -> None:
    with open("conv.txt", "w") as f:
        f.write("")

def style_conv(state: State, idx: int, row: int) -> str:
    if idx is None:
        return None
    elif idx % 2 == 0:
        return "user_message"
    else:
        return "gpt_message"

page = """
<|layout|columns=300px 1|
<|part|render=True|class_name=sidebar|
# Taipy **Shravya**{: .color-primary} # {: .logo-text}
<|New Conversation|button|class_name=fullwidth plain|id=reset_app_button|on_action=erase_conv|>
<br/>
<|{status}|text|>
|>

<|part|render=True|class_name=p2 align-item-bottom table|
<|{conversation}|table|style=style_conv|show_all|width=100%|rebuild|selected={selected_row}|>
|>
|>
"""

gui = Gui(page)
t = Thread(
    target=client_handler,
    args=(
        gui,
        state_id_list,
    ),
)
t.start()
gui.run(debug=True, dark_mode=True)
