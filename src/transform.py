import pandas as pd
import numpy as np
from typing import List
import logging

logger = logging.getLogger(__name__) ## logger já foi carregado antes 

def clean_column_names(df: pd.DataFrame):
    """
    Padronizar nomes de colunas (minúsculas, sem acentos, underscores)
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
