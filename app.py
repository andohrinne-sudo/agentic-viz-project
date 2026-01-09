import streamlit as st
import os
from utilities.llm_client import GeminiClient
from utilities.data_processor import DataProcessor
from utilities.agent_workflow import AgentWorkflowManager

# 1. Page Configuration
st.set_page_config(page_title="Agentic Viz Dashboard", layout="wide")
st.title("☕ Coffee Sales Agentic Insights")

# 2. Directory & Path Setup
DATA_DIR = "data"
os.makedirs(DATA_DIR, exist_ok=True)
csv_path = os.path.join(DATA_DIR, "coffee_sales.csv")

# 3. Sidebar for Controls
st.sidebar.header("📂 Data & Execution")
uploaded_file = st.sidebar.file_uploader("Upload CSV", type=["csv"])

if uploaded_file:
    with open(csv_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    st.sidebar.success("File Ready!")

user_prompt = st.sidebar.text_area(
    "What would you like to visualize?",
    placeholder="e.g., Show me total revenue by coffee type across different locations."
)

run_btn = st.sidebar.button("🚀 Run Analysis")

# 4. Main Workflow Execution
if run_btn:
    if not os.path.exists(csv_path):
        st.error("Please upload a CSV file first!")
    elif not user_prompt:
        st.warning("Please enter a prompt for the agent.")
    else:
        try:
            # Initialize core components
            client = GeminiClient()
            processor = DataProcessor(csv_path)
            agent = AgentWorkflowManager(client, processor)
            
            with st.spinner("Agent is thinking, coding, and critiquing..."):
                st.info("Agent workflow started...")
                v1_path, v2_path = agent.run_visualization_workflow(user_prompt)
            
            st.success("Analysis Complete!")

            # 5. Side-by-Side Visualization Display
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("Draft Visualization (V1)")
                if os.path.exists(v1_path):
                    st.image(v1_path, use_container_width=True)
                else:
                    st.error("Draft plot failed to generate.")

            with col2:
                st.subheader("Refined Visualization (V2)")
                if os.path.exists(v2_path):
                    st.image(v2_path, use_container_width=True)
                else:
                    st.error("Refined plot failed to generate.")
            
            # 6. Show the generated code for transparency
            with st.expander("View Agent-Generated Code"):
                st.markdown("### Initial Code")
                st.code(agent.initial_code, language='python')
                st.markdown("### Refined Code")
                st.code(agent.refined_code, language='python')

        except Exception as e:
            st.error(f"An error occurred: {str(e)}")