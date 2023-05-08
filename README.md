# Acknowledgements
This code is an adaptation of:
https://github.com/marshmellow77/streamlit-chatgpt-ui


# Run App

## Step 1: Download the code Locally and Install Packages
Download the code to your computer. Then, create a virutal environment and install the required packages as follows:
```
conda create --name streamlit_chat_env python=3.9
conda activate streamlit_chat_env
pip install openai streamlit streamlit_chat
```

## Step 2: Create .streamlit/secrets.toml file where you put in your OpenAI API key

You can do this by running:

```
mkdir .streamlit
touch .streamlit/secrets.toml
```

Edit .streamlit/secrets.toml to be the following:

```
[openai]
api_key = 'YOUR_API_KEY_HERE'
```

This secret code should not be pushed to Github. It will be accessed by main.py as follows (you don't need to do anything)
```
openai.api_key = st.secrets.openai.api_key
```

## Step 3: Run app
```
streamlit run main.py
```

# Deploy app to the web
1. Register an account at https://streamlit.io/cloud
2. Upload your code.
3. Add your secret API code (will add details on this shortly.)

