#Dados frequencia, Gráfico de frequência: quantidade de chamados por tipo de atendimento.
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

BASE = Path(__file__).resolve().parent.parent
OUT = BASE / "output"
OUT.mkdir(exist_ok=True)

df = pd.read_csv(BASE / "data" / "dados_frequencia.csv")
freq = df["tipo_atendimento"].value_counts()

fig, ax = plt.subplots(figsize=(10, 6))
barras = ax.bar(freq.index, freq.values, color="#fd8d3c", edgecolor="black")
ax.bar_label(barras, padding=3)
ax.set_title("Frequência de chamados por tipo de atendimento", fontsize=14, fontweight="bold")
ax.set_xlabel("Tipo de atendimento")
ax.set_ylabel("Quantidade de chamados")
ax.grid(axis="y", linestyle="--", alpha=0.5)
plt.tight_layout()
plt.savefig(OUT / "05_frequencia.png", dpi=150)
print("Salvo em", OUT / "05_frequencia.png")
