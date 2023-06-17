import pytest

pytestmark = pytest.mark.usefixtures("post_request_context", "default_settings")
from flaskbb.forum import forms
from flaskbb.forum.models import Forum
from flaskbb.user.models import Group

###################################################################
# CoRise TODO: add unit tests below that test the functionality of
# the `SpecialTopicForm`

from flaskbb.forum.forms import SpecialTopicForm

from werkzeug.datastructures import MultiDict

class TestSpecialTopicForm(object):
    
    def test_special_topic_form(self):
        """Tests addition of 'Special Topic' to title and content."""
        formdata = MultiDict({"title": "abc", 
                    "content": "xyz", })

        stf = SpecialTopicForm(formdata=formdata)
        pattern = "Special Topic"

        # remember: title is a StringField object
        assert stf.title.data   == pattern + ': abc'
        assert stf.content.data == pattern + ': xyz'

class TestSpecialTopicForm2(object):

    def test_submit_special_topic_created_with_prefix(self, Fred, database, category):
        with database.session.no_autoflush:
            forum = Forum(title="no guest", category=category)
            forum.groups = Group.query.filter(Group.guest == False).all()
            forum.save()
        data = MultiDict(
            {
                "submit": True,
                "title": "Tests topic",
                "content": "nothing special",
            }
        )
        form = forms.SpecialTopicForm(formdata=data, meta={"csrf": False})
        topic = form.save(Fred, forum)
        assert topic.title == "Special Topic: Tests topic", f"{topic.title}"
        assert topic.id 
        assert topic.forum_id == forum.id
        assert topic.posts[0].content == "Special Topic: nothing special"

###################################################################