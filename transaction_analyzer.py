import anthropic
import dotenv
import os
import json
from helpers import load_file, save_file

dotenv.load_dotenv()
client = anthropic.Anthropic(
    api_key=os.environ.get("ANTHROPIC_API_KEY"),
)
model = "claude-haiku-4-5-20251001"

def analyze_transactions(transactions):
    system_prompt = """
    Analise as transações financeiras a seguir e identifique se cada uma delas é uma "Possível Fraude" ou deve ser "Aprovada".
    Adicione um atributo "Status" com um dos valores: "Possível Fraude" ou "Aprovado".

    Cada nova transação deve ser inserida dentro da lista do JSON.

    # Possíveis indicações de fraude
    - Transações com valores muito discrepantes
    - Transações que ocorrem em locais muito distantes um do outro

    Adote o formato de resposta abaixo para compor sua resposta.

    # Formato Saída
    {
        "transacoes": [
            {
            "id": "id",
            "tipo": "crédito ou débito",
            "estabelecimento": "nome do estabelecimento",
            "horário": "horário da transação",
            "valor": "R$XX,XX",
            "nome_produto": "nome do produto",
            "localização": "cidade - estado (País)"
            "status": ""
            },
        ]
    }

    """
    user_prompt = f"""
    Considere o CSV abaixo, onde cada linha é uma transação diferente: {transactions}.
    Sua resposta deve adotar o #Formato de Resposta (apenas um json sem outros comentários)
    """
    try:
        print('1 - Iniciou a análise de Fraude')
        message = client.messages.create(
            model=model,
            max_tokens=4000,
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
        json_response = json.loads(response)
        save_file('transacoes.json', response)
        print('2 - Finalizou a análise de Fraude')
        return json_response
    except anthropic.APIConnectionError as e:
        print("O servidor não pode ser acessado! Erro:", e.__cause__)
    except anthropic.RateLimitError as e:
        print("Um status code 429 foi recebido! Limite de acesso atingido.")
    except anthropic.APIStatusError as e:
        print(f"Um erro {e.status_code} foi recebido. Mais informações: {e.response}")
    except Exception as e:
        print(f"Ocorreu um erro inesperado: {e}")

def generate_report(transaction):
    system_prompt = f"""
    Para a seguinte transação, forneça um parecer, apenas se o status dela for de "Possível Fraude". Indique no parecer uma justificativa para que você identifique uma fraude.
    Transação: {transaction}

    ## Formato de Resposta
    "id": "id",
    "tipo": "crédito ou débito",
    "estabelecimento": "nome do estabelecimento",
    "horario": "horário da transação",
    "valor": "R$XX,XX",
    "nome_produto": "nome do produto",
    "localizacao": "cidade - estado (País)"
    "status": "",
    "parecer" : "Colocar Não Aplicável se o status for Aprovado"
    """
    try:
        print('3 - Iniciou a geração de parecer')
        message = client.messages.create(
            model=model,
            max_tokens=4000,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": system_prompt
                        }
                    ]
                }
            ]
        )
        response = message.content[0].text
        print('4 - Finalizou a geração de parecer')
        return response
    except anthropic.APIConnectionError as e:
        print("O servidor não pode ser acessado! Erro:", e.__cause__)
    except anthropic.RateLimitError as e:
        print("Um status code 429 foi recebido! Limite de acesso atingido.")
    except anthropic.APIStatusError as e:
        print(f"Um erro {e.status_code} foi recebido. Mais informações: {e.response}")
    except Exception as e:
        print(f"Ocorreu um erro inesperado: {e}")

def generate_recommendation(report):
    system_prompt = f"""
    Para a seguinte transação, forneça uma recomendação apropriada baseada no status e nos detalhes da Transação: {report}

    As recomendações podem ser "Notificar Cliente", "Acionar setor Anti-Fraude" ou "Realizar Verificação Manual".
    Elas devem ser escritas no formato técnico.

    Inclua também uma classificação do tipo de fraude, se aplicável.
    """
    try:
        print('5 - Iniciou a geração de recomendação')
        message = client.messages.create(
            model=model,
            max_tokens=4000,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": system_prompt
                        }
                    ]
                }
            ]
        )
        response = message.content[0].text
        print('6 - Finalizou a geração de recomendação')
        return response
    except anthropic.APIConnectionError as e:
        print("O servidor não pode ser acessado! Erro:", e.__cause__)
    except anthropic.RateLimitError as e:
        print("Um status code 429 foi recebido! Limite de acesso atingido.")
    except anthropic.APIStatusError as e:
        print(f"Um erro {e.status_code} foi recebido. Mais informações: {e.response}")
    except Exception as e:
        print(f"Ocorreu um erro inesperado: {e}")

if __name__ == "__main__":
    transactions = load_file('transacoes.csv')
    analyzed_transactions = analyze_transactions(transactions)

    for transaction in analyzed_transactions["transacoes"]:
        if transaction['status'] == "Possível Fraude":
            report = generate_report(transaction)
            recommendation = generate_recommendation(report)
            save_file(
                f'transacao-{transaction["id"]}-{transaction["nome_produto"]}-{transaction["status"]}.txt',
                recommendation
            )
