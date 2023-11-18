import pandas as pd
import matplotlib.pyplot as plt

def grafico_barras_quantidade(coluna: pd.Series, titulo = "Número de bolsistas"):
    """Essa função recebe um objeto pd.Series e, opcionalmente, um título. Pega os atributos únicos da variável, bem como seus respectivos valores e os usa para fazer um gráfico de barras. Retorna um fig, ax para serem plotados"""
    fig, ax = plt.subplots()

    variavel = coluna.unique()
    observacoes = []
    for num, tipo in enumerate(variavel):
        observacoes.append(coluna.value_counts()[tipo])
        
    bar_colors = ['tab:red', 'tab:green']
    ax.bar(variavel, observacoes, color=bar_colors)
    
    ax.set_ylabel('número de bolsistas')
    ax.set_title(titulo)

    return fig, ax

def grafico_barras_proporcao(coluna: pd.Series, titulo = "Número de bolsistas"):
    """Essa função recebe um objeto pd.Series e, opcionalmente, um título. Pega os atributos únicos da variável, bem como seus respectivos valores e os usa para fazer um gráfico de barras com as proporções de cada entrada. Retorna um fig, ax para serem plotados"""
    fig, ax = plt.subplots()

    variavel = coluna.unique()
    total = coluna.count()
    observacoes = []
    for num, tipo in enumerate(variavel):
        observacoes.append(coluna.value_counts()[tipo] / total)

    bar_colors = ['tab:red', 'tab:green']
    ax.bar(variavel, observacoes, color=bar_colors)
    
    ax.set_ylabel('número de bolsistas')
    ax.set_title(titulo)

    return fig, ax