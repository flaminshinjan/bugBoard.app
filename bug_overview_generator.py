# streamlit_bug_overview.py

import openai
import streamlit as st
import os
from dotenv import load_dotenv
import matplotlib.pyplot as plt
import networkx as nx  # For generating complex graphs

# Load environment variables from .env file
load_dotenv()

# Set your OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")

# Function to generate a bug overview using OpenAI API
def generate_bug_overview(mitigation_text):
    messages = [
        {"role": "system", "content": "You are an expert software engineer."},
        {"role": "user", "content": (
            f"Given the following mitigations, provide a comprehensive bug overview.\n\n"
            f"Mitigations:\n{mitigation_text}\n\nBug Overview:"
        )}
    ]
    
    response = openai.ChatCompletion.create(
        model="gpt-4",  # Replace this with your fine-tuned model if available
        messages=messages,
        max_tokens=500,
        temperature=0.7,
    )
    
    bug_overview = response.choices[0].message['content'].strip()
    return bug_overview

# Function to generate code change analysis using OpenAI API
def analyze_code(code_snippet, programming_language):
    messages = [
        {"role": "system", "content": f"You are an expert {programming_language} developer."},
        {"role": "user", "content": (
            "Analyze the following code for bugs and potential issues. Provide a detailed list of bugs, "
            f"security vulnerabilities, and any improvements that can be made.\n\n"
            f"Code:\n{code_snippet}\n\nAnalysis:"
        )}
    ]
    
    response = openai.ChatCompletion.create(
        model="gpt-4",  # Replace this with your fine-tuned model if available
        messages=messages,
        max_tokens=750,
        temperature=0.7,
    )
    
    analysis = response.choices[0].message['content'].strip()
    return analysis

# Function to generate a complex graph showing actual code changes
# Function to generate a complex graph showing actual code changes with improved layout
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
    nx.draw(G, pos, with_labels=True, node_color='lightgreen', node_size=4000, font_size=10, font_weight='bold', arrows=True, edge_color='black')
    
    # Add labels with improved positioning
    labels = nx.get_node_attributes(G, 'label')
    nx.draw_networkx_labels(G, pos, labels, font_size=9, font_color='black', verticalalignment='bottom')

    plt.title("BugBoard: Cycle of Code Changes, Bug Fixes, and Mitigations")

    # Return the figure for rendering
    return plt


# Streamlit UI
st.set_page_config(page_title="BugBoard - Squash Bugs in Style!", layout="centered")
st.markdown("""
    <style>
    body {
        background-color: #202124;
        color: white;
    }
    .css-18e3th9 {
        background-color: #202124 !important;
    }
    .css-1d391kg p {
        color: white;
    }
    .css-15tx938 {
        background-color: #202124;
        color: white;
        border-radius: 8px;
        border: 1px solid #434343;
    }
    .stTextArea, .stTextInput {
        background-color: #292b2e;
        color: white;
        border-radius: 8px;
        border: 1px solid #565656;
        padding: 10px;
    }
    .stButton button {
        background-color: #ff5656;
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
        background-color: #ff4c4c;
    }
    .css-164nlkn {
        background-color: #292b2e !important;
        color: white;
    }
    .css-1d391kg h1, .css-1d391kg h2 {
        color: white;
    }
    .css-1v3fvcr {
        background-color: #1f1f1f;
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
        border-bottom: 3px solid #ff5656;
        color: #ff5656;
    }
    .stTabs [data-baseweb="tab-list"] button:hover {
        color: #ff5656;
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
    </style>
""", unsafe_allow_html=True)

# Streamlit UI for BugBoard
st.title("🛠️ BugBoard - Let's Squash Those Bugs!")

st.write("""
Welcome to **BugBoard** where bug squashing meets fun! Enter your code changes, mitigations, and let the magic happen! 🎯
""")

# Text input for entering the mitigation
mitigation_input = st.text_area("Enter Your Bug-Busting Strategy 🐞:", placeholder="Tell us how you'll squash that bug!", height=150)

# Text input for entering code snippet for analysis
code_input = st.text_area("Paste Your Battle Code 🛠️:", placeholder="Drop your code snippet here...", height=150)

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

                # Display bug overview and code analysis in two columns
                col1, col2 = st.columns(2)
                with col1:
                    st.markdown(f"#### Bug Breakdown 🕵️")
                    st.markdown(f'<div class="output-bubble">{bug_overview}</div>', unsafe_allow_html=True)
                
                with col2:
                    st.markdown(f"#### Code Review 🔍")
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

                # Display the complex graph below the two columns
                st.write("### 🚀 Visualizing Your Code Changes and Mitigations in BugBoard:")
                fig = generate_complex_code_change_graph(code_changes, bug_overview, mitigations)
                st.pyplot(fig)

            except Exception as e:
                st.error(f"💥 Oops, something went wrong: {str(e)}")
