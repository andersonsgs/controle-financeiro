import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

# Configuração simples
st.set_page_config(page_title="Finanças Anderson")
st.title("📊 Controle Anderson")

# Link da sua planilha
url = "https://docs.google.com/spreadsheets/d/1y06RxnrltG1VqHS1pomuY-ZoeND0jBPU8S41OHnUSHc/edit?usp=sharing"

# Conexão
conn = st.connection("gsheets", type=GSheetsConnection)

# Formulário
with st.form("meu_form"):
    desc = st.text_input("Descrição")
    valor = st.number_input("Valor R$", min_value=0.0)
    if st.form_submit_button("Salvar"):
        st.success(f"Registrado: {desc} - R$ {valor}")
