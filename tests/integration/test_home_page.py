###################################################################
# CoRise TODO: add an integration test that uses the test client to
# load the home page ('/'). Make sure the response code is 200 and
# that the response data contains something you expect to see on the
# home page.
#
# Hint: you can get the test client by calling `application.test_client()`
# when using the application test fixture.
from flaskbb.utils.helpers import to_bytes

def test_home_page(application, default_settings, default_groups, translations):
    # the parameters are the fixtures we need for this test

    with application.test_client() as client:
        response = client.get('/')
        # print('THIS IS RESPONSE.DATA  \n',response.data)  
        # use pytest -s to see this print and disable '--capture  ' in setup.cfg

        assert response.status_code == 200
        assert to_bytes("A lightweight forum software in Flask") in response.data, f"Wrong response data {response.data}"
        # one can see the homepage at https://forums.flaskbb.org

###################################################################