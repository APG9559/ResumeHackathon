# Smart Resume Screener - Backend

Flask REST API for the Smart Resume Screener application.

## Setup

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create .env file:
```bash
cp .env.example .env
```

4. Run the application:
```bash
python run.py
```

The API will be available at http://localhost:5000

## API Endpoints

### Authentication
- POST /api/auth/register - Register new user
- POST /api/auth/login - Login and get JWT token
- GET /api/auth/me - Get current user info (protected)

### Resumes
- POST /api/resumes/upload - Upload resume (protected)
- GET /api/resumes - List user's resumes (protected)
- DELETE /api/resumes/<id> - Delete resume (protected)

### Jobs
- POST /api/jobs - Create job description (protected)
- GET /api/jobs - List user's jobs (protected)
- PUT /api/jobs/<id> - Update job (protected)
- DELETE /api/jobs/<id> - Delete job (protected)

### Evaluation
- POST /api/evaluate - Evaluate resumes against job (protected)
- GET /api/evaluate/<job_id> - Get cached results (protected)
