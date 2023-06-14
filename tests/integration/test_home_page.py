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
        # I tried to print response.data to create more tests but pytest -s
        # would not unblock the prints for some reason
        # maybe I come back later to this when I run the app and I can see the homepage

        assert response.status_code == 200
        assert b"Forum" in response.data

        # I tried with assert False since the error message is displayed but
        # pytest shows only the beginning of response.data
        # assert False, f"{response.data}" 

###################################################################