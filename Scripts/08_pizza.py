#Dados Pizza, Gráfico de pizza: participação de cada canal no faturamento.
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

BASE = Path(__file__).resolve().parent.parent
OUT = BASE / "output"
OUT.mkdir(exist_ok=True)

df = pd.read_csv(BASE / "data" / "dados_pizza.csv")

fig, ax = plt.subplots(figsize=(8, 8))
ax.pie(df["faturamento"], labels=df["canal_venda"], autopct="%1.1f%%", startangle=90,
       wedgeprops=dict(edgecolor="white"), textprops=dict(fontsize=11))
ax.set_title("Faturamento por canal de venda", fontsize=14, fontweight="bold")
plt.tight_layout()
plt.savefig(OUT / "08_pizza.png", dpi=150)
print("Salvo em", OUT / "08_pizza.png")
