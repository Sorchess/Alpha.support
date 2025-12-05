## Endpoints

### Users

 - GET /api/users/me/
   - headers Cookie
 - GET /api/users/{user_oid}
 - POST /api/users/sign-up/
   - body {
  "email": EmailStr,
  "password": string
}
 - POST /api/users/sign-in/
   - body {
  "email": EmailStr,
  "password": string
}
 - POST /api/users/logout/
   - headers Cookie
 - PATCH /api/users/edit/
   - body {
  "email": EmailStr | None,
  "password": string | None,
  "username": string | None,
}      
 - DELETE /api/users/delete/
   - headers Cookie
 - POST /api/users/verify-email/
   - headers Cookie
 - PATCH /api/users/change-avatar/
   - headers Cookie
   - body {"file": string($binary)}

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
- POST /api/topics/{topic_oid}/message/
  - headers Cookie
  - body {
  "content": string
} 
- POST /api/topics/{topic_oid}/messages/
   - headers Cookie

### Websockets

- POST /api/ws/
   - headers Cookie
- WEBSOCKET /api/ws/?token=
   - headers token

### Files

- POST /api/file/
   - headers Cookie
   - body {"file": string($binary)}
- GET /api/file/{file_name}/
   - headers Cookie
- DELETE /api/file/{file_name}/
   - headers Cookie