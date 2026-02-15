import json
from flask_jwt_extended import create_access_token

# --------------------------------------------------------------------------
# REGISTER TESTS
# --------------------------------------------------------------------------
def test_register_success(client):
    """Test that a user can register """
    payload = {
        "email": "test@example.com",
        "password": "password123"
    }
    response = client.post('/auth/register', json=payload)
    
    assert response.status_code == 201
    assert response.get_json()['msg'] == "User created successfully"

def test_register_missing_data(client):
    """Test that registration fails if fields are missing."""
    # Missing password
    response = client.post('/auth/register', json={"email": "test@example.com"})
    assert response.status_code == 400
    assert "Email and password are required" in response.get_json()['msg']

def test_register_duplicate_user(client):
    """Test that you cannot register the same email twice."""
    payload = {"email": "duplicate@example.com", "password": "123"}
    
    # First registration
    client.post('/auth/register', json=payload)
    
    # Second registration
    response = client.post('/auth/register', json=payload)
    
    assert response.status_code == 400
    assert response.get_json()['msg'] == "User already exists"


# --------------------------------------------------------------------------
# LOGIN TESTS
# --------------------------------------------------------------------------

def test_login_success(client):
    """Test valid login returns a token."""
    # Create user 
    client.post('/auth/register', json={"email": "login@test.com", "password": "securepass"})
    
    # Try logging in
    response = client.post('/auth/login', json={"email": "login@test.com", "password": "securepass"})
    
    assert response.status_code == 200
    data = response.get_json()
    assert "access_token" in data
    assert len(data['access_token']) > 0

def test_login_failure(client):
    """Test login with wrong password."""
    # Create user
    client.post('/auth/register', json={"email": "fail@test.com", "password": "securepass"})
    
    # Wrong password
    response = client.post('/auth/login', json={"email": "fail@test.com", "password": "wrongpassword"})
    
    assert response.status_code == 401
    assert response.get_json()['msg'] == "Bad email or password"

def test_login_nonexistent_user(client):
    """Test login for a user that doesn't exist."""
    response = client.post('/auth/login', json={"email": "ghost@test.com", "password": "123"})
    assert response.status_code == 401


# --------------------------------------------------------------------------
# PROTECTED ROUTE TESTS
# --------------------------------------------------------------------------

def test_protected_route_access(client):
    """Test accessing a protected route with a valid token."""
    # Register
    client.post('/auth/register', json={"email": "protect@test.com", "password": "123"})
    
    # Login and get token
    login_resp = client.post('/auth/login', json={"email": "protect@test.com", "password": "123"})
    token = login_resp.get_json()['access_token']
    
    headers = {'Authorization': f'Bearer {token}'}
    response = client.get('/auth/protected', headers=headers)
    
    assert response.status_code == 200
    assert response.get_json()['logged_in_as'] == "protect@test.com"

def test_protected_route_no_token(client):
    """Test accessing protected route without a token fails."""
    response = client.get('/auth/protected')
    
    assert response.status_code == 401

def test_protected_route_invalid_token(client):
    """Test accessing protected route with a fake token."""
    headers = {'Authorization': 'Bearer FAKE_TOKEN_123'}
    response = client.get('/auth/protected', headers=headers)
    
    # JWT Extended usually returns 422 (Unprocessable) for malformed tokens
    # or 401 if signature is invalid.
    assert response.status_code in [401, 422]

# this test is more for completition
def test_protected_route_user_doesnt_exist(client, app):
    """
    Logic: The token is valid (correct signature), but the User ID 
    inside it (e.g., 9999) does not exist in the DB.
    Covers line: if not user: return ... 404
    """
    # 1. Generate a valid token for a non-existent user ID
    # We need the app context to access the JWT configuration
    with app.app_context():
        # '9999' is an ID that we know doesn't exist in the empty test DB
        fake_token = create_access_token(identity="9999")

    # 2. Try to access the protected route with this token
    headers = {'Authorization': f'Bearer {fake_token}'}
    response = client.get('/auth/protected', headers=headers)

    # 3. Assertions
    assert response.status_code == 404
    assert response.get_json()['msg'] == "User not found"