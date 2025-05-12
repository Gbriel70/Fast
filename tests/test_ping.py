import pytest
import pytest_asyncio
from app.services.ping import ping_site

@pytest.mark.asyncio
async def test_ping_site():
    # Test a sucessful ping
    result = await ping_site("https://www.google.com")
    assert result["status"] == "online"
    assert isinstance(result["response_time"], float)
    assert result["url"].startswith("http")

@pytest.mark.asyncio
async def test_ping_site_invalid_url():
    # Test an invalid URL
    result = await ping_site("invalid-site-that-does-not-exist-123456.com")
    assert result["status"] == "offline"