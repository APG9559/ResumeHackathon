# Smart Resume Screener

An AI-powered web application that evaluates and ranks candidate resumes against job descriptions using natural language processing.

## Features

- **User Authentication**: Secure JWT-based authentication system
- **Resume Management**: Upload and manage candidate resumes (PDF, TXT)
- **Job Description Management**: Create, edit, and manage job descriptions
- **AI-Powered Evaluation**: NLP-based resume screening using spaCy and scikit-learn
- **Results Visualization**: View ranked candidates with fit scores and matching keywords
- **Export Functionality**: Export evaluation results to CSV
- **Responsive Design**: Works seamlessly on desktop, tablet, and mobile devices

## Tech Stack

### Backend
- Flask 3.x
- SQLAlchemy (SQLite)
- Flask-JWT-Extended
- Custom TF-IDF implementation (pure Python)
- PyPDF2 (PDF text extraction)

### Frontend
- React 18.x
- React Router
- Axios
- Tailwind CSS

## Setup Instructions

### Backend Setup

1. Navigate to the backend directory:
```bash
cd backend
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create .env file:
```bash
cp .env.example .env
```

5. Run the backend server:
```bash
python run.py
```

The backend API will be available at http://localhost:5000

### Frontend Setup

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Create .env file:
```bash
cp .env.example .env
```

4. Start the development server:
```bash
npm start
```

The frontend will be available at http://localhost:3000

## Usage

1. **Register/Login**: Create an account or login with existing credentials
2. **Upload Resumes**: Navigate to the Resumes page and upload candidate resumes
3. **Create Job Descriptions**: Go to the Jobs page and create job descriptions
4. **Evaluate**: Visit the Evaluation page, select a job, and click "Evaluate" to rank candidates
5. **View Results**: See ranked candidates with fit scores and matching keywords
6. **Export**: Download evaluation results as CSV for further analysis

## API Endpoints

### Authentication
- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - Login and get JWT token
- `GET /api/auth/me` - Get current user info

### Resumes
- `POST /api/resumes/upload` - Upload resume
- `GET /api/resumes` - List user's resumes
- `DELETE /api/resumes/<id>` - Delete resume

### Jobs
- `POST /api/jobs` - Create job description
- `GET /api/jobs` - List user's jobs
- `PUT /api/jobs/<id>` - Update job
- `DELETE /api/jobs/<id>` - Delete job

### Evaluation
- `POST /api/evaluate` - Evaluate resumes against job
- `GET /api/evaluate/<job_id>` - Get cached results

## Project Structure

```
smart-resume-screener/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── config.py
│   │   ├── models/
│   │   ├── routes/
│   │   └── utils/
│   ├── requirements.txt
│   └── run.py
├── frontend/
│   ├── public/
│   ├── src/
│   │   ├── components/
│   │   ├── context/
│   │   ├── pages/
│   │   ├── services/
│   │   └── App.js
│   └── package.json
└── README.md
```

## License

MIT
