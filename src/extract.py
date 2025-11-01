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

def extract_from_portal(year: int, month: int, data_dir: str = "data/raw"):
    """
    Extrair dados mensais do portal de dados abertos da Secretaria de Segurança de São Paulo 
    
    Params:
        year: Ano dos dados
        month: Mês dos dados
        data_dir: Diretório para salvar dados brutos
    --------
    Returns:
        DataFrame (pandas) com os dados extraídos
    """
    # URL exemplo (PRECISA AJUSTAR)
    url = f"https://www.ssp.sp.gov.br/estatistica/dados/{year}/{month:02d}/dados.csv"
    file_path = f"{data_dir}/{year}_{month:02d}_raw.csv"
    
    downloaded = download_csv_ssp(url, file_path)
    if downloaded:
        return pd.read_csv(downloaded, encoding='latin1', sep=';') #o utf tem que ser latin se não dá erro
    return None

def extract_local_file(file_path: str, **kwargs):
    """
    Extrair dados de arquivo local CSV/Excel
    
    Args:
        file_path: Caminho do arquivo
        **kwargs: Argumentos adicionais para pd.read_csv ou pd.read_excel
    
    Returns:
        DataFrame com os dados
    """
    try:
        if file_path.endswith('.csv'): # caminho terminou com csv
            return pd.read_csv(file_path, **kwargs) 
        elif file_path.endswith(('.xlsx', '.xls')):
            return pd.read_excel(file_path, **kwargs) # caminho terminou em planilha
        else:
            logger.error(f"Formato não suportado: {file_path}")
            return None
    except Exception as e:
        logger.error(f"Erro ao ler arquivo {file_path}: {e}")
        return None
    
def extract_api_data(endpoint: str, params: dict = None):
    """
    Extrair dados da API (se cabível/disponível)
    
    Args:
        endpoint: URL da API
        params: Parâmetros da requisição
    
    Returns:
        Dados em formato .json
    """
    try:
        response = requests.get(endpoint, params=params, timeout=30)
        response.raise_for_status()
        return response.json() # compacta em json a resposta
    except Exception as e:
        logger.error(f"Erro ao acessar API {endpoint}: {e}")
        return None