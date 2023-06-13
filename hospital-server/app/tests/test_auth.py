from fastapi.testclient import TestClient
from main import app
from auth.models import User,Groups

client = TestClient(app)

""" 1. USER """

# create a new user
def test_create_user(client,db_session): # antes sin client
    response = client.post(
        "/auth/users",
        #headers={"X-Token": "coneofsilence"},
        json={"name": "nico","last_name":"las"},
    )

    assert response.status_code == 201
    data = response.json()
    assert data['name'] == "nico"
    assert "id" in data
    # que efectivamente haya sido ingresado
    esta = db_session.query(User).filter(User.id==data['id']).first()
    assert esta



# try to create an user with invalida data
def test_create_user_invalid_data(client):
    response = client.post(
        "/auth/users",
        json={},
    )
    assert response.status_code == 422


# inserto un usuario y testeo que haya quedado bien
def test_get_single_user(client,add_user):
    
    # given
    user = add_user(name='nombre',last_name='df')
    
    # when
    response = client.get(f"/auth/users/{user.id}/")
    data = response.json()

    # then
    assert response.status_code == 200
    assert data["name"] == "nombre"
    for key in data.keys():
        assert key in ["id", "name", "last_name","groups"] # da error si no están todas las claves



# todos los usuarios
def test_get_all_users(client, add_user):
    # given
    user_one = add_user(name='nombre1',last_name='a1')
    user_two = add_user(name='nombre2',last_name='a2')
    
    # when
    response = client.get(f"/auth/users/")
    data = response.json()

    # then
    assert response.status_code == 200
    assert data[0]["name"] == user_one.name
    assert data[1]["name"] == user_two.name



# edit an user
def test_edit_user(client, add_user, db_session):
    # inserto un nuevo usuario
    user = add_user(name='nombre',last_name='apellido')
    # edito
    response = client.put(
        f"/auth/users/{user.id}/",
        json={"name": "nombreEditado","last_name": "apellidoEditado"},
    )
    data = response.json()
    assert response.status_code == 201
    assert data["name"] == 'nombreEditado'
    # que efectivamente lo haya editado en la base
    esta = db_session.query(User).filter(User.id==user.id).first()
    assert esta.name == 'nombreEditado'



# edit an user
def test_delete_user(client, add_user,db_session):
    # inserto un nuevo usuario
    user = add_user(name='nombre',last_name='apellido')
    temp = user.id
    # borro
    response = client.delete(
        f"/auth/users/{user.id}/",
    )
    assert response.status_code == 200
    # chequeo que efectivamente lo haya borrado
    esta = db_session.query(User).filter(User.id==temp).first()
    assert esta == None




""" 2. GROUPS """

# create a new group
def test_create_group(client,db_session): # antes sin client
    response = client.post(
        "/auth/groups",
        json={"name": "grupo"},
    )

    assert response.status_code == 201
    data = response.json()
    assert data['name'] == "grupo"
    assert "id" in data
    # que efectivamente haya sido ingresado
    esta = db_session.query(Groups).filter(Groups.id==data['id']).first()
    assert esta



# try to create an group with invalida data
def test_create_group_invalid_data(client):
    response = client.post(
        "/auth/groups",
        json={},
    )
    assert response.status_code == 422


# inserto un usuario y testeo que haya quedado bien
def test_get_single_group(client,add_group):
    
    # given
    group = add_group(name='nombre')
    
    # when
    response = client.get(f"/auth/groups/{group.id}/")
    data = response.json()

    # then
    assert response.status_code == 200
    assert data["name"] == "nombre"
    for key in data.keys():
        assert key in ["id", "users","name"] # da error si no están todas las claves



# todos los grupos
def test_get_all_groups(client, add_group):
    # given
    group_one = add_group(name='grupo1')
    group_two = add_group(name='grupo2')
    
    # when
    response = client.get(f"/auth/groups/")
    data = response.json()

    # then
    assert response.status_code == 200
    assert data[0]["name"] == group_one.name
    assert data[1]["name"] == group_two.name



# edit a group (not implemented yet)
"""
def test_edit_group(client, add_group, db_session):
    # inserto un nuevo usuario
    user = add_group(name='nombre')
    # edito
    response = client.put(
        f"/auth/groups/{user.id}/",
        json={"name": "nombreEditado"},
    )
    data = response.json()
    assert response.status_code == 201
    assert data["name"] == 'nombreEditado'
    # que efectivamente lo haya editado en la base
    esta = db_session.query(Groups).filter(Groups.id==user.id).first()
    assert esta.name == 'nombreEditado'
"""


# delete a group
def test_delete_group(client, add_group,db_session):
    # inserto un nuevo usuario
    group = add_group(name='nombre')
    temp = group.id
    # borro
    response = client.delete(
        f"/auth/groups/{group.id}/",
    )
    assert response.status_code == 200
    # chequeo que efectivamente lo haya borrado
    esta = db_session.query(Groups).filter(Groups.id==temp).first()
    assert esta == None




"""" 3. GROUPS AND USERS """


def test_add_groups_to_user(client,add_user,add_group):
    
    # given
    user = add_user(name="u1",last_name='a1')
    group_one = add_group(name='grupo1')
    group_two = add_group(name='grupo2')
    listaGroups = [group_one.id,group_two.id]
    #add_groups_user(user=user.id,groups=listaGroups)

    
    # when
    response = client.post(
        f"/auth/userAndGroups/",
        json = {
                "user": {
                        "name":user.name,
                        "last_name":user.last_name
                    }
                ,
                "groups":listaGroups
               }
    )
    data = response.json()


    # then
    assert response.status_code == 201
    assert data['User']['name'] == user.name
    assert data['Groups'] == listaGroups
   
    



# edit groups per user
def test_edit_groups_to_user(client,add_user,add_group,add_groups_user):
    
    # GIVEN 
    user = add_user(name="u1",last_name='a1')
    group_one = add_group(name='grupo1')
    group_two = add_group(name='grupo2')
    listaGroups = [group_one.id,group_two.id]
    add_groups_user(user.id,listaGroups)
    # new groups
    group_three = add_group(name='grupo3')
    group_four = add_group(name='grupo4')
    nuevosGrupos = [group_three.id, group_four.id]
    
    # WHEN
    response = client.put(
        f"/auth/userAndGroups/{user.id}",
        json = {
                "groups":nuevosGrupos
               }
    )
    data = response.json()
    print(data) # imprime ok


    # THEN
    assert response.status_code == 201
    assert data['Groups']['groups'] == nuevosGrupos




# obs: no es bueno poner req.body en un delete (desaconsejado)
# dilema: cómo borrar varios a la vez (un patch puede estar bien)



# delete an user
# inserto,
# lo borro y me fijo que no esté en la base



#https://blog.j-labs.pl/index.php?page=2017/02/Given-When-Then-pattern-in-unit-tests


#https://cosasdedevs.com/posts/tests-fastapi/

