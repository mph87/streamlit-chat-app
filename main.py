import openai
import streamlit as st
from streamlit_chat import message

#from streamlit.scriptrunner.script_run_context import add_script_run_ctx
# Get session id
#session_id = add_script_run_ctx().streamlit_script_run_ctx.session_id



# Set API key
openai.api_key = st.secrets.openai.api_key

###### THIS IS WHERE YOU CHANGE THINGS

# Set model
model_name = "gpt-3.5-turbo"

# Set system message
system_message = "You are a helpful assistant." # This is where you can put your prompt.
first_ai_message = None 
# Uncomment the next line if you want the AI to give the first message.
first_ai_message = "Hello, how can I help you today" 

##### NO NEED TO CHANGE THINGS BELOW

# Setting page title and header
st.set_page_config(page_title="Chat", page_icon=":robot_face:")
st.markdown("<h1 style='text-align: center;'>ChatBot</h1>", unsafe_allow_html=True)

# Initialise session state variables
if 'messages' not in st.session_state:
    st.session_state['messages'] = [
        {"role": "system", "content": system_message}
    ]

    if first_ai_message is not None:
        st.session_state['messages'].append({"role": "assistant", "content": first_ai_message})

if 'cost' not in st.session_state:
    st.session_state['cost'] = []
if 'total_tokens' not in st.session_state:
    st.session_state['total_tokens'] = []
if 'total_cost' not in st.session_state:
    st.session_state['total_cost'] = 0.0

# Sidebar - let user choose model, show total cost of current conversation, and let user clear the current conversation
st.sidebar.title("Sidebar")
#model_name = st.sidebar.radio("Choose a model:", ("GPT-3.5", "GPT-4"))
clear_button = st.sidebar.button("Clear Conversation", key="clear")

# reset everything
if clear_button:
    st.session_state['messages'] = [
        {"role": "system", "content": "You are a helpful assistant."}
    ]
    st.session_state['number_tokens'] = []
    st.session_state['cost'] = []
    st.session_state['total_cost'] = 0.0
    st.session_state['total_tokens'] = []


# generate a response
def generate_response(prompt):
    st.session_state['messages'].append({"role": "user", "content": prompt})

    completion = openai.ChatCompletion.create(
        model=model_name,
        messages=st.session_state['messages']
    )
    response = completion.choices[0].message.content
    st.session_state['messages'].append({"role": "assistant", "content": response})

    # print(st.session_state['messages'])
    total_tokens = completion.usage.total_tokens
    prompt_tokens = completion.usage.prompt_tokens
    completion_tokens = completion.usage.completion_tokens
    return response, total_tokens, prompt_tokens, completion_tokens


# container for chat history
response_container = st.container()
# container for text box
container = st.container()

with container:
    with st.form(key='my_form', clear_on_submit=True):
        user_input = st.text_area("You:", key='input', height=100)
        submit_button = st.form_submit_button(label='Send')

    if submit_button and user_input:
        output, total_tokens, prompt_tokens, completion_tokens = generate_response(user_input)
        st.session_state['total_tokens'].append(total_tokens)

        # from https://openai.com/pricing#language-models
        if model_name == "GPT-3.5":
            cost = total_tokens * 0.002 / 1000
        else:
            cost = (prompt_tokens * 0.03 + completion_tokens * 0.06) / 1000

        st.session_state['cost'].append(cost)
        st.session_state['total_cost'] += cost

# Specify the avatar style and avatar_seed for the user and AI
# See options here: https://www.dicebear.com/styles
user_avatar, user_avatar_seed = 'pixel-art', "hh"
ai_avatar, ai_avatar_seed = 'initials', "AI"

# Alternatively, you can specify a custom avatar image with a URL
user_logo_url = None
ai_logo_url = None

# Example logo urls (uncomment to use)
#user_logo_url = "https://avatars.dicebear.com/api/initials/John%20Doe.svg"
#ai_logo_url = "https://avatars.dicebear.com/api/initials/AI.svg" 

if st.session_state['messages']:
    with response_container:
        for i in range(len(st.session_state['messages'])):
            msg = st.session_state['messages'][i]
            if msg['role'] == 'system': # Don't display the system message
                continue

            avatar_style = user_avatar if msg['role'] == 'user' else ai_avatar
            seed = user_avatar_seed if msg['role'] == 'user' else ai_avatar_seed
            is_user = msg['role'] == 'user'
            key = str(i) + ('_user' if is_user else '')

            message(msg['content'], is_user=is_user, key=key,
                    avatar_style=avatar_style, seed=seed) # logo_=user_logo_url)