# charmed-backend
backend for charmed.lol


## Users

### POST /login
Authenticates a user and returns token.

**request:**
```json
method: POST
url: http://127.0.0.1:5000/users/login
headers:
  Content-Type: application/json
body:
{
    "email": "john@doe.com",
    "password": "password"
}
```

**response:**
```json
{
    "message": "Hello There John",
    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3NjI2NjkzMDcsImlhdCI6MTc2MjY2NTcwNywic3ViIjoiMSJ9.yJc7L8GBR9i-tu5mgaroSfeSeea_Q5jMOyZ8EqGpZBs"
}
```

### GET /users/profile
Retrieves the profile of the authenticated user.

**request:**
```json
method: GET
url: http://127.0.0.1:5000/users/profile
headers:
  Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3NjI2NzA0MDcsImlhdCI6MTc2MjY2NjgwNywic3ViIjoiMSJ9.d3QaYMj-MQZ9WL-cQZut3RwBgAiMMmSuXoNnFWKwd7c
```

**response:**
```json
{
    "bio": "Competitive gamer and streamer with a passion for RPGs and esports.",
    "birthdate": "1996-04-15",
    "city": "Los Angeles",
    "country": "United States",
    "created_at": "2025-11-08T22:21:12.248813",
    "email": "john@doe.com",
    "first_name": "John",
    "gender": "Male",
    "id": 1,
    "in_game_name": "ShadowStrike99",
    "last_name": "Doe",
    "password": "scrypt:32768:8:1$UcT3XbDT5J5ne15p$d57ee55a7d5026fbab30e6365a0db8aeb29205d5649e84c4473914e8b031b545fc505292e36c4cf8e8093df0148fc434882333bcbeeb79173695a5b8f4e5e324",
    "role": "user",
    "state": "California",
    "tagline": "Leveling up every day."
}
```

### POST /users
Creates a new user.

**request:**
```json
method: POST
url: http://127.0.0.1:5000/users
headers:
  Content-Type: application/json
body:
 {
    "bio": "Competitive gamer and streamer with a passion for RPGs and esports.",
    "birthdate": "1996-04-15",
    "city": "Los Angeles",
    "country": "United States",
    "email": "johndoe@example.com",
    "first_name": "John",
    "gender": "Male",
    "in_game_name": "ShadowStrike99",
    "last_name": "Doe",
    "password": "P@ssw0rd123!",
    "state": "California",
    "tagline": "Leveling up every day."
}
```

**response:**
```json
{
    "bio": "Competitive gamer and streamer with a passion for RPGs and esports.",
    "birthdate": "1996-04-15",
    "city": "Los Angeles",
    "country": "United States",
    "created_at": "2025-11-08T22:03:21.968521",
    "email": "johndoe@example.com",
    "first_name": "John",
    "gender": "Male",
    "id": 1,
    "in_game_name": "ShadowStrike99",
    "last_name": "Doe",
    "password": "scrypt:32768:8:1$yADGUrEwFA8xO86o$984513cd9cbfc0ff99156009ceea095d799ad5372ac94e3977b5da64fece10787558cd4281acdc5f0a3f1e1ccfe1dfe231f5366356e3d27548ac4ae7628406a4",
    "role": "user",
    "state": "California",
    "tagline": "Leveling up every day."
}
```


### GET /users
Retrieves all users.

**request:**
```json
method: GET
url: http://127.0.0.1:5000/users
```

**response:**
```json
[
    {
        "bio": "Competitive gamer and streamer with a passion for RPGs and esports.",
        "birthdate": "1996-04-15",
        "city": "Los Angeles",
        "country": "United States",
        "created_at": "2025-11-08T22:12:00.824016",
        "email": "lux@demacia.com",
        "first_name": "John",
        "gender": "Male",
        "id": 1,
        "in_game_name": "ShadowStrike99",
        "last_name": "Doe",
        "password": "scrypt:32768:8:1$ojGpo848Wh3c0wHx$3b1389d8b03df561c50aeed0a65e1978caa534cef126bfe782de32b487cbd2477951a8350ac27c2b3f0128bfbc752db8df26d24e97b1fdcaccd375ff0315e50e",
        "role": "user",
        "state": "California",
        "tagline": "Leveling up every day."
    },
    ...
]
```

### GET /users/<id>
Retrieves a user by ID.

**request:**
```json
method: GET
url: http://127.0.0.1:5000/users/1
```

**response:**
```json
{
    "bio": "Competitive gamer and streamer with a passion for RPGs and esports.",
    "birthdate": "1996-04-15",
    "city": "Los Angeles",
    "country": "United States",
    "created_at": "2025-11-08T22:21:12.248813",
    "email": "john@doe.com",
    "first_name": "John",
    "gender": "Male",
    "id": 1,
    "in_game_name": "ShadowStrike99",
    "last_name": "Doe",
    "password": "scrypt:32768:8:1$UcT3XbDT5J5ne15p$d57ee55a7d5026fbab30e6365a0db8aeb29205d5649e84c4473914e8b031b545fc505292e36c4cf8e8093df0148fc434882333bcbeeb79173695a5b8f4e5e324",
    "role": "user",
    "state": "California",
    "tagline": "Leveling up every day."
}
```


### PUT /users/<id>
Updates a user by ID.

request:
```json
method: PUT
url: http://127.0.0.1:5000/users/1
authorization: Bearer <token>
headers:
  Content-Type: application/json
body:
 {
    "bio": "Competitive gamer and streamer with a passion for RPGs and esports.",
    "birthdate": "1996-04-15",
    "city": "Los Angeles",
    "country": "United States",
    "email": "johndoe@example.com",
    "first_name": "John",
    "gender": "Male",
    "in_game_name": "ShadowStrike99",
    "last_name": "Doe",
    "password": "P@ssw0rd123!",
    "state": "California",
    "tagline": "Leveling up every day."
}
```

response:
```json
{
    "bio": "Competitive gamer and streamer with a passion for RPGs and esports.",
    "birthdate": "1996-04-15",
    "city": "Los Angeles",
    "country": "United States",
    "created_at": "2025-11-08T22:03:21.968521",
    "email": "johndoe@example.com",
    "first_name": "John",
    "gender": "Male",
    "id": 1,
    "in_game_name": "ShadowStrike99",
    "last_name": "Doe",
    "password": "scrypt:32768:8:1$yADGUrEwFA8xO86o$984513cd9cbfc0ff99156009ceea095d799ad5372ac94e3977b5da64fece10787558cd4281acdc5f0a3f1e1ccfe1dfe231f5366356e3d27548ac4ae7628406a4",
    "role": "user",
    "state": "California",
    "tagline": "Leveling up every day."
}
``` 

### DELETE /users/<id>
Deletes a user by ID.

**request:**
```json
method: DELETE
url: http://127.0.0.1:5000/users/1
authorization: Bearer <token>
```

**response:**
```json
{
    "message": "Successfully deleted user 1"
}
```

## Messages

### POST /messages
```json
{
    "sender_id": 1,
    "recipient_id": 2,
    "content": "Hello, how are you?"
}
```