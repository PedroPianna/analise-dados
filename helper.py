import pandas as pd
import matplotlib.pyplot as plt

def grafico_barras_quantidade(coluna: pd.Series, titulo = "Número de bolsistas"):
    """Essa função recebe um objeto pd.Series e uma legenda. Retorna elementos para plotar um gráfico de barras"""
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