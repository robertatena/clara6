import streamlit as st
import matplotlib.pyplot as plt
import re
from docx import Document
import PyPDF2
from datetime import datetime

# Configuração inicial da página
st.set_page_config(
    page_title="Clara - Análise Jurídica de Contratos",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Chave PIX fornecida
PIX_KEY = "f0368079-483d-40af-9245-627b24f95da8"

# CSS personalizado
st.markdown(f"""
<style>
    .header-style {{
        font-size: 20px;
        font-weight: bold;
        color: #2e86de;
        padding: 10px;
        border-radius: 5px;
        margin-bottom: 10px;
    }}
    .risk-high {{
        background-color: #ff6b6b;
        color: white;
        padding: 5px 10px;
        border-radius: 5px;
        font-weight: bold;
    }}
    .risk-medium {{
        background-color: #feca57;
        color: white;
        padding: 5px 10px;
        border-radius: 5px;
        font-weight: bold;
    }}
    .risk-low {{
        background-color: #1dd1a1;
        color: white;
        padding: 5px 10px;
        border-radius: 5px;
        font-weight: bold;
    }}
    .contract-summary {{
        background-color: #f8f9fa;
        padding: 15px;
        border-radius: 10px;
        border-left: 5px solid #2e86de;
        margin-bottom: 20px;
    }}
    .clause-card {{
        padding: 15px;
        border-radius: 10px;
        margin-bottom: 15px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }}
    .footer {{
        font-size: 12px;
        text-align: center;
        margin-top: 30px;
        color: #7f8c8d;
    }}
    .user-info-form {{
        background-color: #f8f9fa;
        padding: 20px;
        border-radius: 10px;
        margin-bottom: 20px;
    }}
    .disclaimer {{
        font-size: 12px;
        color: #ff6b6b;
        margin-top: 10px;
    }}
    .pix-box {{
        background-color: #f0f8ff;
        padding: 20px;
        border-radius: 10px;
        border: 2px dashed #32CD32;
        margin: 20px 0;
        text-align: center;
    }}
    .pix-key {{
        font-family: monospace;
        background-color: #e6f3ff;
        padding: 10px;
        border-radius: 5px;
        word-break: break-all;
    }}
    .copy-btn {{
        background-color: #32CD32 !important;
        color: white !important;
        border: none !important;
    }}
</style>
""", unsafe_allow_html=True)

# [...] (mantenha todas as outras funções analisar_clausulas e gerar_resumo_contrato como estão)

def show_payment_section(num_clauses):
    total_amount = num_clauses * 5.00  # R$5 por cláusula
    
    st.markdown("---")
    st.markdown(f"## 💰 Pagamento para Visualizar Detalhes")
    st.markdown(f"""
    <div style='background-color:#fffacd; padding:15px; border-radius:10px; margin-bottom:20px'>
    Para visualizar os detalhes completos das {num_clauses} cláusulas identificadas e as recomendações específicas, 
    é necessário realizar um pagamento de <strong>R$ {total_amount:.2f}</strong> via PIX.
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("### ⚡ Método de Pagamento")
    
    # Seção PIX
    with st.container():
        st.markdown(f"""
        <div class='pix-box'>
            <h3 style='color:#32CD32'>Pagamento via PIX</h3>
            <p>Utilize a chave PIX abaixo para realizar o pagamento:</p>
            <div class='pix-key'>{PIX_KEY}</div>
            <p style='font-size:12px; margin-top:10px;'>Chave PIX (Copiar e Colar)</p>
            <button onclick="navigator.clipboard.writeText('{PIX_KEY}')" class='copy-btn'>Copiar Chave PIX</button>
            <p style='margin-top:15px;'>Envie o comprovante para <strong>financeiro@claraanalytics.com.br</strong></p>
        </div>
        """, unsafe_allow_html=True)
    
    # Verificação de pagamento (simulado)
    with st.form("payment_confirmation"):
        st.markdown("### ✅ Confirmação de Pagamento")
        email_comprovante = st.text_input("E-mail onde enviaremos a análise completa*", placeholder="seu@email.com")
        comprovante = st.file_uploader("Anexe o comprovante de pagamento (opcional)", type=["jpg", "png", "pdf"])
        
        submitted = st.form_submit_button("Já realizei o pagamento")
        
        if submitted:
            if not email_comprovante:
                st.error("Por favor, informe seu e-mail para envio da análise")
            else:
                st.success("""
                Pagamento confirmado! Estamos processando sua solicitação. 
                Você receberá a análise completa por e-mail em até 24 horas.
                """)
                return True
    return False

def main():
    # [...] (mantenha todo o código anterior até a análise do contrato)

            if resultados:
                # Calcula pontuação total
                pontuacao_total = sum(item["pontuacao"] for item in resultados if item["pontuacao"] > 0)
                clausulas_favoraveis = sum(1 for item in resultados if item["tipo"] == "favoravel")
                num_clausulas_problematicas = len([item for item in resultados if item["tipo"] != "favoravel"])
                
                # Determina nível de risco
                if pontuacao_total >= 30:
                    risco = "<span class='risk-high'>ALTO RISCO</span>"
                    recomendacao = "⚠️ Contrato com múltiplas cláusulas abusivas. Recomendamos NÃO ASSINAR e consultar um advogado para revisão completa."
                elif pontuacao_total >= 15:
                    risco = "<span class='risk-medium'>RISCO MODERADO</span>"
                    recomendacao = "🔍 Contrato com algumas cláusulas problemáticas. Recomendamos negociar alterações antes de assinar."
                else:
                    risco = "<span class='risk-low'>BAIXO RISCO</span>"
                    recomendacao = "✅ Contrato parece razoável, mas revise cuidadosamente as observações abaixo."
                
                # Mostra resumo de risco
                st.markdown("### 📊 Score do Contrato")
                col1, col2, col3 = st.columns(3)
                col1.markdown(f"**Pontuação Total de Risco**\n# {pontuacao_total} pts")
                col2.markdown(f"**Nível de Risco**\n<div style='margin-top:10px'>{risco}</div>", unsafe_allow_html=True)
                col3.markdown(f"**Cláusulas Favoráveis**\n# {clausulas_favoraveis}")
                
                st.markdown(f"""
                <div style='background-color:#f8f9fa; padding:15px; border-radius:10px; margin-top:20px'>
                <strong>📌 Recomendação:</strong> {recomendacao}
                </div>
                """, unsafe_allow_html=True)

                # Seção de pagamento PIX
                payment_confirmed = show_payment_section(num_clausulas_problematicas)
                
                # Se pagamento foi confirmado, mostra os detalhes
                if payment_confirmed:
                    st.markdown("---")
                    st.markdown("## ⚖️ Detalhes das Cláusulas (Análise Completa)")
                    
                    tab1, tab2 = st.tabs(["Cláusulas Problemáticas", "Cláusulas Favoráveis"])
                    
                    with tab1:
                        clausulas_problematicas = [item for item in resultados if item["tipo"] != "favoravel"]
                        if clausulas_problematicas:
                            for item in clausulas_problematicas:
                                st.markdown(f"""
                                <div class='clause-card' style='border-left: 5px solid {'#ff6b6b' if item["tipo"] == "abusiva" else '#feca57'};'>
                                    <h4>{'🚨 ' if item["tipo"] == "abusiva" else '⚠️ '}{item["mensagem"]}</h4>
                                    <p><strong>Trecho do contrato:</strong> <em>{item["contexto"]}</em></p>
                                    <p><strong>Problema:</strong> {item["explicacao"]}</p>
                                    <p><strong>Pontuação de risco:</strong> {item["pontuacao"]} pontos</p>
                                    <p><strong>✔️ Recomendação:</strong> {item["recomendacao"]}</p>
                                </div>
                                """, unsafe_allow_html=True)
                    
                    with tab2:
                        clausulas_favoraveis = [item for item in resultados if item["tipo"] == "favoravel"]
                        if clausulas_favoraveis:
                            for item in clausulas_favoraveis:
                                st.markdown(f"""
                                <div class='clause-card' style='border-left: 5px solid #1dd1a1;'>
                                    <h4>✅ {item["mensagem"]}</h4>
                                    <p><strong>Trecho do contrato:</strong> <em>{item["contexto"]}</em></p>
                                    <p><strong>Benefício:</strong> {item["explicacao"]}</p>
                                    <p><strong>Pontuação positiva:</strong> {item["pontuacao"]} pontos</p>
                                </div>
                                """, unsafe_allow_html=True)

                # [...] (mantenha o restante do código igual)

if __name__ == "__main__":
    main()