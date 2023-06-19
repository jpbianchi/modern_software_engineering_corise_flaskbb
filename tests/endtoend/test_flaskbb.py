import pytest
from playwright.sync_api import Page

###################################################################
# CoRise TODO: add a new fixture `translations` that calls the
# `compile_translations` function from flaskbb.utils.translations

from flaskbb import create_app
from flaskbb.configs.testing import TestingConfig as Config
from flaskbb.extensions import db
from flaskbb.utils.populate import create_default_groups, create_default_settings, create_user, create_welcome_forum

from flaskbb.utils.translations import compile_translations
from flask import url_for

@pytest.fixture(scope='session')   # <<< I had to specify the scope to pass test
def app():

    app = create_app(Config)

    # let's put the context in a context manager (duh!)
    with app.app_context():
        # let's load the functions in the fixtures passed as parameters
        # to test_home_page, ie application, default_settings, 
        # default_groups and translations
        db.create_all()
        create_default_groups()
        create_default_settings()
        compile_translations()

        # The application and the test run in two different processes
        # so creating the user in the test or fixture doesn't add it to the same DB instance
        create_user("test", "test", "test@example.org", "member")
        create_welcome_forum()

    return app


def test_load_home_page(live_server, page: Page):
    # Hint: Check out `flask.url_for` helper function to get the external url for 
    # an endpoint. Then go to it using playwright's `page.goto(url)`

    home_url = url_for("forum.index", _external=True)
    page.goto(home_url)
    assert page.title() == "FlaskBB - A lightweight forum software in Flask"
    # other solution using Playwright function 'expect'
    # expect(page).to_have_title("FlaskBB - A lightweight forum software in Flask")


from flask_login import login_user, logout_user, current_user
from flaskbb.user.models import User
from flaskbb.forum.models import Category, Forum, Topic, Post

def test_user_post(live_server, page:Page, forum, default_groups):
    """ I first did the bonus by using flaskbb API which
        is not what we were supposed to do
    """

    # I could have used the fixture user, which creates a standard user
    user = User(username="JP", 
                email="JP@example.org",
                password="jp123", 
                primary_group=default_groups[3],
                activated=True)
    JPuser = user.save()

    success = login_user(JPuser)  # I should have normally recreated the User...
    assert success, 'Login failed'
    assert current_user.is_authenticated, f'User is not authenticated'

    # see test_forum_models.py::test_post_save
    text = 'A difficult test'
    topic = Topic(title='test') 
    post = Post(content=text)
    # post.save(topic=topic, user=user)
    topic.save(forum=forum, user=JPuser, post=post)  # let's use the forum fixture

    # otherwise use this code to create a forum
    #with database.session.no_autoflush:
    #        forum = Forum(title="forum name", category=category)
    #        forum.groups = Group.query.filter(Group.guest == False).all()
    #        forum.save()

    # let's read the post using the user
    assert JPuser.last_post.content == text, f'Wrong post content {post.content} instead of {text}'
    assert JPuser.last_post == post
    assert JPuser.post_count == 1
    assert Topic.get_topic(JPuser.last_post.topic_id, JPuser).forum_id == forum.id

    assert topic.last_post == post
    assert topic.user.post_count == 1
    assert topic.post_count == 1
    assert topic.forum.post_count == 1

def test_create_post(live_server, page: Page):
    """ Here we use playwright only to simulate a user using the UI
        Thanks to Chris Bloom
    """
    url = url_for('auth.login', _external=True)
    page.goto(url)
    assert "Login" in page.title()

    page.get_by_label("Username or Email address").fill("test")
    page.get_by_label("Password").fill("test")
    page.get_by_role("button", name="Login").click()
    assert not "Wrong username or password" in page.content()

    page.screenshot(path="welcome.jpeg")
    page.get_by_role("link", name="Welcome", exact=True).click()
    assert "Welcome" in page.title()

    page.screenshot(path="new_topic.jpeg")
    page.get_by_role("link", name="New Topic").click()
    assert "New Topic" in page.title()

    page.get_by_label("Topic title").fill("My Topic")
    page.get_by_label("Content").fill("Hi!")
    page.get_by_role("button", name="Post Topic").click()
    assert "My Topic" in page.title()





