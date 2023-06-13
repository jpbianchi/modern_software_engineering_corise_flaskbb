###################################################################
# CoRise TODO: add an integration test that uses the test client to
# load the home page ('/'). Make sure the response code is 200 and
# that the response data contains something you expect to see on the
# home page.
#
# Hint: you can get the test client by calling `application.test_client()`
# when using the application test fixture.

def test_home_page(application, default_settings, default_groups, translations):
    # the parameters are the fixtures we need for this test

    with application.test_client() as client:
        response = client.get('/')
        print('THIS IS RESPONSE.DATA  '*5, '\n'*15,response.data, '\n'*15)  # use pytest -s to see this print

        assert response.status_code == 200
        assert b"Forum" in response.data
        # assert False, f"{response.data}" # works but pytest shows a small part

###################################################################