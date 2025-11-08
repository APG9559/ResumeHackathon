# Design Document: Smart Resume Screener

## Overview

The Smart Resume Screener is a full-stack web application with a Flask REST API backend and React frontend. The system uses JWT-based authentication to secure endpoints and leverages NLP libraries (spaCy, scikit-learn) for resume analysis. The architecture follows a clear separation between presentation (React), business logic (Flask), and data processing (NLP engine).

## Architecture

### High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     React Frontend (SPA)                     │
│  - Authentication UI  - Resume Upload  - Results Dashboard   │
└───────────────────────┬─────────────────────────────────────┘
                        │ HTTP/JSON + JWT
                        │
┌───────────────────────▼─────────────────────────────────────┐
│                    Flask REST API                            │
│  - JWT Auth Middleware  - Route Handlers  - Business Logic   │
└───────────────────────┬─────────────────────────────────────┘
                        │
        ┌───────────────┼───────────────┐
        │               │               │
┌───────▼──────┐ ┌─────▼──────┐ ┌─────▼──────────┐
│   SQLite DB  │ │ File Storage│ │  NLP Engine    │
│  - Users     │ │  - Resumes  │ │  - spaCy       │
│  - Jobs      │ │             │ │  - TF-IDF      │
│  - Resumes   │ │             │ │  - Similarity   │
└──────────────┘ └─────────────┘ └────────────────┘
```

### Technology Stack

**Backend:**
- Flask 3.x (Web framework)
- Flask-JWT-Extended (JWT authentication)
- Flask-CORS (Cross-origin resource sharing)
- SQLAlchemy (ORM)
- SQLite (Database)
- spaCy (NLP processing)
- scikit-learn (TF-IDF vectorization, cosine similarity)
- PyPDF2 (PDF text extraction)
- Werkzeug (Password hashing)

**Frontend:**
- React 18.x (UI framework)
- React Router (Client-side routing)
- Axios (HTTP client)
- Tailwind CSS (Styling)
- React Context API (State management)

## Components and Interfaces

### Backend Components

#### 1. Authentication Module (`auth.py`)

**Responsibilities:**
- User registration and login
- Password hashing and verification
- JWT token generation and validation

**Key Functions:**
```python
register_user(email: str, password: str) -> dict
login_user(email: str, password: str) -> dict  # Returns JWT token
verify_token(token: str) -> dict  # Returns user identity
```

**API Endpoints:**
- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - Authenticate and receive JWT
- `GET /api/auth/me` - Get current user info (protected)

#### 2. Resume Module (`resumes.py`)

**Responsibilities:**
- Resume file upload and storage
- Text extraction from PDF/TXT
- Resume metadata management

**Key Functions:**
```python
upload_resume(file: FileStorage, user_id: int) -> dict
extract_text(file_path: str, file_type: str) -> str
get_user_resumes(user_id: int) -> list
delete_resume(resume_id: int, user_id: int) -> bool
```

**API Endpoints:**
- `POST /api/resumes/upload` - Upload resume file (protected)
- `GET /api/resumes` - List user's resumes (protected)
- `DELETE /api/resumes/<id>` - Delete resume (protected)

#### 3. Job Description Module (`jobs.py`)

**Responsibilities:**
- Job description CRUD operations
- Job metadata management

**Key Functions:**
```python
create_job(title: str, description: str, user_id: int) -> dict
get_user_jobs(user_id: int) -> list
update_job(job_id: int, title: str, description: str, user_id: int) -> dict
delete_job(job_id: int, user_id: int) -> bool
```

**API Endpoints:**
- `POST /api/jobs` - Create job description (protected)
- `GET /api/jobs` - List user's jobs (protected)
- `PUT /api/jobs/<id>` - Update job description (protected)
- `DELETE /api/jobs/<id>` - Delete job description (protected)

#### 4. Evaluation Module (`evaluation.py`)

**Responsibilities:**
- Resume-to-job matching using NLP
- Fit score calculation
- Keyword extraction and highlighting

**Key Functions:**
```python
evaluate_resumes(job_id: int, user_id: int) -> list
calculate_fit_score(resume_text: str, job_text: str) -> float
extract_matching_keywords(resume_text: str, job_text: str) -> list
```

**NLP Processing Pipeline:**
1. Text preprocessing (lowercase, tokenization, stopword removal)
2. TF-IDF vectorization of resume and job description
3. Cosine similarity calculation (0-1 scale, converted to 0-100)
4. Keyword extraction using spaCy NER and noun phrase chunking
5. Match highlighting based on common tokens

**API Endpoints:**
- `POST /api/evaluate` - Evaluate all resumes against a job (protected)
- `GET /api/evaluate/<job_id>` - Get cached evaluation results (protected)

#### 5. Database Models (`models.py`)

**User Model:**
```python
class User:
    id: int (primary key)
    email: str (unique, indexed)
    password_hash: str
    created_at: datetime
```

**Resume Model:**
```python
class Resume:
    id: int (primary key)
    user_id: int (foreign key)
    filename: str
    file_path: str
    extracted_text: text
    uploaded_at: datetime
```

**Job Model:**
```python
class Job:
    id: int (primary key)
    user_id: int (foreign key)
    title: str
    description: text
    created_at: datetime
    updated_at: datetime
```

**Evaluation Model (cached results):**
```python
class Evaluation:
    id: int (primary key)
    job_id: int (foreign key)
    resume_id: int (foreign key)
    fit_score: float
    matching_keywords: json
    evaluated_at: datetime
```

### Frontend Components

#### 1. Authentication Components

**LoginPage:**
- Email/password form
- Form validation
- JWT token storage in localStorage
- Redirect to dashboard on success

**RegisterPage:**
- Registration form with email/password
- Password confirmation
- Error handling

**PrivateRoute:**
- Route wrapper that checks JWT validity
- Redirects to login if unauthenticated

#### 2. Dashboard Components

**DashboardLayout:**
- Navigation bar with logout
- Sidebar for navigation
- Main content area

**ResumeUpload:**
- Drag-and-drop file upload
- File type validation (PDF, TXT)
- Upload progress indicator
- Resume list display

**JobManager:**
- Job creation form
- Job list with edit/delete actions
- Job selection for evaluation

**EvaluationPanel:**
- Job selection dropdown
- "Evaluate" button
- Loading state during processing

**ResultsView:**
- Ranked candidate list with fit scores
- Score visualization (progress bars/badges)
- Expandable detail view per candidate
- Keyword highlighting
- Filter by minimum score
- Export to CSV button

#### 3. Shared Components

**AuthContext:**
- Global authentication state
- Login/logout functions
- Token management
- User info

**API Service (`api.js`):**
- Axios instance with JWT interceptor
- Centralized API calls
- Error handling

## Data Models

### Request/Response Formats

**Authentication:**
```json
// POST /api/auth/register
Request: { "email": "user@example.com", "password": "securepass" }
Response: { "message": "User registered successfully", "user_id": 1 }

// POST /api/auth/login
Request: { "email": "user@example.com", "password": "securepass" }
Response: { "access_token": "eyJ0eXAi...", "user": { "id": 1, "email": "user@example.com" } }
```

**Resume Upload:**
```json
// POST /api/resumes/upload (multipart/form-data)
Response: {
  "id": 1,
  "filename": "john_doe_resume.pdf",
  "uploaded_at": "2025-11-08T10:30:00Z",
  "text_preview": "John Doe\nSoftware Engineer..."
}

// GET /api/resumes
Response: [
  {
    "id": 1,
    "filename": "john_doe_resume.pdf",
    "uploaded_at": "2025-11-08T10:30:00Z"
  }
]
```

**Job Management:**
```json
// POST /api/jobs
Request: {
  "title": "Senior Python Developer",
  "description": "We are seeking an experienced Python developer..."
}
Response: {
  "id": 1,
  "title": "Senior Python Developer",
  "description": "We are seeking...",
  "created_at": "2025-11-08T10:35:00Z"
}
```

**Evaluation:**
```json
// POST /api/evaluate
Request: { "job_id": 1 }
Response: {
  "job_id": 1,
  "job_title": "Senior Python Developer",
  "results": [
    {
      "resume_id": 1,
      "filename": "john_doe_resume.pdf",
      "fit_score": 87.5,
      "matching_keywords": ["Python", "Flask", "REST API", "PostgreSQL"],
      "evaluated_at": "2025-11-08T10:40:00Z"
    },
    {
      "resume_id": 2,
      "filename": "jane_smith_resume.pdf",
      "fit_score": 72.3,
      "matching_keywords": ["Python", "Django", "API"],
      "evaluated_at": "2025-11-08T10:40:00Z"
    }
  ]
}
```

## Error Handling

### Backend Error Responses

All errors follow a consistent format:
```json
{
  "error": "Error type",
  "message": "Human-readable error message"
}
```

**HTTP Status Codes:**
- 400: Bad Request (validation errors, invalid input)
- 401: Unauthorized (missing/invalid JWT)
- 403: Forbidden (insufficient permissions)
- 404: Not Found (resource doesn't exist)
- 413: Payload Too Large (file size exceeded)
- 500: Internal Server Error (unexpected errors)

**JWT Error Handling:**
- Expired tokens return 401 with message "Token has expired"
- Invalid tokens return 401 with message "Invalid token"
- Missing tokens return 401 with message "Authorization required"

### Frontend Error Handling

**Error Display:**
- Toast notifications for API errors
- Inline form validation errors
- Error boundaries for component crashes

**Token Expiration:**
- Intercept 401 responses
- Clear localStorage
- Redirect to login page
- Display "Session expired" message

## Testing Strategy

### Backend Testing

**Unit Tests:**
- Authentication functions (password hashing, token generation)
- NLP functions (text extraction, similarity calculation)
- Database model operations

**Integration Tests:**
- API endpoint testing with test client
- JWT authentication flow
- File upload and processing
- End-to-end evaluation workflow

**Test Tools:**
- pytest for test framework
- Flask test client for API testing
- Mock file uploads for resume testing

### Frontend Testing

**Component Tests:**
- Form validation logic
- Authentication flow
- File upload component
- Results display and filtering

**Integration Tests:**
- API integration with mock backend
- Route navigation
- Authentication state management

**Test Tools:**
- Jest for test runner
- React Testing Library for component tests
- MSW (Mock Service Worker) for API mocking

### Manual Testing Checklist

- [ ] User registration and login flow
- [ ] JWT token persistence across page refresh
- [ ] Resume upload (PDF and TXT)
- [ ] Job description CRUD operations
- [ ] Evaluation with multiple resumes
- [ ] Results sorting and filtering
- [ ] CSV export functionality
- [ ] Responsive design on mobile/tablet/desktop
- [ ] Error handling for network failures
- [ ] Token expiration and re-authentication

## Security Considerations

**Authentication:**
- Passwords hashed using Werkzeug's pbkdf2:sha256
- JWT tokens with 24-hour expiration
- Secure token storage in httpOnly cookies (alternative to localStorage)

**Authorization:**
- All protected endpoints verify JWT
- User can only access their own resumes/jobs/evaluations
- Database queries filtered by user_id

**File Upload Security:**
- File type validation (whitelist: PDF, TXT)
- File size limit (5MB)
- Sanitized filenames to prevent path traversal
- Files stored outside web root

**CORS Configuration:**
- Whitelist frontend origin only
- Credentials allowed for JWT cookies

## Deployment Considerations

**Backend:**
- Environment variables for secrets (JWT_SECRET_KEY, DATABASE_URL)
- Production WSGI server (Gunicorn)
- File storage on persistent volume
- Database migrations with Flask-Migrate

**Frontend:**
- Build optimization (code splitting, minification)
- Environment-specific API URLs
- Static file serving via CDN

**Infrastructure:**
- Backend and frontend can be deployed separately
- Backend: Heroku, AWS EC2, DigitalOcean
- Frontend: Vercel, Netlify, S3 + CloudFront
