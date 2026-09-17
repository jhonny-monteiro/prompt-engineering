from helpers import load_file, save_file
from sentiment_analyzer import analyze_sentiment
from transaction_analyzer import analyze_transactions, generate_report, generate_recommendation
from profile_identifier import identify_profile
from food_categorizer import categorize_food

SEPARATOR = "=" * 60

def print_step(title):
    print(f"\n{SEPARATOR}")
    print(f"  {title}")
    print(f"{SEPARATOR}\n")

def run_sentiment_analysis():
    print_step("ETAPA 1: Análise de Sentimentos de Restaurantes")

    restaurant_list = [
        'Restaurante de Comida Vegana',
        'Restaurante de Comida Chinesa',
        'Restaurante de Bolos e Doces',
    ]
    for restaurant in restaurant_list:
        analyze_sentiment(restaurant)

    print("\nAnálise de sentimentos concluída!")

def run_transaction_analysis():
    print_step("ETAPA 2: Análise de Transações Financeiras")

    transactions = load_file('transacoes.csv')
    analyzed_transactions = analyze_transactions(transactions)

    if analyzed_transactions:
        for transaction in analyzed_transactions["transacoes"]:
            if transaction['status'] == "Possível Fraude":
                report = generate_report(transaction)
                recommendation = generate_recommendation(report)
                save_file(
                    f'transacao-{transaction["id"]}-{transaction["nome_produto"]}-{transaction["status"]}.txt',
                    recommendation
                )

    print("\nAnálise de transações concluída!")

def run_profile_identification():
    print_step("ETAPA 3: Identificação de Perfil de Consumo")

    assistant_response = identify_profile()
    response_text = assistant_response.content[0].text
    token_usage = assistant_response.usage

    print(response_text)
    print(f'\nTokens de entrada: {token_usage.input_tokens}')
    print(f'Tokens de saída:   {token_usage.output_tokens}')
    print("\nIdentificação de perfis concluída!")

def run_food_categorizer():
    print_step("ETAPA 4: Categorização de Alimentos (Demonstração)")

    demo_categories = "Frutas,Verduras,Legumes,Proteínas,Laticínios,Grãos"
    demo_foods = ["Maçã", "Brócolis", "Cenoura", "Frango", "Queijo", "Arroz"]

    print(f"Categorias: {demo_categories}")
    print(f"Alimentos:  {', '.join(demo_foods)}\n")

    for food_name in demo_foods:
        response_text = categorize_food(demo_categories, food_name)
        print(response_text)

    print("\nCategorização de alimentos concluída!")

if __name__ == "__main__":
    print_step("INICIANDO PIPELINE DE ANÁLISE DE DADOS COM IA")

    run_sentiment_analysis()
    run_transaction_analysis()
    run_profile_identification()
    run_food_categorizer()

    print_step("PIPELINE CONCLUÍDO COM SUCESSO")
