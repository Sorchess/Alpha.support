## Endpoints

### Users 

Cookie - session_id

 - GET /api/users/me/
   - headers Cookie
   - status_code 200 json {
  "status": "success",
  "data": {
    "oid": "6f006a76f2c84e58bf6de7343854e6cf",
    "username": "294d8004b6a14604b6b4dcc00cebe601",
    "email": "user@example.com",
    "email_verified": false,
    "registered_in": "2025-12-04T11:56:39.804682Z",
    "avatar_url": "..."
  }
}
   - status_code 401 Unauthorized json {
"detail": "Missing cookie"
}
 - GET /api/users/{user_oid}
 - POST /api/users/sign-up/
   - body {
  "email": EmailStr,
  "password": string
}
   - status_code 200 {
  "status": "success",
  "message": "User created successfully.",
  "data": {
    "oid": "08dd5ed1a45d466ca375bbd11541e087",
    "username": "ed42774c325442bcb00deac1039f9a4f",
    "email": "user@esxample.com",
    "email_verified": false,
    "registered_in": "2025-12-05T14:34:03.694462Z",
    "avatar_url": "..."
  }
}
 - POST /api/users/sign-in/
   - body {
   - status_code 200 {
  "status": "success",
  "message": "You have successfully logged in.",
  "data": {
    "oid": "6f006a76f2c84e58bf6de7343854e6cf",
    "username": "294d8004b6a14604b6b4dcc00cebe601",
    "email": "user@example.com",
    "email_verified": false,
    "registered_in": "2025-12-04T11:56:39.804682Z",
    "avatar_url": "..."
  }
}
  "email": EmailStr,
  "password": string
}
 - POST /api/users/logout/
   - headers Cookie
   - status_code 200 {
  "status": "success",
  "message": "You have successfully logged out."
}
 - PATCH /api/users/edit/
   - headers Cookie
   - body {
  "email": EmailStr | None,
  "password": string | None,
  "username": string | None,
}
   - status_code 200 json {
  "status": "success",
  "message": "Code sent successfully"
}
 - DELETE /api/users/delete/
   - headers Cookie
 - POST /api/users/verify-email/
   - headers Cookie
   - status_code 200 json {
  "status": "success",
  "message": "Code sent successfully"
}
 - PATCH /api/users/change-avatar/
   - headers Cookie
   - body {"file": string($binary)}
   - status_code 200 json {
  "status": "success",
  "message": "Avatar changed successfully."
}

### Emails

 - POST /api/emails/confirm/ - only dev, пока не работает реальная отправка письма
   - headers Cookie
   - body {"code": string}


### Topics

- GET /api/topics/
   - headers Cookie
- POST /api/topics/
   - headers Cookie
  - body {
  "title": string,
  "description": string
}
  - status_code 201 json {
  "status": "success",
  "data": {
    "title": "string",
    "description": "string",
    "oid": "5fd6caefbab64089925122a261f0801e",
    "author_oid": "08dd5ed1a45d466ca375bbd11541e087",
    "created_at": "2025-12-05T14:38:35.178141"
  }
}
- POST /api/topics/{topic_oid}/message/
  - headers Cookie
  - body {
  "content": string
} 
  - status_code 200 json {
  "status": "success",
  "data": {
    "content": "string",
    "topic_oid": "5fd6caefbab64089925122a261f0801e",
    "author_oid": "08dd5ed1a45d466ca375bbd11541e087",
    "oid": "e52d64d5da76477d922968c5a9e43cb5",
    "sended_at": "2025-12-05T14:40:25.415531"
  }
}
- POST /api/topics/{topic_oid}/messages/
   - headers Cookie
   - status_code 200 json {
  "status": "success",
  "data": [
    {
      "content": "string",
      "topic_oid": "5fd6caefbab64089925122a261f0801e",
      "author_oid": "08dd5ed1a45d466ca375bbd11541e087",
      "oid": "e52d64d5da76477d922968c5a9e43cb5",
      "sended_at": "2025-12-05T14:40:25.415531Z"
    },
  ]
}

### Websockets

- POST /api/ws/
   - headers Cookie
   - status_code 200 json {
  "status": "success",
  "data": "04380e973d8c48bb9ed02462802a5a6c"
}
- WEBSOCKET /api/ws/?token=
   - headers token

### Files

- POST /api/file/
   - headers Cookie
   - body {"file": string($binary)}
   - status_code 200 json {
  "status": "success",
  "message": "File uploaded successfully.",
  "data": {
    "oid": "fef9920f6d60422fb1b021bf53134b58",
    "key": "21e9a0a7409c469a9f5f04195bd3d153.png",
    "origin": "Discord_KKauZFtQJE.png",
    "size": 145907,
    "topic_oid": null,
    "owner_oid": "1b5bf93e82e747f1adcc2a675eae0fc2"
  }
}
- GET /api/file/{file_name}/
   - headers Cookie
   - status_code 200 json - { status_code 200 json {  "status": "success",
  "data": "...ссылка на файл" }
- DELETE /api/file/{file_name}/
   - headers Cookie
   - status_code 200 json {  "status": "success",
  "message": "File successfully deleted." }



## Docker operations

```
docker compose up --build -d
```

```
docker compose down
```