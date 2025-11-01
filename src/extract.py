import requests ## lib para requisição web
import pandas as pd
from pathlib import Path
from typing import Optional
import logging ## lib para fazer o registro das ações

## Carregar log
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def download_csv_ssp(url: str, save_path: str):
    """
    Baixar arquivo CSV do portal da SSP-SP
    
    Params:
        url: URL do arquivo CSV
        save_path: Caminho para salvar o arquivo
    --------
    Returns:
        Caminho do arquivo salvo ou None em caso de erro
    """
    try:
        response = requests.get(url, timeout=30) ## Se não acessar em 30 segundos, falha
        response.raise_for_status()
        
        Path(save_path).parent.mkdir(parents=True, exist_ok=True) ## criaru m novo diretório
        with open(save_path, 'wb') as f:
            f.write(response.content) ## conteúdo encontrado
        
        logger.info(f"Arquivo baixado: {save_path}")
        return save_path ## Retorna o caminho encontrado
    except Exception as e:
        logger.error(f"Erro ao baixar {url}: {e}")
        return None

