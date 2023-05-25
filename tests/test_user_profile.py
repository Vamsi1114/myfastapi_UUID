from app import schemas
import pytest

#test create user profile
def test_user_profile(authorized_client):
   res = authorized_client.post("/profile", json = {"bio": "cool", "image_url": "img.jpg", "gender": "male", "address":"goa"})
   assert res.status_code == 201


#test user with profile already existed
def test_existed_user_profile(authorized_client, user_profile):
   res = authorized_client.post("/profile", json = {"bio": "cool", "image_url": "img.jpg", "gender": "male", "address":"goa"})
   assert res.status_code == 409

#test unauthorized user to create user profile
def test_unauthorized_user_create_profile(client):
    res = client.post("/profile", json = {"bio": "cool", "image_url": "img.jpg", "gender": "male", "address":"goa"})
    assert res.status_code == 401

#test edit user details
def test_edit_user_details(authorized_client, user_profile):
   user_data = {
    "bio": "movie",
    "image_url": "img.png",
    "gender": "male",
    "address":"mvp, vizag"
}
   res = authorized_client.put("/edit_profile", json = user_data)
   assert res.status_code == 200

#test unauthorized user to edit user profile
def test_unauthorized_user_edit_profile(client):
    user_data = {
    "bio": "movie",
    "image_url": "img.png",
    "gender": "male",
    "address":"mvp, vizag"}
    res = client.post("/profile", json = user_data)
    assert res.status_code == 401

