import React from 'react';
import { Routes, Route, Link, useLocation } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import ResumesPage from '../pages/ResumesPage';
import JobsPage from '../pages/JobsPage';
import EvaluationPage from '../pages/EvaluationPage';

const DashboardLayout = () => {
  const { user, logout } = useAuth();
  const location = useLocation();

  const isActive = (path) => {
    return location.pathname.includes(path);
  };

  return (
    <div className="min-h-screen bg-gray-100">
      <nav className="bg-white shadow-md">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex flex-col sm:flex-row justify-between h-auto sm:h-16 py-2 sm:py-0">
            <div className="flex flex-col sm:flex-row w-full sm:w-auto">
              <div className="flex-shrink-0 flex items-center mb-2 sm:mb-0">
                <h1 className="text-lg sm:text-xl font-bold text-gray-800">Smart Resume Screener</h1>
              </div>
              <div className="flex sm:ml-6 space-x-4 sm:space-x-8">
                <Link
                  to="/dashboard/resumes"
                  className={`inline-flex items-center px-1 pt-1 border-b-2 text-sm font-medium ${
                    isActive('/resumes')
                      ? 'border-blue-500 text-gray-900'
                      : 'border-transparent text-gray-500 hover:border-gray-300 hover:text-gray-700'
                  }`}
                >
                  Resumes
                </Link>
                <Link
                  to="/dashboard/jobs"
                  className={`inline-flex items-center px-1 pt-1 border-b-2 text-sm font-medium ${
                    isActive('/jobs')
                      ? 'border-blue-500 text-gray-900'
                      : 'border-transparent text-gray-500 hover:border-gray-300 hover:text-gray-700'
                  }`}
                >
                  Jobs
                </Link>
                <Link
                  to="/dashboard/evaluation"
                  className={`inline-flex items-center px-1 pt-1 border-b-2 text-sm font-medium ${
                    isActive('/evaluation')
                      ? 'border-blue-500 text-gray-900'
                      : 'border-transparent text-gray-500 hover:border-gray-300 hover:text-gray-700'
                  }`}
                >
                  Evaluation
                </Link>
              </div>
            </div>
            <div className="flex items-center mt-2 sm:mt-0 justify-between sm:justify-end w-full sm:w-auto">
              <span className="text-sm sm:text-base text-gray-700 mr-2 sm:mr-4 truncate max-w-[150px] sm:max-w-none">{user?.email}</span>
              <button
                onClick={logout}
                className="bg-red-600 text-white px-3 sm:px-4 py-1.5 sm:py-2 rounded-md text-xs sm:text-sm font-medium hover:bg-red-700 focus:outline-none focus:ring-2 focus:ring-red-500"
              >
                Logout
              </button>
            </div>
          </div>
        </div>
      </nav>

      <main className="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
        <Routes>
          <Route path="/" element={<ResumesPage />} />
          <Route path="/resumes" element={<ResumesPage />} />
          <Route path="/jobs" element={<JobsPage />} />
          <Route path="/evaluation" element={<EvaluationPage />} />
        </Routes>
      </main>
    </div>
  );
};

export default DashboardLayout;
