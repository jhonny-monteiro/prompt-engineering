import anthropic
import dotenv
import os
from helpers import load_file, save_file

dotenv.load_dotenv()
client = anthropic.Anthropic(
    api_key=os.environ.get("ANTHROPIC_API_KEY"),
)
model = "claude-3-5-sonnet-20240620"

def analyze_sentiment(restaurant):
    system_prompt = f"""
    Você é um analisador de sentimentos de avaliações de restaurantes.
    Escreva um parágrafo com até 50 palavras resumindo as avaliações e
    depois atribua qual o sentimento geral para o produto.
    Identifique também 3 pontos fortes e 3 pontos fracos identificados a partir das avaliações.

    # Formato de Saída

    Nome do Restaurante: {restaurant}
    Resumo das Avaliações:
    Sentimento Geral: [utilize aqui apenas Positivo, Negativo ou Neutro]
    Ponto fortes: lista com três bullets
    Pontos fracos: lista com três bullets

    """
    user_prompt = load_file(f'./dados/avaliacoes/avaliacoes-{restaurant}.txt')
    print(f'Iniciou a análise do {restaurant}')
    try:
        message = client.messages.create(
            model=model,
            max_tokens=2000,
            temperature=0,
            system=system_prompt,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": user_prompt
                        }
                    ]
                }
            ]
        )
        response = message.content[0].text
        save_file(f'./dados/avaliacoes/analise-{restaurant}.txt', response)
        print(f'Finalizou a análise do {restaurant}')
    except anthropic.APIConnectionError as e:
        print("O servidor não pode ser acessado! Erro:", e.__cause__)
    except anthropic.RateLimitError as e:
        print("Um status code 429 foi recebido! Limite de acesso foi atingido.")
    except anthropic.APIStatusError as e:
        print(f"Um erro {e.status_code} foi recebido. Mais informações: {e.response}")
    except Exception as e:
        print(f"Um erro inesperado ocorreu: {e}")

if __name__ == "__main__":
    restaurant_list = [
        'Restaurante de Comida Vegana',
        'Restaurante de Comida Chinesa',
        'Restaurante de Bolos e Doces',
    ]
    for restaurant in restaurant_list:
        analyze_sentiment(restaurant)
