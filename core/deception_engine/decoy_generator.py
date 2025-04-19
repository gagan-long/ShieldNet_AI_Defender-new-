from langchain.prompts import PromptTemplate
from langchain.llms import LlamaCpp

class DecoyGenerator:
    def __init__(self):
        self.llm = LlamaCpp(
            model_path="llama-2-7b-chat.Q4_K_M.gguf",
            temperature=0.7,
            max_tokens=200
        )
        
        self.templates = {
            "fake_credentials": PromptTemplate(
                input_variables=["domain"],
                template="Generate a fake {domain} login page HTML with form fields for username and password"
            ),
            "decoy_document": PromptTemplate(
                input_variables=[],
                template="Create a realistic-looking but fake internal document containing placeholder financial figures"
            )
        }

    def generate_decoy(self, decoy_type, **kwargs):
        if decoy_type not in self.templates:
            raise ValueError(f"Unknown decoy type: {decoy_type}")
            
        prompt = self.templates[decoy_type].format(**kwargs)
        return self.llm(prompt)
