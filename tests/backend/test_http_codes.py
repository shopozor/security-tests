import requests

from urllib.parse import urljoin


def test_only_post_works(graphql_endpoint):
    res = requests.get(graphql_endpoint)
    assert res.status_code == 405

    res = requests.post(graphql_endpoint)
    assert res.status_code == 400

    res = requests.put(graphql_endpoint)
    assert res.status_code == 405

    res = requests.patch(graphql_endpoint)
    assert res.status_code == 405

    res = requests.delete(graphql_endpoint)
    assert res.status_code == 405

    res = requests.head(graphql_endpoint)
    assert res.status_code == 405

    # TODO find out how to test the other verbs

    #res = requests.copy(graphql_endpoint)
    #assert res.status_code == 405
    #res = requests.link(graphql_endpoint)
    #assert res.status_code == 405
    #res = requests.unlink(graphql_endpoint)
    #assert res.status_code == 405
    #res = requests.purge(graphql_endpoint)
    #assert res.status_code == 405
    #res = requests.trace(graphql_endpoint)
    #assert res.status_code == 405
    #res = requests.lock(graphql_endpoint)
    #assert res.status_code == 405
    #res = requests.unlock(graphql_endpoint)
    #assert res.status_code == 405
    #res = requests.propfind(graphql_endpoint)
    #assert res.status_code == 405
    #res = requests.view(graphql_endpoint)
    #assert res.status_code == 405
