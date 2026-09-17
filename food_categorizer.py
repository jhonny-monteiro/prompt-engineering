import anthropic
import os
import dotenv

dotenv.load_dotenv()
client = anthropic.Anthropic(
    api_key=os.environ.get("ANTHROPIC_API_KEY"),
)
model = "claude-3-5-sonnet-20240620"

def categorize_food(valid_categories, food_name):
    system_prompt = f"""
    Você é um categorizador de alimentos.
    Você deve assumir as categorias presentes na lista abaixo.
    Você não deve responder outros objetos que não são alimentos.

    # Lista de Categorias Válidas
    {valid_categories.split(",")}

    # Formato da Saída
    Produto: Nome do Produto
    Categoria: apresente a categoria do produto

    # Exemplo de Saída
    Produto: Maçã
    Categoria: Frutas
    """
    user_prompt = food_name
    message = client.messages.create(
        model=model,
        max_tokens=1000,
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
    return response

if __name__ == "__main__":
    valid_categories = input("Informe as categorias válidas, separando por vírgula: ")
    while True:
        food_name = input("Informe o nome do alimento: ")
        response_text = categorize_food(valid_categories, food_name)
        print(response_text)
