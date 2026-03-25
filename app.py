import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import datetime

# Configuração da página
st.set_page_config(page_title="Controle Anderson", page_icon="📊")
st.title("📊 Controle Financeiro Anderson")

# Conectar à planilha usando os Secrets do Streamlit
conn = st.connection("gsheets", type=GSheetsConnection)

# Formulário de entrada
with st.form("meu_form"):
    descricao = st.text_input("Descrição")
    valor = st.number_input("Valor R$", min_value=0.0, step=0.01)
    tipo = st.selectbox("Tipo", ["Despesa", "Receita"])
    categoria = st.text_input("Categoria")
    banco = st.text_input("Banco")
    parcelas = st.number_input("Parcelas", min_value=1, value=1)
    
    submit = st.form_submit_button("Salvar na Planilha")

    if submit:
        if descricao and valor > 0:
            hoje = datetime.now()
            
            # ESTA PARTE É A MAIS IMPORTANTE: 
            # Os nomes abaixo devem ser IGUAIS à primeira linha da sua planilha.
            novo_dado = pd.DataFrame([{
                "data": hoje.strftime("%d/%m/%Y"),
                "ano": hoje.year,
                "mes": hoje.month,
                "descricao": descricao,
                "tipo": tipo,
                "categoria": categoria,
                "banco": banco,
                "valor_total": valor,  # Ajustado com underline como você confirmou
                "parcelas": parcelas
            }])
            
            try:
                # Tenta ler a aba 'lancamentos'
                df_atual = conn.read(worksheet="lancamentos")
                
                # Junta o novo dado com o que já existe
                df_final = pd.concat([df_atual, novo_dado], ignore_index=True)
                
                # Atualiza a planilha no Google
                conn.update(worksheet="lancamentos", data=df_final)
                st.success("✅ Gravado com sucesso em São Gonçalo do Sapucaí!")
            except Exception as e:
                st.error(f"Erro ao salvar: Verifique se a aba se chama 'lancamentos' e se você é 'Editor' na planilha.")
        else:
            st.error("Por favor, preencha a descrição e o valor!")
            
