
from flask import url_for
from flaskbb.forum.models import Topic

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