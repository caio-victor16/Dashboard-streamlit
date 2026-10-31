#Dados HeatMap, Mapa de calor: movimento de clientes por dia da semana e horário
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

BASE = Path(__file__).resolve().parent.parent
OUT = BASE / "output"
OUT.mkdir(exist_ok=True)

df = pd.read_csv(BASE / "data" / "dados_heatmap.csv")
ordem_dias = ["Segunda", "Terça", "Quarta", "Quinta", "Sexta", "Sábado", "Domingo"]
tabela = df.pivot(index="dia_semana", columns="horario", values="movimento_clientes")
tabela = tabela.reindex([d for d in ordem_dias if d in tabela.index])

fig, ax = plt.subplots(figsize=(10, 6))
im = ax.imshow(tabela.values, cmap="YlOrRd", aspect="auto")
ax.set_xticks(range(len(tabela.columns)), labels=tabela.columns)
ax.set_yticks(range(len(tabela.index)), labels=tabela.index)
limite = tabela.values.max() * 0.65
for i in range(tabela.shape[0]):
    for j in range(tabela.shape[1]):
        valor = tabela.values[i, j]
        ax.text(j, i, int(valor), ha="center", va="center", fontsize=9,
                color="white" if valor > limite else "black")
fig.colorbar(im, ax=ax, label="Movimento de clientes")
ax.set_title("Movimento de clientes por dia e horário", fontsize=14, fontweight="bold")
ax.set_xlabel("Horário")
ax.set_ylabel("Dia da semana")
plt.tight_layout()
plt.savefig(OUT / "06_heatmap.png", dpi=150)
print("Salvo em", OUT / "06_heatmap.png")
