import pytest

from flaskbb.forum.topic_manager import TopicManager
from flaskbb.forum.models import Topic

class TestTopicManager(object):

    def test_set_lock_state(self,topic):
        subject = TopicManager([topic])
        result = subject.set_lock_state(True)

        assert result == 1
        assert topic.locked == True

    def test_set_lock_state_doesnot_modify_topic_with_desired_state(self, topic_locked):
        subject = TopicManager([topic_locked])
        result = subject.set_lock_state(True)

        assert result == 0

    def test_set_lock_state_handles_each_topic(self, topic, topic_locked):
        subject = TopicManager([topic_locked, topic])
        result = subject.set_lock_state(False)

        assert result == 1

    def test_set_imporant_state(self, topic):
        subject = TopicManager([topic])
        result = subject.set_important_state(True)

        assert result == 1
        assert topic.important == True

    def test_set_imporant_state_handles_each_topic(self, topic, topic_important):
        subject = TopicManager([topic_important, topic])
        result = subject.set_important_state(False)

        assert result == 1
        assert topic_important.important == False

    def test_delete_topics(self, topic, topic_important):
        subject = TopicManager([topic_important, topic])
        result = subject.delete_topics()

        assert result == 2
        assert Topic.query.filter_by(id=topic.id).first() is None
        assert Topic.query.filter_by(id=topic_important.id).first() is None

    def test_set_hidden_state_to_false(self, user, topic, topic_important, topic_hidden):
        subject = TopicManager([topic_important, topic, topic_hidden])
        result = subject.set_hidden_state(user, False)

        assert result == 1
        assert topic_hidden.hidden == False

    def test_set_hidden_state_to_true(self, user, topic, topic_important, topic_hidden):
        subject = TopicManager([topic_important, topic, topic_hidden])
        result = subject.set_hidden_state(user, True)

        assert result == 2
        assert topic.hidden == True
        assert topic_important.hidden == True
