def load_file(file_name):
    try:
        with open(file_name, "r", encoding="utf-8") as file:
            data = file.read()
            return data
    except IOError as e:
        print(f"Erro: {e}")

def save_file(file_name, content):
    try:
        with open(file_name, "w", encoding="utf-8") as file:
            file.write(content)
    except IOError as e:
        print(f"Erro ao salvar arquivo: {e}")
