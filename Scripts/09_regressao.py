#Data Regressão, Regressão linear: gasto mensal em função da renda mensal
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

BASE = Path(__file__).resolve().parent.parent
OUT = BASE / "output"
OUT.mkdir(exist_ok=True)
import numpy as np

df = pd.read_csv(BASE / "data" / "dados_regressao.csv")
x, y = df["renda_mensal"].to_numpy(), df["gasto_mensal"].to_numpy()
a, b = np.polyfit(x, y, 1)
r2 = np.corrcoef(x, y)[0, 1] ** 2
xs = np.linspace(x.min(), x.max(), 100)

fig, ax = plt.subplots(figsize=(10, 6))
ax.scatter(x, y, alpha=0.7, edgecolor="black", label="Observações")
ax.plot(xs, a * xs + b, color="red", linewidth=2,
        label=f"y = {a:.3f}x + {b:.1f}  (R² = {r2:.3f})")
ax.set_title("Regressão linear: renda x gasto mensal", fontsize=14, fontweight="bold")
ax.set_xlabel("Renda mensal (R$)")
ax.set_ylabel("Gasto mensal (R$)")
ax.legend()
ax.grid(linestyle="--", alpha=0.5)
plt.tight_layout()
plt.savefig(OUT / "09_regressao.png", dpi=150)
print("Salvo em", OUT / "09_regressao.png")
