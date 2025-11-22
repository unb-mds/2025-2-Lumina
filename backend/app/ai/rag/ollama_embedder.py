import ollama
from typing import List
from app.ai.ai_models.EmbeddingPlatform import EmbeddingPlatform

class OllamaEmbeddings(EmbeddingPlatform):
    """
    Implementação do cliente de embedding usando Ollama,
    aderente à interface EmbeddingPlatform.
    """
    
    def __init__(self, model_name: str = "bge-m3"):
        """
        Inicializa o modelo de embedding.
        
        Args:
            model_name: Nome do modelo Ollama (ex: 'bge-m3')
        """
        self.model_name = model_name
        self._verify_model()
    
    def _verify_model(self):
        """Verifica se o modelo está disponível localmente e funcional."""
        try:
            # Tenta gerar um embedding de teste
            ollama.embed(model=self.model_name, input="teste")
            print(f"✅ Modelo '{self.model_name}' carregado com sucesso!")
        except Exception as e:
            print(f"❌ Erro ao carregar modelo '{self.model_name}': {e}")
            print(f"💡 Execute: ollama pull {self.model_name}")
            raise

    def embed_document(self, text: str) -> List[float]:
        """
        Gera o vetor de embedding para um único texto (Implementação da Interface).
        """
        response = ollama.embed(
            model=self.model_name,
            input=text
        )
        # A API do Ollama retorna 'embeddings' como uma lista de listas. 
        # Pegamos o primeiro (e único) elemento.
        return response["embeddings"][0]

    def embed_documents(self, texts: List[str], batch_size: int = 32) -> List[List[float]]:
        """
        Gera os vetores de embedding para uma lista de textos (Implementação da Interface).
        Inclui lógica de batching para evitar sobrecarga.
        """
        embeddings = []
        
        for i in range(0, len(texts), batch_size):
            batch = texts[i:i + batch_size]
            
            # Ollama suporta batch nativo passando uma lista no input
            response = ollama.embed(
                model=self.model_name,
                input=batch
            )
            
            # Adiciona os resultados deste lote à lista principal
            embeddings.extend(response["embeddings"])
            
            print(f"Processados {min(i + batch_size, len(texts))}/{len(texts)} textos")
        
        return embeddings

    # --- Métodos Utilitários Extras 

    def embed_article(self, article: dict) -> List[float]:
        """
        Gera embedding para um artigo completo (Método auxiliar específico).
        Reutiliza o embed_document para consistência.
        """
        combined_text = f"{article.get('title', '')}. {article.get('content', '')}"
        return self.embed_document(combined_text)
    
    def get_embedding_dimension(self) -> int:
        """Retorna a dimensão do vetor de embedding."""
        test_embedding = self.embed_document("teste")
        return len(test_embedding)