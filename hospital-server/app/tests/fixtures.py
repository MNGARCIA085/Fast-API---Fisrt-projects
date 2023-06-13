import pytest
from auth import models

# add an user to the database
@pytest.fixture(scope='function')
def add_user(db_session): #db_session:db_session
    def _add_user(name, last_name):
        db_user = models.User(name=name,last_name=last_name)
        db_session.add(db_user)
        db_session.commit()
        return db_user
    return _add_user




# add a group to the database
@pytest.fixture(scope='function')
def add_group(db_session):
    def _add_group(name):
        db_group = models.Groups(name=name)
        db_session.add(db_group)
        db_session.commit()
        return db_group
    return _add_group




# add a user and a list of his courses by id
@pytest.fixture(scope='function')
def add_groups_user(db_session):
    def _add_groups_user(user_id,groups):
        for g in groups:
            db_item = models.UserGroups(user_id=user_id,group_id=g)
            db_session.add(db_item)
        db_session.commit()
        return 'Ok'
    return _add_groups_user



