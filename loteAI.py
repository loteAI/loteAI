import streamlit as st
from datetime import datetime

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="LoteIA - Admin", page_icon="🔑")

# Inicialização do estado do sistema
if "status" not in st.session_state:
    st.session_state.status = "visitante"
if "creditos" not in st.session_state:
    st.session_state.creditos = 0

# --- CONFIGURAÇÕES DO DONO ---
CHAVE_PIX = "49999688715"
SENHA_MESTRE = "bebe211826" # Sua senha secreta para acesso vitalício

# --- LÓGICA DE CALENDÁRIO ---
hoje = datetime.now()
dia_hoje = hoje.day

# --- REGRA DE BLOQUEIO (DIA 07) ---
# Se for Criador Vitalício, o bloqueio nunca acontece.
bloqueado = False
if st.session_state.status != "CRIADOR_VITALICIO":
    if dia_hoje >= 7 and st.session_state.status != "assinante_pago":
        bloqueado = True

# --- FUNÇÃO DA ÁREA SECRETA DO CRIADOR ---
def area_do_criador(identificador):
    st.markdown("---")
    if st.checkbox("Sou o criador", key=f"check_{identificador}"):
        senha = st.text_input("Digite a senha mestre:", type="password", key=f"pass_{identificador}")
        if senha == SENHA_MESTRE:
            if st.button("🔓 Ativar Meu Acesso Vitalício", key=f"btn_{identificador}"):
                st.session_state.status = "CRIADOR_VITALICIO"
                st.session_state.creditos = 999999
                st.success("Acesso de Criador ativado! Você tem passe livre para sempre.")
                st.rerun()
        elif senha != "":
            st.error("Senha incorreta!")

# --- BARRA LATERAL ---
with st.sidebar:
    st.title("👤 Área do Cliente")
    
    if st.session_state.status == "visitante":
        st.info("Bem-vindo ao LoteIA")
    else:
        # Exibição de Status Personalizada
        if st.session_state.status == "CRIADOR_VITALICIO":
            st.success("⭐ STATUS: CRIADOR")
            st.caption("Acesso Vitalício Liberado")
        else:
            st.success(f"Status: {st.session_state.status.upper()}")
            st.metric("Créditos", st.session_state.creditos)
            
            if 1 <= dia_hoje < 7:
                st.warning(f"⚠️ Vencimento em {7 - dia_hoje} dias!")

    st.markdown("---")
    st.write("Suporte: @benicioterci")
    st.markdown(f'[**Instagram do Criador**](https://www.instagram.com/benicioterci)')
    
    if st.button("❌ Sair / Logout"):
        st.session_state.status = "visitante"
        st.rerun()

# --- ÁREA PRINCIPAL DO APLICATIVO ---
st.title("🤖 LoteIA")

# 1. TELA DE BLOQUEIO (ATIVADA A PARTIR DO DIA 07)
if bloqueado:
    st.error("🚫 ACESSO SUSPENSO")
    st.subheader("O pagamento da mensalidade venceu dia 07.")
    st.write("Para continuar usando a fábrica de textos, faça o PIX abaixo:")
    
    st.markdown("### 📥 Pagamento via PIX:")
    st.code(CHAVE_PIX, language="text")
    st.info("Após pagar, envie o comprovante para o administrador liberar seu acesso.")
    
    # Sua entrada secreta na tela de bloqueio
    area_do_criador("bloqueio")

# 2. TELA PARA VISITANTES (ANTES DE PAGAR OU USAR SENHA)
elif st.session_state.status == "visitante":
    st.header("Sua Fábrica de Conteúdo em Lote")
    st.write("Gere dezenas de textos de uma só vez com o poder da IA.")
    
    st.markdown("---")
    st.subheader("Escolha um Plano")
    if st.button("💎 Assinar Plano Mensal - R$ 15,00"):
        st.session_state.checkout = True

    if st.session_state.get("checkout"):
        st.write("**Realize o pagamento para liberar o acesso:**")
        st.code(CHAVE_PIX, language="text")
        
        # Sua entrada secreta na tela de checkout
        area_do_criador("checkout")

# 3. PAINEL DE TRABALHO (LIBERADO APENAS PARA PAGANTES OU CRIADOR)
else:
    st.write(f"### 🚀 Painel de Geração")
    
    user_key = st.text_input("Sua Chave API Google Gemini:", type="password", help="Pegue sua chave no Google AI Studio")
    
    col1, col2 = st.columns(2)
    with col1:
        tema = st.text_input("Sobre o que vamos escrever?")
    with col2:
        qtd = st.number_input("Quantidade de textos:", 1, 15, 5)
    
    if st.button("Gerar Textos em Lote"):
        if not user_key:
            st.error("Por favor, insira sua Chave API do Google.")
        elif st.session_state.status != "CRIADOR_VITALICIO" and st.session_state.creditos < qtd:
            st.error("Créditos insuficientes para esta quantidade!")
        else:
            # Se não for o criador, desconta os créditos
            if st.session_state.status != "CRIADOR_VITALICIO":
                st.session_state.creditos -= qtd
                
            st.success(f"Iniciando a produção de {qtd} textos... Aguarde!")
            # Simulação de geração
            for i in range(qtd):
                st.write(f"✅ **Texto {i+1} finalizado com sucesso!**")
            
            if st.session_state.status != "CRIADOR_VITALICIO":
                st.info(f"Você ainda possui {st.session_state.creditos} créditos.")

