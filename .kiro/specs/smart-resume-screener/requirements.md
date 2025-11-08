# Requirements Document

## Introduction

The Smart Resume Screener is a web application that enables recruiters and hiring managers to evaluate and rank candidate resumes against job descriptions using AI-powered natural language processing. The system provides secure access through JWT authentication, allowing users to upload resumes, define job requirements, and receive ranked candidate recommendations based on fit scores.

## Glossary

- **Resume Screener System**: The complete web application including frontend, backend API, and NLP processing components
- **User**: A recruiter or hiring manager who uses the system to evaluate candidates
- **Resume**: A PDF or text document containing a candidate's qualifications and experience
- **Job Description**: Text defining the requirements, skills, and qualifications for a position
- **Fit Score**: A numerical value between 0 and 100 representing how well a resume matches a job description
- **JWT (JSON Web Token)**: A secure token used for authenticating API requests
- **NLP Engine**: The natural language processing component that analyzes and compares text

## Requirements

### Requirement 1: User Authentication

**User Story:** As a recruiter, I want to securely log in to the system, so that my resume data and evaluations are protected.

#### Acceptance Criteria

1. WHEN a User submits valid credentials, THE Resume Screener System SHALL generate a JWT token with an expiration time of 24 hours.
2. WHEN a User submits invalid credentials, THE Resume Screener System SHALL return an authentication error within 2 seconds.
3. THE Resume Screener System SHALL validate the JWT token on every protected API request.
4. WHEN a JWT token expires, THE Resume Screener System SHALL return an unauthorized error and prompt for re-authentication.
5. THE Resume Screener System SHALL allow a User to register a new account with email and password.

### Requirement 2: Resume Upload and Management

**User Story:** As a recruiter, I want to upload multiple candidate resumes, so that I can evaluate them against job descriptions.

#### Acceptance Criteria

1. THE Resume Screener System SHALL accept resume uploads in PDF and TXT formats with a maximum file size of 5 megabytes.
2. WHEN a User uploads a resume, THE Resume Screener System SHALL extract text content within 5 seconds.
3. THE Resume Screener System SHALL store uploaded resumes with metadata including filename, upload timestamp, and extracted text.
4. THE Resume Screener System SHALL allow a User to view a list of all uploaded resumes.
5. THE Resume Screener System SHALL allow a User to delete uploaded resumes.

### Requirement 3: Job Description Management

**User Story:** As a recruiter, I want to create and save job descriptions, so that I can reuse them for evaluating multiple candidate batches.

#### Acceptance Criteria

1. THE Resume Screener System SHALL allow a User to create a job description with a title and description text.
2. THE Resume Screener System SHALL store job descriptions with metadata including title, creation timestamp, and description text.
3. THE Resume Screener System SHALL allow a User to view a list of all saved job descriptions.
4. THE Resume Screener System SHALL allow a User to edit existing job descriptions.
5. THE Resume Screener System SHALL allow a User to delete job descriptions.

### Requirement 4: Resume Evaluation and Ranking

**User Story:** As a recruiter, I want to evaluate uploaded resumes against a job description, so that I can identify the best-fit candidates quickly.

#### Acceptance Criteria

1. WHEN a User initiates an evaluation, THE Resume Screener System SHALL process all uploaded resumes against the selected job description.
2. THE Resume Screener System SHALL calculate a Fit Score between 0 and 100 for each resume using the NLP Engine.
3. THE Resume Screener System SHALL complete evaluation of up to 50 resumes within 30 seconds.
4. THE Resume Screener System SHALL return results sorted by Fit Score in descending order.
5. THE Resume Screener System SHALL display key matching skills and qualifications for each evaluated resume.

### Requirement 5: Results Visualization

**User Story:** As a recruiter, I want to view evaluation results in an intuitive interface, so that I can make informed hiring decisions.

#### Acceptance Criteria

1. THE Resume Screener System SHALL display evaluated candidates in a ranked list with Fit Score prominently shown.
2. THE Resume Screener System SHALL allow a User to view detailed match analysis for each candidate.
3. THE Resume Screener System SHALL highlight matching keywords between the resume and job description.
4. THE Resume Screener System SHALL allow a User to filter results by minimum Fit Score threshold.
5. THE Resume Screener System SHALL allow a User to export evaluation results as a CSV file.

### Requirement 6: User Interface Responsiveness

**User Story:** As a recruiter, I want a responsive and intuitive interface, so that I can use the system efficiently on different devices.

#### Acceptance Criteria

1. THE Resume Screener System SHALL render the user interface within 2 seconds of page load.
2. THE Resume Screener System SHALL provide visual feedback within 500 milliseconds for all user interactions.
3. THE Resume Screener System SHALL display loading indicators during file uploads and evaluations.
4. THE Resume Screener System SHALL adapt the layout for screen widths between 320 pixels and 2560 pixels.
5. WHEN an API error occurs, THE Resume Screener System SHALL display a user-friendly error message.

### Requirement 7: Session Management

**User Story:** As a recruiter, I want my session to persist across page refreshes, so that I don't lose my work.

#### Acceptance Criteria

1. THE Resume Screener System SHALL store the JWT token in browser local storage upon successful authentication.
2. WHEN a User refreshes the page, THE Resume Screener System SHALL restore the authenticated session if the JWT token is valid.
3. WHEN a User logs out, THE Resume Screener System SHALL remove the JWT token from local storage.
4. THE Resume Screener System SHALL redirect unauthenticated Users to the login page when accessing protected routes.
5. THE Resume Screener System SHALL automatically log out a User when the JWT token expires.
