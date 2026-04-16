Dashboard de Vendas 2024 — Análise Completa

> Projeto de portfólio desenvolvido para demonstrar habilidades em análise de dados, Python e visualização aplicadas a uma base real de varejo.

---

Objetivo

Transformar 20.000 registros de vendas em insights acionáveis para o negócio, respondendo perguntas como:

- Qual foi o melhor mês e por quê?
- Quais vendedores e categorias geram mais receita?
- Existe sazonalidade no faturamento?
- Quais produtos merecem mais atenção?

---

Estrutura do projeto

``
vendas-dashboard/
│
├── data/
│   └── base_vendas_grande.csv      # Dataset original (20k linhas)
│
├── analise_vendas.py               # EDA completa com Python
├── dashboard_vendas_2024.png       # Dashboard exportado
│
├── notebooks/
│   └── analise_exploratoria.ipynb  # Jupyter Notebook comentado
│
└── README.md
```

Principais descobertas

| Indicador | Valor |
|-----------|-------|
| Faturamento total 2024 | R$ 8.157.579,95 |
| Ticket médio por venda | R$ 407,88 |
| Melhor mês | Julho (R$ 705.659) |
| Pior mês | Fevereiro (R$ 636.581) |
| Categoria líder | Higiene (25,7%) |
| Cidade líder | Curitiba (R$ 2,09M) |
| Top produto | Leite (R$ 858.028) |

### Insights principais

1. Sazonalidade suave — o faturamento é relativamente estável ao longo do ano (~R$ 680k/mês), sem pico sazonal forte. Isso indica oportunidade para campanhas pontuais nos meses mais fracos (Fev, Set, Dez).

2. Vendedores equilibrados — a diferença entre o melhor (Maria, R$ 1,38M) e o pior desempenho (Marcos, R$ 1,32M) é de apenas 4,4%. Sinal de equipe bem gerenciada ou meta pouco desafiadora.

3. Categorias empatadas — Higiene e Bebidas dominam com quase o mesmo share (~25,7% cada). Alimentos e Limpeza têm espaço para crescimento.

4. Curitiba lidera com folga — R$ 104k acima de RJ. Vale investigar o que diferencia a operação nessa praça.

---

#Tecnologias utilizadas

- Python 3.11+
- **Pandas** — limpeza e transformação dos dados
- **Matplotlib & Seaborn** — visualizações estáticas
- **Chart.js** — dashboard interativo
- **Jupyter Notebook** — documentação e narrativa analítica

---

Como executar

```bash
Clone o repositório
git clone https://github.com/seu-usuario/vendas-dashboard.git
cd vendas-dashboard

Instale as dependências
pip install pandas matplotlib seaborn

Execute a análise
python analise_vendas.py
```

---

Visualizações

O script gera um dashboard com 6 gráficos:

1. Faturamento mensal — série temporal com destaque no mês pico
2. Variação MoM*— crescimento mês a mês (positivo/negativo)
3. Ranking de vendedores — barras horizontais ordenadas
4. Share por categoria — gráfico de pizza com percentuais
5. Distribuição por loja — boxplot comparativo
6. Heatmap categoria × mês — onde cada categoria performa melhor

---

Felipe Fiame
- LinkedIn: [linkedin.com/in/seu-perfil](https://www.linkedin.com/in/felipe-fiame-78143a113/)
- GitHub: [github.com/seu-usuario](https://github.com/felipefiamerj)

---
Este projeto foi desenvolvido com fins educacionais e de portfólio. Os dados são fictícios.
