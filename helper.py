import pandas as pd
import matplotlib.pyplot as plt

from matplotlib import colors
from matplotlib.ticker import PercentFormatter

def grafico_barras(coluna: pd.Series, titulo = "Número de bolsistas"):
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

def grafico_setores_proporcao(coluna: pd.Series, titulo = "Número de bolsistas"):
    """Essa função recebe um objeto pd.Series e, opcionalmente, um título. Pega os atributos únicos da variável, bem como seus respectivos valores e os usa para fazer um gráfico de barras com as proporções de cada entrada. Retorna um fig, ax para serem plotados"""
    fig, ax = plt.subplots()

    variavel = coluna.unique()
    total = coluna.count()
    observacoes = []
    for num, tipo in enumerate(variavel):
        observacoes.append(coluna.value_counts()[tipo] / total)

    ax.pie(observacoes, labels = variavel, autopct='%1.1f%%')
    
    ax.set_ylabel('número de bolsistas')
    ax.set_title(titulo)

    return fig, ax

def histograma(coluna: pd.Series, bins = 10, titulo = "bolsistas"):
    """Essa função recebe um objeto pd.Series e, opcionalmente, um título. Pega os valores da variável e os divide em intervalos. Depois plota o histograma"""
    # Referência: https://matplotlib.org/stable/gallery/statistics/hist.html#sphx-glr-gallery-statistics-hist-py

    fig, axs = plt.subplots(1, 2, tight_layout=True)

    # N is the count in each bin, bins is the lower-limit of the bin
    N, bins, patches = axs[0].hist(coluna, bins=bins)

    # We'll color code by height, but you could use any scalar
    fracs = N / N.max()

    # we need to normalize the data to 0..1 for the full range of the colormap
    norm = colors.Normalize(fracs.min(), fracs.max())

    # Now, we'll loop through our objects and set the color of each accordingly
    for thisfrac, thispatch in zip(fracs, patches):
        color = plt.cm.viridis(norm(thisfrac))
        thispatch.set_facecolor(color)

    # We can also normalize our inputs by the total number of counts
    axs[1].hist(coluna, bins=bins, density=True)

    # Now we format the y-axis to display percentage
    axs[1].yaxis.set_major_formatter(PercentFormatter(xmax=1))

    # Colocar o título
    axs[0].set_title('Número de ' + titulo)
    axs[1].set_title('Densidade de ' + titulo)

    return fig, axs