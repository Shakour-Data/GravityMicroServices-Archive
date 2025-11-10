<!--
================================================================================
FILE IDENTITY
================================================================================
Project      : Gravity MicroServices Platform
File         : SERVICE_SPECIFICATIONS.md
Description  : Detailed technical specifications for all 30 microservices
               including database schemas, API endpoints, and dependencies
Language     : English (UK)
Document Type: Technical Specifications

================================================================================
AUTHORSHIP & CONTRIBUTION
================================================================================
Primary Author    : Dr. Sarah Chen (Chief Architect)
Contributors      : Elena Volkov, Dr. Fatima Al-Mansouri
Team Standard     : Elite Engineers (IQ 180+, 15+ years experience)

================================================================================
TIMELINE & EFFORT
================================================================================
Created Date      : 2025-11-07 20:00 UTC
Last Modified     : 2025-11-07 20:00 UTC
Planning Time     : 4 hours 0 minutes
Total Cost        : 4 × $150 = $600.00 USD

================================================================================
LICENSE & COPYRIGHT
================================================================================
Copyright (c) 2025 Gravity MicroServices Platform
License: MIT License
Repository: https://github.com/GravityWavesMl/GravityMicroServices

================================================================================
-->

# 📋 Service Specifications

**Detailed technical specifications for all 30 Gravity microservices**

---

## Table of Contents

1. [Core Services](#core-services)
2. [Advanced Services](#advanced-services)
3. [Media Services](#media-services)
4. [Communication Services](#communication-services)
5. [Data Services](#data-services)
6. [Infrastructure Services](#infrastructure-services)
7. [Platform Services](#platform-services)
8. [Utility Services](#utility-services)

---

## Core Services

### 1. User Service (Port 8082)

**Purpose:** User profile and preference management

**Database Schema:**
```sql
-- users table (extends auth_service users)
CREATE TABLE user_profiles (
    id SERIAL PRIMARY KEY,
    user_id INTEGER UNIQUE NOT NULL,  -- References auth_service
    display_name VARCHAR(100),
    bio TEXT,
    avatar_url VARCHAR(500),
    cover_image_url VARCHAR(500),
    location VARCHAR(200),
    website VARCHAR(500),
    date_of_birth DATE,
    gender VARCHAR(20),
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE user_preferences (
    id SERIAL PRIMARY KEY,
    user_id INTEGER UNIQUE NOT NULL,
    language VARCHAR(10) DEFAULT 'en',
    timezone VARCHAR(50) DEFAULT 'UTC',
    theme VARCHAR(20) DEFAULT 'light',
    email_notifications BOOLEAN DEFAULT TRUE,
    sms_notifications BOOLEAN DEFAULT FALSE,
    push_notifications BOOLEAN DEFAULT TRUE,
    privacy_settings JSONB,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE user_sessions (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL,
    session_token VARCHAR(255) UNIQUE NOT NULL,
    ip_address VARCHAR(45),
    user_agent TEXT,
    device_type VARCHAR(50),
    last_activity TIMESTAMP DEFAULT NOW(),
    expires_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_user_sessions_user_id ON user_sessions(user_id);
CREATE INDEX idx_user_sessions_token ON user_sessions(session_token);
```

**API Endpoints:**
```
GET    /api/v1/users                  # List all users (admin only)
GET    /api/v1/users/{id}             # Get user profile
POST   /api/v1/users                  # Create user profile
PATCH  /api/v1/users/{id}             # Update user profile
DELETE /api/v1/users/{id}             # Delete user (soft delete)

GET    /api/v1/users/me               # Get current user profile
PATCH  /api/v1/users/me               # Update current user profile

GET    /api/v1/users/{id}/preferences # Get user preferences
PATCH  /api/v1/users/{id}/preferences # Update preferences

GET    /api/v1/users/{id}/sessions    # List user sessions
DELETE /api/v1/users/{id}/sessions/{session_id}  # Revoke session

POST   /api/v1/users/{id}/avatar      # Upload avatar
DELETE /api/v1/users/{id}/avatar      # Remove avatar

GET    /api/v1/users/search           # Search users (query, filters)
```

**Dependencies:**
- auth-service (for user authentication)
- file-service (for avatar uploads)

**Technology Stack:**
- FastAPI, SQLAlchemy, PostgreSQL
- Redis (session caching)
- Pydantic (validation)

**Estimated Time:** 40 hours ($6,000)

---

### 2. Notification Service (Port 8083)

**Purpose:** Multi-channel notification delivery (email, SMS, push)

**Database Schema:**
```sql
CREATE TABLE notification_templates (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) UNIQUE NOT NULL,
    type VARCHAR(20) NOT NULL,  -- 'email', 'sms', 'push'
    subject VARCHAR(255),
    body TEXT NOT NULL,
    variables JSONB,  -- List of template variables
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE notifications (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL,
    type VARCHAR(20) NOT NULL,
    channel VARCHAR(20) NOT NULL,  -- 'email', 'sms', 'push'
    template_id INTEGER REFERENCES notification_templates(id),
    subject VARCHAR(255),
    body TEXT NOT NULL,
    metadata JSONB,
    status VARCHAR(20) DEFAULT 'pending',  -- pending, sent, failed, delivered
    sent_at TIMESTAMP,
    delivered_at TIMESTAMP,
    error_message TEXT,
    retry_count INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE user_notification_preferences (
    id SERIAL PRIMARY KEY,
    user_id INTEGER UNIQUE NOT NULL,
    email_enabled BOOLEAN DEFAULT TRUE,
    sms_enabled BOOLEAN DEFAULT FALSE,
    push_enabled BOOLEAN DEFAULT TRUE,
    quiet_hours_start TIME,
    quiet_hours_end TIME,
    notification_types JSONB,  -- Which types of notifications to receive
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_notifications_user_id ON notifications(user_id);
CREATE INDEX idx_notifications_status ON notifications(status);
CREATE INDEX idx_notifications_created_at ON notifications(created_at);
```

**API Endpoints:**
```
POST   /api/v1/notifications/send            # Send single notification
POST   /api/v1/notifications/send-batch      # Send bulk notifications
GET    /api/v1/notifications/user/{user_id}  # Get user notifications
PATCH  /api/v1/notifications/{id}/read       # Mark as read
DELETE /api/v1/notifications/{id}            # Delete notification

GET    /api/v1/notifications/templates       # List templates
POST   /api/v1/notifications/templates       # Create template
GET    /api/v1/notifications/templates/{id}  # Get template
PATCH  /api/v1/notifications/templates/{id}  # Update template
DELETE /api/v1/notifications/templates/{id}  # Delete template

GET    /api/v1/notifications/preferences/{user_id}  # Get preferences
PATCH  /api/v1/notifications/preferences/{user_id}  # Update preferences

GET    /api/v1/notifications/stats           # Notification statistics
```

**Dependencies:**
- auth-service (authentication)
- user-service (user data)
- email-service (email delivery)
- sms-service (SMS delivery)

**Technology Stack:**
- FastAPI, SQLAlchemy, PostgreSQL
- Redis (queue for async delivery)
- Celery (background tasks)

**Estimated Time:** 35 hours ($5,250)

---

### 3. File Service (Port 8084)

**Purpose:** File upload, storage, and CDN integration

**Database Schema:**
```sql
CREATE TABLE files (
    id SERIAL PRIMARY KEY,
    file_id VARCHAR(255) UNIQUE NOT NULL,  -- UUID
    user_id INTEGER NOT NULL,
    filename VARCHAR(255) NOT NULL,
    original_filename VARCHAR(255) NOT NULL,
    mime_type VARCHAR(100) NOT NULL,
    file_size BIGINT NOT NULL,
    storage_backend VARCHAR(50) NOT NULL,  -- 's3', 'local', 'azure'
    storage_path VARCHAR(500) NOT NULL,
    public_url VARCHAR(500),
    cdn_url VARCHAR(500),
    is_public BOOLEAN DEFAULT FALSE,
    folder VARCHAR(255),
    tags TEXT[],
    metadata JSONB,
    checksum VARCHAR(64),  -- SHA256 hash
    virus_scan_status VARCHAR(20),  -- pending, clean, infected
    expires_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE file_access_logs (
    id SERIAL PRIMARY KEY,
    file_id VARCHAR(255) NOT NULL,
    user_id INTEGER,
    ip_address VARCHAR(45),
    action VARCHAR(20) NOT NULL,  -- upload, download, delete
    accessed_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE file_shares (
    id SERIAL PRIMARY KEY,
    file_id VARCHAR(255) NOT NULL,
    shared_by INTEGER NOT NULL,
    shared_with INTEGER,  -- NULL for public share
    share_token VARCHAR(255) UNIQUE,
    permissions VARCHAR(20) DEFAULT 'read',  -- read, write
    expires_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_files_user_id ON files(user_id);
CREATE INDEX idx_files_folder ON files(folder);
CREATE INDEX idx_files_created_at ON files(created_at);
```

**API Endpoints:**
```
POST   /api/v1/files/upload          # Upload file (multipart)
POST   /api/v1/files/upload-url      # Get presigned upload URL
GET    /api/v1/files/{file_id}       # Get file metadata
GET    /api/v1/files/{file_id}/download  # Download file
DELETE /api/v1/files/{file_id}       # Delete file

GET    /api/v1/files/user/{user_id}  # List user files
GET    /api/v1/files/folder/{folder} # List files in folder

POST   /api/v1/files/{file_id}/share # Share file
GET    /api/v1/files/shared/{token}  # Access shared file
DELETE /api/v1/files/shares/{id}     # Revoke share

POST   /api/v1/files/{file_id}/copy  # Copy file
POST   /api/v1/files/{file_id}/move  # Move file to folder

GET    /api/v1/files/storage-stats   # Storage statistics
```

**Dependencies:**
- auth-service (authentication)
- Storage: AWS S3, Azure Blob, or local filesystem
- CDN: CloudFlare, AWS CloudFront

**Technology Stack:**
- FastAPI, SQLAlchemy, PostgreSQL
- boto3 (AWS S3)
- Pillow (image processing)
- python-magic (MIME type detection)

**Estimated Time:** 45 hours ($6,750)

---

### 4. Payment Service (Port 8085)

**Purpose:** Payment processing, subscriptions, invoicing

**Database Schema:**
```sql
CREATE TABLE payment_methods (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL,
    provider VARCHAR(50) NOT NULL,  -- 'stripe', 'paypal'
    provider_customer_id VARCHAR(255),
    type VARCHAR(20) NOT NULL,  -- 'card', 'bank_account'
    last4 VARCHAR(4),
    brand VARCHAR(50),
    exp_month INTEGER,
    exp_year INTEGER,
    is_default BOOLEAN DEFAULT FALSE,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE transactions (
    id SERIAL PRIMARY KEY,
    transaction_id VARCHAR(255) UNIQUE NOT NULL,
    user_id INTEGER NOT NULL,
    payment_method_id INTEGER REFERENCES payment_methods(id),
    amount DECIMAL(10, 2) NOT NULL,
    currency VARCHAR(3) DEFAULT 'USD',
    status VARCHAR(20) NOT NULL,  -- pending, succeeded, failed, refunded
    type VARCHAR(20) NOT NULL,  -- charge, refund
    description TEXT,
    provider VARCHAR(50) NOT NULL,
    provider_transaction_id VARCHAR(255),
    metadata JSONB,
    error_message TEXT,
    processed_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE subscriptions (
    id SERIAL PRIMARY KEY,
    subscription_id VARCHAR(255) UNIQUE NOT NULL,
    user_id INTEGER NOT NULL,
    plan_id VARCHAR(100) NOT NULL,
    status VARCHAR(20) NOT NULL,  -- active, canceled, past_due
    amount DECIMAL(10, 2) NOT NULL,
    currency VARCHAR(3) DEFAULT 'USD',
    interval VARCHAR(20) NOT NULL,  -- month, year
    current_period_start TIMESTAMP NOT NULL,
    current_period_end TIMESTAMP NOT NULL,
    cancel_at_period_end BOOLEAN DEFAULT FALSE,
    canceled_at TIMESTAMP,
    ended_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE invoices (
    id SERIAL PRIMARY KEY,
    invoice_id VARCHAR(255) UNIQUE NOT NULL,
    user_id INTEGER NOT NULL,
    subscription_id INTEGER REFERENCES subscriptions(id),
    amount_due DECIMAL(10, 2) NOT NULL,
    amount_paid DECIMAL(10, 2) DEFAULT 0,
    currency VARCHAR(3) DEFAULT 'USD',
    status VARCHAR(20) DEFAULT 'draft',  -- draft, open, paid, void
    due_date TIMESTAMP,
    paid_at TIMESTAMP,
    invoice_pdf_url VARCHAR(500),
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_transactions_user_id ON transactions(user_id);
CREATE INDEX idx_subscriptions_user_id ON subscriptions(user_id);
CREATE INDEX idx_invoices_user_id ON invoices(user_id);
```

**API Endpoints:**
```
POST   /api/v1/payments/methods       # Add payment method
GET    /api/v1/payments/methods       # List payment methods
DELETE /api/v1/payments/methods/{id}  # Remove payment method
PATCH  /api/v1/payments/methods/{id}/default  # Set default

POST   /api/v1/payments/charge        # Create charge
GET    /api/v1/payments/transactions  # List transactions
GET    /api/v1/payments/transactions/{id}  # Get transaction
POST   /api/v1/payments/refund/{id}   # Refund transaction

POST   /api/v1/payments/subscriptions # Create subscription
GET    /api/v1/payments/subscriptions # List subscriptions
PATCH  /api/v1/payments/subscriptions/{id}/cancel  # Cancel
POST   /api/v1/payments/subscriptions/{id}/resume  # Resume

GET    /api/v1/payments/invoices      # List invoices
GET    /api/v1/payments/invoices/{id} # Get invoice
POST   /api/v1/payments/invoices/{id}/pay  # Pay invoice

POST   /api/v1/payments/webhooks/stripe   # Stripe webhook
POST   /api/v1/payments/webhooks/paypal   # PayPal webhook
```

**Dependencies:**
- auth-service (authentication)
- user-service (user data)
- notification-service (payment notifications)

**Technology Stack:**
- FastAPI, SQLAlchemy, PostgreSQL
- stripe-python (Stripe API)
- paypalrestsdk (PayPal API)
- reportlab (PDF invoices)

**Estimated Time:** 50 hours ($7,500)

---

## Advanced Services

### 5. Search Service (Port 8086)

**Purpose:** Full-text search using Elasticsearch

**Technology Stack:**
- FastAPI
- Elasticsearch 8.x
- Redis (search cache)

**Key Features:**
- Full-text search across multiple indices
- Faceted search and filtering
- Autocomplete suggestions
- Search analytics
- Synonym support

**API Endpoints:**
```
POST   /api/v1/search               # Execute search query
GET    /api/v1/search/suggest       # Autocomplete suggestions
POST   /api/v1/search/index/{type}  # Index document
DELETE /api/v1/search/index/{type}/{id}  # Remove from index
GET    /api/v1/search/stats         # Search analytics
```

**Estimated Time:** 40 hours ($6,000)

---

### 6. Analytics Service (Port 8087)

**Purpose:** User behavior tracking and analytics

**Database Schema:**
```sql
CREATE TABLE events (
    id SERIAL PRIMARY KEY,
    event_id VARCHAR(255) UNIQUE NOT NULL,
    user_id INTEGER,
    session_id VARCHAR(255),
    event_type VARCHAR(100) NOT NULL,  -- pageview, click, conversion
    event_name VARCHAR(100),
    properties JSONB,
    user_agent TEXT,
    ip_address VARCHAR(45),
    referrer TEXT,
    url TEXT,
    timestamp TIMESTAMP DEFAULT NOW()
);

CREATE TABLE page_views (
    id SERIAL PRIMARY KEY,
    user_id INTEGER,
    session_id VARCHAR(255),
    url TEXT NOT NULL,
    title VARCHAR(255),
    referrer TEXT,
    duration_seconds INTEGER,
    viewed_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_events_user_id ON events(user_id);
CREATE INDEX idx_events_type ON events(event_type);
CREATE INDEX idx_events_timestamp ON events(timestamp);
CREATE INDEX idx_page_views_url ON page_views(url);
```

**API Endpoints:**
```
POST   /api/v1/analytics/track       # Track event
POST   /api/v1/analytics/pageview    # Track pageview
GET    /api/v1/analytics/user/{id}   # User analytics
GET    /api/v1/analytics/dashboard   # Dashboard data
GET    /api/v1/analytics/reports     # Generate report
```

**Estimated Time:** 45 hours ($6,750)

---

### 7. Recommendation Service (Port 8088)

**Purpose:** ML-based recommendation engine

**Database Schema:**
```sql
CREATE TABLE user_interactions (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL,
    item_id INTEGER NOT NULL,
    interaction_type VARCHAR(50) NOT NULL,  -- view, like, purchase
    score FLOAT DEFAULT 1.0,
    timestamp TIMESTAMP DEFAULT NOW()
);

CREATE TABLE recommendations (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL,
    item_id INTEGER NOT NULL,
    score FLOAT NOT NULL,
    algorithm VARCHAR(50),  -- collaborative, content-based
    generated_at TIMESTAMP DEFAULT NOW(),
    expires_at TIMESTAMP
);

CREATE INDEX idx_interactions_user ON user_interactions(user_id);
CREATE INDEX idx_interactions_item ON user_interactions(item_id);
CREATE INDEX idx_recommendations_user ON recommendations(user_id);
```

**API Endpoints:**
```
GET    /api/v1/recommendations/user/{id}  # Get recommendations
POST   /api/v1/recommendations/track      # Track interaction
POST   /api/v1/recommendations/train      # Train model
GET    /api/v1/recommendations/similar/{item_id}  # Similar items
```

**Technology Stack:**
- FastAPI, scikit-learn
- TensorFlow/PyTorch (optional)
- Redis (cache)

**Estimated Time:** 55 hours ($8,250)

---

### 8. Chat Service (Port 8089)

**Purpose:** Real-time messaging with WebSocket

**Database Schema:**
```sql
CREATE TABLE conversations (
    id SERIAL PRIMARY KEY,
    conversation_id VARCHAR(255) UNIQUE NOT NULL,
    type VARCHAR(20) NOT NULL,  -- private, group
    name VARCHAR(100),
    created_by INTEGER NOT NULL,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE conversation_members (
    id SERIAL PRIMARY KEY,
    conversation_id INTEGER REFERENCES conversations(id),
    user_id INTEGER NOT NULL,
    role VARCHAR(20) DEFAULT 'member',  -- admin, member
    joined_at TIMESTAMP DEFAULT NOW(),
    last_read_at TIMESTAMP
);

CREATE TABLE messages (
    id SERIAL PRIMARY KEY,
    message_id VARCHAR(255) UNIQUE NOT NULL,
    conversation_id INTEGER REFERENCES conversations(id),
    sender_id INTEGER NOT NULL,
    content TEXT NOT NULL,
    message_type VARCHAR(20) DEFAULT 'text',  -- text, image, file
    attachments JSONB,
    is_edited BOOLEAN DEFAULT FALSE,
    is_deleted BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_messages_conversation ON messages(conversation_id);
CREATE INDEX idx_messages_created_at ON messages(created_at);
```

**API Endpoints:**
```
WS     /api/v1/chat/ws              # WebSocket connection

GET    /api/v1/chat/conversations   # List conversations
POST   /api/v1/chat/conversations   # Create conversation
GET    /api/v1/chat/conversations/{id}/messages  # Get messages
POST   /api/v1/chat/conversations/{id}/messages  # Send message
PATCH  /api/v1/chat/messages/{id}   # Edit message
DELETE /api/v1/chat/messages/{id}   # Delete message

POST   /api/v1/chat/conversations/{id}/members  # Add member
DELETE /api/v1/chat/conversations/{id}/members/{user_id}  # Remove
```

**Technology Stack:**
- FastAPI, WebSocket
- Redis (pub/sub)
- PostgreSQL

**Estimated Time:** 50 hours ($7,500)

---

## Summary Table

| Service | Port | Priority | Time | Cost | Dependencies |
|---------|------|----------|------|------|--------------|
| User Service | 8082 | HIGH | 40h | $6,000 | auth |
| Notification Service | 8083 | HIGH | 35h | $5,250 | auth, user |
| File Service | 8084 | HIGH | 45h | $6,750 | auth |
| Payment Service | 8085 | HIGH | 50h | $7,500 | auth, user |
| Search Service | 8086 | MEDIUM | 40h | $6,000 | user |
| Analytics Service | 8087 | MEDIUM | 45h | $6,750 | auth |
| Recommendation Service | 8088 | MEDIUM | 55h | $8,250 | user, analytics |
| Chat Service | 8089 | MEDIUM | 50h | $7,500 | auth, user |

---

**Last Updated:** 2025-11-07  
**Version:** 1.0.0  
**Maintainer:** Dr. Sarah Chen (Chief Architect)
