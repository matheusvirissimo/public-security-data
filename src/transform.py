import pandas as pd
import numpy as np
from typing import List
import logging

logger = logging.getLogger(__name__) ## logger já foi carregado antes 

def clean_column_names(df: pd.DataFrame):
    """
    Padronizar nomes de colunas (minúsculas, sem acentos, underscores)

    Params:
        df: DataFrame contendo o dado a ser transformado 
    -------
    Returns: 
        df: retorna o DataFrame normalizado
    """
    df = df.copy()
    df.columns = (df.columns
                  .str.lower() # tudo minusculo 
                  .str.normalize('NFKD') # normalização unicode no formato NNFD
                  .str.encode('ascii', errors='ignore') # botar em asc tudo
                  .str.decode('utf-8') # talvez colocar em latin. Usar para não ficar tudo em byte
                  .str.replace(' ', '_')
                  .str.replace(r'[^\w]', '', regex=True))
    return df

def remove_duplicates(df: pd.DataFrame, subset: List[str] = None):
    """
    Remover registros duplicados para facilitar
    
    Params:
        df: DataFrame
        subset: Colunas para verificar duplicidade
    ------
    Returns: 
        df: DataFrame normalizado
    """
    initial_count = len(df)
    df = df.drop_duplicates(subset=subset)
    removed = initial_count - len(df)
    
    if removed > 0:
        logger.info(f"Removidas {removed} linhas duplicadas")
    
    return df

def handle_missing_values(df: pd.DataFrame, strategy: str = 'drop'):
    """
    Tratamento de valores ausentes
    
    Params:
        df: DataFrame
        strategy: 'drop', 'fill_zero', 'fill_mean', 'fill_median'
    --------
    Returns:
        df: Dataframe sem valores ausentes (ou tratados)
    """
    df = df.copy()
    
    if strategy == 'drop':
        df = df.dropna()
    elif strategy == 'fill_zero':
        df = df.fillna(0)
    elif strategy == 'fill_mean':
        df = df.fillna(df.mean(numeric_only=True))
    elif strategy == 'fill_median':
        df = df.fillna(df.median(numeric_only=True))
    
    return df

def normalize_dates(df: pd.DataFrame, date_columns: List[str]):
    """
    Normalização de datas

    Params: 
        df: DataFrame
        date_columns: lista com as datas
    """
    df = df.copy()
    
    for col in date_columns:
        if col in df.columns: ## Ver esse if com mais carinho
            df[col] = pd.to_datetime(df[col], errors='coerce')
    
    return df

