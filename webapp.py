import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st

# Inicializar dados
dados = pd.DataFrame({"Produto": [], "Preco": []})

# Salvar os dados em um arquivo CSV
dados.to_csv("compras.csv", index=False)

# Interface do usuário
st.title("Controle de Gastos")
orcamento = st.number_input("Orçamento:", min_value=0.0)

# Calcula o total gasto
total = dados["Preco"].sum() if not dados.empty else 0

# Formulário para nova compra
with st.form("nova_compra"):
    produto = st.text_input("Produto:")
    preco = st.number_input("Preço:", min_value=0.0)

    if st.form_submit_button("Adicionar"):
        if preco <= (orcamento - total):
            nova_linha = pd.DataFrame({"Produto": [produto], "Preco": [preco]})
            dados = pd.concat([dados, nova_linha], ignore_index=True)
            dados.to_csv("compras.csv", index=False)
            st.success("Compra adicionada!")
        else:
            st.error("Sem orçamento suficiente!")

# Exibir gráfico se orçamento foi definido
if orcamento > 0:
    # Criar gráfico Donut
    fig, ax = plt.subplots(figsize=(8, 8))
    if not dados.empty:
        produtos = dados["Produto"].tolist()
        valores = dados["Preco"].tolist()
        restante = orcamento - total
        if restante > 0:
            produtos.append("Disponível")
            valores.append(restante)
        plt.pie(
            valores,
            labels=produtos,
            autopct='%1.1f%%',
            pctdistance=0.85
        )
        plt.title(f"Orçamento: {orcamento}€")

        # Criar círculo central
        centro = plt.Circle((0, 0), 0.70, fc='white')
        ax.add_artist(centro)

        st.pyplot(fig)
        st.dataframe(dados)
        st.write(f"Total Gasto: {total}€")
        st.write(f"Resta: {orcamento - total}€")
