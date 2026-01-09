import os
import re
import traceback
import matplotlib.pyplot as plt
import seaborn as sns
from utilities.llm_client import GeminiClient
from utilities.data_processor import DataProcessor

class AgentWorkflowManager:
    def __init__(self, client: GeminiClient, processor: DataProcessor):
        self.client = client
        self.processor = processor
        self.initial_code = None
        self.refined_code = None

    def run_visualization_workflow(self, user_prompt: str):
        """Executes the two-step agentic workflow: Draft and Refine."""
        v1_path = "visualizations/plot_v1.png"
        v2_path = "visualizations/plot_v2.png"
        os.makedirs("visualizations", exist_ok=True)
        
        print(f"--- Starting Workflow for: {user_prompt} ---")

        # --- Step 1: Draft (V1) ---
        data_summary = self.processor.generate_prompt_summary()
        initial_prompt = f"""
        Data Summary: {data_summary}
        Request: {user_prompt}
        Task: Create a visualization and save it to exactly '{v1_path}'.
        Provide ONLY the Python code in a markdown block.
        """
        
        print("Step 1: Generating initial visualization...")
        self.initial_code = self._extract_code(self.client.generate_content(initial_prompt))
        self._execute_code(self.initial_code, v1_path)

        # --- Step 2: Self-Critique & Refine (V2) ---
        critique_prompt = f"""
        Original Request: {user_prompt}
        Initial Code: {self.initial_code}
        Task: Critique the code above for visual appeal and clarity. 
        Provide a refined version that saves the plot to exactly '{v2_path}'.
        Provide ONLY the refined Python code in a markdown block.
        """
        
        print("Step 2: Refining visualization via self-critique...")
        self.refined_code = self._extract_code(self.client.generate_content(critique_prompt))
        self._execute_code(self.refined_code, v2_path)
        
        print("--- Workflow Complete ---")
        return v1_path, v2_path

    def _extract_code(self, text: str):
        """Extracts code blocks from LLM responses."""
        match = re.search(r"```(?:python)?\n?(.*?)```", text, re.DOTALL)
        if match:
            return match.group(1).strip()
        return text.strip()

    def _execute_code(self, code: str, path: str):
        """Safely executes generated code with local data context."""
        try:
            # Provide dataframe and plotting libraries to the execution context
            exec_globals = {
                "df": self.processor.df,
                "plt": plt,
                "sns": sns,
                "plt_path": path
            }
            exec(code, exec_globals)
            plt.close('all') # Cleanup to prevent memory issues
        except Exception as e:
            print(f"Error executing code for {path}:")
            traceback.print_exc()