import pytest

pytestmark = pytest.mark.usefixtures("post_request_context", "default_settings")

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
                    #"track_topic":False}

        stf = SpecialTopicForm(formdata=formdata)
        pattern = "Special Topic"
        N = len(pattern)  

        # remember: title is a StringField object
        assert stf.title.data   == pattern + ': abc'
        assert stf.content.data == pattern + ': xyz'

###################################################################