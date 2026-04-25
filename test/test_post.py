
from typing import List
from app import schemas

#Extra challenge for testing posts 
# as we need authentication

#MAKE USE OF FIXTURE
def test_get_post(authorized_client,test_create_posts):
    response=authorized_client.get("/posts/") # sending data in the body, we pass a dictionary
    
    print(f"POST RESPONSE: {response.json()}")
    
    assert response.status_code==200
    assert response.json()[0]["Post🪆"]["title"]== "first title"
    assert response.json()[0]["Post🪆"]["user_id"]==test_create_posts[0].user_id