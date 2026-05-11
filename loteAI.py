import streamlit as st
from datetime import datetime

# --- CONFIGURAÇÃO ---
st.set_page_config(page_title="LoteIA - Sistema de Bloqueio", page_icon="🔒")

# Inicialização do estado
if "status" not in st.session_state:
    st.session_state.status = "visitante"
if "creditos" not in st.session_state:
    st.session_state.creditos = 0

# --- DADOS DO DONO ---
CHAVE_PIX = "49999688715"
URL_QR_CODE = "https://seu-link-aqui.com/qrcode.png" # Coloque o link da sua imagem aqui

# --- LÓGICA DE CALENDÁRIO ---
hoje = datetime.now()
dia_hoje = hoje.day

# --- REGRA DE BLOQUEIO ---
# Se for dia 07 ou depois, e o usuário não renovou (ainda está como trial ou créditos zerados)
bloqueado = False
if dia_hoje >= 7 and st.session_state.status != "assinante_pago":
    bloqueado = True

# --- BARRA LATERAL ---
with st.sidebar:
    st.title("👤 Área do Cliente")
    
    if st.session_state.status == "visitante":
        if st.button("🎁 Ativar 30 Dias Grátis"):
            st.session_state.status = "trial"
            st.session_state.creditos = 5
            st.rerun()
    else:
        st.success(f"Status: {st.session_state.status.upper()}")
        st.metric("Créditos", st.session_state.creditos)
        
        # Aviso pré-vencimento (Dia 01 ao 06)
        if 1 <= dia_hoje < 7:
            st.warning(f"⚠️ Vencimento em {7 - dia_hoje} dias!")

        st.markdown("---")
        st.write("Siga @benicioterci")
        st.markdown(f'[**Vá ao instagram do criador**](https://www.instagram.com/benicioterci)')
        
        if st.button("❌ Sair"):
            st.session_state.status = "visitante"
            st.rerun()

# --- ÁREA PRINCIPAL ---
st.title("🤖 LoteIA")

# TELA DE BLOQUEIO (DIA 07)
if bloqueado:
    st.error("🚫 ACESSO SUSPENSO")
    st.subheader("Hoje é dia de pagamento (Dia 07)")
    st.write("Para continuar usando a fábrica de textos, realize o pagamento da sua mensalidade.")
    
    st.info(f"**Valor do seu plano:** R$ 15,00 (ou o valor acordado)")
    
    # Exibe o QR Code para desbloqueio
    st.markdown("### 📥 Pague com PIX para desbloquear:")
    # st.image(URL_QR_CODE, width=250) # Descomente quando tiver a imagem
    st.code(CHAVE_PIX, language="text")
    st.caption("Após o pagamento, o administrador liberará seu acesso.")

    # Botão de Administrador para você liberar o cliente
    if st.checkbox("Liberar acesso (Dono do App)"):
        if st.button("Confirmar Recebimento"):
            st.session_state.status = "assinante_pago"
            st.session_state.creditos += 15 # Adiciona créditos ou renova
            st.success("Acesso Liberado!")
            st.rerun()

# TELA PARA VISITANTES
elif st.session_state.status == "visitante":
    st.header("Sua Fábrica de Conteúdo em Lote")
    st.write("Gere até 15 textos de uma vez e economize horas de trabalho.")
    if st.button("Quero começar agora!"):
        st.session_state.status = "trial"
        st.rerun()

# TELA DE TRABALHO (SÓ FUNCIONA SE NÃO ESTIVER BLOQUEADO)
else:
    st.write(f"### Painel de Geração")
    user_key = st.text_input("Sua Chave API Google:", type="password")
    
    tema = st.text_input("Tema dos textos:")
    qtd = st.number_input("Quantidade (1-15):", 1, 15)
    
    if st.button("🚀 Gerar em Lote"):
        if not user_key:
            st.error("Insira sua chave API na esquerda.")
        elif st.session_state.creditos < qtd:
            st.error("Créditos insuficientes! Pague para adicionar mais.")
        else:
            st.session_state.creditos -= qtd
            st.success(f"Processando {qtd} textos...")
            for i in range(qtd):
                st.write(f"✅ Texto {i+1} finalizado!")
