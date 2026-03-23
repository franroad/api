#Extra challenge for testing posts 
# as we need authentication

#MAKE USE OF FIXTURE
def test_get_post(authorized_client):
    response=authorized_client.get("/posts/") # sending data in the body, we pass a dictionary
    print(f"POST RESPONSE: {response.json()}")
    
    assert response.status_code==200