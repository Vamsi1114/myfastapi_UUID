from app import schemas
import pytest


#test create user
def test_create_user(authorized_email):
   user_data =  {"first_name" : "vamsi",  "last_name" : "chinni", "password": "password", "date_of_birth" : "1999-04-22", "phone_number" : "89858738738"}
   res = authorized_email.post("/user", json= user_data)
   new_user = schemas.UserOut(**res.json())
   assert res.status_code == 201
   assert new_user.first_name == "vamsi"

#test unauthorized user to create account
def test_unauthorized_create_user(client):
   user_data =  {"first_name" : "krishna", "last_name" : "vamsi", "password": "password", "date_of_birth" : "1999-11-14", "phone_number" : "96758738738"}
   res = client.post("/user", json= user_data)
   assert res.status_code == 401

# already token is used once
def test_expired_token(authorized_email, test_user):
   res = authorized_email.post("/user", json= test_user)
   data = res.json()
   assert data['detail'] == 'Token already used'
   assert res.status_code == 403

#login test
def test_login_user(client, test_user):
    res = client.post("/login", data = {"username":test_user['email'], "password":test_user['password']})
    login_res = schemas.Token(**res.json())
    assert login_res.token_type == "bearer"
    assert res.status_code == 200

@pytest.mark.parametrize("email , password , status_code",[('vamsi12@gmailcom','password123',403), ('vamsi@gmailcom','password123',403), ('vamsi@gmailcom','password23',403), ( None,'password23',422), ('vamsi@gmailcom',None,422)])
#test incorrect login details
def test_incorrect_login(client, email, password, status_code):
    res = client.post("/login", data = {"username": email, "password": password})
    assert res.status_code == status_code   

#test change_password
def test_change_password(authorized_client):
   res = authorized_client.put("/change_password", json = {"old_password": "password", "new_password": "password123"})
   assert res.status_code == 200

#test invalid credentials to change password
def test_change_password_invalid_credentials(authorized_client):
   res = authorized_client.put("/change_password", json = {"old_password": "password1", "new_password": "password123"})
   assert res.status_code == 403
   
#test unauthorized client to change password
def test_unauthorized_user(client):
   res = client.put("/change_password", json = {"old_password": "password", "new_password": "password123"})
   assert res.status_code == 401

#test forgot password
def test_forgot_password(client, test_user):
   res = client.post("/forgot_password", json= {"email": test_user["email"]})
   token = schemas.Token(**res.json())
   assert token.token_type == "bearer"
   assert res.status_code == 200 

#test forgot password with email not existed 
def test_user_forgot_password_email_not_existed(client):
   res = client.post("/forgot_password", json= {"email": "sachin@gmail.com"})
   assert res.status_code == 403 

# test authorized user to set password
def test_authorized_user_set_password(authorized_user):
   res = authorized_user.put("/set_password", json= { "password":"password"})
   data = res.json()
   assert res.status_code == 200

#test unauthorized user to set password
def test_unauthorized_user_set_password(client, test_user):
   client.headers["authorization"] = f"Bearer {'None'}"
   res = client.put("/set_password", json= { "password":test_user["password"]})
   assert res.status_code == 401 

#test logout user
def test_logout_user(authorized_client):
   res = authorized_client.put("/logout")
   assert res.json() == {"Message" : "You have been logged out."}
   assert res.status_code == 200 

#test unauthorized user to logout
def test_unauthorized_user_logout(client):
   res = client.put("/logout")
   assert res.status_code == 401 

#test authorized user print userdetails
def test_authorized_user_print_pdf(authorized_client):
   res = authorized_client.post("/print")
   data = res.json()
   assert data["filename"] == "example.pdf"
   assert data["file_path"] == "C:\\Users\\CS0142302.CSVIZAG\\Documents\\MyfastAPI\\example.pdf"
   assert res.status_code == 200

# test unauthorized user to print userdetails 
def test_unauthorized_user_print_pdf(client):
   res = client.post("/print")
   assert res.status_code == 401