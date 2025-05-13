import pytest
import pytest_asyncio
import socket
from unittest.mock import patch, MagicMock
from app.services.nmap import scan_port, port_scan

@pytest.mark.asyncio
async def test_scan_port_success():
    """Testa se scan_port detecta corretamente uma porta aberta."""
    # Mock do socket para simular uma porta aberta
    with patch('socket.socket') as mock_socket:
        mock_sock_instance = MagicMock()
        mock_sock_instance.connect_ex.return_value = 0  # 0 significa sucesso (porta aberta)
        mock_socket.return_value = mock_sock_instance
        
        result = await scan_port('example.com', 80)
        assert result == True

@pytest.mark.asyncio
async def test_scan_port_closed():
    """Testa se scan_port detecta corretamente uma porta fechada."""
    # Mock do socket para simular uma porta fechada
    with patch('socket.socket') as mock_socket:
        mock_sock_instance = MagicMock()
        mock_sock_instance.connect_ex.return_value = 1  # Não-zero significa erro (porta fechada)
        mock_socket.return_value = mock_sock_instance
        
        result = await scan_port('example.com', 81)
        assert result == False

@pytest.mark.asyncio
async def test_scan_port_error():
    """Testa se scan_port lida corretamente com erros de socket."""
    # Mock do socket para simular um erro
    with patch('socket.socket') as mock_socket:
        mock_sock_instance = MagicMock()
        mock_sock_instance.connect_ex.side_effect = socket.error("Simulando erro")
        mock_socket.return_value = mock_sock_instance
        
        result = await scan_port('example.com', 80)
        assert result == False

@pytest.mark.asyncio
async def test_port_scan_invalid_host():
    """Testa se o port_scan rejeita hosts inválidos."""
    result = await port_scan('localhost')
    assert 'error' in result
    assert result['error'] == 'Invalid or local host specified'
    
    result = await port_scan('127.0.0.1')
    assert 'error' in result
    assert result['error'] == 'Invalid or local host specified'
    
    result = await port_scan('')
    assert 'error' in result
    assert result['error'] == 'Invalid or local host specified'

@pytest.mark.asyncio
async def test_port_scan_url_formatting():
    """Testa se o port_scan formata corretamente a URL."""
    # Mock do scan_port para evitar conexões reais
    with patch('app.services.nmap.scan_port', return_value=False):
        # Testa URL sem protocolo
        result = await port_scan('google.com')
        assert result['host'] == 'google.com'
        
        # Testa URL com HTTP
        result = await port_scan('http://google.com')
        assert result['host'] == 'google.com'
        
        # Testa URL com HTTPS
        result = await port_scan('https://google.com')
        assert result['host'] == 'google.com'
        
        # Testa URL com caminho
        result = await port_scan('https://www.terra.com.br/esportes/futebol/')
        assert result['host'] == 'www.terra.com.br'

@pytest.mark.asyncio
async def test_port_scan_common_only():
    """Testa se o modo common_only escaneia apenas portas comuns."""
    # Mock do scan_port para evitar conexões reais
    with patch('app.services.nmap.scan_port', return_value=False):
        result = await port_scan('example.com', common_only=True)
        # O número de portas escaneadas deve ser menor que 100 no modo common_only
        assert result['ports_scanned'] < 100

@pytest.mark.asyncio
async def test_port_scan_full_range():
    """Testa se o modo common_only=False escaneia todas as portas."""
    # Mock do scan_port para evitar conexões reais
    with patch('app.services.nmap.scan_port', return_value=False):
        result = await port_scan('example.com', max_ports=100, common_only=False)
        assert result['ports_scanned'] == 100

@pytest.mark.asyncio
async def test_port_scan_open_port_detection():
    """Testa se o port_scan detecta portas abertas corretamente."""
    # Mock que simula porta 80 aberta e todas as outras fechadas
    async def mock_scan_port(host, port, timeout=None):
        return port == 80
        
    with patch('app.services.nmap.scan_port', side_effect=mock_scan_port):
        result = await port_scan('example.com')
        
        # Deve haver pelo menos uma porta aberta
        assert len(result['open_ports']) >= 1
        
        # Verificar se a porta 80 está entre as portas abertas
        has_port_80 = any(port_info['port'] == 80 for port_info in result['open_ports'])
        assert has_port_80 == True