import pytest

def test_vote_post(authorized_client, fix_create_posts):
    #response = authorized_client.post("/vote/", json={"post_id":1,"like":1})
    response = authorized_client.post("/vote/", json={"post_id":555,"like":1})
    print(response.json())
    assert response.status_code==200

