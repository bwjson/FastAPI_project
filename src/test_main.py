from urllib.parse import urlencode
from fastapi.testclient import TestClient
from httpx import AsyncClient
import pytest
from redis import asyncio as aioredis
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from main import app

client = TestClient(app)

def test_operations_long_operation():
    redis = aioredis.from_url("redis://localhost", encoding="utf8", decode_responses=True)
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")

    response = client.get('/operations/long_operation')
    assert response.status_code == 200
    assert response.json() == "Много много данных, которые вычислялись сто лет"
    
    redis.close()
    
def test_operations():
    response = client.get('/operations', params={"operation_type": "buy"})
    for i in range(2):
    	assert response.json()["data"][i]["type"] == "buy"

# async tests working only apart from sync tests
@pytest.mark.asyncio
async def test_user_authentication():
    async with AsyncClient(app=app, base_url="http://test") as client:
        test_registration_data = {
            "email": "string2",
            "password": "string2",
            "is_active": True,
            "is_superuser": False,
            "is_verified": False,
            "username": "string2",
            "role_id": 1
        }
        
        registration_response = await client.post(
            '/auth/register', 
            json=test_registration_data, 
            headers={"content-type": "application/json"})
        assert registration_response.status_code == 201

        login_data = {
            "grant_type": "password",
            "username": "string2",
            "password": "string2"
		}
        
        login_response = await client.post(
            '/auth/login',
            data=login_data,
            headers={"content-type": "application/x-www-form-urlencoded"}
		)
        assert login_response.status_code == 204
