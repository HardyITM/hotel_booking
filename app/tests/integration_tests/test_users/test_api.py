
import pytest
from httpx import AsyncClient


@pytest.mark.parametrize(
    'email,password,status_code',
    [
        ("testing@test.com", "testingpass", 200),
        ("testing@test.com", "testingpass1", 409),
        ('adfkdfkdg', '3145fdgdg', 422)
        
    ]
)
async def test_register_user(email, password, status_code, ac: AsyncClient):
    response = await ac.post(
        '/auth/register',
        json={ 
            "email": email,
            "password": password             
        }
    )
    
    assert response.status_code == status_code
    
@pytest.mark.parametrize(
    'email,password,status_code',
    [
        ("test@test.com", "test", 200),
        ('artem@example.com', 'artem', 200),
        ('testing_test@test.com', 'testing', 401)
    ]
)
async def test_login_user(email, password, status_code, ac: AsyncClient):
    response = await ac.post(
        '/auth/login',
        json={ 
            "email": email,
            "password": password             
        }
    )
    assert response.status_code == status_code