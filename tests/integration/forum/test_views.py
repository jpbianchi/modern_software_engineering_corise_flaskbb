
from flask import url_for
from flask_login import login_user
from flaskbb.forum.models import Topic, Forum
from flaskbb.forum.topic_manager import actions_map

# CoRise TODO: implement a integration test to validate the functionality of post method
"""
Hint: All actions require an logged in user autorized to manage topics the super_moderator_user
matches that criteria. Additionally, you will need access to a forum and topic both exist as a fixture.

Additionally, you will need a topic and a forum both are available as fixtures. Finally, you will need to
turn of cross site scripting checks since you are not using a real browser.

Your can use this template for each integration test you write.

def test_<action>(application, forum, topic, super_moderator_user):
    application.config['WTF_CSRF_ENABLED'] = False

    with application.test_client() as test_client:
        manage_forum_url = url_for("forum.manage_forum", forum_id=forum.id)

        login_response = test_client.post(url_for('auth.login'), data={'login': super_moderator_user.username,
                                        'password': 'test'},
                        follow_redirects=True)

        response = test_client.post(manage_forum_url, data = {
            "rowid": topic.id,
            ...
        }, follow_redirects=True)

        assert response.status_code == 200

    fresh_topic = Topic.query.filter_by(id=topic.id).first()
    # validate topic state change here.

"""

def response(application, forum, topic, super_moderator_user, action, forumid=None):
    application.config['WTF_CSRF_ENABLED'] = False

    # let's set the conditions for unlocking the topic
    if action in actions_map:
        _, _, topictype, flag = actions_map.get(action)
        if topictype is not None and flag is not None:
            setattr(topic, topictype, flag)
            assert getattr(topic, topictype) == flag, f"Topic '{topictype}' wrongly set to {not flag}!"
            # print(f"Topic.{topictype} set to {flag}")

    with application.test_client() as test_client:
        manage_forum_url = url_for("forum.manage_forum", forum_id=forum.id)

        login_response = test_client.post(url_for('auth.login'), 
                                          data={'login': super_moderator_user.username,      'password': 'test'},
                                          follow_redirects=True)
        
        assert login_response.status_code == 200, f"Wrong login response {login_response}"
        data = {"rowid": topic.id, action: "1"}
        if forumid is not None:
            data['forum'] = forumid
        response = test_client.post(manage_forum_url, 
                                    data=data, 
                                    follow_redirects=True)

        assert response.status_code == 200, f"Wrong response status code {response.status_code}!"
        # print(f"\nWe passed the response test for action '{action}'")

    fresh_topic = Topic.query.filter_by(id=topic.id).first()

    if action in actions_map:
        
        if flag is not None:
            assert getattr(fresh_topic, topictype) != flag, f"Action '{action}': '{topictype}' did not switch to {not flag}!"
        else:
            assert fresh_topic is None, f"Action '{action}': '{topictype}' did not switch to None!"
    
    return fresh_topic

def test_actions(application, forum, topic, super_moderator_user):

    for action in actions_map:
        print(f"\nTESTING action '{action}' !!!")
        response(application, forum, topic, super_moderator_user, action)


def test_move(application, forum, topic, category, default_groups, super_moderator_user):
    application.config['WTF_CSRF_ENABLED'] = False

    new_forum = Forum(title="Second Test Forum", category_id=category.id)
    new_forum.groups = default_groups
    new_forum.save()

    assert not topic.forum == new_forum

    fresh_topic = response(application, forum, topic, super_moderator_user, 
                           "move", forumid=new_forum.id)
    # move is not in actions mapping so only the login and response tests are done
    
    assert fresh_topic.forum == new_forum

# I added the tests from 'week2_solution'
def test_topic_required(application, forum, super_moderator_user):
    application.config['WTF_CSRF_ENABLED'] = False

    with application.test_client() as test_client:
        manage_forum_url = url_for("forum.manage_forum", forum_id=forum.id)

        login_response = test_client.post(url_for('auth.login'), data={'login': super_moderator_user.username,
                                        'password': 'test'},
                        follow_redirects=True)
        
        assert login_response.status_code == 200
        
        response = test_client.post(manage_forum_url, data = {
             "highlight": True,
        }, follow_redirects=True)

        assert response.status_code == 200
        assert "In order to perform this action you have to select at least one topic." in response.get_data(as_text=True)

def test_requires_a_logged_in_moderator(application, forum, topic):
    application.config['WTF_CSRF_ENABLED'] = False

    with application.test_client() as test_client:
        manage_forum_url = url_for("forum.manage_forum", forum_id=forum.id)
        
        response = test_client.post(manage_forum_url, data = {
            "rowid": topic.id,
             "highlight": True,
        }, follow_redirects=True)

        assert response.status_code == 200
        assert "You are not allowed to manage this forum" in response.get_data(as_text=True)

def test_requires_a_user_with_moderator_permissions(application, forum, topic, user):
     application.config['WTF_CSRF_ENABLED'] = False

     with application.test_client() as test_client:
        manage_forum_url = url_for("forum.manage_forum", forum_id=forum.id)

        login_response = test_client.post(url_for('auth.login'), data={'login': user.username,
                                        'password': 'test'},
                        follow_redirects=True)
        
        assert login_response.status_code == 200
        
        response = test_client.post(manage_forum_url, data = {
            "rowid": topic.id,
             "highlight": True,
        }, follow_redirects=True)

        assert response.status_code == 200
        assert "You are not allowed to manage this forum" in response.get_data(as_text=True)

def test_highlight_topic(application, forum, topic, super_moderator_user):
    application.config['WTF_CSRF_ENABLED'] = False

    with application.test_client() as test_client:
        manage_forum_url = url_for("forum.manage_forum", forum_id=forum.id)

        login_response = test_client.post(url_for('auth.login'), data={'login': super_moderator_user.username,
                                        'password': 'test'},
                        follow_redirects=True)
        
        assert login_response.status_code == 200
        
        response = test_client.post(manage_forum_url, data = {
            "rowid": topic.id,
             "highlight": True,
        }, follow_redirects=True)

        assert response.status_code == 200

    fresh_topic = Topic.query.filter_by(id=topic.id).first()
    
    assert fresh_topic.important == True

def test_delete_topic(application, forum, topic, super_moderator_user):
    application.config['WTF_CSRF_ENABLED'] = False

    with application.test_client() as test_client:
        manage_forum_url = url_for("forum.manage_forum", forum_id=forum.id)

        login_response = test_client.post(url_for('auth.login'), data={'login': super_moderator_user.username,
                                        'password': 'test'},
                        follow_redirects=True)
        
        assert login_response.status_code == 200
        
        response = test_client.post(manage_forum_url, data = {
            "rowid": topic.id,
             "delete": True,
        }, follow_redirects=True)

        assert response.status_code == 200

    fresh_topic = Topic.query.filter_by(id=topic.id).first()
    
    assert fresh_topic is None


def test_requires_a_user_with_moderator_to_delete_topic(application, forum, topic, user):
    application.config['WTF_CSRF_ENABLED'] = False

    with application.test_client() as test_client:
        manage_forum_url = url_for("forum.manage_forum", forum_id=forum.id)

        login_response = test_client.post(url_for('auth.login'), data={'login': user.username,
                                        'password': 'test'},
                        follow_redirects=True)
        
        assert login_response.status_code == 200
        
        response = test_client.post(manage_forum_url, data = {
            "rowid": topic.id,
             "delete": True,
        }, follow_redirects=True)

        assert response.status_code == 200

    fresh_topic = Topic.query.filter_by(id=topic.id).first()
    
    assert fresh_topic is not None