import httpx
import os
from typing import List 

OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://ollama:11434")

class OllamaClient:
    def __init__(self, model: str = "llama3:8b", embedding_model: str = "nomic-embed-text"):
        self.model = model
        # Add a property for the embedding model
        self.embedding_model = embedding_model
        self.base_url = f"{OLLAMA_HOST}/api"
        print(f"Ollama client initialized for model '{self.model}' and embedding model '{self.embedding_model}' at {self.base_url}")

    async def generate(self, prompt: str) -> str:
        async with httpx.AsyncClient(timeout=120.0) as client: # Increased timeout
            try:
                response = await client.post(
                    f"{self.base_url}/generate",
                    json={"model": self.model, "prompt": prompt, "stream": False},
                )
                response.raise_for_status()
                response_data = response.json()
                return response_data.get("response", "").strip()
            except httpx.RequestError as e:
                print(f"Error calling Ollama API: {e}")
                # Provide a more specific error message
                return f"Error: Could not connect to the Ollama service at {OLLAMA_HOST}."
            except Exception as e:
                print(f"An unexpected error occurred: {e}")
                return "Error: An unexpected error occurred while processing the request."
    

    async def get_embedding(self, text: str) -> List[float]:
        """
        Generates an embedding vector for a given text.
        """
        async with httpx.AsyncClient(timeout=60.0) as client:
            try:
                response = await client.post(
                    f"{self.base_url}/embeddings",
                    json={"model": self.embedding_model, "prompt": text},
                )
                response.raise_for_status()
                response_data = response.json()
                # The embedding is in the "embedding" key
                return response_data.get("embedding", [])
            except httpx.RequestError as e:
                print(f"Error calling Ollama embeddings API: {e}")
                # In a real app, you'd want more robust error handling
                return []
            except Exception as e:
                print(f"An unexpected error occurred during embedding: {e}")
                return []