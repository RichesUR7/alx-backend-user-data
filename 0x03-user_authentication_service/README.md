# 0x03. User Authentication Service

## Description

This project focuses on creating a user authentication service, implementing the core functionalities necessary for managing user accounts securely. The service includes features for user registration, login, and session management, ensuring that sensitive data is handled safely.

## Directory Structure

```
0x03-user-authentication-service/
├── app.py             # Main application file for running the authentication service
├── auth.py            # Contains authentication logic and user management functions
├── database.py        # Contains database connection and user data management
├── models.py          # Defines data models for user accounts
├── utils.py           # Utility functions used across the service
├── README.md          # This file
└── test.py            # Contains test cases for validating the authentication service
```

## Requirements

- Python 3.x
- Flask (or other web framework if specified)
- SQLAlchemy (or other ORM if specified)
- pytest (for testing)

## Functionality

### User Registration

**Endpoint:** `/register`

**Method:** POST

**Description:** Registers a new user with a username and password. Passwords should be hashed before storing.

**Request Body:**
```json
{
  "username": "string",
  "password": "string"
}
```

**Response:**
- Success: HTTP 201 Created
- Error: HTTP 400 Bad Request

### User Login

**Endpoint:** `/login`

**Method:** POST

**Description:** Authenticates a user with username and password. Returns a session token upon successful authentication.

**Request Body:**
```json
{
  "username": "string",
  "password": "string"
}
```

**Response:**
- Success: HTTP 200 OK with session token
- Error: HTTP 401 Unauthorized

### Session Management

**Endpoint:** `/logout`

**Method:** POST

**Description:** Logs out a user by invalidating the session token.

**Request Header:**
```
Authorization: Bearer <session_token>
```

**Response:**
- Success: HTTP 200 OK
- Error: HTTP 401 Unauthorized

## Running the Service

To start the authentication service, run the `app.py` script:

```bash
python app.py
```

Ensure that you have set up your environment variables and database configuration before starting the service.

## Running the Tests

To ensure the authentication service works as expected, run the `test.py` script:

```bash
pytest test.py
```

This script includes various test cases to validate registration, login, and session management functionalities.

## Usage

To interact with the authentication service, you can use tools like `curl` or Postman, or integrate it into your application via HTTP requests.

**Example Registration Request:**

```bash
curl -X POST http://localhost:5000/register -H "Content-Type: application/json" -d '{"username": "testuser", "password": "testpassword"}'
```

**Example Login Request:**

```bash
curl -X POST http://localhost:5000/login -H "Content-Type: application/json" -d '{"username": "testuser", "password": "testpassword"}'
```

**Example Logout Request:**

```bash
curl -X POST http://localhost:5000/logout -H "Authorization: Bearer <session_token>"
```

## Contributing

Contributions to enhance the functionality or fix issues are welcome. Please submit pull requests or open issues to discuss improvements.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
