def test_get_all_cats_with_no_records(client):
    #Act
    response = client.get("/cats")
    response_body = response.get_json()

    #Assert 
    assert response.status_code == 200
    assert response_body == []

def test_get_one_cat_succeeds(client, two_saved_cats):
    response = client.get("cats/1")
    response_body = response.get_json()

    assert response.status_code == 200
    assert response_body == {
        "id": 1,
        "name": "Luna", 
        "color": "ash",
        "personality": "Tomato Queen"
    }

def test_create_one_cat(client):
    response = client.post("/cats", json={
        "name": "Garfield",
        "color": "Orange",
        "personality": "Likes Lasagna, Hates Mondays"
    })
    response_body = response.get_json()

    assert response.status_code == 201
    assert response_body == {
        "id": 1,
        "name": "Garfield",
        "color": "Orange",
        "personality": "Likes Lasagna, Hates Mondays"
    }


