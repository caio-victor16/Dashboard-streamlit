#Dados linhas, Gráfico de linhas: evolução diária das vendas por loja
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

BASE = Path(__file__).resolve().parent.parent
OUT = BASE / "output"
OUT.mkdir(exist_ok=True)
import matplotlib.dates as mdates

df = pd.read_csv(BASE / "data" / "dados_linhas.csv", parse_dates=["data"])
df = df.sort_values("data")

fig, ax = plt.subplots(figsize=(11, 6))
for loja, grupo in df.groupby("loja"):
    ax.plot(grupo["data"], grupo["vendas"], marker="o", markersize=3, label=loja)
ax.set_title("Evolução das vendas por loja", fontsize=14, fontweight="bold")
ax.set_xlabel("Data")
ax.set_ylabel("Vendas")
ax.xaxis.set_major_formatter(mdates.DateFormatter("%d/%m"))
ax.legend(title="Loja")
ax.grid(linestyle="--", alpha=0.5)
fig.autofmt_xdate()
plt.tight_layout()
plt.savefig(OUT / "07_linhas.png", dpi=150)
print("Salvo em", OUT / "07_linhas.png")
