import json
import tkinter as ctk

# Configurações de caminho para os arquivos JSON
DATAPATH = 'exercicios.json'
TREINOS_PATH = 'treinos.json'

# Mensagens
MSG_EXERCICIO_CADASTRADO = "{} foi cadastrado com sucesso."
MSG_EXERCICIO_REMOVIDO = "{} removido com sucesso."
MSG_EXERCICIO_NAO_ENCONTRADO = "Exercício '{}' não encontrado."
MSG_ERRO_LER_ARQUIVO = "Erro ao ler o arquivo JSON. Verifique o formato."
MSG_ERRO_NUMERO_INTEIRO = "Por favor, insira um número inteiro."
MSG_OPCAO_INVALIDA = "Opção inválida!"
MSG_TREINO_CADASTRADO = "{} foi cadastrado como treino com sucesso."
MSG_TREINO_REMOVIDO = "{} removido como treino com sucesso."
MSG_TREINO_NAO_ENCONTRADO = "Treino '{}' não encontrado."

# Funções para manipulação de dados
def obter_numero_inteiro(valor):
    try:
        return int(valor)
    except ValueError:
        return None

def cadastrar_exercicio(nome, musculos, equipamentos, serie, repeticoes):
    novo_exercicio = {
        "nome": nome,
        "musculos": musculos.split(","),
        "equipamentos": equipamentos.split(","),
        "serie": serie,
        "repeticoes": repeticoes
    }

    try:
        with open(DATAPATH, "r+") as arquivo:
            dados = json.load(arquivo)
            dados.append(novo_exercicio)
            arquivo.seek(0)
            json.dump(dados, arquivo, indent=4)
        return MSG_EXERCICIO_CADASTRADO.format(novo_exercicio['nome'])
    except FileNotFoundError:
        with open(DATAPATH, "w") as arquivo:
            json.dump([novo_exercicio], arquivo, indent=4)
        return MSG_EXERCICIO_CADASTRADO.format(novo_exercicio['nome'])
    except json.decoder.JSONDecodeError:
        return MSG_ERRO_LER_ARQUIVO

def listar_exercicios():
    try:
        with open(DATAPATH, "r") as arquivo:
            dados = json.load(arquivo)
            return "\n".join([f"Nome: {exercicio['nome']}" for exercicio in dados])
    except (FileNotFoundError, json.decoder.JSONDecodeError):
        return MSG_ERRO_LER_ARQUIVO

def buscar_exercicio(nome):
    try:
        with open(DATAPATH, "r") as arquivo:
            dados = json.load(arquivo)
            for exercicio in dados:
                if exercicio["nome"].lower() == nome.lower():
                    return (
                        f"Nome: {exercicio['nome']}\n"
                        f"Músculos: {', '.join(exercicio['musculos'])}\n"
                        f"Equipamentos: {', '.join(exercicio['equipamentos'])}\n"
                        f"Séries: {exercicio['serie']}\n"
                        f"Repetições: {exercicio['repeticoes']}"
                    )
    except (FileNotFoundError, json.decoder.JSONDecodeError):
        return MSG_ERRO_LER_ARQUIVO

    return MSG_EXERCICIO_NAO_ENCONTRADO.format(nome)

# Classe da interface gráfica
class App(ctk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Gerenciador de Exercícios e Treinos")
        self.geometry("600x400")

        # Criação de frames
        self.frame = ctk.CTkFrame(self)
        self.frame.pack(pady=20, padx=20, fill="both", expand=True)

        # Título
        self.title_label = ctk.CTkLabel(self.frame, text="Gerenciador de Exercícios", font=("Arial", 24))
        self.title_label.pack(pady=10)

        # Campos de entrada
        self.nome_entry = ctk.CTkEntry(self.frame, placeholder_text="Nome do Exercício")
        self.nome_entry.pack(pady=5)

        self.musculos_entry = ctk.CTkEntry(self.frame, placeholder_text="Músculos (separados por vírgula)")
        self.musculos_entry.pack(pady=5)

        self.equipamentos_entry = ctk.CTkEntry(self.frame, placeholder_text="Equipamentos (separados por vírgula)")
        self.equipamentos_entry.pack(pady=5)

        self.serie_entry = ctk.CTkEntry(self.frame, placeholder_text="Número de Séries")
        self.serie_entry.pack(pady=5)

        self.repeticoes_entry = ctk.CTkEntry(self.frame, placeholder_text="Número de Repetições")
        self.repeticoes_entry.pack(pady=5)

        # Botão para cadastrar exercício
        self.cadastrar_button = ctk.CTkButton(self.frame, text="Cadastrar Exercício", command=self.cadastrar_exercicio)
        self.cadastrar_button.pack(pady=10)

        # Botão para listar exercícios
        self.listar_button = ctk.CTkButton(self.frame, text="Listar Exercícios", command=self.listar_exercicios)
        self.listar_button.pack(pady=10)

        # Campo para buscar exercício
        self.buscar_entry = ctk.CTkEntry(self.frame, placeholder_text="Nome do Exercício para Buscar")
        self.buscar_entry.pack(pady=5)

        # Botão para buscar exercício
        self.buscar_button = ctk.CTkButton(self.frame, text="Buscar Exercício", command=self.buscar_exercicio)
        self.buscar_button.pack(pady=10)

        # Label para exibir mensagens
        self.result_label = ctk.CTkLabel(self.frame, text="", wraplength=400)
        self.result_label.pack(pady=10)

    def cadastrar_exercicio(self):
        nome = self.nome_entry.get()
        musculos = self.musculos_entry.get()
        equipamentos = self.equipamentos_entry.get()
        serie = obter_numero_inteiro(self.serie_entry.get())
        repeticoes = obter_numero_inteiro(self.repeticoes_entry.get())

        if nome and musculos and equipamentos and serie is not None and repeticoes is not None:
            mensagem = cadastrar_exercicio(nome, musculos, equipamentos, serie, repeticoes)
            self.result_label.configure(text=mensagem)
        else:
            self.result_label.configure(text=MSG_ERRO_NUMERO_INTEIRO)

    def listar_exercicios(self):
        exercicios = listar_exercicios()
        self.result_label.configure(text=exercicios)

    def buscar_exercicio(self):
        nome = self.buscar_entry.get()
        resultado = buscar_exercicio(nome)
        self.result_label.configure(text=resultado)

if __name__ == "__main__":
    app = App()
    app.mainloop()