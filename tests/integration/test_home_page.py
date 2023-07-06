def test_index_route(application, default_settings, default_groups, default_translations):
    with application.test_client() as test_client:
        response = test_client.get('/')
        assert response.status_code == 200
        assert b"Forum" in response.data
        assert b"Portal" in response.data
