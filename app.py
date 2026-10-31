"""
Dashboard Streamlit - Gráficos com Pandas e Matplotlib
Coloque este arquivo na raiz do projeto (mesma pasta de /data e /scripts)
e execute:  streamlit run app.py
"""
from pathlib import Path

import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import streamlit as st

# ----------------------------------------------------------------------------
# CONFIGURAÇÃO
# ----------------------------------------------------------------------------
BASE = Path(__file__).resolve().parent
DATA = BASE / "data"

st.set_page_config(
    page_title="Dashboard de Gráficos",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",  # o usuário pode recolher pela seta
)

# ----------------------------------------------------------------------------
# SIDEBAR (recolhível) - INFORMAÇÕES DO ALUNO
# ----------------------------------------------------------------------------
with st.sidebar:
    st.markdown("**Nome:** João Gabriel Costa Galbas")      # <- altere aqui
    st.markdown("**Nº da chamada:** 17")            # <- altere aqui
    st.markdown("**Turma:** 3D2")                   # <- altere aqui
    st.divider()
    st.caption("Atividade 06 · Gráficos com Pandas e Matplotlib")
    st.caption("Use a seta no topo da barra lateral para recolhê-la.")


# ----------------------------------------------------------------------------
# CARREGAMENTO DOS DADOS
# ----------------------------------------------------------------------------
@st.cache_data
def carregar(nome: str, **kwargs) -> pd.DataFrame:
    return pd.read_csv(DATA / nome, **kwargs)


def brl(valor: float) -> str:
    """Formata número no padrão brasileiro (1.234,56)."""
    return f"{valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


FIGSIZE = (6, 4.2)

# ----------------------------------------------------------------------------
# GRÁFICOS (cada função devolve uma figura)
# ----------------------------------------------------------------------------
def fig_barras():
    df = carregar("dados_barras.csv")
    tabela = df.pivot(index="categoria", columns="regiao", values="vendas_medias")
    fig, ax = plt.subplots(figsize=FIGSIZE)
    tabela.plot(kind="bar", ax=ax, width=0.8, edgecolor="black")
    ax.set_title("Vendas médias por categoria e região", fontsize=12, fontweight="bold")
    ax.set_xlabel("Categoria")
    ax.set_ylabel("Vendas médias")
    ax.legend(title="Região", fontsize=8)
    ax.grid(axis="y", linestyle="--", alpha=0.5)
    plt.setp(ax.get_xticklabels(), rotation=0, fontsize=8)
    fig.tight_layout()
    return fig


def fig_boxplot():
    df = carregar("dados_boxplot.csv")
    deptos = sorted(df["departamento"].unique())
    dados = [df.loc[df["departamento"] == d, "salario"] for d in deptos]
    fig, ax = plt.subplots(figsize=FIGSIZE)
    ax.boxplot(dados, tick_labels=deptos, patch_artist=True, showmeans=True,
               boxprops=dict(facecolor="#9ecae1"), medianprops=dict(color="red"))
    ax.set_title("Distribuição de salários por departamento", fontsize=12, fontweight="bold")
    ax.set_xlabel("Departamento")
    ax.set_ylabel("Salário (R$)")
    ax.grid(axis="y", linestyle="--", alpha=0.5)
    fig.tight_layout()
    return fig


def fig_dispersao():
    df = carregar("dados_dispersao.csv")
    fig, ax = plt.subplots(figsize=FIGSIZE)
    for sexo, grupo in df.groupby("sexo"):
        ax.scatter(grupo["altura_cm"], grupo["peso_kg"], label=sexo,
                   alpha=0.7, edgecolor="black", s=25)
    ax.set_title("Relação entre altura e peso", fontsize=12, fontweight="bold")
    ax.set_xlabel("Altura (cm)")
    ax.set_ylabel("Peso (kg)")
    ax.legend(title="Sexo", fontsize=8)
    ax.grid(linestyle="--", alpha=0.5)
    fig.tight_layout()
    return fig


def fig_distribuicao():
    df = carregar("dados_distribuicao.csv")
    fig, ax = plt.subplots(figsize=FIGSIZE)
    ax.hist(df["idade"], bins=15, color="#74c476", edgecolor="black", alpha=0.85)
    media = df["idade"].mean()
    ax.axvline(media, color="red", linestyle="--", label=f"Média: {media:.1f} anos")
    ax.set_title("Distribuição da idade dos clientes", fontsize=12, fontweight="bold")
    ax.set_xlabel("Idade (anos)")
    ax.set_ylabel("Número de clientes")
    ax.legend(fontsize=8)
    ax.grid(axis="y", linestyle="--", alpha=0.5)
    fig.tight_layout()
    return fig


def fig_frequencia():
    df = carregar("dados_frequencia.csv")
    freq = df["tipo_atendimento"].value_counts()
    fig, ax = plt.subplots(figsize=FIGSIZE)
    barras = ax.bar(freq.index, freq.values, color="#fd8d3c", edgecolor="black")
    ax.bar_label(barras, padding=3)
    ax.set_title("Frequência de chamados por tipo", fontsize=12, fontweight="bold")
    ax.set_xlabel("Tipo de atendimento")
    ax.set_ylabel("Quantidade de chamados")
    ax.grid(axis="y", linestyle="--", alpha=0.5)
    plt.setp(ax.get_xticklabels(), fontsize=8)
    fig.tight_layout()
    return fig


def _tabela_heatmap():
    df = carregar("dados_heatmap.csv")
    ordem = ["Segunda", "Terça", "Quarta", "Quinta", "Sexta", "Sábado", "Domingo"]
    tabela = df.pivot(index="dia_semana", columns="horario", values="movimento_clientes")
    return tabela.reindex([d for d in ordem if d in tabela.index])


def fig_heatmap():
    tabela = _tabela_heatmap()
    fig, ax = plt.subplots(figsize=FIGSIZE)
    im = ax.imshow(tabela.values, cmap="YlOrRd", aspect="auto")
    ax.set_xticks(range(len(tabela.columns)), labels=tabela.columns, fontsize=8)
    ax.set_yticks(range(len(tabela.index)), labels=tabela.index, fontsize=8)
    limite = tabela.values.max() * 0.65
    for i in range(tabela.shape[0]):
        for j in range(tabela.shape[1]):
            v = tabela.values[i, j]
            ax.text(j, i, int(v), ha="center", va="center", fontsize=7,
                    color="white" if v > limite else "black")
    fig.colorbar(im, ax=ax, label="Movimento de clientes")
    ax.set_title("Movimento de clientes por dia e horário", fontsize=12, fontweight="bold")
    ax.set_xlabel("Horário")
    ax.set_ylabel("Dia da semana")
    fig.tight_layout()
    return fig


def fig_linhas():
    df = carregar("dados_linhas.csv", parse_dates=["data"]).sort_values("data")
    fig, ax = plt.subplots(figsize=FIGSIZE)
    for loja, grupo in df.groupby("loja"):
        ax.plot(grupo["data"], grupo["vendas"], marker="o", markersize=3, label=loja)
    ax.set_title("Evolução das vendas por loja", fontsize=12, fontweight="bold")
    ax.set_xlabel("Data")
    ax.set_ylabel("Vendas")
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%d/%m"))
    ax.legend(title="Loja", fontsize=8)
    ax.grid(linestyle="--", alpha=0.5)
    fig.autofmt_xdate()
    fig.tight_layout()
    return fig


def fig_pizza():
    df = carregar("dados_pizza.csv")
    fig, ax = plt.subplots(figsize=FIGSIZE)
    ax.pie(df["faturamento"], labels=df["canal_venda"], autopct="%1.1f%%",
           startangle=90, wedgeprops=dict(edgecolor="white"), textprops=dict(fontsize=9))
    ax.set_title("Faturamento por canal de venda", fontsize=12, fontweight="bold")
    fig.tight_layout()
    return fig


def fig_regressao():
    df = carregar("dados_regressao.csv")
    x, y = df["renda_mensal"].to_numpy(), df["gasto_mensal"].to_numpy()
    a, b = np.polyfit(x, y, 1)
    r2 = np.corrcoef(x, y)[0, 1] ** 2
    xs = np.linspace(x.min(), x.max(), 100)
    fig, ax = plt.subplots(figsize=FIGSIZE)
    ax.scatter(x, y, alpha=0.7, edgecolor="black", s=25, label="Observações")
    ax.plot(xs, a * xs + b, color="red", linewidth=2,
            label=f"y = {a:.3f}x + {b:.1f}  (R² = {r2:.3f})")
    ax.set_title("Regressão linear: renda x gasto", fontsize=12, fontweight="bold")
    ax.set_xlabel("Renda mensal (R$)")
    ax.set_ylabel("Gasto mensal (R$)")
    ax.legend(fontsize=8)
    ax.grid(linestyle="--", alpha=0.5)
    fig.tight_layout()
    return fig


# ----------------------------------------------------------------------------
# ANÁLISES (calculadas a partir dos dados)
# ----------------------------------------------------------------------------
def analise_barras():
    df = carregar("dados_barras.csv")
    top = df.loc[df["vendas_medias"].idxmax()]
    low = df.loc[df["vendas_medias"].idxmin()]
    por_cat = df.groupby("categoria")["vendas_medias"].mean().sort_values(ascending=False)
    por_reg = df.groupby("regiao")["vendas_medias"].mean().sort_values(ascending=False)
    return (
        f"A maior venda média é de **{top['categoria']}** na região **{top['regiao']}** "
        f"(R$ {brl(top['vendas_medias'])}), e a menor é de **{low['categoria']}** na região "
        f"**{low['regiao']}** (R$ {brl(low['vendas_medias'])}). Em média, a categoria líder é "
        f"**{por_cat.index[0]}** e a região com melhor desempenho é **{por_reg.index[0]}**. "
        f"Nenhuma categoria domina todas as regiões, o que indica perfis de consumo regionais."
    )


def analise_boxplot():
    df = carregar("dados_boxplot.csv")
    med = df.groupby("departamento")["salario"].median().sort_values(ascending=False)

    def n_out(s):
        q1, q3 = s.quantile([0.25, 0.75])
        return int(((s < q1 - 1.5 * (q3 - q1)) | (s > q3 + 1.5 * (q3 - q1))).sum())

    out = df.groupby("departamento")["salario"].apply(n_out)
    return (
        f"**{med.index[0]}** tem a maior mediana salarial (R$ {brl(med.iloc[0])}) e "
        f"**{med.index[-1]}** a menor (R$ {brl(med.iloc[-1])}). Todos os departamentos "
        f"apresentam *outliers* (total de {int(out.sum())} pontos), que puxam a média acima "
        f"da mediana (marcador verde acima da linha vermelha). Vendas e TI também têm maior "
        f"dispersão que Marketing e RH."
    )


def analise_dispersao():
    df = carregar("dados_dispersao.csv")
    r = df["altura_cm"].corr(df["peso_kg"])
    return (
        f"Há uma **correlação positiva forte** entre altura e peso (r = {r:.2f}): pessoas mais "
        f"altas tendem a ser mais pesadas. A altura varia de {df['altura_cm'].min():.0f} a "
        f"{df['altura_cm'].max():.0f} cm e o peso de {df['peso_kg'].min():.0f} a "
        f"{df['peso_kg'].max():.0f} kg. Os grupos por sexo se sobrepõem bastante, ou seja, "
        f"a separação por sexo não explica a relação."
    )


def analise_distribuicao():
    s = carregar("dados_distribuicao.csv")["idade"]
    jovens = (s < 38).mean() * 100
    return (
        f"A idade média é de **{s.mean():.1f} anos** (mediana {s.median():.0f}), com clientes "
        f"entre {s.min()} e {s.max()} anos. O histograma mostra **dois grupos**: um grande "
        f"concentrado entre 18 e 37 anos (≈ {jovens:.0f}% dos clientes) e outro menor entre 40 "
        f"e 55 anos, além de poucos casos acima disso. A média, portanto, fica entre os dois "
        f"grupos e não descreve bem nenhum deles."
    )


def analise_frequencia():
    freq = carregar("dados_frequencia.csv")["tipo_atendimento"].value_counts()
    total = freq.sum()
    return (
        f"Foram registrados **{total} chamados**. O tipo mais comum é **{freq.index[0]}** "
        f"({freq.iloc[0]} chamados, {freq.iloc[0] / total * 100:.0f}%), seguido de "
        f"**{freq.index[1]}** ({freq.iloc[1]}). O menos frequente é **{freq.index[-1]}** "
        f"({freq.iloc[-1]}). Somadas, reclamações, bugs e cancelamentos superam os elogios, "
        f"sinalizando espaço para melhorar o produto e o atendimento."
    )


def analise_heatmap():
    t = _tabela_heatmap()
    dia, hora = t.stack().idxmax()
    fim = t.loc[[d for d in ["Sábado", "Domingo"] if d in t.index]].values.mean()
    semana = t.drop(index=[d for d in ["Sábado", "Domingo"] if d in t.index]).values.mean()
    return (
        f"O pico de movimento ocorre no(a) **{dia} às {hora}** ({int(t.loc[dia, hora])} "
        f"clientes). Os fins de semana têm média de {fim:.0f} clientes por horário contra "
        f"{semana:.0f} nos dias úteis, ou seja, bem mais movimento. Durante a semana, os "
        f"valores são irregulares, sem um horário fixo de pico."
    )


def analise_linhas():
    df = carregar("dados_linhas.csv", parse_dates=["data"])
    mensal = df.groupby(df["data"].dt.month)["vendas"].mean()
    cresc = (mensal.iloc[-1] / mensal.iloc[0] - 1) * 100
    loja = df.groupby("loja")["vendas"].mean().sort_values(ascending=False)
    return (
        f"As vendas têm **tendência clara de crescimento** no trimestre: a média diária passou "
        f"de R$ {brl(mensal.iloc[0])} em janeiro para R$ {brl(mensal.iloc[-1])} em março "
        f"(≈ +{cresc:.0f}%). As duas lojas seguem a mesma trajetória: a média da "
        f"**{loja.index[0]}** é R$ {brl(loja.iloc[0])} e a da **{loja.index[1]}** é "
        f"R$ {brl(loja.iloc[1])}, uma diferença pequena."
    )


def analise_pizza():
    df = carregar("dados_pizza.csv").sort_values("faturamento", ascending=False)
    total = df["faturamento"].sum()
    p = df["faturamento"] / total * 100
    return (
        f"O faturamento total é de R$ {brl(total)}. O canal **{df.iloc[0]['canal_venda']}** "
        f"lidera com {p.iloc[0]:.1f}%, seguido de **{df.iloc[1]['canal_venda']}** "
        f"({p.iloc[1]:.1f}%). Juntos, os dois primeiros representam {p.iloc[:2].sum():.0f}% "
        f"da receita, enquanto **{df.iloc[-1]['canal_venda']}** responde por apenas "
        f"{p.iloc[-1]:.1f}%."
    )


def analise_regressao():
    df = carregar("dados_regressao.csv")
    a, b = np.polyfit(df["renda_mensal"], df["gasto_mensal"], 1)
    r2 = df["renda_mensal"].corr(df["gasto_mensal"]) ** 2
    return (
        f"A reta ajustada indica que a cada R$ 1,00 de renda o gasto aumenta cerca de "
        f"**R$ {a:.2f}** (≈ {a * 100:.0f}% da renda adicional). Com **R² = {r2:.3f}**, a renda "
        f"explica aproximadamente {r2 * 100:.0f}% da variação dos gastos, uma relação linear "
        f"muito forte."
    )


# ----------------------------------------------------------------------------
# PÁGINA PRINCIPAL
# ----------------------------------------------------------------------------
GRAFICOS = [
    ("1 · Barras agrupadas", fig_barras, analise_barras),
    ("2 · Boxplot", fig_boxplot, analise_boxplot),
    ("3 · Dispersão", fig_dispersao, analise_dispersao),
    ("4 · Distribuição", fig_distribuicao, analise_distribuicao),
    ("5 · Frequência", fig_frequencia, analise_frequencia),
    ("6 · Mapa de calor", fig_heatmap, analise_heatmap),
    ("7 · Linhas", fig_linhas, analise_linhas),
    ("8 · Pizza", fig_pizza, analise_pizza),
    ("9 · Regressão linear", fig_regressao, analise_regressao),
]

st.title("📊 Dashboard de Visualização de Dados")
st.caption("Gráficos produzidos com Pandas e Matplotlib, exibidos três a três com uma breve análise abaixo de cada um.")

for inicio in range(0, len(GRAFICOS), 3):
    colunas = st.columns(3, gap="large")
    for col, (titulo, func_fig, func_analise) in zip(colunas, GRAFICOS[inicio:inicio + 3]):
        with col:
            st.subheader(titulo)
            try:
                fig = func_fig()
                st.pyplot(fig, use_container_width=True)
                plt.close(fig)
                st.markdown("**Análise:** " + func_analise())
            except FileNotFoundError as e:
                st.error(f"Arquivo de dados não encontrado: {e.filename}")
    st.divider()