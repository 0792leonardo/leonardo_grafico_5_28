# Gráfico 5.28 — NO₂

Gráfico interativo em Python + Plotly baseado no arquivo `Dd_grafico_5_28.csv`.

## Dados

Campo das estações: `estacao`.

As colunas numéricas com nomes de anos são utilizadas automaticamente. O período atualmente presente no CSV é utilizado sem necessidade de alterar o código.

## Configuração visual

- Eixo Y: 0–80 µg/m³.
- Intervalos de 20 µg/m³.
- Uma série por estação.
- Marcadores diferenciados.
- Fundo `#DDE9F4`.
- Grade horizontal pontilhada.
- Legenda horizontal.
- Tooltip interativo.
- Zoom.
- Valores ausentes permanecem como lacunas.
- HTML autocontido.

## Gerar

```bash
pip install pandas plotly
python gerar_grafico.py
```

## Publicar no GitHub Pages

```bash
git init
git add .
git commit -m "Adicionar grafico 5.28 NO2"
git branch -M main
git remote add origin https://github.com/SEU_USUARIO/SEU_REPOSITORIO.git
git push -u origin main
```

No GitHub:

**Settings → Pages → Build and deployment → Source → GitHub Actions**
