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

def categorize_crimes(df: pd.DataFrame, crime_column: str = 'tipo_crime'):
    """
    Categorizar tipos de crime em grupos (violentos, de posse e outros)
    """
    df = df.copy()
    
    crime_categories = {
        'Crimes Violentos': ['homicidio', 'latrocinio', 'lesao_corporal', 'estupro'],
        'Crimes Patrimoniais': ['roubo', 'furto', 'extorsao'],
        'Crimes de Trânsito': ['acidente_fatal', 'direcao_perigosa'],
        'Outros': []
    }
    
    #Subfunção para categorização de outros crimes
    def categorize(crime):
        crime_lower = str(crime).lower()
        for category, keywords in crime_categories.items():
            if any(keyword in crime_lower for keyword in keywords):
                return category
        return 'Outros'
    
    df['categoria_crime'] = df[crime_column].apply(categorize)
    return df

def aggregate_by_region(df: pd.DataFrame, region_col: str = 'municipio'):
    """
    Unir estatísticas por região
    """
    return df.groupby(region_col).agg({
        'ocorrencias': 'sum',
        'vitimas': 'sum',
        # pensar em mais agregações para se realizar
    }).reset_index()

def calculate_crime_rate(df: pd.DataFrame, population_data: pd.DataFrame):
    """
    Calcula da taxa de criminalidade por 100 mil habitantes 
    """
    df = df.merge(population_data, on='municipio', how='left')
    # Fazer uma possível validação para que os valores das colunas sejam de um tipo numérico
    df['taxa_criminalidade'] = (df['ocorrencias'] / df['populacao']) * 100000
    return df