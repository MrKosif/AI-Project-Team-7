import google.generativeai as genai

class GeminiFlash25:
    def __init__(self):
        # Configure the API key for authentication
        genai.configure(api_key="AIzaSyAjEbWzD3LKzGcdYVMSUXm3wD901skTqVQ")
        # Initialize the Gemini 2.5 Flash model
        self.model = genai.GenerativeModel('gemini-2.5-flash')

    def ask_question(self, question: str) -> str:

        response = self.model.generate_content(question)
        return response.text