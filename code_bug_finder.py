# streamlit_bug_overview.py

import openai
import streamlit as st
import os
from dotenv import load_dotenv
import matplotlib.pyplot as plt
import numpy as np
from io import BytesIO
from PIL import Image

# Load environment variables from .env file
load_dotenv()

# Set your OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")

# Function to generate a graph using Matplotlib
def generate_graph(graph_type):
    fig, ax = plt.subplots()
    
    if graph_type == "Bar Chart":
        x = np.arange(1, 6)
        y = np.random.randint(1, 100, size=5)
        ax.bar(x, y, color='skyblue')
        ax.set_title("Random Bar Chart")
        ax.set_xlabel("Categories")
        ax.set_ylabel("Values")

    elif graph_type == "Line Graph":
        x = np.linspace(0, 10, 100)
        y = np.sin(x)
        ax.plot(x, y, color='green')
        ax.set_title("Sine Wave Line Graph")
        ax.set_xlabel("X-axis")
        ax.set_ylabel("Y-axis")

    # Return the figure for rendering
    return fig

# Function to generate an image using DALL·E
def generate_image(description):
    response = openai.Image.create(
        prompt=description,
        n=1,
        size="512x512"
    )
    image_url = response['data'][0]['url']
    return image_url

# Streamlit UI and Dark Theme Setup
st.set_page_config(page_title="Bug Overview and Assistant Tool", layout="centered")
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
        width: 80%;
        word-wrap: break-word;
    }
    </style>
""", unsafe_allow_html=True)

# Streamlit UI
st.title("🛠️ Bug Overview, Graph & Image Generator Tool")

st.write(
    """
    Generate comprehensive bug overviews, analyze code snippets, or request the assistant to generate graphs or images.
    """
)

# Adding tabs for different functionalities
tabs = st.tabs(["🔍 Bug Overview Generator", "💻 Code Analysis", "📊 Graph Generator", "🖼️ Image Generator"])

# --- Bug Overview Section ---
with tabs[0]:
    st.subheader("Bug Overview Generator")

    # Text input for entering the mitigation
    mitigation_input = st.text_area("Enter Mitigation", placeholder="Enter the mitigation here...", height=150)

    # Buttons for generating the bug overview and clearing the input
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Generate Bug Overview"):
            if mitigation_input.strip() == "":
                st.error("Please enter a mitigation.")
            else:
                with st.spinner("Generating bug overview..."):
                    try:
                        bug_overview = generate_bug_overview(mitigation_input)
                        st.success("Bug Overview Generated Successfully!")
                        # Displaying the output in a bubble
                        st.markdown(f'<div class="output-bubble">{bug_overview}</div>', unsafe_allow_html=True)
                    except Exception as e:
                        st.error(f"Error generating bug overview: {str(e)}")

    with col2:
        if st.button("Clear Input"):
            mitigation_input = ""

# --- Code Analysis Section ---
with tabs[1]:
    st.subheader("Code Analysis")

    # Input for the programming language (dropdown with Python, JavaScript, Flutter)
    language_input = st.selectbox("Select Programming Language", ["Python", "JavaScript", "Flutter (Dart)"])

    # Text area for the code snippet
    code_input = st.text_area("Paste Code Snippet", placeholder="Paste your code here...", height=150)

    # Buttons for analyzing the code and clearing the input
    col3, col4 = st.columns(2)
    with col3:
        if st.button("Analyze Code"):
            if not language_input or not code_input:
                st.error("Please select the programming language and paste a code snippet.")
            else:
                # Map "Flutter" to "Dart" for the API
                if language_input == "Flutter (Dart)":
                    language_input = "Dart"
                    
                with st.spinner("Analyzing code..."):
                    try:
                        code_analysis = analyze_code(code_input, language_input)
                        st.success("Code Analysis Completed Successfully!")
                        # Displaying the output in a bubble
                        st.markdown(f'<div class="output-bubble">{code_analysis}</div>', unsafe_allow_html=True)
                    except Exception as e:
                        st.error(f"Error analyzing code: {str(e)}")
    
    with col4:
        if st.button("Clear Code Input"):
            language_input = ""
            code_input = ""

# --- Graph Generator Section ---
with tabs[2]:
    st.subheader("Graph Generator")

    # Select type of graph
    graph_type = st.selectbox("Select Graph Type", ["Bar Chart", "Line Graph"])

    if st.button("Generate Graph"):
        with st.spinner("Generating graph..."):
            fig = generate_graph(graph_type)
            st.pyplot(fig)

# --- Image Generator Section ---
with tabs[3]:
    st.subheader("Image Generator")

    # Input for describing the image
    image_description = st.text_area("Describe the Image You Want", placeholder="e.g., A futuristic city skyline at sunset", height=100)

    if st.button("Generate Image"):
        if image_description.strip() == "":
            st.error("Please enter a description for the image.")
        else:
            with st.spinner("Generating image..."):
                image_url = generate_image(image_description)
                st.image(image_url, caption=f"Generated Image: {image_description}")

