from fastapi.testclient import TestClient
from .conftest import app



# create a new movie
def test_create_movie():
    with TestClient(app) as client:

        data = {
                "title": "Mad Max",
                "genres":['action','drama'],
        }

        response = client.post("/movies/", json=data)
        body = response.json()

        assert response.status_code == 201
        assert body.get("title") == "Mad Max"
        assert body.get("genres") == ['action','drama']
        #assert "_id" in body


# create a new movie (invalid data)
def test_create_movie_missing_data():
    with TestClient(app) as client:
        data = {
                "genres":['action','drama'],
        }
        response = client.post("/movies/", json=data)
        assert response.status_code == 422

# get all movies
def test_get_all_movies(add_movie):
    with TestClient(app) as client:
        # given
        movie_one = add_movie('nico',['drama'])
        movie_two = add_movie('algo',['drama','comedy'])

        # when
        response = client.get("/movies/")
        data = response.json()

        # then
        assert response.status_code == 200
        assert data[0]['title'] == movie_one['title']
        assert data[1]['title'] == movie_two['title']
        assert data[1]['genres'] == movie_two['genres']
        assert len(data) == 2
        



# get single movie
def test_get_single_movie(add_movie):

    with TestClient(app) as client:
    
        # given
        movie_one = add_movie('nico',['drama'])
        
        # when
        response = client.get(f"/movies/{movie_one['_id']}/")
        data = response.json()

        # then
        assert response.status_code == 200
        assert data["title"] == "nico"
        for key in data.keys():
            assert key in ["_id", "title", "genres","reviews"]




# edit a movie
def test_edit_movie(add_movie):
    with TestClient(app) as client:
        # insert a new movie
        movie = add_movie('nico',['drama'])
        
        # edito
        edit_data = {"title": "once upon a time","genres":['comedy']}

        response = client.put(
            f"/movies/{movie['_id']}/",
            json=edit_data,
        )
        data = response.json()

        assert response.status_code == 201
        assert data["title"] == edit_data['title']
        assert data["genres"] == edit_data['genres']
        # que efectivamente lo haya editado en la base
        updated_movie = app.database["movies"].find_one({"_id": movie['_id']})
        assert edit_data['title'] == updated_movie['title']




# delete a movie
def test_delete_user(add_movie):
    with TestClient(app) as client:
        # inserto un nuevo usuario
        movie = add_movie('nico',['drama'])
        temp = movie['_id']
        # borro
        response = client.delete(
            f"/movies/{temp}/",
        )
        assert response.status_code == 204
        # chequeo que efectivamente lo haya borrado
        assert app.database["movies"].find_one({"_id": temp}) == None





