import os
from datetime import datetime
import gradio as gr
from zoneinfo import ZoneInfo
import pandas as pd

PASTA = os.path.dirname(os.path.abspath(__file__))
ARQUIVO_CSV = os.path.join(PASTA, "pacientes.csv")

COLUNAS = [
    "timestamp", "nome", "data_nascimento", "idade", "telefone",
    "convenio", "prioridade", "motivo",
]

FUSO = ZoneInfo("America/Sao_Paulo")  # servidores (ex.: Streamlit Cloud) rodam em UTC

CONVENIOS = ["Particular", "Unimed", "Bradesco Saúde", "SulAmérica", "Outro"]

def ultimos_pacientes(n=5):
    """Lê o CSV (se existir) e devolve as últimas n linhas."""
    if os.path.exists(ARQUIVO_CSV):
        return pd.read_csv(ARQUIVO_CSV).tail(n)
    return pd.DataFrame(columns=COLUNAS)

def cadastrar_paciente(nome, data_nascimento, idade, telefone, convenio, prioridade, motivo):
    # Validações simples antes de gravar
    if not nome or not nome.strip():
        return "⚠️ Informe o nome do paciente.", ultimos_pacientes()
    if idade is None or idade < 0 or idade > 120:
        return "⚠️ Informe uma idade válida (0 a 120).", ultimos_pacientes()
    if data_nascimento:
        try:
            datetime.strptime(data_nascimento.strip(), "%d/%m/%Y")
        except ValueError:
            return "⚠️ Data de nascimento deve estar no formato DD/MM/AAAA.", ultimos_pacientes()

    linha = {
        "timestamp": datetime.now(FUSO).strftime("%Y-%m-%d %H:%M:%S"),
        "nome": nome.strip(),
        "data_nascimento": (data_nascimento or "").strip(),
        "idade": int(idade),
        "telefone": (telefone or "").strip(),
        "convenio": convenio,
        "prioridade": int(prioridade),
        "motivo": (motivo or "").strip(),
    }
    novo = pd.DataFrame([linha], columns=COLUNAS)

    if os.path.exists(ARQUIVO_CSV):
        novo.to_csv(ARQUIVO_CSV, mode="a", header=False, index=False)
    else:
        novo.to_csv(ARQUIVO_CSV, mode="w", header=True, index=False)

    return f"✅ Paciente {linha['nome']} cadastrado com sucesso!", ultimos_pacientes()


# layout em coluna única (sem gr.Row com várias colunas) melhor no celular
with gr.Blocks(title="Cadastro de Pacientes") as demo:
    gr.Markdown("## 🏥 Cadastro de Pacientes\nRecepção — preencha os dados do paciente que chegou.")

    nome = gr.Textbox(label="Nome do paciente", placeholder="Ex.: Maria da Silva")
    data_nascimento = gr.Textbox(label="Data de nascimento (opcional)", placeholder="DD/MM/AAAA")
    idade = gr.Number(label="Idade", precision=0, minimum=0, maximum=120)
    telefone = gr.Textbox(label="Telefone (opcional)", placeholder="(11) 99999-9999")
    convenio = gr.Dropdown(CONVENIOS, label="Convênio", value="Particular")
    prioridade = gr.Slider(1, 5, step=1, value=3, label="Prioridade do atendimento (5 = urgente)")
    motivo = gr.Textbox(label="Motivo da consulta / observações", lines=3)

    botao = gr.Button("Cadastrar", variant="primary")
    saida_msg = gr.Textbox(label="Status", interactive=False)
    tabela = gr.Dataframe(label="Últimos pacientes cadastrados", interactive=False)

    botao.click(
        cadastrar_paciente,
        inputs=[nome, data_nascimento, idade, telefone, convenio, prioridade, motivo],
        outputs=[saida_msg, tabela],
    )
    # Recarrega a tabela do CSV sempre que alguém abre/atualiza a página
    demo.load(ultimos_pacientes, outputs=tabela)

if __name__ == "__main__":
    demo.launch()
