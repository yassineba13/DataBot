import streamlit as st
import pandas as pd
from chat import process_chat_query
from utils import clean_dataset

def load_data(uploaded_file):
    if uploaded_file is not None:
        file_extension = uploaded_file.name.split('.')[-1].lower()
        
        try:
            if file_extension == 'csv':
                df = pd.read_csv(uploaded_file)
            elif file_extension in ['xls', 'xlsx']:
                df = pd.read_excel(uploaded_file)
            elif file_extension == 'json':
                df = pd.read_json(uploaded_file)
            else:
                st.error('Unsupported format. Please upload CSV, XLS, or JSON files.')
                return None
            return df
        except Exception as e:
            st.error(f'Error loading file: {str(e)}')
            return None
    return None

def main():
    st.title('Data Visualization Assistant')
    
    # File upload section
    st.header('Upload Your Dataset')
    uploaded_file = st.file_uploader(
        "Choose a file (CSV, XLS, or JSON)",
        type=['csv', 'xls', 'xlsx', 'json']
    )
    
    # Initialize session state for chat history
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    
    if 'df' not in st.session_state:
        st.session_state.df = None
    
    # Load and display data
    if uploaded_file:
        st.session_state.df = load_data(uploaded_file)
        
        if st.session_state.df is not None:
            st.write("Dataset Preview:")
            st.dataframe(st.session_state.df.head())
            
            # Clean data button
            if st.button('Clean Data'):
                st.session_state.df = clean_dataset(st.session_state.df)
                st.success('Data cleaned successfully!')
                st.dataframe(st.session_state.df.head())
    
    # Chat interface
    st.header('Chat with Your Data')
    
    # Display chat history
    for message in st.session_state.chat_history:
        with st.chat_message(message["role"]):
            st.write(message["content"])
    
    # Chat input
    if prompt := st.chat_input("Ask questions about your data..."):
        if st.session_state.df is None:
            st.error("Please upload a dataset first!")
        else:
            # Display user message
            with st.chat_message("user"):
                st.write(prompt)
            
            # Add user message to chat history
            st.session_state.chat_history.append({"role": "user", "content": prompt})
            
            # Get and display assistant response
            with st.chat_message("assistant"):
                response = process_chat_query(prompt, st.session_state.df)
                st.write(response)
            
            # Add assistant response to chat history
            st.session_state.chat_history.append(
                {"role": "assistant", "content": response})

if __name__ == "__main__":
    main()