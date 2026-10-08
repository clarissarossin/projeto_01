import pandas as pd
import matplotlib.pyplot as plt
import requests
import time 
import openpyxl
# web scrapping 
def carregar_pagina(url, tentativas=3, espera=5):
    for tentativa in range(1, tentativas + 1):
        try:
            resposta = requests.get(url, timeout=10)
            resposta.raise_for_status()
            return resposta.text
        except requests.exceptions.RequestException as erro:
            print(f"Tentativa {tentativa} falhou: {erro}")
            if tentativa == tentativas:
                raise  # depois de esgotar as tentativas, aí sim deixa o erro estourar
            time.sleep(espera)  # espera antes de tentar de novo
from pathlib import Path
pasta = Path(__file__).parent
caminho = pasta / "base_vendas_projeto_2.xlsx"
df= pd.read_excel(caminho)
def carregar_arquivo(caminho):
    try:
        df=pd.read_excel(caminho)
        return df
    except Exception as erro:
        print(f'Erro no processamento do arquivo  {erro}')
        return None
def limpar_colunas(df):
    print(df.columns)
    print(df.head())
    df.columns = df.columns.str.strip().str.lower()
    if "valor da venda"in df.columns:
        df = df.rename(columns={"valor da venda": "vendas"})
    return df

def limpar_dados(df):
    if 'vendas' in df.columns:
        df["vendas"] = pd.to_numeric(df["vendas"], errors='coerce')
    df = df.drop_duplicates()
    print(df.isnull().sum())
    print(df.dtypes)
    return df

def analisar_dados(df):
    if 'vendas' not in df.columns:
        print("A coluna 'vendas' não está presente no DataFrame.")
    else:
        fat_total = df["vendas"].sum()
        ticket_medio = df["vendas"].mean()
        maior_venda = df["vendas"].max()
        menor_venda = df["vendas"].min()
        fat_produto= df.groupby('produto')['vendas'].sum()
        fat_cidade= df.groupby('cidade')['vendas'].sum()
        total_de_vendas= len(df)
    return fat_total, ticket_medio, maior_venda, menor_venda, fat_produto, fat_cidade,total_de_vendas

def gerar_grafico_produto(df):
    df.plot(
        x='produto', y='vendas', kind='bar')
    plt.title('faturamento por produto')
    plt.xlabel('produto')
    plt.ylabel('valor')
    plt.tight_layout()
    plt.show()
    return df
def gerar_grafico_cidade(df):
    df.plot(
        x='cidade', y='vendas', kind='bar')
    plt.title('faturamento por cidade')
    plt.xlabel('cidades')
    plt.ylabel('valor')
    plt.tight_layout()
    plt.show()
    return df

