import pytest

def test_invalid_content_type(client):
    """잘못된 Content-Type 테스트"""
    response = client.post(
        "/correct",
        headers={"Content-Type": "text/plain"},
        content=b"invalid data",
    )
    
    assert response.status_code == 415