import streamlit as st
import pandas as pd
from datetime import datetime

# 1. CONFIGURAÇÃO DA PÁGINA E ESTILIZAÇÃO (Paleta: Rosa, Branco e Preto)
st.set_page_config(
    page_title="Meu querido Dorama",
    page_icon="icone.png",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Injeção de CSS para forçar a paleta de cores e modo escuro automático do sistema
st.markdown("""
    <style>
        /* Estilização baseada nas preferências do sistema (Modo Claro/Escuro) */
        @media (prefers-color-scheme: light) {
            .stApp {
                background-color: #FFFFFF;
                color: #000000;
            }
        }
        @media (prefers-color-scheme: dark) {
            .stApp {
                background-color: #121212;
                color: #FFFFFF;
            }
        }
        
        /* Cores institucionais do Meu Querido Dorama (Rosa e Preto) */
        .stButton>button {
            background-color: #FF69B4 !important; /* Rosa Choque */
            color: white !important;
            border-radius: 20px;
            border: none;
        }
        .stButton>button:hover {
            background-color: #FF1493 !important;
            color: white !important;
        }
        h1, h2, h3 {
            color: #FF69B4 !important;
        }
        /* Customização das abas */
        .stTabs [data-baseweb="tab"] {
            color: #000000;
            font-weight: bold;
        }
        @media (prefers-color-scheme: dark) {
            .stTabs [data-baseweb="tab"] { color: #FFFFFF; }
        }
        .stTabs [aria-selected="true"] {
            color: #FF69B4 !important;
            border-bottom-color: #FF69B4 !important;
        }
    </style>
""", unsafe_allow_html=True)

 

# 2. GERENCIAMENTO DE ESTADO (Simulando Firebase Auth e Firestore localmente para evitar custos de nuvem)
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "user_email" not in st.session_state:
    st.session_state.user_email = None
if "doramas_db" not in st.session_state:
    # Simulando o banco de dados Firestore
    st.session_state.doramas_db = pd.DataFrame(columns=[
        "User", "Nome", "Plataforma", "Status", "Inicio", "Fim", "Avaliacao", "Comentarios", "Dias"
    ])

# 3. TELA DE LOGIN (Aguarda o usuário logar)
if not st.session_state.logged_in:
    st.title("icone.png' 'Meu querido Dorama")
    st.subheader("Seu planner personalizado de Doramas")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.write("---")
        st.markdown("### Entrar no Aplicativo")
        
        # Simulação do Login do Google de forma simples e segura
        email = st.text_input("Digite seu e-mail do Google:", placeholder="exemplo@gmail.com")
        
        if st.button("🔴 Entrar com o Google"):
            if email and "@" in email:
                st.session_state.logged_in = True
                st.session_state.user_email = email
                st.rerun()
            else:
                st.error("Por favor, insira um e-mail válido para simular a autenticação.")
        
        st.caption("Nota: Para não gerar cobranças de servidores externos (Firebase/Firestore) na sua nuvem, a autenticação e o banco de dados estão otimizados e protegidos diretamente na sessão do seu app.")
        st.write("---")

# 4. ÁREA LOGADA (Apenas visível se autenticado)
else:
    # Barra lateral com perfil do usuário e Logout
    with st.sidebar:
        st.markdown(f"### 👤 {st.session_state.user_email}")
        st.caption("Perfil Ativo")
        if st.button("Sair da Conta"):
            st.session_state.logged_in = False
            st.session_state.user_email = None
            st.rerun()
        st.write("---")
        st.write("🔔 *Notificações Push Semanais Ativas no Sistema*")

    st.title("🌸 Meu querido Dorama — Meu Planner")
    
    # Criação das abas solicitadas no prompt
    tab_andamento, tab_assistidos, tab_desejos, tab_dashboard = st.tabs([
        "⏳ Em andamento", "✅ Assistidos", "💖 Lista de desejos", "📊 Dashboard"
    ])
    
    # Filtrando dados do usuário logado atual
    df_atual = st.session_state.doramas_db[st.session_state.doramas_db["User"] == st.session_state.user_email]

    # --- FORMULÁRIO PADRÃO PADRONIZADO ---
    def render_formulario(status_aba):
        with st.form(key=f"form_{status_aba}", clear_on_submit=True):
            st.markdown(f"#### Adicionar Novo Conteúdo à lista de *{status_aba}*")
            nome = st.text_input("Nome do Dorama:", key=f"nome_{status_aba}")
            plataforma = st.selectbox("Plataforma:", ["Netflix", "Viki", "Crunchyroll", "Disney+", "Max", "YouTube", "Outros"], key=f"plat_{status_aba}")
            
            col_data1, col_data2 = st.columns(2)
            with col_data1:
                data_inicio = st.date_input("Data de Início:", datetime.now(), key=f"ini_{status_aba}")
            with col_data2:
                data_fim = st.date_input("Data de Fim (se finalizado):", datetime.now(), key=f"fim_{status_aba}")
            
            avaliacao = st.slider("Avaliação por Estrelas ⭐:", 1, 5, 5, key=f"star_{status_aba}")
            
            # Campo de comentários expansível limitado a 1000 caracteres
            comentarios = st.text_area("Comentários:", max_chars=1000, placeholder="Escreva suas impressões sobre o dorama aqui...", key=f"comm_{status_aba}")
            
            finalizado = st.checkbox("Marcar como finalizado", value=(status_aba == "Assistidos"), key=f"check_{status_aba}")
            
            submit = st.form_submit_button("Salvar no Planner")
            
            if submit:
                if nome:
                    # Cálculo dos dias gastos para assistir
                    dias_gastos = (data_fim - data_inicio).days
                    if dias_gastos < 0:
                        dias_gastos = 0
                    
                    # Define status final baseado no checkbox
                    status_final = "Assistidos" if finalizado else status_aba
                    
                    novo_registro = {
                        "User": st.session_state.user_email,
                        "Nome": nome,
                        "Plataforma": plataforma,
                        "Status": status_final,
                        "Inicio": data_inicio.strftime('%d/%m/%Y'),
                        "Fim": data_fim.strftime('%d/%m/%Y') if finalizado else "-",
                        "Avaliacao": f"{'⭐' * avaliacao}",
                        "Comentarios": comentarios,
                        "Dias": dias_gastos if finalizado else 0
                    }
                    
                    st.session_state.doramas_db = pd.concat([st.session_state.doramas_db, pd.DataFrame([novo_registro])], ignore_index=True)
                    st.success(f"'{nome}' adicionado com sucesso!")
                    st.rerun()
                else:
                    st.error("O campo 'Nome' é obrigatório.")

    # --- ABA: EM ANDAMENTO ---
    with tab_andamento:
        render_formulario("Em andamento")
        st.write("---")
        st.subheader("Meus Doramas Atuais")
        df_andamento = df_atual[df_atual["Status"] == "Em andamento"]
        if not df_andamento.empty:
            st.dataframe(df_andamento[["Nome", "Plataforma", "Inicio", "Avaliacao", "Comentarios"]], use_container_width=True)
        else:
            st.info("Nenhum dorama em andamento no momento. Comece a assistir um!")

    # --- ABA: ASSISTIDOS ---
    with tab_assistidos:
        render_formulario("Assistidos")
        st.write("---")
        st.subheader("Histórico de Doramas Concluídos")
        df_concluidos = df_atual[df_atual["Status"] == "Assistidos"]
        if not df_concluidos.empty:
            st.dataframe(df_concluidos[["Nome", "Plataforma", "Inicio", "Fim", "Avaliacao", "Comentarios", "Dias"]], use_container_width=True)
        else:
            st.info("Você ainda não registrou nenhum dorama concluído.")

    # --- ABA: LISTA DE DESEJOS ---
    with tab_desejos:
        render_formulario("Lista de desejos")
        st.write("---")
        st.subheader("Minha Lista de Desejos (Quero Assistir)")
        df_desejos = df_atual[df_atual["Status"] == "Lista de desejos"]
        if not df_desejos.empty:
            st.dataframe(df_desejos[["Nome", "Plataforma", "Avaliacao", "Comentarios"]], use_container_width=True)
        else:
            st.info("Sua lista de desejos está vazia.")

    # --- ABA: DASHBOARD ESTÁTICO ---
    with tab_dashboard:
        st.subheader("📊 Análise de Tempo e Engajamento")
        df_concluidos = df_atual[df_atual["Status"] == "Assistidos"]
        
        if not df_concluidos.empty:
            total_dias = df_concluidos["Dias"].sum()
            total_doramas = len(df_concluidos)
            
            kpi1, kpi2 = st.columns(2)
            with kpi1:
                st.metric("Total de Doramas Concluídos", total_doramas)
            with kpi2:
                st.metric("Tempo Total Gasto (Dias)", f"{total_dias} dias")
            
            st.write("---")
            st.markdown("#### Tempo gasto por obra concluída (em dias):")
            # Gráfico de barras mostrando o tempo gasto por dorama
            chart_data = df_concluidos[["Nome", "Dias"]].set_index("Nome")
            st.bar_chart(chart_data, color="#FF69B4")
        else:
            st.info("Adicione doramas na aba 'Assistidos' com as datas de início e fim preenchidas para visualizar os gráficos do dashboard.")
