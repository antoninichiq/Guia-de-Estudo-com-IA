import streamlit as st
from langchain.llms import CTransformers
import matplotlib.pyplot as plt
from spacy import load


# Inicializando a LLAMA 2
llm = CTransformers(
    model="llama-2-7b-chat.ggmlv3.q4_K_M.bin",
    model_type="llama"
)
# Inicializando algumas variáveis
if 'user_materia' not in st.session_state:
    st.session_state['user_materia'] = ''
if 'indice_pergunta' not in st.session_state:
    st.session_state['indice_pergunta'] = 0
if 'progresso' not in st.session_state:
    st.session_state.progresso = 0
if 'materia_atual' not in st.session_state:
    st.session_state.materia_atual = None
if 'dicio_grafico' not in st.session_state:
    st.session_state.dicio_grafico = {}
nlp = load('pt_core_news_lg') # Modelo de processamento de linguagem natural (PLN) do pacote spaCy para português
gramatica = ''


st.title('Guia de Estudo com IA')
perguntas_respostas = {
    'Física': [
        {
            "pergunta": "O que é um campo magnético?",
            "opcoes": [
                "Uma região ao redor de um ímã onde forças magnéticas são exercidas.",
                "Uma área onde a gravidade é nula.",
                "O espaço ao redor de uma carga elétrica.",
                "Uma região onde ocorrem apenas fenômenos ópticos."
            ],
            "resposta_correta": "Uma região ao redor de um ímã onde forças magnéticas são exercidas."
        },
        {
            "pergunta": "O que caracteriza um condutor elétrico?",
            "opcoes": [
                "Um material que não permite o fluxo de eletricidade.",
                "Um material que armazena cargas elétricas.",
                "Um material que permite o livre movimento de elétrons.",
                "Um material que sempre produz campos magnéticos."
            ],
            "resposta_correta": "Um material que permite o livre movimento de elétrons."
        },
        {
            "pergunta": "Qual é a afirmação da Segunda Lei da Termodinâmica?",
            "opcoes": [
                "A energia não pode ser criada nem destruída",
                "A entropia de um sistema isolado tende a aumentar",
                "O calor sempre passa de um corpo mais quente para um mais frio",
                "A pressão é inversamente proporcional ao volume"
            ],
            "resposta_correta": "A entropia de um sistema isolado tende a aumentar"
        },
        {
            "pergunta": "O que é calor específico?",
            "opcoes": [
                "A energia necessária para alterar o estado físico de um material.",
                "A quantidade de calor liberada durante uma reação química.",
                "A temperatura na qual um líquido começa a ferver.",
                "A quantidade de calor necessária para aumentar a temperatura de um objeto em 1°C."
            ],
            "resposta_correta": "A quantidade de calor necessária para aumentar a temperatura de um objeto em 1°C."
        },
        {
            "pergunta": "O que é refração da luz?",
            "opcoes": [
                "A absorção da luz por um material opaco",
                "A reflexão da luz em uma superfície polida",
                "O desvio da luz ao passar por um material transparente",
                "A difração da luz através de uma fenda"
            ],
            "resposta_correta": "O desvio da luz ao passar por um material transparente"
        },
        {
            "pergunta": "Qual a principal diferença entre a luz refletida e a luz refratada?",
            "opcoes": [
                "A luz refletida muda de direção, enquanto a luz refratada muda de velocidade.",
                "A luz refletida muda de velocidade, enquanto a luz refratada muda de direção.",
                "Não há diferença; ambas são fenômenos idênticos.",
                "A luz refletida é absorvida, enquanto a luz refratada é transmitida."
            ],
            "resposta_correta": "A luz refletida muda de direção, enquanto a luz refratada muda de velocidade."
        },
        {
            "pergunta": "Qual fenômeno ocorre quando duas ondas se encontram e ocorre um aumento da amplitude?",
            "opcoes": [
                "Interferência destrutiva",
                "Interferência construtiva",
                "Ressonância",
                "Refração"
            ],
            "resposta_correta": "Interferência construtiva"
        },
        
    ],
    "Matemática": [
    {"pergunta": "Qual é a raiz quadrada de 144?", "opcoes": ["12", "14", "16", "18"], "resposta_correta": "12"},
    {"pergunta": "Se você divide 20 por 0,5, qual é o resultado?", "opcoes": ["10", "40", "0", "15"], "resposta_correta": "40"},
    {"pergunta": "Qual é o valor de Pi (truncado para duas casas decimais)?", "opcoes": ["3.13", "3.14", "3.15", "3.16"], "resposta_correta": "3.14"},
    {"pergunta": "Quanto é 15% de 200?", "opcoes": ["25", "35", "40", "30"], "resposta_correta": "30"},
    {"pergunta": "Se um triângulo tem lados de 3 cm, 4 cm e 5 cm, que tipo de triângulo é?", "opcoes": ["Escaleno", "Equilátero", "Retângulo", "Isósceles"], "resposta_correta": "Retângulo"},
    {"pergunta": "Qual é a soma dos ângulos internos de um quadrado?", "opcoes": ["360 graus","270 graus", "180 graus", "90 graus"], "resposta_correta": "360 graus"},
    {"pergunta": "Se a equação é 2x + 6 = 14, qual é o valor de x?", "opcoes": ["2","3","4", "5"], "resposta_correta": "4"}
],
    "Química": [
    {"pergunta": "Qual é o símbolo químico do Ouro?", "opcoes": ["Cu", "Au", "Ag", "Fe"], "resposta_correta": "Au"},
    {"pergunta": "O que H2O representa?", "opcoes": ["Dióxido de Carbono","Acetona", "Ácido Sulfúrico", "Água"], "resposta_correta": "Água"},
    {"pergunta": "Qual é o número atômico do Carbono?", "opcoes": ["6","8", "12", "14"], "resposta_correta": "6"},
    {"pergunta": "Qual elemento é conhecido por ter o maior número atômico na Tabela Periódica?", "opcoes": ["Flúor","Urânio", "Oganessônio", "Califórnio"], "resposta_correta": "Oganessônio"},
    {"pergunta": "O que é uma ligação covalente?", "opcoes": ["Compartilhamento de elétrons", "Atração de prótons", "Transferência de elétrons", "Atração magnética entre moléculas"], "resposta_correta": "Compartilhamento de elétrons"},
    {"pergunta": "Qual destes não é um gás nobre?", "opcoes": ["Hélio", "Neônio", "Radônio", "Cálcio"], "resposta_correta": "Cálcio"},
    {"pergunta": "Qual é a fórmula química do sal de cozinha?", "opcoes": ["H2O2", "NaCl", "KCl", "CaCl2"], "resposta_correta": "NaCl"}
], 
    "Gramática": [
    {"pergunta": "Qual é o plural de 'lápis'?", "opcoes": ["Lápiss", "Lápises", "Lápis", "Lápeis"], "resposta_correta": "Lápis"},
    {"pergunta": "Em 'Ela canta muito bem', qual é o verbo?", "opcoes": [ "Ela", "Canta","Muito", "Bem"], "resposta_correta": "Canta"},
    {"pergunta": "Qual palavra está no diminutivo: 'casa', 'homenzinho', 'casarão', homúnculo?", "opcoes": ["Casa", "Homenzinho", "Casarão", "Homúnculo"], "resposta_correta": "Homúnculo"},
    {"pergunta": "Qual é a função do pronome 'se' em 'Eles se abraçaram'?", "opcoes": ["Indicativo", "Reflexivo", "Condicional", "Bicondicional"], "resposta_correta": "Reflexivo"},
    {"pergunta": "Em 'João gosta de correr', 'correr' é um:", "opcoes": ["Predicado", "Substantivo", "Verbo", "Infinitivo"], "resposta_correta": "Infinitivo"},
    {"pergunta": "Qual é a forma correta: 'Ele interviu' ou 'Ele interveio'?", "opcoes": ["Interviu", "Interveio", "Ambas estão corretas"], "resposta_correta": "Interveio"},
    {"pergunta": "Qual palavra é um exemplo de um advérbio: 'Rapidamente', 'Feliz', 'Beleza', 'Correr'?", "opcoes": ["Rapidamente", "Feliz", "Beleza", "Correr"], "resposta_correta": "Rapidamente"}
]
}


def gerar_resposta(materia, tema):# Definição da função gerar_resposta pela ia
    with st.spinner('Gerando uma resposta com base em suas preferências...'):
        st.session_state.boolean = True
        if user_tema == 'Gramática':
            if gramatica == 'Criar uma redação com inteligência artificial':
                prompt = f"Faça uma redação com até 160 palavras sobre o tema: {tema}"
                response = llm.predict(prompt)
        elif tema:
            if gramatica == 'Análise Sintática':
                response = None
            else:
                prompt = f"Você é um professor de {materia}. Explique em até 160 palavras o tema: {tema}."
                response = llm.predict(prompt)
        return response
       
user_materia = st.selectbox('Escolha uma matéria', ['Selecionar', 'Matemática', 'Química', 'Física', 'Gramática'])

def grafic():
    materias = list(st.session_state.dicio_grafico.keys())
    valores = list(st.session_state.dicio_grafico.values())

    fig, ax = plt.subplots() 

    # Criando o gráfico de barras
    ax.bar(materias, valores)

    # Adicionando títulos e rótulos
    ax.set_title("Desempenho nas Matérias")
    ax.set_xlabel("Matérias")
    ax.set_ylabel("Valores")

    return fig

if user_materia != 'Selecionar': # Verifica se o usuário selecionou uma matéria (não a opção padrão)

    with st.sidebar.expander('Mostrar Gráfico de rendimento'):
        figura = grafic()
        st.pyplot(figura)

    if user_materia == "Gramática":
        gramatica = st.selectbox('Escolha uma opção', ['Selecionar','Fazer uma Pergunta','Criar uma redação com inteligência artificial', 'Análise Sintática'])
        
        if gramatica != 'Selecionar':
            if gramatica == 'Criar uma redação com inteligência artificial':
                user_tema = st.text_area(label='Insira o tema da redação?', max_chars=25)

            elif gramatica == 'Análise Sintática': 
                user_tema = st.text_area(label='Coloque um texto aqui', max_chars=200)
                doc = nlp(user_tema)
                filtro = st.multiselect(
                    'Filtro',
                    ['VERB', 'PROPN', 'ADV', 'AUX'],
                    default=['VERB', 'PROPN']
                )
                with st.expander('Dados do spaCy'):
                    st.json(doc.to_json())

                container = st.container()
                a, b, c = container.columns(3)
                a.subheader('Palavras')
                b.subheader('Análise Sintática')
                c.subheader('Morfologia')
                for t in doc:
                    if t.tag_ in filtro:
                        container = st.container()
                        a, b, c = container.columns(3)
                        a.info(t)
                        b.warning(t.tag_)
                        c.error(t.morph)
            else:
                user_tema = st.text_area(label='Qual tema você tem dúvida', max_chars=25)
    else:
        user_tema = st.text_area(label='Qual tema você tem dúvida', max_chars=25)

    if st.button('Aplicar'):
        if user_tema:
            response = gerar_resposta(user_materia, user_tema) # resposta da ia
            if response is not None:
                st.markdown(response)
                st.success('Espero que a resposta tenha ajudado! Se tiver mais dúvidas, sinta-se à vontade para perguntar.')
        else:
            st.error("Por favor, insira um tema para gerar a resposta.")

if user_materia != st.session_state.materia_atual: # Reseta a barra de progresso e o indice quando muda de materia
    st.session_state.progresso = 0
    st.session_state.indice_pergunta = 0
    st.session_state.materia_atual = user_materia


st.session_state['user_materia'] = user_materia
if user_materia != 'Selecionar': # Jogo de pergunta e resposta com a barra de progresso
    
    pergunta_atual = perguntas_respostas[user_materia][st.session_state['indice_pergunta']]
    st.subheader(f'Vamos testar seu conhecimento em {user_materia}!')
    st.write(pergunta_atual['pergunta']) # Pergunta que aparece na tela 
    opcao_escolhida = st.radio("Alternativas", pergunta_atual['opcoes'])

    if st.button("Validar resposta"): 
        if opcao_escolhida == pergunta_atual['resposta_correta']:
            st.success("Resposta correta!")
            st.session_state.progresso += 1 
        else:
            st.error("Resposta incorreta.")

    st.session_state.dicio_grafico[st.session_state['user_materia']] = st.session_state.progresso # Armazena materia e progresso no dicionario para o gráfico

    def proxima_pergunta():
        st.session_state['indice_pergunta'] += 1
        if st.session_state['indice_pergunta'] >= len(perguntas_respostas[user_materia]):
            st.session_state['indice_pergunta'] = 0
            st.info(f"Você completou todas as perguntas de {st.session_state.user_materia}! Refaça ou troque a matéria!.")

    def criar_botao(): # Cria o botao da função acima
        col1, col2 = st.columns([0.85, 0.24])
        with col2: 
            st.button("Próxima pergunta", on_click=proxima_pergunta)
    criar_botao()

    total_perguntas = len(perguntas_respostas[user_materia])
    porcentagem_acertos = (st.session_state.progresso / total_perguntas) * 100 
    progresso_percentual = st.session_state.progresso / total_perguntas
    st.progress(progresso_percentual) # criação da barra de progresso
    st.write(f"Porcentagem de acerto: {porcentagem_acertos:.2f}%<span style='float: right;'>Questão {st.session_state['indice_pergunta']+1} de 7</span>", unsafe_allow_html=True)


