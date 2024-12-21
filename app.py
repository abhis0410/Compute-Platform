import streamlit as st
import pandas as pd
from functions import get_results, ComputeHandler

class ComputeResult:
    def __init__(self, user_id):
        self.user_id = user_id
        self.file = None
        self.column_name = None
        self.operation = None
        self.dataframe = None

    def file_input(self):
        self.file = st.file_uploader("Upload a CSV or Excel file", type=["csv", "xlsx"])
        if self.file is not None:
            try:
                if self.file.name.endswith(".csv"):
                    self.dataframe = pd.read_csv(self.file)
                elif self.file.name.endswith(".xlsx"):
                    self.dataframe = pd.read_excel(self.file)
                    
                st.success("File uploaded successfully!")
                st.write("Preview of the data:")
                st.dataframe(self.dataframe.head())
            except Exception as e:
                st.error(f"Error reading file: {e}")
    
    def column_name_input(self):
        if self.dataframe is not None:
            column_names = self.dataframe.columns.tolist()
            self.column_name = st.selectbox("Select a column name:", column_names)
            if self.column_name:
                if self.column_name in self.dataframe.columns:
                    st.success(f"Column '{self.column_name}' found!")
                    st.write(self.dataframe[[self.column_name]].head())
                else:
                    st.error(f"Column '{self.column_name}' not found in the file.")

    def operation_input(self):
        self.operation = st.text_input("Enter name of operation to be performed:")
        if self.operation:
            st.write(f"You entered: {self.operation}")


    def run(self):
        
        st.subheader("Compute Result")

        self.file_input()
        self.column_name_input()
        self.operation_input()

        if st.button("Submit"):
            x = ComputeHandler(
                user_id=self.user_id, 
                file_name=self.file.name,
                df=self.dataframe, 
                column_name=self.column_name, 
                operation=self.operation
            )
            exec_check = x.workflow()
            if exec_check is not None:
                st.error(exec_check)
                return
            
            try:
                st.write(f"Result : {x.data['result']}")
            except:
                pass

            st.write("Successful Results")
            return

class FetchResult:
    def __init__(self, user_id):
        self.user_id = user_id

    def run(self):
        df = get_results(self.user_id)
        st.subheader( f"Showing results for user {self.user_id}")
        st.dataframe(df, use_container_width=True)

class StreamlitApp:
    def __init__(self):
        pass

    def util_sidebar(self):
        if 'user_id' not in st.session_state:
            st.session_state['user_id'] = None
        
        if not st.session_state['user_id']:
            user_id_input = st.sidebar.text_input("Enter your user ID")
            if user_id_input:
                st.session_state['user_id'] = user_id_input


    def main(self):
        st.set_page_config(
            page_title="Computation Platform",
            layout="centered",
            initial_sidebar_state="expanded",
        )
        
        st.header("Computational Platform")
        st.sidebar.header("USER_ID")
        self.util_sidebar()

        if st.session_state['user_id'] : 
            
            user_id = st.session_state['user_id']
            page = st.selectbox("Current Page", ("Compute Results", "Fetch Results"))
            x = None
            if page == "Compute Results":
                x = ComputeResult(user_id=user_id)
            elif page == "Fetch Results":
                x = FetchResult(user_id=user_id)

            x.run()

        return None


if __name__ == "__main__":
    app = StreamlitApp()
    app.main()
