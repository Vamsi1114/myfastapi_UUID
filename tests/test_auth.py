from app import schemas
import pytest


def test_root(client):
    res = client.get("/")
    print(res.json())
    assert res.json().get('message') == 'Hello World'
    assert res.status_code == 200

@pytest.mark.parametrize("email , status_code", [('vamsi@gmail.com', 200),('vamsi123@gmail.com', 200),('vamsi123@gmail.com', 200)])
# email test
def test_email(client, email , status_code):
 res = client.post("/email_verify", json= {"email": email})
 token = schemas.Token(**res.json())
 assert res.status_code == status_code
 assert token.token_type == "bearer"

#test the user already existed  email
def test_existed_user_email(client, test_user):
 res = client.post("/email_verify", json= {"email": "vamsi@gmail.com"})
 assert res.status_code == 409