# API 테스트 가이드 - JWT 토큰 인증

## 📌 개요
이 프로젝트는 JWT(JSON Web Token) 기반 인증을 사용합니다.
인증이 필요한 API를 호출할 때는 반드시 **Authorization 헤더**에 토큰을 포함해야 합니다.

---

## 🔐 인증 플로우

### 1단계: 회원가입 (선택)
```http
POST /auth/register
Content-Type: application/json

{
  "email": "test@example.com",
  "password": "password123",
  "nickname": "테스트유저"
}
```

**응답 예시:**
```json
{
  "success": true,
  "message": "회원가입이 완료되었습니다."
}
```

### 2단계: 로그인 (토큰 받기)
```http
POST /auth/login
Content-Type: application/json

{
  "email": "test@example.com",
  "password": "password123"
}
```

**응답 예시:**
```json
{
  "success": true,
  "message": "로그인 성공",
  "data": {
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX25vIjoxLCJyb2xlX25vIjoxLCJleHAiOjE3MDkxMjM0NTZ9.abc123...",
    "token_type": "Bearer",
    "user_no": 1,
    "nickname": "테스트유저"
  }
}
```

⚠️ **중요:** `access_token` 값을 복사해서 다음 요청들에 사용하세요!

### 3단계: 토큰 검증 (선택)
```http
GET /auth/verify
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

**응답 예시:**
```json
{
  "success": true,
  "message": "유효한 토큰입니다.",
  "data": {
    "user_no": 1,
    "role_no": 1
  }
}
```

---

## 👤 User API 테스트

### 프로필 조회 (본인 또는 ADMIN)
```http
GET /users/1/profile
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

**성공 응답:**
```json
{
  "success": true,
  "data": {
    "user_no": 1,
    "email": "test@example.com",
    "nickname": "테스트유저",
    "profile_url": null,
    "created_at": "2024-01-01T00:00:00",
    "updated_at": "2024-01-01T00:00:00"
  }
}
```

**실패 응답 (토큰 없음):**
```json
{
  "success": false,
  "message": "Authorization 헤더가 없습니다."
}
```

**실패 응답 (권한 없음):**
```json
{
  "success": false,
  "message": "본인 또는 관리자만 접근 가능합니다."
}
```

### 프로필 수정 (본인 또는 ADMIN)
```http
PUT /users/1/profile
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
Content-Type: application/json

{
  "nickname": "새로운닉네임"
}
```

**응답:**
```json
{
  "success": true,
  "message": "닉네임이 수정되었습니다."
}
```

### 계정 탈퇴 (본인 또는 ADMIN)
```http
DELETE /users/1
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

**응답:**
```json
{
  "success": true,
  "message": "계정이 탈퇴되었습니다."
}
```

---

## 📢 Notice API 테스트

### 공지사항 작성 (ADMIN만)
```http
POST /notice
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
Content-Type: application/json

{
  "title": "공지사항 제목",
  "content": "공지사항 내용입니다."
}
```

**성공 응답 (ADMIN):**
```json
{
  "success": true,
  "data": {
    "notice_no": 1,
    "user_no": 1,
    "title": "공지사항 제목",
    "content": "공지사항 내용입니다."
  }
}
```

**실패 응답 (일반 유저):**
```json
{
  "success": false,
  "message": "권한이 없습니다 (ADMIN 전용)"
}
```

### 공지사항 수정 (ADMIN만)
```http
PUT /notice/1
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
Content-Type: application/json

{
  "title": "수정된 제목",
  "content": "수정된 내용"
}
```

### 공지사항 삭제 (ADMIN만)
```http
DELETE /notice/1
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

### 공지사항 목록 조회 (인증 불필요)
```http
GET /notice
```

**응답:**
```json
{
  "success": true,
  "data": [
    {
      "notice_no": 1,
      "user_no": 1,
      "nickname": "관리자",
      "title": "공지사항 제목",
      "content": "공지사항 내용",
      "created_at": "2024-01-01T00:00:00",
      "updated_at": "2024-01-01T00:00:00"
    }
  ]
}
```

### 공지사항 상세 조회 (인증 불필요)
```http
GET /notice/1
```

---

## 🛠️ 도구별 사용 방법

### Postman
1. **로그인 요청 보내기**
   - Method: `POST`
   - URL: `http://localhost:5000/auth/login`
   - Body → raw → JSON
   - 로그인 JSON 입력

2. **access_token 복사하기**
   - 응답에서 `data.access_token` 값 복사

3. **다음 요청에 토큰 추가**
   - **방법 1: Authorization 탭**
     - Type: `Bearer Token` 선택
     - Token: `<복사한_토큰>` (Bearer 없이)

   - **방법 2: Headers 탭**
     - Key: `Authorization`
     - Value: `Bearer <복사한_토큰>`

### curl
```bash
# 1. 로그인
TOKEN=$(curl -s -X POST http://localhost:5000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"password123"}' \
  | jq -r '.data.access_token')

# 2. 토큰 사용해서 프로필 조회
curl -X GET http://localhost:5000/users/1/profile \
  -H "Authorization: Bearer $TOKEN"

# 3. 프로필 수정
curl -X PUT http://localhost:5000/users/1/profile \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"nickname":"새닉네임"}'
```

### Thunder Client (VS Code Extension)
1. Auth 탭 → Bearer 선택
2. Token 입력란에 토큰 붙여넣기

---

## 🔑 권한 체계

### role_no
- `1`: 일반 사용자 (USER)
- `2`: 관리자 (ADMIN)

### API 권한
| API | 권한 요구사항 |
|-----|--------------|
| POST /auth/register | 없음 (공개) |
| POST /auth/login | 없음 (공개) |
| GET /auth/verify | 인증 필요 |
| GET /users/:user_no/profile | 본인 또는 ADMIN |
| PUT /users/:user_no/profile | 본인 또는 ADMIN |
| DELETE /users/:user_no | 본인 또는 ADMIN |
| POST /notice | ADMIN 전용 |
| PUT /notice/:notice_no | ADMIN 전용 |
| DELETE /notice/:notice_no | ADMIN 전용 |
| GET /notice | 없음 (공개) |
| GET /notice/:notice_no | 없음 (공개) |

---

## ❌ 자주 발생하는 에러

### 401 Unauthorized
```json
{
  "success": false,
  "message": "Authorization 헤더가 없습니다."
}
```
**해결:** Authorization 헤더 추가

---

```json
{
  "success": false,
  "message": "토큰 형식이 올바르지 않습니다."
}
```
**해결:** `Bearer ` 접두사 확인 (Bearer 뒤에 공백 필수)

---

```json
{
  "success": false,
  "message": "토큰이 만료되었습니다."
}
```
**해결:** 다시 로그인해서 새 토큰 받기 (토큰 유효기간: 24시간)

---

### 403 Forbidden
```json
{
  "success": false,
  "message": "본인 또는 관리자만 접근 가능합니다."
}
```
**해결:** 본인 리소스에만 접근하거나 ADMIN 계정 사용

---

```json
{
  "success": false,
  "message": "권한이 없습니다 (ADMIN 전용)"
}
```
**해결:** ADMIN 권한(role_no=2) 계정으로 로그인

---

## 💡 테스트 시나리오

### 시나리오 1: 일반 유저 플로우
```
1. 회원가입 → POST /auth/register
2. 로그인 → POST /auth/login (토큰 받기)
3. 내 프로필 조회 → GET /users/1/profile (본인)
4. 닉네임 수정 → PUT /users/1/profile (본인)
5. 다른 사람 프로필 조회 시도 → GET /users/2/profile (실패: 403)
6. 공지사항 목록 조회 → GET /notice (성공: 공개)
7. 공지사항 작성 시도 → POST /notice (실패: 403)
```

### 시나리오 2: ADMIN 플로우
```
1. ADMIN 계정 로그인 → POST /auth/login (role_no=2)
2. 공지사항 작성 → POST /notice (성공)
3. 공지사항 수정 → PUT /notice/1 (성공)
4. 모든 유저 프로필 조회 → GET /users/X/profile (성공)
5. 공지사항 삭제 → DELETE /notice/1 (성공)
```

---

## 📝 참고사항

- JWT 토큰 유효기간: **24시간**
- 토큰은 `services/auth.py:103-111`에서 생성됩니다
- 토큰 검증은 `middleware/auth_utils.py`에서 처리됩니다
- DB에서 ADMIN 계정 생성: `UPDATE user SET role_no = 2 WHERE user_no = 1;`
