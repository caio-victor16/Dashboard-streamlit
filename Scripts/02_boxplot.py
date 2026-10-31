#Dados boxplot, Boxplot: distribuição salarial por departamento
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

BASE = Path(__file__).resolve().parent.parent
OUT = BASE / "output"
OUT.mkdir(exist_ok=True)

df = pd.read_csv(BASE / "data" / "dados_boxplot.csv")
deptos = sorted(df["departamento"].unique())
dados = [df.loc[df["departamento"] == d, "salario"] for d in deptos]

fig, ax = plt.subplots(figsize=(10, 6))
ax.boxplot(dados, tick_labels=deptos, patch_artist=True, showmeans=True,
           boxprops=dict(facecolor="#9ecae1"), medianprops=dict(color="red"))
ax.set_title("Distribuição de salários por departamento", fontsize=14, fontweight="bold")
ax.set_xlabel("Departamento")
ax.set_ylabel("Salário (R$)")
ax.grid(axis="y", linestyle="--", alpha=0.5)
plt.tight_layout()
plt.savefig(OUT / "02_boxplot.png", dpi=150)
print("Salvo em", OUT / "02_boxplot.png")
