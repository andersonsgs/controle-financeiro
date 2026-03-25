import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="Controle Anderson", page_icon="📊")
st.title("📊 Controle Anderson")

# Conectar à planilha (usa os Secrets que vamos configurar)
conn = st.connection("gsheets", type=GSheetsConnection)

with st.form("lancamento"):
    descricao = st.text_input("Descrição")
    valor = st.number_input("Valor R$", min_value=0.0, step=0.01)
    submit = st.form_submit_button("Salvar na Planilha")

    if submit:
        if descricao and valor > 0:
            # Prepara os dados conforme suas colunas: data, ano, mes, descricao
            hoje = datetime.now()
            novo_dado = pd.DataFrame([{
                "data": hoje.strftime("%d/%m/%Y"),
                "ano": hoje.year,
                "mes": hoje.month,
                "descricao": descricao,
                "valor": valor # Adicionei valor, sua planilha precisa dessa coluna E
            }])
            
            # Lê os dados atuais e adiciona o novo
            dados_atuais = conn.read(worksheet="lancamentos")
            dados_finais = pd.concat([dados_atuais, novo_dado], ignore_index=True)
            
            # Envia de volta para o Google
            conn.update(worksheet="lancamentos", data=dados_finais)
            st.success("✅ Registrado com sucesso!")
        else:
            st.error("Preencha a descrição e o valor!")
            
