import time
import httpx
from typing import Dict, Any

async def ping_site(url: str) -> Dict[str, Any]:
    """
    Função para verificar se um site está online.
    :param url: URL do site a ser verificado.
    :return: Dicionário com o status do site e o tempo de resposta.
    """
    # ADD PREFIX
    if not url.startswith(('http://', 'https://')):
        url = 'http://' + url

    start_time = time.time()
    status = "offline"
    status_code = None

    try:
        async with httpx.AsyncClient(timeout=10.0, follow_redirects=True) as client:
            response = await client.get(url)
            if 200 <= response.status_code < 400:
                status = "online"
            else:
                status = "offline"
            
            status_code = response.status_code

    except Exception as e:
        status = "offline"
        print(f"Error: checking {url}: {str(e)}")
    
    end_time = time.time()
    response_time = round((end_time - start_time) * 1000, 2)

    result = \
    {
        "url": url,
        "status": status,
        "response_time": response_time
    }

    if status_code is not None:
        result["status_code"] = status_code

    return result