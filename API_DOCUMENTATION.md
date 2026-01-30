# Film API - Complete Documentation

## Table of Contents
1. [Overview](#overview)
2. [Authentication](#authentication)
3. [API Endpoints](#api-endpoints)
4. [Data Models](#data-models)
5. [Error Handling](#error-handling)
6. [Complete cURL Examples](#complete-curl-examples)

---

## Overview

This is a Flask-based REST API for managing films, directors, users, and film ratings. The API uses token-based authentication with Bearer tokens.

**Base URL:** `http://localhost:5000`

**Default Port:** 5000

**Database:** PostgreSQL

**Authentication:** Bearer Token (JWT-like)

---

## Authentication

### Login to Get Token

**Endpoint:** `POST /login`

**Description:** Authenticate a user and receive a Bearer token for subsequent requests.

**Request Headers:**
```
Content-Type: application/json
```

**Request Body:**
```json
{
  "username": "alice",
  "password": "password123"
}
```

**Success Response (200):**
```json
{
  "status": "success",
  "token": "a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6q7r8s9t0u1v2w3x4y5z6",
  "message": "Successfully logged in"
}
```

**Error Response (401):**
```json
{
  "status": "error",
  "message": "Invalid username or password"
}
```

**Error Response (400):**
```json
{
  "status": "error",
  "message": "Missing credentials"
}
```

**cURL Example:**
```bash
curl -X POST http://localhost:5000/login \
  -H "Content-Type: application/json" \
  -d '{
    "username": "alice",
    "password": "password123"
  }'
```

---

### Logout (Invalidate Token)

**Endpoint:** `POST /logout`

**Description:** Invalidate the current bearer token and log out the user.

**Request Headers:**
```
Authorization: Bearer <your_token_here>
```

**Success Response (200):**
```json
{
  "status": "success",
  "message": "Successfully logged out"
}
```

**Error Response (401):**
```json
{
  "status": "unauthorized",
  "message": "Invalid token"
}
```

**cURL Example:**
```bash
curl -X POST http://localhost:5000/logout \
  -H "Authorization: Bearer a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6q7r8s9t0u1v2w3x4y5z6"
```

---

## API Endpoints

### Overview of All Endpoints

| Method | Endpoint | Auth Required | Description |
|--------|----------|---------------|-------------|
| POST | `/login` | No | Get authentication token |
| POST | `/logout` | Yes | Invalidate token |
| GET | `/users` | Yes | Get all users |
| POST | `/users` | Yes | Create new user |
| GET | `/users/<id>` | Yes | Get user by ID |
| DELETE | `/users/<id>` | Yes | Delete user |
| GET | `/users/<id>/profile` | Yes | Get user profile |
| POST | `/users/<id>/profile` | Yes | Create user profile |
| PUT | `/users/<id>/profile` | Yes | Update user profile |
| GET | `/directors` | Yes | Get all directors |
| POST | `/directors` | Yes | Create new director |
| DELETE | `/directors/<id>` | Yes | Delete director |
| GET | `/films` | Yes | Get all films |
| POST | `/films` | Yes | Create new film |
| GET | `/films/<id>` | Yes | Get film by ID |
| DELETE | `/films/<id>` | Yes | Delete film |
| GET | `/marks` | Yes | Get all marks |
| POST | `/marks` | Yes | Create new mark |
| DELETE | `/marks/<id>` | Yes | Delete mark |
| GET | `/films/<id>/marks` | Yes | Get marks for film |

---

## Data Models

### User Model

**Database Table:** `utilisateurs`

**Fields:**
```json
{
  "id": 1,
  "username": "alice",
  "mail": "alice@example.com",
  "langue": "français"
}
```

**Constraints:**
- `username`: Unique, required, max 100 chars
- `mail`: Unique, required, max 150 chars
- `langue`: Optional, max 50 chars

---

### User Profile Model

**Database Table:** `user_profile`

**Fields:**
```json
{
  "id": 1,
  "user_id": 1,
  "bio": "Passionate about sci-fi films",
  "avatar_url": "https://example.com/avatar1.jpg",
  "created_at": "2025-01-30T12:00:00",
  "updated_at": "2025-01-30T14:30:00"
}
```

**Constraints:**
- `user_id`: Foreign key to User, unique (one profile per user)
- `bio`: Optional text
- `avatar_url`: Optional, max 500 chars
- `created_at`: Auto-set on creation
- `updated_at`: Auto-updated on modification

---

### Director Model

**Database Table:** `director`

**Fields:**
```json
{
  "id": 1,
  "name": "Christopher",
  "surname": "Nolan"
}
```

**Constraints:**
- `name`: Required, max 100 chars
- `surname`: Required, max 100 chars

---

### Film Model

**Database Table:** `film`

**Fields:**
```json
{
  "id": 1,
  "titre": "Inception",
  "annee": 2010,
  "duree": 148,
  "id_director": 1,
  "director": {
    "id": 1,
    "name": "Christopher",
    "surname": "Nolan"
  }
}
```

**Constraints:**
- `titre`: Required, max 200 chars
- `annee`: Required, integer (year)
- `duree`: Required, integer (minutes)
- `id_director`: Optional foreign key to Director

---

### Mark (Rating) Model

**Database Table:** `mark`

**Fields:**
```json
{
  "id": 1,
  "id_film": 1,
  "id_user": 1,
  "mark": 9
}
```

**Constraints:**
- `id_film`: Required, foreign key to Film
- `id_user`: Required, foreign key to User
- `mark`: Required, integer between 0-10
- Unique constraint: One mark per user per film

---

## Complete Endpoint Reference

### USER ENDPOINTS

#### 1. Get All Users

**Endpoint:** `GET /users`

**Auth Required:** Yes (Bearer Token)

**Response (200):**
```json
[
  {
    "id": 1,
    "username": "alice",
    "mail": "alice@example.com",
    "langue": "français"
  },
  {
    "id": 2,
    "username": "bob",
    "mail": "bob@example.com",
    "langue": "anglais"
  }
]
```

**cURL Example:**
```bash
curl -X GET http://localhost:5000/users \
  -H "Authorization: Bearer YOUR_TOKEN"
```

---

#### 2. Create New User

**Endpoint:** `POST /users`

**Auth Required:** Yes (Bearer Token)

**Request Headers:**
```
Content-Type: application/json
Authorization: Bearer YOUR_TOKEN
```

**Request Body:**
```json
{
  "username": "diana",
  "mail": "diana@example.com",
  "langue": "deutsch"
}
```

**Success Response (201):**
```json
{
  "message": "Utilisateur ajouté",
  "user": {
    "id": 4,
    "username": "diana",
    "mail": "diana@example.com",
    "langue": "deutsch"
  }
}
```

**Error Response (400):**
```json
{
  "error": "username et mail obligatoires"
}
```

**Error Response (400) - Duplicate:**
```json
{
  "error": "Cet utilisateur existe déjà"
}
```

**cURL Example:**
```bash
curl -X POST http://localhost:5000/users \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -d '{
    "username": "diana",
    "mail": "diana@example.com",
    "langue": "deutsch"
  }'
```

---

#### 3. Get User by ID

**Endpoint:** `GET /users/<id>`

**Auth Required:** Yes (Bearer Token)

**URL Parameters:**
- `id` (integer): User ID

**Success Response (200):**
```json
{
  "id": 1,
  "username": "alice",
  "mail": "alice@example.com",
  "langue": "français"
}
```

**Error Response (404):**
```json
{
  "error": "Utilisateur introuvable"
}
```

**cURL Example:**
```bash
curl -X GET http://localhost:5000/users/1 \
  -H "Authorization: Bearer YOUR_TOKEN"
```

---

#### 4. Delete User

**Endpoint:** `DELETE /users/<id>`

**Auth Required:** Yes (Bearer Token)

**URL Parameters:**
- `id` (integer): User ID

**Success Response (200):**
```json
{
  "message": "Utilisateur supprimé"
}
```

**Error Response (404):**
```json
{
  "error": "Utilisateur introuvable"
}
```

**cURL Example:**
```bash
curl -X DELETE http://localhost:5000/users/4 \
  -H "Authorization: Bearer YOUR_TOKEN"
```

---

### USER PROFILE ENDPOINTS

#### 1. Get User Profile

**Endpoint:** `GET /users/<id>/profile`

**Auth Required:** Yes (Bearer Token)

**URL Parameters:**
- `id` (integer): User ID

**Success Response (200):**
```json
{
  "id": 1,
  "user_id": 1,
  "bio": "Passionate about sci-fi films",
  "avatar_url": "https://example.com/avatar1.jpg",
  "created_at": "2025-01-30T12:00:00",
  "updated_at": "2025-01-30T12:00:00"
}
```

**Error Response (404):**
```json
{
  "error": "Profil utilisateur introuvable"
}
```

**cURL Example:**
```bash
curl -X GET http://localhost:5000/users/1/profile \
  -H "Authorization: Bearer YOUR_TOKEN"
```

---

#### 2. Create User Profile

**Endpoint:** `POST /users/<id>/profile`

**Auth Required:** Yes (Bearer Token)

**URL Parameters:**
- `id` (integer): User ID

**Request Headers:**
```
Content-Type: application/json
Authorization: Bearer YOUR_TOKEN
```

**Request Body:**
```json
{
  "bio": "Film enthusiast and critic",
  "avatar_url": "https://example.com/avatar_new.jpg"
}
```

**Success Response (201):**
```json
{
  "message": "Profil créé",
  "profile": {
    "id": 4,
    "user_id": 4,
    "bio": "Film enthusiast and critic",
    "avatar_url": "https://example.com/avatar_new.jpg",
    "created_at": "2025-01-30T12:00:00",
    "updated_at": "2025-01-30T12:00:00"
  }
}
```

**Error Response (404):**
```json
{
  "error": "Utilisateur introuvable"
}
```

**Error Response (400):**
```json
{
  "error": "Ce utilisateur a déjà un profil"
}
```

**cURL Example:**
```bash
curl -X POST http://localhost:5000/users/4/profile \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -d '{
    "bio": "Film enthusiast and critic",
    "avatar_url": "https://example.com/avatar_new.jpg"
  }'
```

---

#### 3. Update User Profile

**Endpoint:** `PUT /users/<id>/profile`

**Auth Required:** Yes (Bearer Token)

**URL Parameters:**
- `id` (integer): User ID

**Request Headers:**
```
Content-Type: application/json
Authorization: Bearer YOUR_TOKEN
```

**Request Body:**
```json
{
  "bio": "Updated bio text",
  "avatar_url": "https://example.com/new_avatar.jpg"
}
```

**Success Response (200):**
```json
{
  "message": "Profil mise à jour",
  "profile": {
    "id": 1,
    "user_id": 1,
    "bio": "Updated bio text",
    "avatar_url": "https://example.com/new_avatar.jpg",
    "created_at": "2025-01-30T12:00:00",
    "updated_at": "2025-01-30T14:30:00"
  }
}
```

**Error Response (404):**
```json
{
  "error": "Profil utilisateur introuvable"
}
```

**cURL Example:**
```bash
curl -X PUT http://localhost:5000/users/1/profile \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -d '{
    "bio": "Updated bio text",
    "avatar_url": "https://example.com/new_avatar.jpg"
  }'
```

---

### DIRECTOR ENDPOINTS

#### 1. Get All Directors

**Endpoint:** `GET /directors`

**Auth Required:** Yes (Bearer Token)

**Success Response (200):**
```json
[
  {
    "id": 1,
    "name": "Christopher",
    "surname": "Nolan"
  },
  {
    "id": 2,
    "name": "Lana",
    "surname": "Wachowski"
  }
]
```

**cURL Example:**
```bash
curl -X GET http://localhost:5000/directors \
  -H "Authorization: Bearer YOUR_TOKEN"
```

---

#### 2. Create Director

**Endpoint:** `POST /directors`

**Auth Required:** Yes (Bearer Token)

**Request Headers:**
```
Content-Type: application/json
Authorization: Bearer YOUR_TOKEN
```

**Request Body:**
```json
{
  "name": "Steven",
  "surname": "Spielberg"
}
```

**Success Response (201):**
```json
{
  "message": "Réalisateur ajouté",
  "director": {
    "id": 4,
    "name": "Steven",
    "surname": "Spielberg"
  }
}
```

**Error Response (400):**
```json
{
  "error": "name et surname obligatoires"
}
```

**cURL Example:**
```bash
curl -X POST http://localhost:5000/directors \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -d '{
    "name": "Steven",
    "surname": "Spielberg"
  }'
```

---

#### 3. Delete Director

**Endpoint:** `DELETE /directors/<id>`

**Auth Required:** Yes (Bearer Token)

**URL Parameters:**
- `id` (integer): Director ID

**Success Response (200):**
```json
{
  "message": "Réalisateur supprimé"
}
```

**Error Response (404):**
```json
{
  "error": "Réalisateur introuvable"
}
```

**cURL Example:**
```bash
curl -X DELETE http://localhost:5000/directors/4 \
  -H "Authorization: Bearer YOUR_TOKEN"
```

---

### FILM ENDPOINTS

#### 1. Get All Films

**Endpoint:** `GET /films`

**Auth Required:** Yes (Bearer Token)

**Success Response (200):**
```json
[
  {
    "id": 1,
    "titre": "Inception",
    "annee": 2010,
    "duree": 148,
    "id_director": 1,
    "director": {
      "id": 1,
      "name": "Christopher",
      "surname": "Nolan"
    }
  },
  {
    "id": 2,
    "titre": "The Matrix",
    "annee": 1999,
    "duree": 136,
    "id_director": 2,
    "director": {
      "id": 2,
      "name": "Lana",
      "surname": "Wachowski"
    }
  }
]
```

**cURL Example:**
```bash
curl -X GET http://localhost:5000/films \
  -H "Authorization: Bearer YOUR_TOKEN"
```

---

#### 2. Create Film

**Endpoint:** `POST /films`

**Auth Required:** Yes (Bearer Token)

**Request Headers:**
```
Content-Type: application/json
Authorization: Bearer YOUR_TOKEN
```

**Request Body:**
```json
{
  "titre": "The Dark Knight",
  "annee": 2008,
  "duree": 152,
  "id_director": 1
}
```

**Success Response (201):**
```json
{
  "message": "Film ajouté",
  "film": {
    "id": 4,
    "titre": "The Dark Knight",
    "annee": 2008,
    "duree": 152,
    "id_director": 1,
    "director": {
      "id": 1,
      "name": "Christopher",
      "surname": "Nolan"
    }
  }
}
```

**Error Response (400):**
```json
{
  "error": "titre, annee et duree obligatoires"
}
```

**Error Response (404):**
```json
{
  "error": "Réalisateur introuvable"
}
```

**cURL Example:**
```bash
curl -X POST http://localhost:5000/films \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -d '{
    "titre": "The Dark Knight",
    "annee": 2008,
    "duree": 152,
    "id_director": 1
  }'
```

---

#### 3. Get Film by ID

**Endpoint:** `GET /films/<id>`

**Auth Required:** Yes (Bearer Token)

**URL Parameters:**
- `id` (integer): Film ID

**Success Response (200):**
```json
{
  "id": 1,
  "titre": "Inception",
  "annee": 2010,
  "duree": 148,
  "id_director": 1,
  "director": {
    "id": 1,
    "name": "Christopher",
    "surname": "Nolan"
  }
}
```

**Error Response (404):**
```json
{
  "error": "Film introuvable"
}
```

**cURL Example:**
```bash
curl -X GET http://localhost:5000/films/1 \
  -H "Authorization: Bearer YOUR_TOKEN"
```

---

#### 4. Delete Film

**Endpoint:** `DELETE /films/<id>`

**Auth Required:** Yes (Bearer Token)

**URL Parameters:**
- `id` (integer): Film ID

**Success Response (200):**
```json
{
  "message": "Film supprimé"
}
```

**Error Response (404):**
```json
{
  "error": "Film introuvable"
}
```

**cURL Example:**
```bash
curl -X DELETE http://localhost:5000/films/4 \
  -H "Authorization: Bearer YOUR_TOKEN"
```

---

### MARK (RATING) ENDPOINTS

#### 1. Get All Marks

**Endpoint:** `GET /marks`

**Auth Required:** Yes (Bearer Token)

**Success Response (200):**
```json
[
  {
    "id": 1,
    "id_film": 1,
    "id_user": 1,
    "mark": 9
  },
  {
    "id": 2,
    "id_film": 2,
    "id_user": 1,
    "mark": 8
  }
]
```

**cURL Example:**
```bash
curl -X GET http://localhost:5000/marks \
  -H "Authorization: Bearer YOUR_TOKEN"
```

---

#### 2. Create or Update Mark

**Endpoint:** `POST /marks`

**Auth Required:** Yes (Bearer Token)

**Request Headers:**
```
Content-Type: application/json
Authorization: Bearer YOUR_TOKEN
```

**Request Body:**
```json
{
  "id_film": 1,
  "id_user": 1,
  "mark": 9
}
```

**Success Response (201):** (New mark created)
```json
{
  "message": "Note ajoutée",
  "mark": {
    "id": 7,
    "id_film": 1,
    "id_user": 1,
    "mark": 9
  }
}
```

**Success Response (200):** (Existing mark updated)
```json
{
  "message": "Note mise à jour",
  "mark": {
    "id": 1,
    "id_film": 1,
    "id_user": 1,
    "mark": 10
  }
}
```

**Error Response (400):**
```json
{
  "error": "id_film, id_user et mark obligatoires"
}
```

**Error Response (400) - Invalid Mark:**
```json
{
  "error": "mark doit être entre 0 et 10"
}
```

**Error Response (404):**
```json
{
  "error": "Film introuvable"
}
```

**cURL Example:**
```bash
curl -X POST http://localhost:5000/marks \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -d '{
    "id_film": 1,
    "id_user": 1,
    "mark": 9
  }'
```

---

#### 3. Delete Mark

**Endpoint:** `DELETE /marks/<id>`

**Auth Required:** Yes (Bearer Token)

**URL Parameters:**
- `id` (integer): Mark ID

**Success Response (200):**
```json
{
  "message": "Note supprimée"
}
```

**Error Response (404):**
```json
{
  "error": "Note introuvable"
}
```

**cURL Example:**
```bash
curl -X DELETE http://localhost:5000/marks/7 \
  -H "Authorization: Bearer YOUR_TOKEN"
```

---

#### 4. Get Marks for a Film

**Endpoint:** `GET /films/<id>/marks`

**Auth Required:** Yes (Bearer Token)

**URL Parameters:**
- `id` (integer): Film ID

**Success Response (200):**
```json
[
  {
    "id": 1,
    "id_film": 1,
    "id_user": 1,
    "mark": 9
  },
  {
    "id": 3,
    "id_film": 1,
    "id_user": 2,
    "mark": 10
  }
]
```

**Error Response (404):**
```json
{
  "error": "Film introuvable"
}
```

**cURL Example:**
```bash
curl -X GET http://localhost:5000/films/1/marks \
  -H "Authorization: Bearer YOUR_TOKEN"
```

---

## Error Handling

### Common Error Responses

#### 400 - Bad Request
```json
{
  "error": "Description of what went wrong"
}
```
**When:** Missing required fields, invalid format, constraint violations

---

#### 401 - Unauthorized

```json
{
  "status": "unauthorized",
  "message": "Missing or invalid token"
}
```
**When:** Token is missing, malformed, or invalid

---

#### 404 - Not Found

```json
{
  "error": "Resource introuvable"
}
```
**When:** Requested resource (user, film, director, mark) doesn't exist

---

### Standard Error Messages

| Message | Meaning |
|---------|---------|
| `"Missing credentials"` | Login request missing username or password |
| `"Invalid username or password"` | Login failed - wrong credentials |
| `"Missing or invalid token"` | Authorization header missing or malformed |
| `"Invalid token format"` | Token doesn't follow `Bearer <token>` format |
| `"Invalid or expired token"` | Token not found in active sessions |
| `"username et mail obligatoires"` | User creation missing required fields |
| `"Cet utilisateur existe déjà"` | Username already exists |
| `"Utilisateur introuvable"` | User not found |
| `"titre, annee et duree obligatoires"` | Film missing required fields |
| `"mark doit être entre 0 et 10"` | Rating not in valid range |

---

## Complete cURL Examples

### Full Workflow Example

```bash
#!/bin/bash

# Step 1: Login
echo "=== STEP 1: LOGIN ==="
TOKEN=$(curl -s -X POST http://localhost:5000/login \
  -H "Content-Type: application/json" \
  -d '{
    "username": "alice",
    "password": "password123"
  }' | grep -o '"token":"[^"]*' | cut -d'"' -f4)

echo "Token: $TOKEN"
echo ""

# Step 2: Get all users
echo "=== STEP 2: GET ALL USERS ==="
curl -s -X GET http://localhost:5000/users \
  -H "Authorization: Bearer $TOKEN" | json_pp
echo ""

# Step 3: Get specific user
echo "=== STEP 3: GET USER BY ID ==="
curl -s -X GET http://localhost:5000/users/1 \
  -H "Authorization: Bearer $TOKEN" | json_pp
echo ""

# Step 4: Get user profile
echo "=== STEP 4: GET USER PROFILE ==="
curl -s -X GET http://localhost:5000/users/1/profile \
  -H "Authorization: Bearer $TOKEN" | json_pp
echo ""

# Step 5: Update user profile
echo "=== STEP 5: UPDATE USER PROFILE ==="
curl -s -X PUT http://localhost:5000/users/1/profile \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{
    "bio": "Updated bio",
    "avatar_url": "https://example.com/new.jpg"
  }' | json_pp
echo ""

# Step 6: Get all films
echo "=== STEP 6: GET ALL FILMS ==="
curl -s -X GET http://localhost:5000/films \
  -H "Authorization: Bearer $TOKEN" | json_pp
echo ""

# Step 7: Get all marks
echo "=== STEP 7: GET ALL MARKS ==="
curl -s -X GET http://localhost:5000/marks \
  -H "Authorization: Bearer $TOKEN" | json_pp
echo ""

# Step 8: Create a new mark
echo "=== STEP 8: CREATE NEW MARK ==="
curl -s -X POST http://localhost:5000/marks \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{
    "id_film": 2,
    "id_user": 1,
    "mark": 8
  }' | json_pp
echo ""

# Step 9: Get marks for a specific film
echo "=== STEP 9: GET MARKS FOR FILM ==="
curl -s -X GET http://localhost:5000/films/1/marks \
  -H "Authorization: Bearer $TOKEN" | json_pp
echo ""

# Step 10: Logout
echo "=== STEP 10: LOGOUT ==="
curl -s -X POST http://localhost:5000/logout \
  -H "Authorization: Bearer $TOKEN" | json_pp
echo ""

echo "=== WORKFLOW COMPLETE ==="
```

Save this as `api-workflow.sh`, make it executable with `chmod +x api-workflow.sh`, and run with `./api-workflow.sh`

---

### Inline cURL Examples

**Login and Extract Token:**
```bash
TOKEN=$(curl -s -X POST http://localhost:5000/login \
  -H "Content-Type: application/json" \
  -d '{"username":"alice","password":"password123"}' \
  | jq -r '.token')

echo "Your token is: $TOKEN"
```

**Get all users (with jq for pretty output):**
```bash
curl -X GET http://localhost:5000/users \
  -H "Authorization: Bearer $TOKEN" | jq '.'
```

**Create a new film:**
```bash
curl -X POST http://localhost:5000/films \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{
    "titre": "Oppenheimer",
    "annee": 2023,
    "duree": 180,
    "id_director": 1
  }' | jq '.'
```

**Create and rate a film in one workflow:**
```bash
# Get token
TOKEN=$(curl -s -X POST http://localhost:5000/login \
  -H "Content-Type: application/json" \
  -d '{"username":"bob","password":"password456"}' \
  | jq -r '.token')

# Create film
FILM_ID=$(curl -s -X POST http://localhost:5000/films \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{
    "titre": "New Film",
    "annee": 2025,
    "duree": 120,
    "id_director": 1
  }' | jq -r '.film.id')

# Rate the film
curl -X POST http://localhost:5000/marks \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d "{
    \"id_film\": $FILM_ID,
    \"id_user\": 2,
    \"mark\": 8
  }" | jq '.'
```

---

## Testing Checklist

Use this checklist to test all API functionality:

- [ ] **Authentication**
  - [ ] Login with valid credentials
  - [ ] Login with invalid credentials
  - [ ] Logout

- [ ] **Users**
  - [ ] Get all users
  - [ ] Get single user
  - [ ] Create new user
  - [ ] Delete user

- [ ] **User Profiles**
  - [ ] Get profile
  - [ ] Create profile
  - [ ] Update profile

- [ ] **Directors**
  - [ ] Get all directors
  - [ ] Create new director
  - [ ] Delete director

- [ ] **Films**
  - [ ] Get all films
  - [ ] Get single film
  - [ ] Create new film
  - [ ] Delete film

- [ ] **Marks**
  - [ ] Get all marks
  - [ ] Create new mark
  - [ ] Update existing mark
  - [ ] Delete mark
  - [ ] Get marks for specific film

- [ ] **Error Handling**
  - [ ] Test with missing token
  - [ ] Test with invalid token
  - [ ] Test with missing required fields
  - [ ] Test with invalid data types

---

## Notes

- All timestamps are in ISO 8601 format
- All IDs are integers
- The mark field must be between 0 and 10 (inclusive)
- Users, Directors, and Films must have unique identifiers
- A user can only have one profile
- A user can only rate each film once (updating overwrites previous rating)
- Deleting a user cascades to delete their profile and marks
- Deleting a director cascades to delete their films (and associated marks)

