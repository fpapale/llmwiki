class LLMService:
    def __init__(self, llm_config, features_config):
        self.config = llm_config
        self.features = features_config
        self.is_mock = self.features.enable_mock_llm

    def generate_summary(self, content: str) -> str:
        if not self.config.enabled or self.is_mock:
            return f"# Summary (Mock)\n\nQuesto è un summary generato in modalità mock per il contenuto di {len(content)} caratteri."
        
        # Here we would normally use openai library
        # import openai
        # client = openai.OpenAI(api_key=self.config.api_key_env, base_url=self.config.base_url)
        # ...
        return "# Summary\n\nGenerato da LLM reale."

    def answer_query(self, question: str, context: str) -> str:
        if not self.config.enabled or self.is_mock:
            return f"Mock answer for: {question}. \n\nContext used: {len(context)} chars."
        
        return "Risposta dall'LLM."
