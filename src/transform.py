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

