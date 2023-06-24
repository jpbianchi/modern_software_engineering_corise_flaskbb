from flask import url_for
import os
import pytest
from flaskbb import create_app
from flaskbb.configs.testing import TestingConfig as Config
from flaskbb.extensions import db
from flaskbb.utils.populate import create_default_groups, create_default_settings
from flaskbb.utils.translations import compile_translations
from playwright.sync_api import Page, expect

os.environ['FLASK_ENV'] = 'development'

@pytest.fixture
def app():
    """application with context."""
    app = create_app(Config)
    
    with app.app_context():
        db.create_all()
        create_default_groups()
        create_default_settings()
        compile_translations()

    return app

def test_create_new_account(live_server, page: Page):    
    url=url_for('forum.index', _external=True)

    page.goto(url)
    expect(page).to_have_title("FlaskBB - A lightweight forum software in Flask")
    

    
