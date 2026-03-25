import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import datetime

st.title("CONTROLE FINANCEIRO ANDERSON")

# Conectar à planilha
conn = st.connection("gsheets", type=GSheetsConnection)

# Formulário de entrada
with st.form(key="finance_form"):
    col1, col2 = st.columns(2)
    with col1:
        data = st.date_input("Data do Gasto", datetime.now())
        descricao = st.text_input("Descrição (Ex: Aluguel)")
        categoria = st.selectbox("Categoria", ["Alimentação", "Transporte", "Lazer", "Contas Fixas", "Outros"])
        valor = st.number_input("Valor Unitário (R$)", min_value=0.0, format="%.2f")
    
    with col2:
        banco = st.text_input("Banco (Ex: Nubank)")
        parcelas = st.number_input("Número de Parcelas", min_value=1, value=1)
        vencimento = st.date_input("Data de Vencimento", datetime.now())
        valor_total = valor * parcelas
        status = st.selectbox("Status", ["Pago", "Pendente"])

    submit_button = st.form_submit_button(label="Salvar na Planilha")

if submit_button:
    if descricao == "" or valor == 0:
        st.warning("Por favor, preencha a descrição e o valor.")
    else:
        # Criar a linha com as 9 COLUNAS EXATAS da sua planilha
        nova_linha = pd.DataFrame([{
            "data": data.strftime("%d/%m/%Y"),
            "descricao": descricao,
            "categoria": categoria,
            "valor": valor,
            "banco": banco,
            "parcelas": parcelas,
            "vencimento": vencimento.strftime("%d/%m/%Y"),
            "vt": vt,
            "status": status
        }])

        try:
            # Tenta ler os dados atuais da aba 'lancamentos'
            dados_atuais = conn.read(worksheet="lancamentos", usecols=list(range(9)))
            # Junta com a nova linha
            dados_atualizados = pd.concat([dados_atuais, nova_linha], ignore_index=True)
            # Salva de volta
            conn.update(worksheet="lancamentos", data=dados_atualizados)
            st.success("✅ Gravado com sucesso na planilha!")
        except Exception as e:
            st.error(f"Erro: Verifique se a aba se chama 'lancamentos' e se você é 'Editor' na planilha.")
            st.info("Dica: No notebook, confira se o link nos Secrets termina em 'usp=sharing'.")
