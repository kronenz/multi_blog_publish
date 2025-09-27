# Quickstart: Frontend SaaS Service

This document provides a quick overview of how to use the Frontend SaaS Service API.

## 1. Create a new user

Send a `POST` request to the `/users` endpoint with the following payload:

```json
{
  "name": "John Doe",
  "email": "john.doe@example.com",
  "password": "password123"
}
```

## 2. Create a new knowledge vault

Send a `POST` request to the `/knowledge_vaults` endpoint with the following payload:

```json
{
  "user_id": "<user_id>",
  "name": "My Knowledge Vault"
}
```

## 3. Create a new blog post

Send a `POST` request to the `/blog_posts` endpoint with the following payload:

```json
{
  "vault_id": "<vault_id>",
  "title": "My First Blog Post",
  "content": "This is the content of my first blog post.",
  "status": "draft"
}
```
