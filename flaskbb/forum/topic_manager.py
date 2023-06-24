# CoRise TODO: implement a class for managing topics with in a forum
from flaskbb.utils.helpers import (FlashAndRedirect, do_topic_action,
                                   format_quote, get_online_users, real,
                                   register_view, render_template, time_diff,
                                   time_utcnow)

from flaskbb.utils.requirements import (CanAccessForum, CanDeletePost,
                                        CanDeleteTopic, CanEditPost,
                                        CanPostReply, CanPostTopic, Has,
                                        IsAtleastModeratorInForum)
from flask_allows import And, Permission
from flask import (Blueprint, abort, current_app, flash, redirect, request,
                   url_for)

from flask_babelplus import gettext as _

# this mapping is used to set flags before login and response tests, 
# then test if the flag changed
# if an action is not in this map, only login and response tests happen
actions_map = { # action, reverse, topic, flag to test
               "lock":("locked", False, "locked",False), 
               "unlock":("locked", True, "locked",True), 
               "highlight":("important", False, "important",False),
               "trivialize":("important", True, "important",True),
               "delete":("delete", False, "delete", None),
               "unhide":("unhide", False, "hidden", None),
               "hide":("hide", False, "hidden", None),}


class TopicManager:
    def __init__(self) -> None:
        pass

    @staticmethod
    def get_changed(topics, action, msg):
        """ This comment comes from helpers.do_topic_action
            whose logic I'm bringing in here
            Executes a specific action for topics. 
            Returns a list with the modified topic objects.

        :param topics: A iterable with ``Topic`` objects.
        :param user: The user object which wants to perform the action.
        :param action: One of the following actions: locked, important and delete.
        :param reverse: If the action should be done in a reversed way.
                        For example, to unlock a topic, ``reverse`` should be
                        set to ``True``.
        """
        # do not use _ otherwise you overwrite the imported method '_'
        act, reverse, attribute, flag = actions_map.get(action)

        # logic from helpers.do_topic_action
        modified_topics = 0
        if action not in {"delete", "hide", "unhide"}:
            for topic in topics:
                if getattr(topic, attribute) and not reverse:
                    continue

                setattr(topic, attribute, not reverse)
                modified_topics += 1
                topic.save()

        if msg is not None:
            flash(_(f"%(count)s {msg}.", count=modified_topics), "success")
        
        return modified_topics
    

    def lock(self,topics,msg=None):
        return self.get_changed(topics, "lock", msg)
    

    def unlock(self,topics,msg=None):
        return self.get_changed(topics, "unlock", msg)


    def highlight(self,topics, msg=None):
        return self.get_changed(topics, "highlight", msg)


    def trivialize(self,topics, msg=None):
        return self.get_changed(topics, "trivialize", msg)


    def delete(self,topics, msg=None):
        if not Permission(CanDeleteTopic):
            flash(
                _("You do not have the permissions to delete these topics."),
                "danger",
            )
            return False
        else:
            modified_topics = 0 
            for topic in topics:
                modified_topics += 1
                topic.delete()
            flash(_(f"%(count)s {msg}.", count=modified_topics), "success")
            return modified_topics
    
    
    def unhide(self,topics, msg=None):
        if not Permission(Has("makehidden")):
            flash(
                _("You do not have the permissions to unhide these topics."),
                "danger",
            )
            return False
        else:
            modified_topics = 0
            for topic in topics:
                if not topic.hidden:
                    continue
                modified_topics += 1
                topic.unhide()

            flash(_(f"%(count)s {msg}.", count=modified_topics), "success")
            return modified_topics
        
    def hide(self,topics, user, msg=None):
        if not Permission(Has("makehidden")):
            flash(
                _("You do not have the permissions to hide these topics."),
                "danger",
            )
            return False
        else:
            modified_topics = 0
            for topic in topics:
                if topic.hidden:
                    continue
                modified_topics += 1
                topic.hide(user)

            flash(_(f"%(count)s {msg}.", count=modified_topics), "success")
            return modified_topics

    