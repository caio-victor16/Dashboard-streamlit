#Dados barra, Gráfico de barras agrupadas: vendas médias por categoria e região
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

BASE = Path(__file__).resolve().parent.parent
OUT = BASE / "output"
OUT.mkdir(exist_ok=True)

df = pd.read_csv(BASE / "data" / "dados_barras.csv")
tabela = df.pivot(index="categoria", columns="regiao", values="vendas_medias")

ax = tabela.plot(kind="bar", figsize=(10, 6), width=0.8, edgecolor="black")
ax.set_title("Vendas médias por categoria e região", fontsize=14, fontweight="bold")
ax.set_xlabel("Categoria")
ax.set_ylabel("Vendas médias")
ax.legend(title="Região")
ax.grid(axis="y", linestyle="--", alpha=0.5)
plt.xticks(rotation=0)
plt.tight_layout()
plt.savefig(OUT / "01_barras.png", dpi=150)
print("Salvo em", OUT / "01_barras.png")
