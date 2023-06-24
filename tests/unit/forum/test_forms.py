from flaskbb.forum import forms
import pytest
from werkzeug.datastructures import MultiDict

pytestmark = pytest.mark.usefixtures("post_request_context", "default_settings")

class TestSpecialTopicForm(object):
    def test_special_topic_title(self):
        data = MultiDict({"title": "my topic", "content": "my content", "track_topic":False})
        form = forms.SpecialTopicForm(formdata=data)

        assert form.data.get("title") == "Special Topic: my topic"

    def test_special_topic_content(self):
        data = MultiDict({"title": "my topic", "content": "my content", "track_topic":False})
        form = forms.SpecialTopicForm(formdata=data)

        assert form.data.get("content") == "Special Topic: my content"

        
