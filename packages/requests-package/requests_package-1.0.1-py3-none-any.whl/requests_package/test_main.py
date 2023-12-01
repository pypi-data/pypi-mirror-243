from unittest.mock import Mock, patch
from requests_package.main import RetryRequest

@patch("requests_package.main.requests.get")
def test_get_504(mock_get: Mock):
    mock_get.return_value.status_code = 504
    response = RetryRequest(sleep_time_sec=0, retries=10).get("url", params="mock_params", headers="mock_headers")
    assert mock_get.call_count == 10
    assert response.status_code == 504
    mock_get.assert_called_with(url="url", params="mock_params", headers="mock_headers")

@patch("requests_package.main.requests.get")
def test_get_429(mock_get: Mock):
    mock_get.return_value.status_code = 429
    response = RetryRequest(sleep_time_sec=0, retries=10).get("url", params="mock_params", headers="mock_headers")
    assert mock_get.call_count == 10
    assert response.status_code == 429
    mock_get.assert_called_with(url="url", params="mock_params", headers="mock_headers")

@patch("requests_package.main.requests.get")
def test_get_200(mock_get: Mock):
    mock_get.return_value.status_code = 200
    response = RetryRequest(sleep_time_sec=0, retries=10).get("url", params="mock_params", headers="mock_headers")
    mock_get.assert_called_once_with(url="url", params="mock_params", headers="mock_headers")
    assert response.status_code == 200

@patch("requests_package.main.requests.post")
def test_post_504(mock_post: Mock):
    mock_post.return_value.status_code = 504
    response = RetryRequest(sleep_time_sec=0, retries=10).post("url", json="json_mock", params="mock_params", headers="mock_headers")
    assert mock_post.call_count == 10
    assert response.status_code == 504
    mock_post.assert_called_with(json="json_mock", url="url", params="mock_params", headers="mock_headers")

@patch("requests_package.main.requests.post")
def test_post_429(mock_post: Mock):
    mock_post.return_value.status_code = 429
    response = RetryRequest(sleep_time_sec=0, retries=10).post("url", json="json_mock", params="mock_params", headers="mock_headers")
    assert mock_post.call_count == 10
    assert response.status_code == 429
    mock_post.assert_called_with(json="json_mock", url="url", params="mock_params", headers="mock_headers")

@patch("requests_package.main.requests.post")
def test_post_200(mock_post: Mock):
    mock_post.return_value.status_code = 200
    response = RetryRequest(sleep_time_sec=0, retries=10).post("url", json="json_mock", params="mock_params", headers="mock_headers")
    mock_post.assert_called_once_with(json="json_mock", url="url", params="mock_params", headers="mock_headers")
    assert response.status_code == 200

@patch("requests_package.main.requests.put")
def test_put_504(mock_put: Mock):
    mock_put.return_value.status_code = 504
    response = RetryRequest(sleep_time_sec=0, retries=10).put("url", json="json_mock", params="mock_params", headers="mock_headers")
    assert mock_put.call_count == 10
    assert response.status_code == 504
    mock_put.assert_called_with(json="json_mock", url="url", params="mock_params", headers="mock_headers")

@patch("requests_package.main.requests.put")
def test_put_429(mock_put: Mock):
    mock_put.return_value.status_code = 429
    response = RetryRequest(sleep_time_sec=0, retries=10).put("url", json="json_mock", params="mock_params", headers="mock_headers")
    assert mock_put.call_count == 10
    assert response.status_code == 429
    mock_put.assert_called_with(json="json_mock", url="url", params="mock_params", headers="mock_headers")

@patch("requests_package.main.requests.put")
def test_put_200(mock_put: Mock):
    mock_put.return_value.status_code = 200
    response = RetryRequest(sleep_time_sec=0, retries=10).put("url", json="json_mock", params="mock_params", headers="mock_headers")
    mock_put.assert_called_once_with(json="json_mock", url="url", params="mock_params", headers="mock_headers")
    assert response.status_code == 200

@patch("requests_package.main.requests.delete")
def test_delete_504(mock_delete: Mock):
    mock_delete.return_value.status_code = 504
    response = RetryRequest(sleep_time_sec=0, retries=10).delete("url", json="json_mock", params="mock_params", headers="mock_headers")
    assert mock_delete.call_count == 10
    assert response.status_code == 504
    mock_delete.assert_called_with(json="json_mock", url="url", params="mock_params", headers="mock_headers")

@patch("requests_package.main.requests.delete")
def test_delete_429(mock_delete: Mock):
    mock_delete.return_value.status_code = 429
    response = RetryRequest(sleep_time_sec=0, retries=10).delete("url", json="json_mock", params="mock_params", headers="mock_headers")
    assert mock_delete.call_count == 10
    assert response.status_code == 429
    mock_delete.assert_called_with(json="json_mock", url="url", params="mock_params", headers="mock_headers")

@patch("requests_package.main.requests.delete")
def test_delete_200(mock_delete: Mock):
    mock_delete.return_value.status_code = 200
    response = RetryRequest(sleep_time_sec=0, retries=10).delete("url", json="json_mock", params="mock_params", headers="mock_headers")
    mock_delete.assert_called_once_with(json="json_mock", url="url", params="mock_params", headers="mock_headers")
    assert response.status_code == 200
