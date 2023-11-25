import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.signal import savgol_filter
import scipy.stats
from matplotlib import colors
from matplotlib.ticker import PercentFormatter

def ler_dataset(path: str, remover_colunas = [], sample = 0) -> pd.DataFrame:
    """Essa função recebe um path do arquivo csv e, opcionalmente, uma lista de colunas a serem removidas e um número amostral. Ela lê o arquivo csv e cria um objeto pd.Dataframe e remove as colunas indesejadas. A função depois faz um tratamento básico dos dados, tirando uma amostra aleatória caso especificado valor para 'sample' e removendo valores faltantes (NAs). Retorna um objeto pd.Dataframe"""
    df = pd.read_csv(path).drop(remover_colunas, axis=1)
    if sample:
        df = df.sample(sample)
    df = df.dropna()
    return df

def coluna_qualitativa_para_quantitativo(coluna: pd.Series) -> pd.Series:
    """Essa função recebe uma variável qualitativa em um objeto pd.Series e a transforma em uma variável quantitativa, na qual cada linha possui o número de entradas de uma categoria"""
    variavel = coluna.unique()
    observacoes = []
    for tipo in variavel:
        observacoes.append(coluna.value_counts()[tipo])
    return pd.Series(data=observacoes, index=variavel)

def filtrar_coluna(coluna: pd.Series, n_categorias = 0, crescente = False) -> pd.Series:
    """Essa função recebe um objeto pd.Series e o ordenada, remove valores pequenos, que podem representar erros no sistema ou categorias muito específicas e, em geral, irrelevantes. Depois disso, a função pega as maiores n_categorias e transforma o resto em uma categoria chamada de 'outros', que agrupa o restante das caregorias"""
    coluna = coluna.sort_values(ascending = crescente)
    coluna = coluna[coluna > coluna.count() // 20]
    outros = 0

    if not n_categorias:
        if len(coluna.index) > 100:
            n_categorias = len(coluna.index) // 50
        elif 100 > len(coluna.index) > 20:
            n_categorias = len(coluna.index) // 10
        else:
            n_categorias = len(coluna.index)

    for num, valor_da_linha in enumerate(coluna):
        if num > n_categorias:
            outros += valor_da_linha

    if outros:
        coluna = coluna[:n_categorias]
        outros_series = pd.Series(data=outros, index=["Outros"])
        coluna = pd.concat([coluna, outros_series])
        
    return coluna
    
def grafico_barras(coluna: pd.Series, titulo = "Número de bolsistas"):
    """Essa função recebe um objeto pd.Series e, opcionalmente, um título. Pega os atributos únicos da variável, bem como seus respectivos valores e os usa para fazer um gráfico de barras. Retorna um fig, ax para serem plotados"""
    fig, ax = plt.subplots()

    variavel = coluna.unique()
    observacoes = []
    for tipo in variavel:
        observacoes.append(coluna.value_counts()[tipo])

    xmin = coluna.min()
    xmax = coluna.max()
    xticks = [i for i in range(xmin,xmax + 1)]
    plt.xlim(xmin,xmax)
    plt.xticks(xticks)

    ax.bar(variavel, observacoes)

    if xmax - xmin > 3:
        polinomio = 3
    else:
        polinomio = 2

    ax.plot(variavel, savgol_filter(observacoes, xmax - xmin + 1, polinomio), c = "red")
    ax.set_ylabel('número de bolsistas')
    ax.set_title(titulo)

    return fig, ax

def grafico_barras_proporcao(coluna: pd.Series, titulo = "Número de bolsistas"):
    """Essa função recebe um objeto pd.Series e, opcionalmente, um título. Pega os atributos únicos da variável, bem como seus respectivos valores e os usa para fazer um gráfico de barras com as proporções de cada entrada. Retorna um fig, ax para serem plotados"""
    fig, ax = plt.subplots()

    variavel = coluna.unique()
    total = coluna.count()
    observacoes = []
    for tipo in variavel:
        observacoes.append(coluna.value_counts()[tipo] / total)

    ax.bar(variavel, observacoes)
    
    ax.set_ylabel('número de bolsistas')
    ax.set_title(titulo)

    return fig, ax

def grafico_setores(coluna: pd.Series, titulo = "Proporção de bolsistas"):
    """Essa função recebe um objeto pd.Series e, opcionalmente, um título. Pega os atributos únicos da variável, bem como seus respectivos valores e os usa para fazer um gráfico de setores (pizza) com as proporções de cada entrada. Retorna um fig, ax para serem plotados"""
    fig, ax = plt.subplots()

    ax.pie(coluna, labels = coluna.index, autopct='%1.1f%%')
    
    ax.set_title(titulo)

    return fig, ax

def histograma(coluna: pd.Series, bins = 10, titulo = "bolsistas"):
    """Essa função recebe um objeto pd.Series e, opcionalmente, um título. Pega os valores da variável e os divide em intervalos. Depois plota o histograma, além de estatísticas descritivas da variável em questão"""
    # Referência: https://matplotlib.org/stable/gallery/statistics/hist.html#sphx-glr-gallery-statistics-hist-py
    fig, axs = plt.subplots(1, 2, tight_layout=True)
    
    # Mudar os limites do hhistograma para melhor visualização
    axs[0].set_xlim(19,60)
    axs[0].set_xticks([19, 22, 25, 30, 35, 40, 45, 50, 55, 60])
    axs[1].set_xlim(19,60)
    axs[1].set_xticks([19, 22, 25, 30, 35, 40, 45, 50, 55, 60])
    # Tirar a margem horizontal
    axs[0].margins(x=0)
    axs[1].margins(x=0)

    #Histograma 1
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

    # Histograma 2
    axs[1].hist(coluna, bins=bins,density=True, ec="black")
    # Now we format the y-axis to display percentage
    axs[1].yaxis.set_major_formatter(PercentFormatter(xmax=1))

    # Aproximar o histograma a uma distribuição (referência: https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.rv_histogram.html#scipy.stats.rv_histogram)
    hist = np.histogram(coluna, bins=int(coluna.max() - coluna.min()))
    hist_dist = scipy.stats.rv_histogram(hist, density=False)
    X = np.linspace(19, 60, 1000)
    yhat = savgol_filter(hist_dist.pdf(X), 500,3)
    axs[1].plot(X, yhat, label='PDF')

    # Colocar o título
    axs[0].set_title('' + titulo)
    axs[1].set_title('Densidade de ' + titulo)
    axs[0].set_xlabel("Idade")
    axs[1].set_xlabel("Idade")
    # Adicionar estatísticas descritivas (referência: https://stackoverflow.com/questions/34243737/how-to-add-some-statistics-to-the-plot-in-python)
    estatisticas = coluna.describe()
    media = "Média: " + str(round(estatisticas[1],1)) + " anos\n"  
    desvio_padrao = "Desvio-padrão: " + str(round(estatisticas[2],1)) + " anos\n" 
    total_alunos = "N. Alunos: " + str(int(estatisticas[0]))
    s = media + desvio_padrao + total_alunos
    plt.figtext(1.0, 0.2, s) 
    
    return fig, axs