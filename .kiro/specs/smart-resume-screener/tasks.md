# Implementation Plan

- [x] 1. Set up Flask backend project structure and dependencies




  - Create Flask application with proper directory structure (app/, models/, routes/, utils/)
  - Install and configure dependencies: Flask, Flask-JWT-Extended, Flask-CORS, SQLAlchemy, spaCy, scikit-learn, PyPDF2
  - Set up configuration management for development and production environments
  - Initialize SQLite database connection with SQLAlchemy
  - _Requirements: 1.1, 1.3_

- [x] 2. Implement database models and initialization


  - Create User model with email, password_hash, and timestamps
  - Create Resume model with user relationship, file metadata, and extracted text field
  - Create Job model with user relationship, title, description, and timestamps
  - Create Evaluation model for caching results with job/resume relationships and fit scores
  - Write database initialization script and migrations
  - _Requirements: 1.5, 2.3, 3.2_



- [ ] 3. Implement JWT authentication system
  - Create user registration endpoint with email validation and password hashing
  - Create login endpoint that generates JWT tokens with 24-hour expiration
  - Implement JWT token validation middleware for protected routes
  - Create endpoint to get current user information


  - Handle authentication errors (invalid credentials, expired tokens)
  - _Requirements: 1.1, 1.2, 1.3, 1.4, 1.5, 7.5_

- [ ] 4. Implement resume upload and management endpoints
  - Create file upload endpoint accepting PDF and TXT files with 5MB size limit
  - Implement text extraction from PDF using PyPDF2 and plain text files


  - Create endpoint to list user's uploaded resumes with metadata
  - Create endpoint to delete resumes with authorization check
  - Store files in designated upload directory with sanitized filenames
  - _Requirements: 2.1, 2.2, 2.3, 2.4, 2.5_



- [ ] 5. Implement job description management endpoints
  - Create endpoint to create new job descriptions with title and description
  - Create endpoint to list user's job descriptions
  - Create endpoint to update existing job descriptions with authorization check
  - Create endpoint to delete job descriptions with authorization check
  - _Requirements: 3.1, 3.2, 3.3, 3.4, 3.5_



- [ ] 6. Implement NLP evaluation engine
  - Set up spaCy NLP pipeline for text processing
  - Implement text preprocessing function (lowercase, tokenization, stopword removal)
  - Create TF-IDF vectorization using scikit-learn for resume and job description texts
  - Implement cosine similarity calculation to generate fit scores (0-100 scale)


  - Create keyword extraction function using spaCy for matching terms between resume and job
  - _Requirements: 4.2, 4.5_

- [ ] 7. Implement evaluation API endpoint
  - Create endpoint to trigger evaluation of all user resumes against selected job
  - Process resumes in batch and calculate fit scores using NLP engine


  - Store evaluation results in database with timestamps
  - Return sorted results by fit score in descending order
  - Implement performance optimization to handle up to 50 resumes within 30 seconds
  - _Requirements: 4.1, 4.2, 4.3, 4.4, 4.5_

- [ ] 8. Set up React frontend project structure
  - Initialize React application with Create React App or Vite

  - Install dependencies: React Router, Axios, Tailwind CSS
  - Set up project directory structure (components/, pages/, context/, services/, utils/)
  - Configure Tailwind CSS for styling
  - Create base layout components and routing structure
  - _Requirements: 6.1, 6.4_

- [ ] 9. Implement authentication context and API service
  - Create AuthContext for global authentication state management
  - Implement login and logout functions in context
  - Create Axios instance with JWT token interceptor for automatic header injection
  - Implement token storage and retrieval from localStorage
  - Create API service functions for all backend endpoints
  - Handle token expiration with automatic redirect to login
  - _Requirements: 1.1, 1.4, 7.1, 7.2, 7.3, 7.4, 7.5_

- [x] 10. Build authentication UI components

  - Create LoginPage with email/password form and validation
  - Create RegisterPage with registration form and password confirmation
  - Implement form validation and error display
  - Add loading states during authentication requests
  - Implement PrivateRoute component for protected routes
  - Add redirect to dashboard after successful login
  - _Requirements: 1.1, 1.2, 1.4, 1.5, 6.2, 6.5_

- [x] 11. Build dashboard layout and navigation


  - Create DashboardLayout component with navigation bar and sidebar
  - Implement logout functionality in navigation
  - Add routing for different dashboard sections (resumes, jobs, evaluation, results)
  - Display current user information in header
  - Implement responsive layout for mobile and desktop views
  - _Requirements: 6.1, 6.2, 6.4, 7.2, 7.3_



- [ ] 12. Build resume upload and management UI
  - Create ResumeUpload component with drag-and-drop file upload
  - Implement file type validation (PDF, TXT only) on client side
  - Add upload progress indicator and loading states
  - Create resume list component displaying uploaded resumes with metadata
  - Implement delete functionality with confirmation dialog
  - Add error handling for upload failures and file size exceeded

  - _Requirements: 2.1, 2.2, 2.4, 2.5, 6.2, 6.3, 6.5_

- [x] 13. Build job description management UI

  - Create job creation form with title and description fields
  - Create job list component with edit and delete actions
  - Implement job edit modal with pre-filled form
  - Add delete confirmation dialog
  - Display creation and update timestamps
  - Add form validation and error handling
  - _Requirements: 3.1, 3.2, 3.3, 3.4, 3.5, 6.2, 6.5_

- [x] 14. Build evaluation and results UI


  - Create evaluation panel with job selection dropdown
  - Implement "Evaluate" button with loading state during processing
  - Create ResultsView component displaying ranked candidates with fit scores
  - Add visual score indicators (progress bars or badges)
  - Implement expandable detail view showing matching keywords
  - Add keyword highlighting in resume text
  - Implement filter by minimum fit score threshold
  - Create CSV export functionality for results
  - _Requirements: 4.1, 4.3, 4.4, 5.1, 5.2, 5.3, 5.4, 5.5, 6.2, 6.3_

- [x] 15. Implement error handling and user feedback


  - Add toast notification system for API errors and success messages
  - Implement error boundaries for component crash handling
  - Add inline validation errors for all forms
  - Create user-friendly error messages for common scenarios
  - Implement loading indicators for all async operations
  - Add session expiration handling with redirect to login
  - _Requirements: 6.2, 6.3, 6.5, 7.4, 7.5_

- [x] 16. Implement session persistence and token management


  - Store JWT token in localStorage on successful login
  - Restore authentication state on page refresh by validating stored token
  - Clear token from localStorage on logout
  - Implement automatic logout when token expires
  - Add token refresh logic if needed for extended sessions
  - _Requirements: 7.1, 7.2, 7.3, 7.4, 7.5_

- [x] 17. Add responsive design and UI polish


  - Ensure all components adapt to screen widths from 320px to 2560px
  - Test and fix layout issues on mobile, tablet, and desktop
  - Add consistent spacing, colors, and typography using Tailwind
  - Implement smooth transitions and animations for better UX
  - Add empty states for lists (no resumes, no jobs, no results)
  - Optimize page load performance and render times
  - _Requirements: 6.1, 6.2, 6.4_

- [ ]* 18. Write backend tests
  - Write unit tests for authentication functions (password hashing, token generation)
  - Write unit tests for NLP functions (text extraction, similarity calculation)
  - Write integration tests for all API endpoints using Flask test client
  - Write tests for JWT authentication flow and authorization
  - Write tests for file upload and text extraction
  - Write tests for evaluation workflow with mock data
  - _Requirements: All_

- [ ]* 19. Write frontend tests
  - Write component tests for authentication forms
  - Write tests for file upload component
  - Write tests for results display and filtering
  - Write integration tests for API calls using MSW
  - Write tests for authentication state management
  - Write tests for route navigation and PrivateRoute
  - _Requirements: All_

- [x] 20. Configure CORS and integrate frontend with backend



  - Configure Flask-CORS to allow requests from React frontend origin
  - Set up environment variables for API URL in React app
  - Test all API integrations end-to-end
  - Verify JWT token flow between frontend and backend
  - Test file upload with actual PDF and TXT files
  - Verify evaluation results display correctly
  - _Requirements: 1.3, 2.1, 4.1, 6.5_
