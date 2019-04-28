def test_hello(server):
    server = server
    response = server.request('get', url='http://127.0.0.1:5000/')
    print(response)
    assert response
