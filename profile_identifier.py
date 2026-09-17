import anthropic
import dotenv
import os
from helpers import load_file

dotenv.load_dotenv()
client = anthropic.Anthropic(
    api_key=os.environ.get("ANTHROPIC_API_KEY"),
)
model = "claude-haiku-4-5-20251001"

def identify_profile():
    system_prompt = f"""
    Identifique o perfil de consumo de comida para cada cliente a seguir.

    # Formato da Saída

    cliente - perfil do cliente em 3 palavras.
    """
    user_prompt = load_file('./dados/lista_de_consumo/lista_de_consumo_100_clientes.csv')

    message = client.messages.create(
        model=model,
        max_tokens=2000,
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
    return message

if __name__ == "__main__":
    assistant_response = identify_profile()
    response_text = assistant_response.content[0].text
    token_usage = assistant_response.usage
    print(response_text)
    print(f'Tokens de entrada: {token_usage.input_tokens}')
    print(f'Tokens de saida: {token_usage.output_tokens}')
