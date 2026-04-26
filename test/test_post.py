
from typing import List
from app import schemas
import pytest

#Extra challenge for testing posts 
# as we need authentication

#MAKE USE OF FIXTURE
def test_get_post(authorized_client,fix_create_posts):
    response=authorized_client.get("/posts/") # sending data in the body, we pass a dictionary
    
    print(f"POST RESPONSE: {response.json()}")
    
    assert response.status_code==200
    assert response.json()[0]["Post🪆"]["title"]== "first title"
    assert response.json()[0]["Post🪆"]["user_id"]==fix_create_posts[0].user_id

def test_unauthorized_get_all(client,fix_create_posts):
    response=client.get("/posts/")
    assert response.status_code==401
    print(f"unauthorized RESPONSE: {response.json()}")
    print(f"status code: {response.status_code}")

def test_get_post_by_id(client,fix_create_posts):
    response=client.get(f"/posts/{fix_create_posts[0].id}")
    assert response.status_code==200
    assert response.json()["Post🪆"]["id"]==fix_create_posts[0].id
    print(f"Post by id: {response.json()}")
    print(f"status code: {response.status_code}")

def test_non_existing_post(authorized_client,fix_create_posts):
    response=authorized_client.get(f"/posts/9999")
    assert response.status_code==404
    print(f"Non existing post :{response.json()}")

#Usando parameritrice con diccionario.

@pytest.mark.parametrize("payload", [
    {"title": "Post 1", "content": "C1", "published": False}, # Caso False
    {"title": "Post 2", "content": "C2", "published": True},  # Caso True
    {"title": "Post 3", "content": "C3"}                       # Caso Default (Omitido)
])
def test_create_post_limpio(authorized_client, payload):
    response = authorized_client.post("/posts/", json=payload)
    
    assert response.status_code == 201
    assert response.json()["content"]==payload[2].content
    
    # Aquí está la clave: 
    # Si 'published' no está en el payload, esperamos que sea True (por tu Pydantic)
    # expected_val = payload.get("published", True) 
    
    # assert res_json["Post🪆"]["published"] == expected_val