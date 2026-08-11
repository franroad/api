import pytest

def test_vote_post(authorized_client, fix_create_posts):
    post_id=fix_create_posts[0].id
    response = authorized_client.post("/vote/", json={"post_id":post_id,"like":1})
    print(response.json())
    assert response.status_code==200

def test_vote_twice(authorized_client, fix_create_posts):
    post_id=fix_create_posts[0].id
    first_vote = authorized_client.post("/vote/", json={"post_id":post_id,"like":1})
    second_vote = authorized_client.post("/vote/", json={"post_id":post_id,"like":1})
    print(second_vote.json())
    assert second_vote.status_code==403



def test_vote_non_existing_post(authorized_client):
    response = authorized_client.post("/vote/", json={"post_id":555,"like":1})
    print (response.json())
    assert response.status_code==404

def test_unauthorized_vote(client,fix_create_posts):
    post_id=fix_create_posts[0].id
    response = client.post("/vote/", json={"post_id":post_id,"like":1})
    print (response.json())
    assert response.status_code==401
