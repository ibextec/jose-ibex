import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4

# Função para gerar o plano 2D
def gerar_plano_2d(plano_corte, chapa_largura, chapa_altura):
    fig, ax = plt.subplots(figsize=(10, 7))
    ax.set_title("Plano de Corte")
    ax.set_xlim(0, chapa_largura)
    ax.set_ylim(0, chapa_altura)
    
    for _, x, y, w, h in plano_corte:
        cor = plt.cm.tab20(np.random.randint(20))
        ret = plt.Rectangle((x, y), w, h, edgecolor='black', facecolor=cor, alpha=0.6)
        ax.add_patch(ret)
        ax.text(x + w/2, y + h/2, f"{w}x{h}", ha='center', va='center', fontsize=8)
    
    plt.gca().invert_yaxis()
    return fig

# Função para gerar o relatório de fitas e cortes
def gerar_relatorio_fitas_e_cortes(plano_corte, espessura_chapa):
    total_metros = 0
    for _, x, y, w, h in plano_corte:
        perimetro = 2 * (w + h)
        total_metros += perimetro / 1000  # Convertendo para metros
    return f"Espessura da chapa: {espessura_chapa}mm\nMetragem linear total de corte: {total_metros:.2f}m\nCusto estimado: R${total_metros * 2.5:.2f} (considerando R$2,50/m)"

# Função para gerar o relatório de aproveitamento
def gerar_relatorio_aproveitamento(plano_corte, chapa_largura, chapa_altura, num_chapas):
    area_total = chapa_largura * chapa_altura * num_chapas
    area_utilizada = sum(w * h for _, _, _, w, h in plano_corte)
    aproveitamento = (area_utilizada / area_total) * 100
    return f"Aproveitamento: {aproveitamento:.2f}%"

# Função para gerar o relatório de etiquetas de identificação
def gerar_relatorio_etiquetas(plano_corte):
    etiquetas = []
    for idx, (_, x, y, w, h) in enumerate(plano_corte, 1):
        etiquetas.append(
            f"Peça {idx}\n"
            f"Posição: ({x+1}mm, {y+1}mm)\n"
            f"Dimensões: {w}x{h}mm"
        )
    return "\n".join(etiquetas)

# Função para gerar o relatório em PDF
def gerar_relatorio_pdf(plano_corte, espessura_chapa, chapa_largura, chapa_altura, num_chapas):
    buffer = BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=A4)
    
    pdf.setTitle("Relatório de Corte")
    pdf.setFont("Helvetica-Bold", 16)
    pdf.drawString(50, 750, "Relatório de Corte")
    
    pdf.setFont("Helvetica", 12)
    pdf.drawString(50, 730, f"Espessura da chapa: {espessura_chapa}mm")
    pdf.drawString(50, 710, f"Total de chapas: {num_chapas}")
    pdf.drawString(50, 690, f"Largura da chapa: {chapa_largura}mm")
    pdf.drawString(50, 670, f"Altura da chapa: {chapa_altura}mm")
    
    pdf.showPage()
    pdf.save()
    
    buffer.seek(0)
    return buffer

# Função para a página de corte
def pagina_corte():
    st.header("📐 Plano de Corte")
    st.write("Aqui você pode configurar as dimensões da chapa e as peças.")

    # Campos de entrada
    chapa_largura = st.number_input("Largura da Chapa (mm)", min_value=0, value=1000)
    chapa_altura = st.number_input("Altura da Chapa (mm)", min_value=0, value=500)
    espessura_chapa = st.number_input("Espessura da Chapa (mm)", min_value=0, value=1)
    maquina = st.selectbox("Selecione a Máquina", ["Rauter", "Seccionadora"], index=0)
    
    # Tabela para entrada de peças (zerada inicialmente)
    st.subheader("Peças")
    pecas = st.data_editor(
        pd.DataFrame(columns=["Largura (mm)", "Altura (mm)", "Quantidade"]),
        num_rows="dynamic"
    )
    
    if st.button("Calcular"):
        pecas_list = []
        for _, row in pecas.iterrows():
            pecas_list.extend([(row["Largura (mm)"], row["Altura (mm)"], row["Quantidade"])])
        
        # Simulação de corte (por simplicidade, vamos usar uma lista fixa)
        plano_corte = [
            (0, 0, 0, 100, 50),
            (0, 0, 100, 50, 1),
            (0, 50, 0, 100, 50),
            (0, 50, 100, 50, 1),
        ]
        
        # Gerar o plano 2D
        plano_fig = gerar_plano_2d(plano_corte, chapa_largura, chapa_altura)
        st.pyplot(plano_fig)
        
        # Gerar o relatório de fitas e cortes
        relatorio_fitas = gerar_relatorio_fitas_e_cortes(plano_corte, espessura_chapa)
        st.subheader("Relatório de Fitas e Cortes")
        st.write(relatorio_fitas)
        
        # Gerar o relatório de aproveitamento
        relatorio_aproveitamento = gerar_relatorio_aproveitamento(plano_corte, chapa_largura, chapa_altura, len(plano_corte))
        st.subheader("Relatório de Aproveitamento")
        st.write(relatorio_aproveitamento)
        
        # Gerar o relatório de etiquetas de identificação
        relatorio_etiquetas = gerar_relatorio_etiquetas(plano_corte)
        st.subheader("Etiquetas de Identificação")
        st.text_area("", relatorio_etiquetas, height=200)
        
        # Gerar o relatório em PDF
        pdf_buffer = gerar_relatorio_pdf(plano_corte, espessura_chapa, chapa_largura, chapa_altura, len(plano_corte))
        st.download_button(
            label="Baixar Relatório PDF",
            data=pdf_buffer,
            file_name="relatorio_corte.pdf",
            mime="application/pdf"
        )

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
