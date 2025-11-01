import pandas as pd
from pathlib import Path
from typing import Optional
import json
import logging

logger = logging.getLogger(__name__)

def save_to_csv(df: pd.DataFrame, output_path: str, **kwargs):
    """
    Salvar DataFrame em arquivo CSV
    
    Params:
        df: DataFrame a ser salvo
        output_path: Caminho do arquivo de saída
        **kwargs: Argumentos adicionais para 'to_csv'
    """
    try:
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        df.to_csv(output_path, index=False, encoding='utf-8-sig', **kwargs)
        logger.info(f"Dados salvos em: {output_path}")
        return True
    except Exception as e:
        logger.error(f"Erro ao salvar CSV: {e}")
        return False

def save_to_parquet(df: pd.DataFrame, output_path: str, **kwargs):
    """
    Salvar DataFrame em formato Parquet (bem mais eficiente)
    """
    try:
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        df.to_parquet(output_path, index=False, **kwargs)
        logger.info(f"Dados salvos em: {output_path}")
        return True
    except Exception as e:
        logger.error(f"Erro ao salvar Parquet: {e}")
        return False

## Se for usar parquet, bom usar o duckdb para manipular depois os dados

def save_to_excel(df: pd.DataFrame, output_path: str, sheet_name: str = 'Dados'):
    """
    Salvar DataFrame em arquivo Excel (bônus)
    """
    try:
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        df.to_excel(output_path, sheet_name=sheet_name, index=False)
        logger.info(f"Dados salvos em: {output_path}")
        return True
    except Exception as e:
        logger.error(f"Erro ao salvar Excel: {e}")
        return False
    
