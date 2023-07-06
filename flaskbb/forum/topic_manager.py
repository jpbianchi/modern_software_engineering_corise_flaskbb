"""
A class for managing topic state.

It operates on a list of topics and makes sure that the desired state is the actual state of the topic
"""
class TopicManager(object):
    def __init__(self, topics) -> None:
        self.__topics = topics

    def set_lock_state(self, desired_state):
        return self.__set_field_state('locked',desired_state)

    def set_important_state(self, desired_state):
        return self.__set_field_state('important', desired_state)

    def delete_topics(self):
        modified_topics = 0
        for topic in self.__topics:
            topic.delete()
            modified_topics+=1

        return modified_topics

    def set_hidden_state(self, user, desired_state):
        modified_topics = 0
        for topic in self .__topics:
            if topic.hidden != desired_state:
                if topic.hidden:
                    topic.unhide()
                else:
                    topic.hide(user)
                topic.save()
                modified_topics+=1

        return modified_topics

    # Sets the specified field to the desired state
    def __set_field_state(self, field, desired_state):
        modified_topics = 0
        for topic in self.__topics:
            if getattr(topic, field) != desired_state:
                setattr(topic, field, desired_state)
                topic.save()
                modified_topics+=1

        return modified_topics
