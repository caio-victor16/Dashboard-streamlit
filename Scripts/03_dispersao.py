#Dados dispersão, Gráfico de dispersão: altura x peso, colorido por sexo
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

BASE = Path(__file__).resolve().parent.parent
OUT = BASE / "output"
OUT.mkdir(exist_ok=True)

df = pd.read_csv(BASE / "data" / "dados_dispersao.csv")

fig, ax = plt.subplots(figsize=(10, 6))
for sexo, grupo in df.groupby("sexo"):
    ax.scatter(grupo["altura_cm"], grupo["peso_kg"], label=sexo, alpha=0.7, edgecolor="black")
ax.set_title("Relação entre altura e peso", fontsize=14, fontweight="bold")
ax.set_xlabel("Altura (cm)")
ax.set_ylabel("Peso (kg)")
ax.legend(title="Sexo")
ax.grid(linestyle="--", alpha=0.5)
plt.tight_layout()
plt.savefig(OUT / "03_dispersao.png", dpi=150)
print("Salvo em", OUT / "03_dispersao.png")
