import os
import ast
import tempfile
import base64
from dotenv import load_dotenv
from anthropic import Anthropic
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import plotly.io as pio
import streamlit as st

# Load environment variables directly
load_dotenv()
        
# Retrieve API key directly from environment
api_key = os.getenv('ANTHROPIC_API_KEY')
        

class DataChatbot:
    def __init__(self, api_key):
        self.anthropic = Anthropic(api_key=api_key)
        
    def generate_visualization_code(self, df, query):

        # Prepare dataset information
        df_info = f"""
        Dataset Overview:
        - Columns: {', '.join(df.columns)}
        - Number of Rows: {len(df)}
        - Column Types:
        {df.dtypes.to_string()}

        Numeric Columns: {list(df.select_dtypes(include=['int64', 'float64']).columns)}
        Categorical Columns: {list(
            df.select_dtypes(include=['object', 'category']).columns)}
        """
        
        # Prompt for visualization code generation
        prompt = f"""You are a data visualization expert. Given the dataset:
                    {df_info}

                    User's Visualization Request: {query}

                    Important Constraints:
                    1. USE THE PRE-LOADED DATAFRAME 'df' DIRECTLY
                    2. DO NOT attempt to read any CSV file
                    3. Generate Streamlit visualization code using Plotly

                    Tasks:
                    1. Understand the visualization request
                    2. Select appropriate Plotly visualization
                    3. Generate complete, executable Streamlit code
                    4. Provide explanation of the visualization

                    Return a Python dictionary with:
                    {{
                        "code": "Full Streamlit Python code for visualization",
                        "explanation": "Brief visualization explanation",
                        "plot_type": "Type of plot"
                    }}

                    Requirements:
                    - Use Plotly Express or Plotly Graph Objects
                    - Ensure code is fully executable
                    - Match the specific visualization request
                    """
        
        # Get response from Claude
        response = self.anthropic.messages.create(
            model="claude-3-sonnet-20240229",
            max_tokens=1024,
            messages=[{"role": "user", "content": prompt}]
        )
        
        try:
            # Parse the response
            response_text = response.content[0].text
            
            # Handle code block formatting
            if response_text.startswith('```python'):
                response_text = response_text.strip('```python```')
            
            # Use ast.literal_eval for safer parsing
            result = ast.literal_eval(response_text)
            
            return result
        
        except Exception as e:
            # Fallback to a basic error handling
            return {
                "code": f"st.error('Visualization generation failed: {str(e)}')",
                "explanation": f"Error in generating visualization: {str(e)}",
                "plot_type": "Error"
            }
        
    def interpret_visualization(self, plot_path):
        """
        Interpret the visualization by converting plot to base64
        
        Args:
            plot_path (str): Path to the saved plot image
        
        Returns:
            str: Detailed plot interpretation
        """
        # Convert image to base64
        with open(plot_path, "rb") as image_file:
            base64_image = base64.b64encode(image_file.read()).decode('utf-8')
        
        prompt = """Analyze this visualization image carefully:
                    [Image of data visualization]

                    Please provide a comprehensive interpretation. Include:
                    1. Types of data/variables shown
                    2. Key insights from the visualization
                    3. Significant patterns or trends
                    4. Any notable statistical observations
                    5. Potential implications or conclusions

                    Be specific and extract concrete insights from the visual data."""
        
        # Send image to Claude with prompt
        response = self.anthropic.messages.create(
            model="claude-3-sonnet-20240229",
            max_tokens=1024,
            messages=[
                {"role": "user", "content": [
                    {"type": "text", "text": prompt},
                    {"type": "image", "source": {
                        "type": "base64",
                        "media_type": "image/png",
                        "data": base64_image
                    }}
                ]}
            ]
        )
        
        return response.content[0].text

def process_chat_query(query, df):
    try:
        # Initialize chatbot
        chatbot = DataChatbot(api_key)
        
        # Generate visualization code
        viz_result = chatbot.generate_visualization_code(df, query)
        
        # Execute the generated code
        if viz_result and 'code' in viz_result:
            st.markdown(f"**Visualization Type:** {viz_result.get(
                'plot_type', 'Unknown')}")
            st.markdown(f"**Explanation:** {viz_result.get(
                'explanation', 'No explanation provided')}")
            
            
            # Create a temporary file to save the plot
            with tempfile.NamedTemporaryFile(delete=False, suffix='.png') as temp_plot:
                temp_plot_path = temp_plot.name
            
            exec_globals = {
                'df': df, 
                'st': st, 
                'px': px, 
                'go': go, 
                'pd': pd,
                'pio': pio,
                'temp_plot_path': temp_plot_path
            }
            
            # Modify the generated code to save the plot
            modified_code = viz_result['code'].replace(
                'st.plotly_chart(fig)', 
                'fig_image = pio.to_image(fig, format="png")\n'
                'with open(temp_plot_path, "wb") as f:\n'
                '    f.write(fig_image)\n'
                'st.plotly_chart(fig)'
            )
            
            # Execute the modified code
            exec(modified_code, exec_globals)
            
            # Generate plot interpretation
            try:
                plot_interpretation = chatbot.interpret_visualization(temp_plot_path)
                
                # Display interpretation
                st.markdown("### Plot Interpretation")
                st.write(plot_interpretation)
                
                # Clean up temporary file
                os.unlink(temp_plot_path)
                
                return plot_interpretation
            except Exception as e:
                st.error(f"Error in plot interpretation: {e}")
                # Clean up temporary file
                os.unlink(temp_plot_path)
                return "Error in plot interpretation"
        else:
            st.error("Failed to generate visualization")
            return "Error in visualization generation"
    except ValueError as e:
        st.error(str(e))
        return "Error: API Key configuration failed"