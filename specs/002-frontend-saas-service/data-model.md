# Data Model: Frontend SaaS Service

## Entities

- **User**:
    - `id`: UUID (Primary Key)
    - `name`: String
    - `email`: String (Unique)
    - `password_hash`: String
    - `created_at`: Timestamp
    - `updated_at`: Timestamp

- **KnowledgeVault**:
    - `id`: UUID (Primary Key)
    - `user_id`: UUID (Foreign Key to User)
    - `name`: String
    - `created_at`: Timestamp
    - `updated_at`: Timestamp

- **BlogPost**:
    - `id`: UUID (Primary Key)
    - `vault_id`: UUID (Foreign Key to KnowledgeVault)
    - `title`: String
    - `content`: Text
    - `status`: String (e.g., "draft", "published")
    - `created_at`: Timestamp
    - `updated_at`: Timestamp
