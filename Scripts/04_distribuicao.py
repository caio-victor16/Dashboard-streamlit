#Dados distribuicao, Histograma: distribuição da idade dos clientes
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

BASE = Path(__file__).resolve().parent.parent
OUT = BASE / "output"
OUT.mkdir(exist_ok=True)

df = pd.read_csv(BASE / "data" / "dados_distribuicao.csv")

fig, ax = plt.subplots(figsize=(10, 6))
ax.hist(df["idade"], bins=15, color="#74c476", edgecolor="black", alpha=0.85)
media = df["idade"].mean()
ax.axvline(media, color="red", linestyle="--", label=f"Média: {media:.1f} anos")
ax.set_title("Distribuição da idade dos clientes", fontsize=14, fontweight="bold")
ax.set_xlabel("Idade (anos)")
ax.set_ylabel("Número de clientes")
ax.legend()
ax.grid(axis="y", linestyle="--", alpha=0.5)
plt.tight_layout()
plt.savefig(OUT / "04_distribuicao.png", dpi=150)
print("Salvo em", OUT / "04_distribuicao.png")
