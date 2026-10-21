#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""

Gráfico 5.28 – NO2 – Evolução das concentrações médias anuais – RMSP – Demais escalas
================================================================================

Este script gera um gráfico interativo em HTML mostrando a evolução temporal
das concentrações médias anuais de NO₂ (dióxido de nitrogênio) para diferentes
estações de monitoramento.

O gráfico exibe:
- Séries temporais para cada estação
- Cores e símbolos automáticos para cada localidade
- Dados carregados de um arquivo CSV
- Layout otimizado para visualização e análise

NO₂ = Dióxido de nitrogênio - poluente primário emitido principalmente por
veículos automotores e processos de combustão industrial. Está associado a
problemas respiratórios e é precursor do ozônio troposférico e da chuva ácida.

Autor: Leonardo Rocha
Data: 2026-09-17
Versão: 1.0.0
"""

# =============================================================================
# IMPORTAÇÃO DAS BIBLIOTECAS
# =============================================================================

from pathlib import Path  # Para manipulação de caminhos de arquivos de forma segura
import pandas as pd       # Para leitura e manipulação de dados em tabelas (DataFrames)
import plotly.graph_objects as go  # Para criação de gráficos interativos


# =============================================================================
# LEITURA DOS DADOS
# =============================================================================

# Define o caminho do arquivo CSV com os dados
# O arquivo deve estar na mesma pasta do script
CSV = Path("Dd_grafico_5_28_v2.csv")

# Lê o arquivo CSV usando codificação UTF-8 com BOM (comum em arquivos do Windows)
# Lê o arquivo CSV com configurações específicas:
# - sep=None: detecta automaticamente o separador (vírgula, ponto-e-vírgula, etc.)
# - engine="python": usa o parser Python para maior flexibilidade
# - encoding="utf-8-sig": lida com arquivos UTF-8 com BOM (comum em Excel)
df = pd.read_csv(CSV, sep=None, engine="python", encoding="utf-8-sig")


# =============================================================================
# PREPARAÇÃO DOS DADOS
# =============================================================================

# Nome da coluna que contém os nomes das estações de monitoramento
station_col = "estacao"

# Identifica as colunas que representam anos e as ORDENA numericamente
# O .strip() remove espaços em branco antes da verificação
# A função sorted() com key=int garante ordem cronológica correta
# Exemplo: ["2010", "2009", "2011"] → ["2009", "2010", "2011"]
year_cols = sorted(
    [c for c in df.columns if str(c).strip().isdigit()],
    key=int  # Ordena numericamente, não alfabeticamente
)

# --- Conversão das colunas de anos para numérico ---
# Cada coluna de ano pode conter valores com vírgula como separador decimal
# (padrão brasileiro: "12,5" em vez de "12.5")
for c in year_cols:
    df[c] = pd.to_numeric(
        df[c].astype(str).str.replace(",", ".", regex=False),
        errors="coerce"  # Valores inválidos se tornam NaN
    )


# =============================================================================
# DEFINIÇÃO DOS ESTILOS VISUAIS
# =============================================================================

# Lista de estilos (cor + símbolo) para as estações
# 15 combinações diferentes para garantir variedade visual
# Os estilos são aplicados ciclicamente se houver mais estações que estilos
# Cores escolhidas para serem distintas e visualmente agradáveis
styles = [
    ("#2E8B9E", "square"),        # Azul petróleo - Quadrado
    ("#7A9A3A", "diamond-open"),  # Verde oliva - Losango vazado
    ("#00A651", "diamond"),       # Verde - Losango
    ("#FF0000", "square-open"),   # Vermelho - Quadrado vazado
    ("#376FA8", "diamond"),       # Azul - Losango
    ("#F28C00", "circle"),        # Laranja - Círculo
    ("#FF1493", "square-open"),   # Rosa choque - Quadrado vazado
    ("#F2B400", "triangle-up"),   # Amarelo dourado - Triângulo
    ("#E87500", "triangle-up"),   # Laranja escuro - Triângulo
    ("#BDBDBD", "diamond"),       # Cinza claro - Losango
    ("#8F83FF", "circle"),        # Lilás - Círculo
    ("#8B2E2E", "diamond"),       # Marrom avermelhado - Losango
    ("#5B24FF", "diamond-open"),  # Azul violeta - Losango vazado
    ("#7A9938", "triangle-up"),   # Verde musgo - Triângulo
    ("#FF0000", "circle")         # Vermelho (repetido) - Círculo
]


# =============================================================================
# CRIAÇÃO DO GRÁFICO
# =============================================================================

# Inicializa uma figura vazia
fig = go.Figure()

# Itera sobre cada linha do DataFrame usando enumerate para ter o índice
# (_, row) desempacota a tupla (índice, linha), ignorando o índice com _
for i, (_, row) in enumerate(df.iterrows()):
    # Seleciona estilo (cor + símbolo) com base no índice
    # O operador % (módulo) garante repetição cíclica se necessário
    color, symbol = styles[i % len(styles)]
    
    # Adiciona uma série (traço) ao gráfico
    fig.add_trace(go.Scatter(
        # Dados do eixo X (anos ordenados) e eixo Y (valores de NO₂)
        x=year_cols,
        y=[row[c] for c in year_cols],        # Extrai valores de cada ano
        
        # Modo: linha conectando pontos + marcadores nos pontos
        mode="lines+markers",
        
        # Nome da estação (aparece na legenda e no hover)
        name=str(row[station_col]),
        
        # Não conecta gaps (NaN) - útil para dados faltantes
        connectgaps=False,
        
        # Configuração da linha
        line=dict(
            color=color,          # Cor definida pela lista styles
            width=1.7             # Espessura da linha (fina para muitas séries)
        ),
        
        # Configuração dos marcadores
        marker=dict(
            color=color,          # Cor do marcador (mesma da linha)
            symbol=symbol,        # Símbolo definido pela lista styles
            size=8                # Tamanho do marcador em pixels
        ),
        
        # Template para o tooltip (informações ao passar o mouse)
        hovertemplate=(
            "<b>%{fullData.name}</b><br>"  # Nome da estação em negrito
            "NO₂: %{y:.0f} µg/m³<extra></extra>"  # Valor com 1 casa decimal
        )
    ))


# =============================================================================
# CONFIGURAÇÃO DO LAYOUT (APARÊNCIA DO GRÁFICO)
# =============================================================================

fig.update_layout(
    # Tema claro com fundo branco e linhas suaves
    template="plotly_white",
    
    # Altura da figura em pixels
    height=760,
    
    # Margens ao redor do gráfico
    # Margem inferior (205px) para acomodar a legenda horizontal com muitas séries
    margin=dict(l=95, r=35, t=25, b=205),
    
    # Cor de fundo do papel (área externa ao gráfico)
    paper_bgcolor="#ffffff",                  # Branco
    
    # Cor de fundo da área do gráfico
    plot_bgcolor="#ffffff",                   # Branco
    
    # Modo de hover: exibe informações de todas as séries simultaneamente
    # quando o mouse passa sobre um ano específico
    hovermode="x unified",
    
    # Configuração da fonte global
    # Nota: cor mais escura (#222222) para melhor legibilidade
    font=dict(
        family="Arial, sans-serif",           # Fonte sans-serif
        size=14,                              # Tamanho padrão
        color="#222222"                       # Cinza muito escuro (quase preto)
    ),
    
    # Configuração do eixo X (horizontal)
    xaxis=dict(
        type="category",                      # Tipo categórico (rótulos, não números)
        showgrid=False,                       # Sem linhas de grade verticais
        zeroline=False,                       # Sem linha no zero
        showline=True,                        # Mostra a linha do eixo
        linecolor="#B8B8B8",                   # Cor da linha do eixo (cinza médio)
        ticks="inside",                            # Marcadores dentro do eixo
        range=[-0.0, len(year_cols) - 0.0],           # Cola o 1º ponto no eixo Y
        categoryorder="array",                        # Mantém ordem original
        categoryarray=[str(c) for c in year_cols],    # Ordem das categorias
    ),
    
    # Configuração do eixo Y (vertical)
    yaxis=dict(
        title="NO₂ (µg/m³)",                  # Título do eixo
        range=[0, 80],                        # Limites fixos: 0 a 80 µg/m³
        dtick=20,                             # Intervalo de 20 em 20 µg/m³
        showgrid=True,                        # Mostra linhas de grade horizontais
        gridcolor="rgba(100,100,100,0.45)",   # Cinza com 45% de opacidade
        griddash="dot",                       # Linhas pontilhadas
        zeroline=False,                       # Sem linha no zero
        showline=True,                        # Mostra a linha do eixo
        linecolor="#B8B8B8",                   # Cor da linha do eixo (cinza médio)
        ticks="outside"                           # Marcadores fora do eixo
    ),
    
    # Configuração da legenda
    legend=dict(
        orientation="h",                      # Horizontal (economiza espaço)
        yanchor="top",                        # Âncora no topo
        y=-0.16,                              # Posicionada abaixo do gráfico
        xanchor="center",                     # Centralizada horizontalmente
        x=0.5,                                # Centro do eixo X (50%)
        font=dict(size=11.5)                  # Fonte um pouco menor para muitas séries
    )
)


# =============================================================================
# EXPORTAÇÃO DO GRÁFICO
# =============================================================================

# Salva o gráfico em um arquivo HTML (autônomo, com Plotly embutido)
fig.write_html(
    "index.html",                             # Nome do arquivo de saída
    include_plotlyjs=True,                    # Inclui a biblioteca Plotly (funciona offline)
    full_html=True,                           # Gera um documento HTML completo
    config={                                  # Configurações do gráfico
        "responsive": True,                   # Gráfico se adapta ao tamanho da tela
        "displaylogo": False,                 # Remove o logo da Plotly
        "scrollZoom": True                    # Permite zoom com scroll do mouse
    }
)


# =============================================================================
# MENSAGEM DE CONFIRMAÇÃO
# =============================================================================

print("=" * 70)
print("✅ GRÁFICO DE NO₂ GERADO COM SUCESSO!")
print("=" * 70)
print(f"📊 Arquivo: index.html")
print(f"📍 Local: {Path.cwd()}")
print(f"📈 Estações: {len(df)}")
print(f"📅 Anos: {year_cols[0]} a {year_cols[-1]} ({len(year_cols)} anos)")
print(f"🎨 Estilos disponíveis: {len(styles)}")
print("=" * 70)
print("🌐 Abra o arquivo no navegador para visualizar o gráfico interativo.")