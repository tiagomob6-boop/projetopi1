import streamlit as st  # Importa a ferramenta para criar sites interativos 

import pandas as pd  # Importa pandas para trabalhar com tabelas de dados 

import numpy as np  # Importa numpy para cálculos numéricos 

import os  # Importa os para acessar arquivos do computador 

 

# ========================== 

# CONFIGURAÇÃO DA PÁGINA 

# ========================== 

st.set_page_config( 

    page_title="Sistema Nutricional",  # Título na aba do navegador 

    page_icon="🥗",  # Ícone na aba do navegador 

    layout="wide"  # Site ocupa a tela toda 

) 

 

@st.cache_data 

def carregar_dados(): 

    """ 

    Função que carrega a tabela de comidas (CSV) e bebidas (Excel) 

    Junta tudo em um único DataFrame com uma coluna 'Categoria' 

    """ 

    dataframes = []  # Lista para guardar os DataFrames de cada arquivo 

     

    try:  # Tenta carregar as comidas 

        # ===== CARREGAR COMIDAS (arquivo CSV) ===== 

        if os.path.exists("Tabela_Alimentos_Original.csv"): 

            df_comidas = pd.read_csv("Tabela_Alimentos_Original.csv", sep=";", encoding="latin1") 

            df_comidas.columns = df_comidas.columns.str.strip() 

            df_comidas['Alimento'] = df_comidas['Alimento'].str.strip() 

            df_comidas['Categoria'] = 'Comida' 

            df_comidas['Unidade'] = 'g' 

            dataframes.append(df_comidas) 

            st.sidebar.success(f"✅ Comidas carregadas: {len(df_comidas)} itens") 

        else: 

            st.sidebar.warning("⚠️ Arquivo Tabela_Alimentos_Original.csv não encontrado") 

    except Exception as e: 

        st.sidebar.error(f"Erro ao carregar comidas: {e}") 

     

    try:  # Tenta carregar as bebidas 

        # ===== CARREGAR BEBIDAS (arquivo Excel) ===== 

        if os.path.exists("tabela_bebidas.xlsx"): 

            # Lê o arquivo Excel de bebidas 

            df_bebidas = pd.read_excel("tabela_bebidas.xlsx") 

             

            # Remove espaços dos nomes das colunas 

            df_bebidas.columns = df_bebidas.columns.str.strip() 

             

            # Mostra as colunas para debug 

            st.sidebar.write("📊 Colunas do arquivo de bebidas:", df_bebidas.columns.tolist()) 

             

            # ===== RENOMEAR COLUNA BEBIDA PARA ALIMENTO ===== 

            if 'BEBIDA' in df_bebidas.columns: 

                df_bebidas = df_bebidas.rename(columns={'BEBIDA': 'Alimento'}) 

                st.sidebar.info("✅ Coluna 'BEBIDA' renomeada para 'Alimento'") 

            elif 'Bebida' in df_bebidas.columns: 

                df_bebidas = df_bebidas.rename(columns={'Bebida': 'Alimento'}) 

                st.sidebar.info("✅ Coluna 'Bebida' renomeada para 'Alimento'") 

            else: 

                # Procura qualquer coluna que tenha "bebida" no nome 

                for col in df_bebidas.columns: 

                    if 'bebida' in col.lower(): 

                        df_bebidas = df_bebidas.rename(columns={col: 'Alimento'}) 

                        st.sidebar.info(f"✅ Coluna '{col}' renomeada para 'Alimento'") 

                        break 

             

            # ===== RENOMEAR COLUNAS NUTRICIONAIS ===== 

            mapa_colunas = { 

                'Calorias (kcal)': ['kcal', 'caloria', 'energia', 'cal'], 

                'Proteínas (g)': ['proteína', 'proteina', 'prot', 'protein'], 

                'Carboidratos (g)': ['carboidrato', 'carb', 'carbo', 'carboidratos'], 

                'Fibras (g)': ['fibra', 'fibras', 'fiber'], 

                'Gorduras (g)': ['gordura', 'gord', 'lipídios', 'lipideos', 'gorduras'] 

            } 

             

            for coluna_padrao, possiveis_nomes in mapa_colunas.items(): 

                for col in df_bebidas.columns: 

                    if any(nome in col.lower() for nome in possiveis_nomes): 

                        df_bebidas = df_bebidas.rename(columns={col: coluna_padrao}) 

                        st.sidebar.info(f"  → {coluna_padrao}: '{col}'") 

                        break 

             

            # Remove espaços dos nomes das bebidas 

            df_bebidas['Alimento'] = df_bebidas['Alimento'].astype(str).str.strip() 

             

            # Adiciona colunas de controle 

            df_bebidas['Categoria'] = 'Bebida' 

            df_bebidas['Unidade'] = 'ml' 

             

            # Garante que todas as colunas necessárias existem 

            colunas_necessarias = ['Alimento', 'Calorias (kcal)', 'Proteínas (g)',  

                                   'Carboidratos (g)', 'Fibras (g)', 'Gorduras (g)'] 

             

            for col in colunas_necessarias: 

                if col not in df_bebidas.columns: 

                    df_bebidas[col] = 0 

                    st.sidebar.warning(f"⚠️ Coluna '{col}' não encontrada, criada com valor 0") 

             

            dataframes.append(df_bebidas) 

            st.sidebar.success(f"✅ Bebidas carregadas: {len(df_bebidas)} itens") 

        else: 

            st.sidebar.warning("⚠️ Arquivo tabela_bebidas.xlsx não encontrado") 

     

    except Exception as e: 

        st.sidebar.error(f"Erro ao carregar bebidas: {e}") 

        import traceback 

        st.sidebar.error(traceback.format_exc()) 

     

    # ===== JUNTAR TUDO ===== 

    if dataframes: 

        df = pd.concat(dataframes, ignore_index=True) 

         

        # Converte colunas numéricas 

        for col in df.columns: 

            if col not in ["Alimento", "Categoria", "Unidade", "#"]: 

                df[col] = df[col].astype(str).str.replace(",", ".").str.strip() 

                df[col] = pd.to_numeric(df[col], errors="coerce") 

         

        return df 

    else: 

        st.error("❌ Nenhum arquivo de dados foi carregado!") 

        return pd.DataFrame() 

     

    # ===== JUNTAR TUDO EM UM ÚNICO DATAFRAME ===== 

    if dataframes:  # Se tem pelo menos um arquivo carregado 

        # Junta todos os DataFrames da lista 

        df = pd.concat(dataframes, ignore_index=True) 

         

        # Converte colunas numéricas (troca vírgula por ponto) 

        for col in df.columns: 

            if col not in ["Alimento", "Categoria", "Unidade", "#"]: 

                # Converte para string, troca vírgula por ponto 

                df[col] = df[col].astype(str).str.replace(",", ".").str.strip() 

                # Converte para número 

                df[col] = pd.to_numeric(df[col], errors="coerce") 

         

        return df  # Devolve a tabela completa 

     

    else:  # Se não carregou nenhum arquivo 

        st.error("❌ Nenhum arquivo de dados foi carregado!") 

        return pd.DataFrame()  # Devolve tabela vazia 

 

# ========================== 

# INICIALIZAR SESSÃO 

# ========================== 

def init_session_state(): 

    """Cria todas as variáveis que precisamos guardar""" 

     

    if 'tdee_usuario' not in st.session_state: 

        st.session_state.tdee_usuario = 0  # Gasto diário 

     

    if 'total_kcal' not in st.session_state: 

        st.session_state.total_kcal = 0  # Total calorias 

     

    if 'total_proteina' not in st.session_state: 

        st.session_state.total_proteina = 0  # Total proteínas 

     

    if 'total_carboidrato' not in st.session_state: 

        st.session_state.total_carboidrato = 0  # Total carboidratos 

     

    if 'total_gordura' not in st.session_state: 

        st.session_state.total_gordura = 0  # Total gorduras 

     

    if 'total_fibra' not in st.session_state: 

        st.session_state.total_fibra = 0  # Total fibras 

     

    if 'lista_alimentos' not in st.session_state: 

        st.session_state.lista_alimentos = []  # Lista de alimentos adicionados 

 

## ========================== 

# ABA 1: SOBRE NUTRIÇÃO (página de informações educativas) 

# ========================== 

def aba_sobre_nutricao(): 

    """Primeira aba com explicações sobre nutrição""" 

     

    st.title("🥗 Guia Alimentar para uma Vida Saudável")  # Título grande 

     

    # Divide a tela em duas colunas: a primeira maior (2) e a segunda menor (1) 

    col1, col2 = st.columns([2, 1]) 

     

    with col1:  # Tudo que está aqui vai para a coluna da esquerda 

        st.markdown(""" 

        ### 🌱 A Base: Qualidade Segundo o Guia Alimentar 

         

        Antes de calcular números, o governo brasileiro destaca que a saúde vem da escolha dos alimentos. 

        """) 

         

        # Tabela de categorias de alimentos 

        categorias = pd.DataFrame({ 

            "Categoria": ["**In Natura**", "**Processados**", "**Ultraprocessados**"], 

            "Recomendação": ["Base da dieta", "Limitar", "Evitar"], 

            "Exemplos": ["Arroz, feijão, carnes, ovos, frutas, tubérculos",  

                        "Queijos, pães artesanais, conservas simples", 

                        "Refrigerantes, biscoitos recheados, macarrão instantâneo"] 

        }) 

         

        st.table(categorias)  # Mostra a tabela na tela 

         

        # ===== NOVO CONTEÚDO: DESINFORMAÇÃO NUTRICIONAL ===== 

        st.markdown("---")  # Linha divisória 

        st.markdown(""" 

        ### ⚠️ 1. Desinformação Nutricional 

         

        As redes sociais frequentemente propagam dietas milagrosas e o medo injustificado de alimentos (como glúten e carboidratos). Essas práticas, geralmente promovidas por pessoas sem qualificação técnica, podem levar a: 

         

        - **Deficiências nutricionais** e queda de imunidade 

        - **Transtornos alimentares** devido a restrições severas 

        - **Perda de fibras** e nutrientes essenciais 

        """) 

         

        # ===== NOVO CONTEÚDO: ENTENDENDO O GASTO ENERGÉTICO ===== 

        st.markdown("---")  # Linha divisória 

        st.markdown(""" 

        ### 🔥 2. Entendendo o Gasto Energético 

         

        Para um planejamento alimentar seguro, é preciso diferenciar tres conceitos-chave: 

         

        **TMB (Taxa Metabólica Basal):** É o gasto energético mínimo para manter as funções vitais (respiração, batimentos cardíacos) em repouso. Representa cerca de 60-75% do gasto diário e varia conforme idade, sexo, peso e altura. 

         

        **TMT (Taxa Metabólica Total):** É o somatório de toda a energia gasta em 24 horas. Ela inclui a TMB acrescida do gasto com atividades físicas (fator de atividade entre 1,2 e 1,9) e a digestão dos alimentos. 

                    
        Déficit calorico :Déficit calórico é o estado em que o corpo consome menos calorias do que gasta ao longo do dia. Esse desequilíbrio força o organismo a utilizar suas reservas de energia — principalmente gordura corporal — para se manter, resultando em emagrecimento. 

        Resumo dos Pontos Chave:
        Como funciona: Se você gasta 2000 calorias por dia (TMT - Gasto Energético Total) e consome apenas 1500, você tem um déficit de 500 calorias.
                    
        Emagrecimento: É o princípio fundamental para a perda de gordura. Sem déficit, não há perda de gordura significativa.
                    
        Como alcançar: Pode ser feito através da redução da ingestão calórica (comer menos/melhor) e/ou do aumento do gasto energético (exercícios físicos).
                    
        Déficit ideal: Reduções muito bruscas (passar fome) podem gerar perda de massa muscular e efeito sanfona. Recomenda-se um déficit gradual de 200 a 500 calorias por dia, dependendo da pessoa.
                    
        Qualidade importa: Não é só a quantidade. Consumir alimentos nutritivos ajuda a manter o corpo saudável enquanto perde gordura.
        """)

         

        # Cards explicativos para TMB e TMT 

        col_tmb, col_tmt = st.columns(2) 

        with col_tmb: 

            st.info(""" 

            **📊 TMB - Taxa Metabólica Basal** 

             

            • Gasto em repouso;

            • 60-75% do gasto diário;

            • Varia com idade, sexo, peso e altura;

            """) 

         

        with col_tmt: 

            st.info(""" 

            **📈 TMT - Taxa Metabólica Total** 

             

            • Gasto total do dia 

            • TMB + atividades físicas 

            • Fator de atividade: 1,2 a 1,9 

            """) 

         

        # ===== NOVO CONTEÚDO: COMO SE PROTEGER ===== 

        st.markdown("---")  # Linha divisória 

        st.markdown(""" 

        ### 🛡️ 3. Como se Proteger 

         

        - **Verifique a fonte:** Priorize informações de nutricionistas registrados e órgãos oficiais. 

         

        - **Desconfie de promessas rápidas:** Não existem "milagres" alimentares sem evidência científica.
                    

        - ** O que realmente é comprovado e que : para um emagrecimento saldavel é necesario faser déficit calorico.

         

        - **Individualidade:** Cálculos de TMB e dietas devem ser personalizados por profissionais, respeitando a biologia de cada pessoa. 

        """) 

     

    with col2:  # Tudo que está aqui vai para a coluna da direita 

        st.markdown(""" 

        ### 🎯 Recomendação Diária (por kg) 

         

        **Proteína:** 1.5g por kg   

        **Gordura:** 1.0g por kg   

        **Carboidrato:** 5.0g por kg   

         

        > **Exemplo:** Pessoa com 80kg precisa de 120g de proteína por dia 

        """) 

         

        st.markdown("---")  # Linha divisória 

         

        st.markdown(""" 

        ### 🍽️ Como Comer 

         

        - Comer em horários regulares 

        - Preferir comida caseira 

        - Evitar telas durante as refeições 

        - Mastigar bem os alimentos 

        - Beber água ao longo do dia 

        """) 

         

        st.markdown("---")  # Linha divisória 

         

        # Dica rápida sobre desinformação 

        st.warning(""" 

        **💡 Dica Importante:** 

         

        Desconfie de dietas da moda e alimentos "proibidos". A nutrição saudável é baseada em equilíbrio e evidências científicas, não em milagres!
                   
        É importante destacar que para o imagrecimento saudavel e necessario faser um defit calorico moderado cerca de 200  a 500 kcal abaixo da TMT!

        """) 

         

        st.markdown("---")  # Linha divisória 

         

        # Links úteis (fictícios - substitua pelos reais se quiser) 

        st.markdown(""" 

        ### 🔗 Fontes Confiáveis 

         

        - [Ministério da Saúde](https://www.gov.br/saude) 

        - [Guia Alimentar População Brasileira](https://www.gov.br/saude) 

        - [CFN - Conselho Federal de Nutrição](https://www.cfn.org.br) 

        """)# Entre na pasta do projeto 

 

 

# Execute o Streamlit 

# ========================== 

# ABA 2: CALCULADORA TMB 

# ========================== 

def aba_calculadora_tmb(): 

    """Segunda aba com calculadora de gasto calórico diário""" 

     

    st.title("⚖️ Calculadora de Gasto Diário") 

     

    col1, col2 = st.columns(2) 

     

    with col1: 

        st.subheader("📝 Dados Pessoais") 

         

        peso = st.number_input("Peso (kg)", min_value=20.0, max_value=200.0, value=70.0, step=0.1) 

        altura = st.number_input("Altura (cm)", min_value=100.0, max_value=250.0, value=170.0, step=0.1) 

        idade = st.number_input("Idade", min_value=15, max_value=100, value=30, step=1) 

        sexo = st.selectbox("Sexo", ["Homem", "Mulher"]) 

         

        atividade = st.selectbox( 

            "Nível de Atividade", 

            ["Sedentário", "Levemente ativo", "Moderado", "Muito ativo", "Extremamente ativo"] 

        ) 

         

        fatores = { 

            "Sedentário": 1.2, 

            "Levemente ativo": 1.375, 

            "Moderado": 1.55, 

            "Muito ativo": 1.725, 

            "Extremamente ativo": 1.9 

        } 

         

        if st.button("Calcular Gasto Diário", type="primary"): 

            if sexo == "Homem": 

                tmb = (10 * peso) + (6.25 * altura) - (5 * idade) + 5 

            else: 

                tmb = (10 * peso) + (6.25 * altura) - (5 * idade) - 161 

             

            tdee = tmb * fatores[atividade] 

            st.session_state.tdee_usuario = tdee 

             

            with col2: 

                st.subheader("📊 Resultados") 

                 

                col_a, col_b = st.columns(2) 

                with col_a: 

                    st.metric("Taxa Metabólica Basal (TMB)", f"{tmb:.0f} kcal") 

                with col_b: 

                    st.metric("Gasto Total Diário (TDEE)", f"{tdee:.0f} kcal") 

                 

                st.subheader("🥩 Recomendação de Macronutrientes") 

                st.info(f""" 

                - **Proteína:** {peso * 1.5:.0f}g por dia 

                - **Gordura:** {peso * 1.0:.0f}g por dia   

                - **Carboidrato:** {peso * 5.0:.0f}g por dia 

                """) 

     

    if st.session_state.tdee_usuario > 0 and 'col2' not in locals(): 

        with col2: 

            st.subheader("📊 Último Cálculo") 

            st.metric("Gasto Total Diário", f"{st.session_state.tdee_usuario:.0f} kcal") 

 

# ========================== 

# ABA 3: CALCULADORA DE REFEIÇÃO (COM ABAS SEPARADAS) 

# ========================== 

def aba_buscador_alimentos(): 

    """Terceira aba com abas separadas para Comidas e Bebidas""" 

     

    st.title("🔍 Calculadora de Refeição") 

     

    # Carrega a base de dados (comidas + bebidas) 

    df = carregar_dados() 

     

    if df.empty: 

        st.error("❌ Nenhuma base de dados carregada!") 

        return 

     

    # Mostra resumo na barra lateral 

    st.sidebar.subheader("📊 Resumo da Base") 

    st.sidebar.write(f"Total de itens: **{len(df)}**") 

    st.sidebar.write(f"Comidas: **{len(df[df['Categoria']=='Comida'])}**") 

    st.sidebar.write(f"Bebidas: **{len(df[df['Categoria']=='Bebida'])}**") 

     

    # Divide a tela principal em duas colunas 

    col_esquerda, col_direita = st.columns([1, 1]) 

     

    with col_esquerda:  # COLUNA DA ESQUERDA - BUSCA 

        # CRIA ABAS PARA SEPARAR COMIDAS E BEBIDAS 

        tab_comida, tab_bebida = st.tabs(["🍛 COMIDAS", "🥤 BEBIDAS"]) 

         

        with tab_comida:  # ===== ABA DE COMIDAS ===== 

            st.subheader("🍛 Buscar Comida") 

             

            # Filtra apenas COMIDAS 

            df_comidas = df[df['Categoria'] == 'Comida'] 

             

            # Campo de busca para comidas 

            busca_comida = st.text_input("Digite o nome da comida se não encontrar verifique a grafia ou tente escrever de outa forma:",  

                                       placeholder="Ex: arroz, frango, feijão...",  

                                       key="busca_comida") 

             

            # Filtra comidas baseado na busca 

            if busca_comida and len(busca_comida.strip()) > 0: 

                busca_limpa = busca_comida.strip().lower() 

                alimentos_filtrados = df_comidas[df_comidas['Alimento'].str.strip().str.lower().str.contains(busca_limpa, na=False)] 

                st.caption(f"🔍 Encontradas: {len(alimentos_filtrados)} comidas") 

            else: 

                alimentos_filtrados = df_comidas 

                st.caption(f"📋 Mostrando todas as {len(df_comidas)} comidas") 

             

            # Se encontrou alguma comida 

            if not alimentos_filtrados.empty: 

                # Menu para escolher a comida 

                alimento_selecionado = st.selectbox( 

                    "Selecione a comida:", 

                    alimentos_filtrados['Alimento'].tolist(), 

                    key="select_comida" 

                ) 

                 

                # Pega as informações da comida escolhida 

                info_alimento = df[df['Alimento'] == alimento_selecionado].iloc[0] 

                 

                st.subheader("⚖️ Quantidade") 

                quantidade = st.number_input("Quantidade (gramas):",  

                                           min_value=1, max_value=2000, value=100, step=10,  

                                           key="qtd_comida") 

                 

                # Calcula os nutrientes 

                kcal = info_alimento['Calorias (kcal)'] * quantidade 

                proteina = info_alimento['Proteínas (g)'] * quantidade 

                carboidrato = info_alimento['Carboidratos (g)'] * quantidade 

                fibra = info_alimento['Fibras (g)'] * quantidade 

                gordura = info_alimento['Gorduras (g)'] * quantidade 

                 

                # Mostra os nutrientes 

                st.subheader("📊 Informação Nutricional") 

                 

                col_n1, col_n2, col_n3, col_n4, col_n5 = st.columns(5) 

                with col_n1: 

                    st.metric("Calorias", f"{kcal:.0f} kcal") 

                with col_n2: 

                    st.metric("Proteínas", f"{proteina:.1f}g") 

                with col_n3: 

                    st.metric("Carboidratos", f"{carboidrato:.1f}g") 

                with col_n4: 

                    st.metric("Gorduras", f"{gordura:.1f}g") 

                with col_n5: 

                    st.metric("Fibras", f"{fibra:.1f}g") 

                 

                # Botão para adicionar comida 

                if st.button("➕ Adicionar comida à refeição", use_container_width=True, key="btn_comida"): 

                    st.session_state.lista_alimentos.append({ 

                        'alimento': alimento_selecionado, 

                        'quantidade': quantidade, 

                        'unidade': 'g', 

                        'kcal': kcal, 

                        'proteina': proteina, 

                        'carboidrato': carboidrato, 

                        'gordura': gordura, 

                        'fibra': fibra, 

                        'categoria': 'Comida' 

                    }) 

                     

                    st.session_state.total_kcal += kcal 

                    st.session_state.total_proteina += proteina 

                    st.session_state.total_carboidrato += carboidrato 

                    st.session_state.total_gordura += gordura 

                    st.session_state.total_fibra += fibra 

                     

                    st.success(f"{alimento_selecionado} adicionado!") 

                    st.rerun() 

         

        with tab_bebida:  # ===== ABA DE BEBIDAS ===== 

            st.subheader("🥤 Buscar Bebida") 

             

            # Filtra apenas BEBIDAS 

            df_bebidas = df[df['Categoria'] == 'Bebida'] 

             

            # Campo de busca para bebidas 

            busca_bebida = st.text_input("Digite o nome da bebida:",  

                                       placeholder="Ex: água, suco, refrigerante...",  

                                       key="busca_bebida") 

             

            # Filtra bebidas baseado na busca 

            if busca_bebida and len(busca_bebida.strip()) > 0: 

                busca_limpa = busca_bebida.strip().lower() 

                alimentos_filtrados = df_bebidas[df_bebidas['Alimento'].str.strip().str.lower().str.contains(busca_limpa, na=False)] 

                st.caption(f"🔍 Encontradas: {len(alimentos_filtrados)} bebidas") 

            else: 

                alimentos_filtrados = df_bebidas 

                st.caption(f"📋 Mostrando todas as {len(df_bebidas)} bebidas") 

             

            # Se encontrou alguma bebida 

            if not alimentos_filtrados.empty: 

                # Menu para escolher a bebida 

                alimento_selecionado = st.selectbox( 

                    "Selecione a bebida:", 

                    alimentos_filtrados['Alimento'].tolist(), 

                    key="select_bebida" 

                ) 

                 

                # Pega as informações da bebida escolhida 

                info_alimento = df[df['Alimento'] == alimento_selecionado].iloc[0] 

                 

                st.subheader("🥤 Volume") 

                quantidade = st.number_input("Quantidade (ml):",  

                                           min_value=1, max_value=2000, value=200, step=50,  

                                           key="qtd_bebida") 

                 

                # Calcula os nutrientes 

                kcal = info_alimento['Calorias (kcal)'] * quantidade 

                proteina = info_alimento['Proteínas (g)'] * quantidade 

                carboidrato = info_alimento['Carboidratos (g)'] * quantidade 

                fibra = info_alimento['Fibras (g)'] * quantidade 

                gordura = info_alimento['Gorduras (g)'] * quantidade 

                 

                # Mostra os nutrientes 

                st.subheader("📊 Informação Nutricional") 

                 

                col_n1, col_n2, col_n3, col_n4, col_n5 = st.columns(5) 

                with col_n1: 

                    st.metric("Calorias", f"{kcal:.0f} kcal") 

                with col_n2: 

                    st.metric("Proteínas", f"{proteina:.1f}g") 

                with col_n3: 

                    st.metric("Carboidratos", f"{carboidrato:.1f}g") 

                with col_n4: 

                    st.metric("Gorduras", f"{gordura:.1f}g") 

                with col_n5: 

                    st.metric("Fibras", f"{fibra:.1f}g") 

                 

                # Botão para adicionar bebida 

                if st.button("➕ Adicionar bebida à refeição", use_container_width=True, key="btn_bebida"): 

                    st.session_state.lista_alimentos.append({ 

                        'alimento': alimento_selecionado, 

                        'quantidade': quantidade, 

                        'unidade': 'ml', 

                        'kcal': kcal, 

                        'proteina': proteina, 

                        'carboidrato': carboidrato, 

                        'gordura': gordura, 

                        'fibra': fibra, 

                        'categoria': 'Bebida' 

                    }) 

                     

                    st.session_state.total_kcal += kcal 

                    st.session_state.total_proteina += proteina 

                    st.session_state.total_carboidrato += carboidrato 

                    st.session_state.total_gordura += gordura 

                    st.session_state.total_fibra += fibra 

                     

                    st.success(f"{alimento_selecionado} adicionado!") 

                    st.rerun() 

     

    with col_direita:  # COLUNA DA DIREITA - LISTA DA REFEIÇÃO 

        st.subheader("📝 Minha Refeição") 

         

        if st.session_state.lista_alimentos: 

            for i, item in enumerate(st.session_state.lista_alimentos): 

                with st.container(): 

                    col_del, col_info = st.columns([1, 5]) 

                    with col_del: 

                        if st.button(f"❌", key=f"del_{i}"): 

                            st.session_state.total_kcal -= item['kcal'] 

                            st.session_state.total_proteina -= item['proteina'] 

                            st.session_state.total_carboidrato -= item['carboidrato'] 

                            st.session_state.total_gordura -= item['gordura'] 

                            st.session_state.total_fibra -= item['fibra'] 

                            st.session_state.lista_alimentos.pop(i) 

                            st.rerun() 

                    with col_info: 

                        # Mostra ícone diferente para comida e bebida 

                        icone = "🍛" if item['categoria'] == 'Comida' else "🥤" 

                        st.write(f"{icone} **{item['alimento']}** ({item['quantidade']}{item['unidade']})") 

                        st.caption(f"{item['kcal']:.0f} kcal | P:{item['proteina']:.1f}g | C:{item['carboidrato']:.1f}g | G:{item['gordura']:.1f}g | F:{item['fibra']:.1f}g") 

             

            st.divider() 

            st.subheader("📊 Total da Refeição") 

             

            col_t1, col_t2, col_t3, col_t4, col_t5 = st.columns(5) 

            with col_t1: 

                st.metric("Total kcal", f"{st.session_state.total_kcal:.0f}") 

            with col_t2: 

                st.metric("Proteínas", f"{st.session_state.total_proteina:.1f}g") 

            with col_t3: 

                st.metric("Carboidratos", f"{st.session_state.total_carboidrato:.1f}g") 

            with col_t4: 

                st.metric("Gorduras", f"{st.session_state.total_gordura:.1f}g") 

            with col_t5: 

                st.metric("Fibras", f"{st.session_state.total_fibra:.1f}g") 

             

            if st.session_state.tdee_usuario > 0: 

                porcentagem = (st.session_state.total_kcal / st.session_state.tdee_usuario) * 100 

                st.progress(min(porcentagem/100, 1.0)) 

                st.caption(f"{porcentagem:.1f}% do gasto diário de {st.session_state.tdee_usuario:.0f} kcal") 

        else: 

            st.info("Sua refeição está vazia. Adicione comidas e bebidas usando as abas ao lado!") 

 

# ========================== 

# FUNÇÃO PRINCIPAL 

# ========================== 

def main(): 

    """Função principal que junta todas as partes do site""" 

     

    init_session_state()  # Inicializa as variáveis 

     

    # Cria as 3 abas principais 

    tab1, tab2, tab3 = st.tabs(["📖 Sobre Nutrição", "⚖️ Calculadora TMB", "🔍 Calculadora de Refeição"]) 

     

    with tab1: 

        aba_sobre_nutricao() 

     

    with tab2: 

        aba_calculadora_tmb() 

     

    with tab3: 

        aba_buscador_alimentos() 

     

    st.divider() 

    st.caption("Sistema Nutricional - Baseado no Guia Alimentar para a População Brasileira") 

 

# ========================== 

# PONTO DE PARTIDA 

# ========================== 

if __name__ == "__main__": 

    main() 