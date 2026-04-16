"""
Análise Exploratória de Dados — Base de Vendas 2024
Portfólio | LinkedIn | Data Analytics

Autor: [Seu Nome]
Dataset: 20.000 registros de vendas, Jan-Dez 2024
"""

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import seaborn as sns
import warnings
warnings.filterwarnings("ignore")

# ── Configuração visual ──────────────────────────────────────────────────────
plt.rcParams.update({
    "figure.facecolor": "white",
    "axes.facecolor": "#f8f8f6",
    "axes.grid": True,
    "grid.color": "#e0e0dc",
    "grid.linewidth": 0.6,
    "font.family": "DejaVu Sans",
    "axes.spines.top": False,
    "axes.spines.right": False,
})
PALETTE_AZUL = ["#3266ad", "#4a8fc0", "#5fa8d3", "#73b8db", "#8dcae3", "#a6d8ea"]

# ── 1. Carregamento e limpeza ─────────────────────────────────────────────────
df = pd.read_csv("data/base_vendas_grande.csv", parse_dates=["data_venda"])
df["mes"]         = df["data_venda"].dt.month
df["mes_nome"]    = df["data_venda"].dt.strftime("%b")
df["trimestre"]   = df["data_venda"].dt.to_period("Q").astype(str)
df["dia_semana"]  = df["data_venda"].dt.day_name()

print("=" * 60)
print("VISÃO GERAL DA BASE")
print("=" * 60)
print(f"Período      : {df['data_venda'].min().date()} → {df['data_venda'].max().date()}")
print(f"Total linhas : {len(df):,.0f}")
print(f"Colunas      : {list(df.columns)}")
print(f"Nulos        : {df.isnull().sum().sum()}")
print(f"Duplicatas   : {df.duplicated().sum()}")
print()
print(df.describe(include="all").T.to_string())

# ── 2. KPIs principais ───────────────────────────────────────────────────────
fat_total    = df["faturamento"].sum()
ticket_medio = df["faturamento"].mean()
qtd_total    = df["quantidade"].sum()
melhor_mes   = df.groupby("mes_nome")["faturamento"].sum().idxmax()

print("\n" + "=" * 60)
print("KPIs PRINCIPAIS")
print("=" * 60)
print(f"Faturamento total : R$ {fat_total:>12,.2f}")
print(f"Ticket médio      : R$ {ticket_medio:>12,.2f}")
print(f"Qtd total vendida : {qtd_total:>14,.0f} unidades")
print(f"Melhor mês        : {melhor_mes}")

# ── 3. Análise por dimensão ───────────────────────────────────────────────────
dims = {
    "vendedor" : "Vendedor",
    "categoria": "Categoria",
    "cidade"   : "Cidade",
    "loja"     : "Loja",
}

for col, label in dims.items():
    print(f"\n── Por {label} ──")
    resumo = (
        df.groupby(col)
        .agg(
            faturamento=("faturamento", "sum"),
            qtd_vendas=("faturamento", "count"),
            ticket_medio=("faturamento", "mean"),
        )
        .sort_values("faturamento", ascending=False)
    )
    resumo["share_%"] = (resumo["faturamento"] / fat_total * 100).round(1)
    print(resumo.to_string())

# ── 4. Série temporal mensal ─────────────────────────────────────────────────
mensal = (
    df.groupby(["mes", "mes_nome"])["faturamento"]
    .sum()
    .reset_index()
    .sort_values("mes")
)

# ── 5. Gráficos ───────────────────────────────────────────────────────────────
fig, axes = plt.subplots(3, 2, figsize=(8, 10))
fig.suptitle("Dashboard de Vendas — 2024", fontsize=18, fontweight="bold", y=0.98)

meses_label = mensal["mes_nome"].tolist()
fat_mensal  = mensal["faturamento"].tolist()
cores_bar   = [PALETTE_AZUL[0] if v == max(fat_mensal) else PALETTE_AZUL[2] for v in fat_mensal]

# 5.1 Faturamento mensal
ax = axes[0, 0]
bars = ax.bar(meses_label, fat_mensal, color=cores_bar, zorder=2, width=0.7)
ax.set_title("Faturamento mensal", fontweight="bold")
ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"R${x/1e3:.0f}k"))
ax.tick_params(axis="x", rotation=30)
for bar, val in zip(bars, fat_mensal):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 3000,
            f"{val/1e3:.0f}k", ha="center", va="bottom", fontsize=7.5)

# 5.2 Crescimento MoM
ax = axes[0, 1]
mom = pd.Series(fat_mensal).pct_change().fillna(0) * 100
cores_mom = [PALETTE_AZUL[0] if v >= 0 else "#c0392b" for v in mom]
ax.bar(meses_label, mom, color=cores_mom, zorder=2, width=0.7)
ax.axhline(0, color="gray", linewidth=0.8, linestyle="--")
ax.set_title("Variação MoM (%)", fontweight="bold")
ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{x:.1f}%"))
ax.tick_params(axis="x", rotation=30)

# 5.3 Faturamento por vendedor
ax = axes[1, 0]
vend = df.groupby("vendedor")["faturamento"].sum().sort_values(ascending=True)
ax.barh(vend.index, vend.values, color=PALETTE_AZUL[:len(vend)], zorder=2)
ax.set_title("Faturamento por vendedor", fontweight="bold")
ax.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"R${x/1e6:.2f}M"))
for i, (idx, val) in enumerate(vend.items()):
    ax.text(val + 3000, i, f"R${val/1e6:.2f}M", va="center", fontsize=8)

# 5.4 Share por categoria (pizza)
ax = axes[1, 1]
cat = df.groupby("categoria")["faturamento"].sum()
wedges, texts, autotexts = ax.pie(
    cat.values, labels=cat.index, autopct="%1.1f%%",
    colors=PALETTE_AZUL[:len(cat)], startangle=90,
    wedgeprops={"edgecolor": "white", "linewidth": 1.5}
)
for at in autotexts:
    at.set_fontsize(9)
ax.set_title("Share por categoria", fontweight="bold")

# 5.5 Boxplot: distribuição de faturamento por loja
ax = axes[2, 0]
lojas_order = df.groupby("loja")["faturamento"].median().sort_values(ascending=False).index
sns.boxplot(
    data=df, x="loja", y="faturamento", order=lojas_order,
    palette=PALETTE_AZUL[:4], ax=ax, flierprops={"markersize": 3}
)
ax.set_title("Distribuição de faturamento por loja", fontweight="bold")
ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"R${x:.0f}"))
ax.tick_params(axis="x", rotation=15)
ax.set_xlabel("")

# 5.6 Heatmap: faturamento por categoria × mês
ax = axes[2, 1]
pivot = df.pivot_table(values="faturamento", index="categoria", columns="mes", aggfunc="sum")
pivot.columns = ["Jan","Fev","Mar","Abr","Mai","Jun","Jul","Ago","Set","Out","Nov","Dez"]
sns.heatmap(
    pivot / 1000, annot=True, fmt=".0f", cmap="Blues",
    linewidths=0.4, ax=ax, cbar_kws={"label": "R$ (mil)"}
)
ax.set_title("Faturamento por categoria × mês (R$ mil)", fontweight="bold")
ax.set_xlabel("")
ax.set_ylabel("")

plt.tight_layout()
plt.savefig("dashboard_vendas_2024.png", dpi=150, bbox_inches="tight")
plt.show()
print("\nGráfico salvo como 'dashboard_vendas_2024.png'")

# ── 6. Top produtos ───────────────────────────────────────────────────────────
print("\n── Top 10 Produtos por Faturamento ──")
top_prod = (
    df.groupby("produto")["faturamento"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
)
for i, (prod, val) in enumerate(top_prod.items(), 1):
    print(f"  {i:>2}. {prod:<20} R$ {val:>10,.2f}")

# ── 7. Análise de correlação ──────────────────────────────────────────────────
print("\n── Correlação: quantidade × faturamento ──")
corr = df[["quantidade", "preco_unitario", "faturamento"]].corr()
print(corr.round(3).to_string())

print("\nAnálise concluída com sucesso!")