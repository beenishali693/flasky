import pytest
from app import create_app
from app.db import db
from flask.signals import request_finished
from dotenv import load_dotenv
import os 
from app.models.cat import Cat

load_dotenv()

@pytest.fixture
def app():
    test_config = {
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": os.environ.get("SQLALCHEMY_TEST_DATABASE_URI")
    }
    app = create_app(test_config)

    @request_finished.connect_via(app)
    def expire_session(sender, response, **extra):
        db.session.remove()

    with app.app_context():
        db.create_all()
        yield app

    with app.app_context():
        db.drop_all()
    
@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def two_saved_cats(app):
    cat_1 = Cat(name="Luna", color="ash", personality="Tomato Queen")
    cat_2 = Cat(name="Simon", color="black", personality="might be a human stuck in a cats body")

    db.session.add_all([cat_1, cat_2])

    db.session.commit()

