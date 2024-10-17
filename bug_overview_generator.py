# streamlit_bug_overview.py

import streamlit as st  # Streamlit must be imported before calling set_page_config

# Set the page config as the first command in the script
st.set_page_config(page_title="BugBoard - Squash Bugs in Style!", layout="centered")

# Now import the rest of the libraries
import openai
import os
from dotenv import load_dotenv
import matplotlib.pyplot as plt
import networkx as nx  # For generating complex graphs

# Load environment variables from .env file
load_dotenv()

# Set your OpenAI API key
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    st.error("API key not loaded! Please check your environment variables.")


# Set your OpenAI API key
openai.api_key = api_key

# Function to generate a bug overview using OpenAI ChatCompletion API
def generate_bug_overview(mitigation_text):
    messages = [
        {"role": "system", "content": "You are an expert software engineer."},
        {"role": "user", "content": (
            f"Given the following mitigations, provide a comprehensive bug overview.\n\n"
            f"Mitigations:\n{mitigation_text}\n\nBug Overview:"
        )}
    ]
    
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=messages,
        max_tokens=500,
        temperature=0.7,
    )
    
    bug_overview = response.choices[0].message['content'].strip()
    return bug_overview

# Function to generate code change analysis using OpenAI ChatCompletion API
# Function to generate code change analysis using OpenAI ChatCompletion API
def analyze_code(code_snippet, programming_language):
    messages = [
        {"role": "system", "content": f"You are an expert {programming_language} developer."},
        {"role": "user", "content": (
            f"Analyze the following {programming_language} code for bugs and potential issues. "
            f"Provide a detailed list of bugs, security vulnerabilities, and improvements that can be made.\n\n"
            f"Code:\n{code_snippet}\n\n"
            f"Once you've analyzed the code, rewrite the code with the necessary improvements applied. "
            f"Ensure the revised code follows best practices and is free of the issues you identified."
        )}
    ]
    
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=messages,
        max_tokens=1000,  # Increased to allow room for the revised code
        temperature=0.7,
    )
    
    analysis_and_fix = response.choices[0].message['content'].strip()
    return analysis_and_fix

# Function to generate a complex graph showing actual code changes
def generate_complex_code_change_graph(code_changes, bug_overview, mitigations):
    # Create a directed graph using NetworkX
    G = nx.DiGraph()

    # Add nodes with actual code snippets or summaries
    G.add_node("Code Change 1", label=code_changes[0][:30] + "...")  # Truncated for better visibility
    G.add_node("Bug Overview 1", label=bug_overview[:50] + "...")  # Truncated for better visibility
    G.add_node("Mitigation 1", label=mitigations[0])
    G.add_node("Code Change 2", label=code_changes[1][:30] + "...")  # Truncated for better visibility
    G.add_node("Bug Overview 2", label=bug_overview[:50] + "...")  # Truncated for better visibility
    G.add_node("Mitigation 2", label=mitigations[1])

    # Add edges to show the relationship between changes
    G.add_edges_from([
        ("Code Change 1", "Bug Overview 1"),
        ("Bug Overview 1", "Mitigation 1"),
        ("Mitigation 1", "Code Change 2"),
        ("Code Change 2", "Bug Overview 2"),
        ("Bug Overview 2", "Mitigation 2"),
        ("Mitigation 2", "Code Change 1")
    ])

    # Create the plot using Matplotlib
    pos = nx.spring_layout(G, k=0.5, seed=42)  # Adjust spring layout for better spacing
    plt.figure(figsize=(10, 8))
    
    # Draw the graph with customized settings
    nx.draw(G, pos, with_labels=True, node_color='#76c7c0', node_size=4000, font_size=12, font_weight='bold', arrows=True, edge_color='#ff6b6b')
    
    # Add labels with improved positioning
    labels = nx.get_node_attributes(G, 'label')
    nx.draw_networkx_labels(G, pos, labels, font_size=10, font_color='#2f3136', verticalalignment='bottom')

    plt.title("BugBoard: Cycle of Code Changes, Bug Fixes, and Mitigations", fontsize=16, color='#ffffff')

    # Return the figure for rendering
    return plt

# Define CSS for Dark Mode and Light Mode
dark_theme_css = """
<style>
    body {
        background-color: #2f3136;
        color: white;
    }
    .css-18e3th9 {
        background-color: #2f3136 !important;
    }
    .css-1d391kg p {
        color: white;
    }
    .css-15tx938 {
        background-color: #2f3136;
        color: white;
        border-radius: 8px;
        border: 1px solid #434343;
    }
    .stTextArea, .stTextInput {
        background-color: #3c4043;
        color: white;
        border-radius: 8px;
        border: 1px solid #676a6d;
        padding: 10px;
    }
    .stButton button {
        background-color: #ff6b6b;
        color: white;
        border: none;
        padding: 10px 20px;
        font-size: 16px;
        margin: 10px 0;
        border-radius: 8px;
        cursor: pointer;
        transition: background-color 0.3s ease;
    }
    .stButton button:hover {
        background-color: #fa5252;
    }
    .css-164nlkn {
        background-color: #3c4043 !important;
        color: white;
    }
    .css-1d391kg h1, .css-1d391kg h2 {
        color: white;
    }
    .css-1v3fvcr {
        background-color: #3c4043;
        border: 1px solid #434343;
        padding: 20px;
        border-radius: 10px;
    }
    .stTabs [data-baseweb="tab-list"] button {
        background-color: transparent;
        border: none;
        color: white;
        padding: 10px 20px;
        font-size: 18px;
    }
    .stTabs [data-baseweb="tab-list"] button[data-highlighted="true"] {
        border-bottom: 3px solid #ff6b6b;
        color: #ff6b6b;
    }
    .stTabs [data-baseweb="tab-list"] button:hover {
        color: #ff6b6b;
    }
    .output-bubble {
        background-color: #3a3b3c;
        color: white;
        padding: 15px;
        border-radius: 15px;
        border: 1px solid #565656;
        margin: 10px 0;
        font-size: 16px;
        width: 100%;
        word-wrap: break-word;
    }
    .graph-container {
        background-color: #2f3136;
        border-radius: 10px;
        padding: 10px;
        border: 2px solid #565656;
    }
    .header-title {
        color: #76c7c0;
        font-weight: bold;
    }
    .chat-bubble {
        background-color: #3a3b3c;
        color: white;
        padding: 15px;
        border-radius: 15px;
        margin-bottom: 15px;
        word-wrap: break-word;
        border: 1px solid #434343;
        font-size: 14px;
    }
</style>
"""

# Session state to toggle between themes
if "theme" not in st.session_state:
    st.session_state["theme"] = "dark"

# Button to toggle between dark and light theme
if st.button("Toggle Dark/Light Mode"):
    if st.session_state["theme"] == "dark":
        st.session_state["theme"] = "light"
    else:
        st.session_state["theme"] = "dark"

# Apply the selected theme
if st.session_state["theme"] == "dark":
    st.markdown(dark_theme_css, unsafe_allow_html=True)
else:
    st.markdown(light_theme_css, unsafe_allow_html=True)

# Initialize session state for chat history
if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = []

# Streamlit sidebar to display chat history in bubbles
st.sidebar.header("🗂️ Chat History")
if st.session_state["chat_history"]:
    for idx, chat in enumerate(st.session_state["chat_history"]):
        st.sidebar.markdown(f'<div class="chat-bubble"><b>Entry {idx + 1}:</b> {chat}</div>', unsafe_allow_html=True)
else:
    st.sidebar.write("No chat history yet. Your bug-busting adventures will appear here!")

# Streamlit UI for BugBoard with tabs
st.title("🛠️ BugBoard - Let's Squash Those Bugs!")

# Instructions
with st.expander("📖 How to Use BugBoard"):
    st.write("""
    1. Enter a bug mitigation strategy or a code snippet.
    2. Click '💥 Hit Me with Bug Overview and Code Fixes' to generate a bug overview, code analysis, and visualize changes.
    3. View results in the generated sections below.
    """)

# Tabs for different functionalities
tab1, tab2, tab3 = st.tabs(["🐞 Bug Overview", "🔍 Code Analysis", "📊 Graph Visualization"])

# Text input for entering the mitigation
mitigation_input = st.text_area("🛡️ Enter Your Bug-Busting Strategy:", placeholder="Tell us how you'll squash that bug!", height=150)

# Text input for entering code snippet for analysis
code_input = st.text_area("🛠️ Paste Your Battle Code:", placeholder="Drop your code snippet here...", height=150)

# Add more user-friendly controls
st.slider("🔧 Confidence Level (Higher is more verbose):", 0, 100, 70)

# Fun button to trigger the bug overview, code analysis, and complex graph generation
if st.button("💥 Hit Me with Bug Overview and Code Fixes"):
    if mitigation_input.strip() == "" or code_input.strip() == "":
        st.error("😱 You forgot to add a bug-busting strategy or your code! Try again!")
    else:
        with st.spinner("Crunching the bugs..."):
            try:
                # Generate bug overview
                bug_overview = generate_bug_overview(mitigation_input)
                st.success("🎉 Bug Overview Ready!")
                
                # Analyze code
                code_analysis = analyze_code(code_input, "Python")
                st.success("🛠️ Code Analysis Complete!")

                # Store in chat history
                st.session_state["chat_history"].append(f"Bug Overview: {bug_overview[:50]}... | Code Analysis: {code_analysis[:50]}...")

                # Show bug overview in the first tab
                with tab1:
                    st.markdown(f"#### Bug Breakdown 🕵️", unsafe_allow_html=True)
                    st.markdown(f'<div class="output-bubble">{bug_overview}</div>', unsafe_allow_html=True)
                
                # Show code analysis in the second tab
                with tab2:
                    st.markdown(f"#### Code Review 🔍", unsafe_allow_html=True)
                    st.markdown(f'<div class="output-bubble">{code_analysis}</div>', unsafe_allow_html=True)

                # Simulate code changes for the graph
                code_changes = [
                    "def fetch_data(): return sanitized_query(query)",
                    "Improved user input handling to prevent SQL injections."
                ]
                mitigations = [
                    "Mitigation: Input validation added for SQL queries.",
                    "Mitigation: Using parameterized queries for secure DB access."
                ]

                # Show the graph in the third tab
                with tab3:
                    st.markdown(f'<h3 class="header-title">🚀 Visualizing Your Code Changes and Mitigations in BugBoard:</h3>', unsafe_allow_html=True)
                    fig = generate_complex_code_change_graph(code_changes, bug_overview, mitigations)
                    st.pyplot(fig)

            except Exception as e:
                st.error(f"💥 Oops, something went wrong: {str(e)}")
