# CoRise TODO: add unit tests for topic manager

from flaskbb.forum.models import Topic
from flaskbb.forum.topic_manager import TopicManager

class TestTopicManager(object):

    def test_lock(self, topic):
        assert topic.locked is False

        TopicManager().lock(topics=[topic])

        fresh_topic = Topic.query.filter_by(id=topic.id).first()
        assert fresh_topic.locked is True


    def test_unlock(self, topic):
        setattr(topic, "locked", True)
        assert topic.locked is True

        TopicManager().unlock(topics=[topic])

        fresh_topic = Topic.query.filter_by(id=topic.id).first()
        assert fresh_topic.locked is False

    def test_highlight(self, topic):
        assert topic.important is False

        TopicManager().highlight(topics=[topic])

        fresh_topic = Topic.query.filter_by(id=topic.id).first()
        assert fresh_topic.important is True

    def test_trivialize(self, topic):
        setattr(topic, "important", True)
        assert topic.important is True

        TopicManager().trivialize(topics=[topic])

        fresh_topic = Topic.query.filter_by(id=topic.id).first()
        assert fresh_topic.important is False

    # def test_delete(self, topic):
    #     TopicManager().delete(topics=[topic])

    #     fresh_topic = Topic.query.filter_by(id=topic.id).first()
    #     assert fresh_topic is None

    # def test_hide(self, topic, super_moderator_user):
    #     assert topic.hidden is False

    #     TopicManager().hide(topics=[topic], user=super_moderator_user)

    #     fresh_topic = Topic.query.filter_by(id=topic.id).first()
    #     assert fresh_topic.hidden is True


    # def test_unhide_cb(self, topic):
    #     setattr(topic, "hidden", True)
    #     assert topic.hidden is True

    #     TopicManager().unhide(topics=[topic])

    #     fresh_topic = Topic.query.filter_by(id=topic.id).first()
    #     assert fresh_topic.hidden is False

