# Atividade Prática – Aula 1: Gradio x Streamlit

Sistema de cadastro de pacientes um consultório médico, feito duas vezes para comparar as duas bibliotecas.

| Pasta | Biblioteca | Onde roda | Onde ficam os dados |
|---|---|---|---|
| `gradio_app/` | Gradio (`gr.Blocks`) | Local (máquina do aluno) | `gradio_app/pacientes.csv` |
| `streamlit_app/` | Streamlit (`st.form`) | Streamlit Community Cloud | `st.session_state` + botão **Baixar CSV** |

**Campos:** nome, data de nascimento, idade, telefone, convênio, prioridade (1–5, 5 = urgente) e motivo da consulta. Cada envio grava uma linha com data/hora.

## Como rodar

```bash
pip install -r requirements.txt

# Versão Gradio (abre em http://127.0.0.1:7860)
cd gradio_app
python gradio_app.py

# Versão Streamlit (abre em http://localhost:8501)
cd streamlit_app
streamlit run streamlit_app.py
```

## Entrega

- App publicado no Streamlit Cloud: ativ1-ads-luiza.streamlit.app
- Print da interface Gradio rodando localmente: [`prints/gradio_desktop.png`](prints/gradio_desktop.png) e [`prints/gradio_celular.png`](prints/gradio_celular.png)
- CSV de exemplo gerado nos testes: [`gradio_app/pacientes.csv`](gradio_app/pacientes.csv)

## Comparação rápida

| | Gradio | Streamlit |
|---|---|---|
| Modelo de execução | Eventos: só a função ligada ao botão roda | O script inteiro roda de novo a cada interação |
| Agrupar campos | `gr.Blocks` + componentes | `st.form` (envia tudo de uma vez) |
| Estado | Arquivo CSV no disco | `st.session_state` (por sessão do navegador) |
| Publicação | Local, ou link temporário com `share=True`, ou Hugging Face Spaces | Streamlit Community Cloud direto do GitHub |
| Persistência na nuvem | — | Disco efêmero: os dados somem quando o app reinicia, por isso o download do CSV |

> Os dados são fictícios.
