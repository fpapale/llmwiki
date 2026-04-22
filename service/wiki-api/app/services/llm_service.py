import os
from openai import OpenAI

class LLMService:
    def __init__(self, llm_config, features_config):
        self.config = llm_config
        self.features = features_config
        self.is_mock = self.features.enable_mock_llm
        
        if self.config.enabled and not self.is_mock:
            # Recupera la chiave dinamicamente in base a quale provider stiamo usando
            api_key = os.environ.get(self.config.api_key_env, "mock_key")
            self.client = OpenAI(
                api_key=api_key,
                base_url=self.config.base_url
            )
        else:
            self.client = None

    def generate_summary(self, content: str) -> str:
        if not self.config.enabled or self.is_mock or not self.client:
            return f"# Summary (Mock - {self.config.provider} - {self.config.model})\n\nQuesto è un summary generato in modalità mock per il contenuto di {len(content)} caratteri."
        
        response = self.client.chat.completions.create(
            model=self.config.model,
            messages=[
                {"role": "system", "content": "Sei un assistente che genera un breve summary in Markdown per i documenti."},
                {"role": "user", "content": content}
            ],
            temperature=0.3
        )
        return response.choices[0].message.content

    def answer_query(self, question: str, context: str) -> str:
        if not self.config.enabled or self.is_mock or not self.client:
            return f"Mock answer for: {question} (Provider: {self.config.provider}, Model: {self.config.model}). \n\nContext used: {len(context)} chars."
        
        response = self.client.chat.completions.create(
            model=self.config.model,
            messages=[
                {"role": "system", "content": f"Rispondi alla domanda in italiano usando questo contesto estratto dal wiki:\n\n{context}"},
                {"role": "user", "content": question}
            ],
            temperature=0.3
        )
        return response.choices[0].message.content
