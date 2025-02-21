import streamlit as st

# Função para a página inicial (ainda vazia)
def pagina_inicial():
    st.title("Otimizador de Corte")
    st.write("Bem-vindo ao Otimizador de Corte!")

# Função para a página de corte
def pagina_corte():
    st.header("📐 Plano de Corte")
    st.write("Aqui você pode configurar as dimensões da chapa e as peças.")

    # Campos de entrada
    chapa_largura = st.number_input("Largura da Chapa (mm)", min_value=0, value=0)
    chapa_altura = st.number_input("Altura da Chapa (mm)", min_value=0, value=0)
    maquina = st.selectbox("Selecione a Máquina", ["Rauter", "Seccionadora"], index=0)

    # Tabela para entrada de peças (zerada inicialmente)
    st.subheader("Peças")
    pecas = st.table(pd.DataFrame(columns=["Largura (mm)", "Altura (mm)", "Quantidade"]))

# Função para a página de relatórios
def pagina_relatorios():
    st.header("📊 Relatórios")
    st.write("Aqui você pode ver os relatórios gerados.")

# Função para a página de configurações
def pagina_configuracoes():
    st.header("⚙️ Configurações")
    st.write("Aqui você pode configurar as opções gerais.")

# Função principal
def main():
    st.set_page_config(page_title="Otimizador de Corte", layout="wide")
    
    # Abas
    tab1, tab2, tab3 = st.tabs(["📐 Plano de Corte", "📊 Relatórios", "⚙️ Configurações"])
    
    with tab1:
        pagina_corte()
    
    with tab2:
        pagina_relatorios()
    
    with tab3:
        pagina_configuracoes()

if __name__ == "__main__":
    main()
