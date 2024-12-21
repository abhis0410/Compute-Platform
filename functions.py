from database import DatabaseHandler
import os
from dotenv import load_dotenv
import google.generativeai as genai


class ComputeHandler:
    
    def __init__(self, user_id, file_name, df, column_name, operation):
        self.values = df[column_name]
        self.data = {
            'user_id' : user_id,
            'file_name' : file_name,
            'column_name' : column_name,
            'operation' : operation,
        }
        load_dotenv()
    
    def _generate_code(self):
        operation = self.data['operation']
        genai.configure(api_key=os.environ["GEMINI_API_KEY"]) 
        model = genai.GenerativeModel('gemini-1.5-flash') 

        prompt = f"""Write Python code to compute the {operation} of a list of numbers called 'values'.
                    Return the result in a variable named 'result'.
                    Write concise and simple code using 'math' and 'numpy'.
                    Do not initialize or define the 'values' variable, assume it has already been given.
                    Store the result in the 'result' variable."""
        response = model.generate_content(prompt)
        self.code_snippet = response.text

        if self.code_snippet.startswith("```python"):
            self.code_snippet = self.code_snippet[len("```python"):]
        
        if self.code_snippet.endswith("\n"):
            self.code_snippet = self.code_snippet[:-1]

        if self.code_snippet.endswith("```"):
            self.code_snippet = self.code_snippet[:-3]

    def _execute_code(self):
        
        exec_globals = {'values': self.values}
        exec(self.code_snippet, exec_globals)
        result = exec_globals['result']
        self.data['result'] = result
    
    def workflow(self):
        try:
            self._generate_code()
            self._execute_code()
        except Exception as e:
            return e

        x = DatabaseHandler()
        x.store_result(
            user_id=self.data['user_id'],
            file_name=self.data['file_name'],
            column_name=self.data['column_name'], 
            operation=self.data['operation'], 
            result=self.data['result']
        )
        return None



def get_results(user_id):
    """ Returns results stored in database based on userId

    Args:
        user_id (string)

    Returns:
        DataFrame
    """
    x = DatabaseHandler()
    return x.fetch_results(user_id=user_id)
