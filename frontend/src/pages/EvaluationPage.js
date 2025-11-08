import React, { useState, useEffect } from 'react';
import { jobAPI, evaluationAPI } from '../services/api';

const EvaluationPage = () => {
  const [jobs, setJobs] = useState([]);
  const [selectedJobId, setSelectedJobId] = useState('');
  const [results, setResults] = useState(null);
  const [loading, setLoading] = useState(false);
  const [evaluating, setEvaluating] = useState(false);
  const [error, setError] = useState('');
  const [minScore, setMinScore] = useState(0);
  const [expandedId, setExpandedId] = useState(null);

  useEffect(() => {
    fetchJobs();
  }, []);

  const fetchJobs = async () => {
    setLoading(true);
    try {
      const response = await jobAPI.getAll();
      setJobs(response.data);
    } catch (err) {
      setError(err.response?.data?.message || 'Failed to fetch jobs');
    } finally {
      setLoading(false);
    }
  };

  const handleEvaluate = async () => {
    if (!selectedJobId) {
      setError('Please select a job description');
      return;
    }

    setEvaluating(true);
    setError('');
    try {
      const response = await evaluationAPI.evaluate(selectedJobId);
      setResults(response.data);
    } catch (err) {
      setError(err.response?.data?.message || 'Failed to evaluate resumes');
    } finally {
      setEvaluating(false);
    }
  };

  const exportToCSV = () => {
    if (!results || !results.results) return;

    const headers = ['Filename', 'Fit Score', 'Matching Keywords'];
    const rows = results.results.map(r => [
      r.filename,
      r.fit_score,
      r.matching_keywords.join('; ')
    ]);

    const csvContent = [
      headers.join(','),
      ...rows.map(row => row.map(cell => `"${cell}"`).join(','))
    ].join('\n');

    const blob = new Blob([csvContent], { type: 'text/csv' });
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `evaluation_${results.job_title}_${new Date().toISOString().split('T')[0]}.csv`;
    a.click();
    window.URL.revokeObjectURL(url);
  };

  const filteredResults = results?.results.filter(r => r.fit_score >= minScore) || [];

  const getScoreColor = (score) => {
    if (score >= 75) return 'bg-green-500';
    if (score >= 50) return 'bg-yellow-500';
    return 'bg-red-500';
  };

  return (
    <div className="px-4 py-6">
      <h2 className="text-2xl font-bold text-gray-800 mb-6">Resume Evaluation</h2>

      {error && (
        <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-4">
          {error}
        </div>
      )}

      <div className="bg-white shadow-md rounded-lg p-6 mb-6">
        <div className="flex items-end space-x-4">
          <div className="flex-1">
            <label className="block text-gray-700 text-sm font-bold mb-2">
              Select Job Description
            </label>
            <select
              value={selectedJobId}
              onChange={(e) => setSelectedJobId(e.target.value)}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              disabled={evaluating}
            >
              <option value="">-- Select a job --</option>
              {jobs.map((job) => (
                <option key={job.id} value={job.id}>
                  {job.title}
                </option>
              ))}
            </select>
          </div>
          <button
            onClick={handleEvaluate}
            disabled={evaluating || !selectedJobId}
            className="bg-blue-600 text-white px-6 py-2 rounded-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {evaluating ? 'Evaluating...' : 'Evaluate'}
          </button>
        </div>
      </div>

      {results && (
        <div className="bg-white shadow-md rounded-lg overflow-hidden">
          <div className="px-6 py-4 border-b border-gray-200 flex justify-between items-center">
            <div>
              <h3 className="text-lg font-semibold text-gray-800">
                Results for: {results.job_title}
              </h3>
              <p className="text-sm text-gray-600">
                {filteredResults.length} candidate(s) found
              </p>
            </div>
            <div className="flex items-center space-x-4">
              <div className="flex items-center space-x-2">
                <label className="text-sm text-gray-700">Min Score:</label>
                <input
                  type="number"
                  min="0"
                  max="100"
                  value={minScore}
                  onChange={(e) => setMinScore(Number(e.target.value))}
                  className="w-20 px-2 py-1 border border-gray-300 rounded-md text-sm"
                />
              </div>
              <button
                onClick={exportToCSV}
                className="bg-green-600 text-white px-4 py-2 rounded-md text-sm hover:bg-green-700"
              >
                Export CSV
              </button>
            </div>
          </div>

          {filteredResults.length === 0 ? (
            <div className="p-6 text-center text-gray-600">
              No candidates match the minimum score filter
            </div>
          ) : (
            <ul className="divide-y divide-gray-200">
              {filteredResults.map((result, index) => (
                <li key={result.resume_id} className="px-6 py-4 hover:bg-gray-50">
                  <div className="flex items-center justify-between">
                    <div className="flex-1">
                      <div className="flex items-center space-x-3">
                        <span className="text-lg font-bold text-gray-700">#{index + 1}</span>
                        <div>
                          <p className="text-sm font-medium text-gray-900">{result.filename}</p>
                          <p className="text-xs text-gray-500">
                            Evaluated: {new Date(result.evaluated_at).toLocaleString()}
                          </p>
                        </div>
                      </div>
                    </div>
                    <div className="flex items-center space-x-4">
                      <div className="text-right">
                        <div className="text-2xl font-bold text-gray-900">{result.fit_score}%</div>
                        <div className="w-32 bg-gray-200 rounded-full h-2 mt-1">
                          <div
                            className={`h-2 rounded-full ${getScoreColor(result.fit_score)}`}
                            style={{ width: `${result.fit_score}%` }}
                          />
                        </div>
                      </div>
                      <button
                        onClick={() => setExpandedId(expandedId === result.resume_id ? null : result.resume_id)}
                        className="text-blue-600 hover:text-blue-800 text-sm font-medium"
                      >
                        {expandedId === result.resume_id ? 'Hide' : 'Details'}
                      </button>
                    </div>
                  </div>
                  
                  {expandedId === result.resume_id && (
                    <div className="mt-4 p-4 bg-gray-50 rounded-md">
                      <h4 className="text-sm font-semibold text-gray-700 mb-2">Matching Keywords:</h4>
                      <div className="flex flex-wrap gap-2">
                        {result.matching_keywords.length > 0 ? (
                          result.matching_keywords.map((keyword, idx) => (
                            <span
                              key={idx}
                              className="px-3 py-1 bg-blue-100 text-blue-800 text-sm rounded-full"
                            >
                              {keyword}
                            </span>
                          ))
                        ) : (
                          <span className="text-sm text-gray-500">No matching keywords found</span>
                        )}
                      </div>
                    </div>
                  )}
                </li>
              ))}
            </ul>
          )}
        </div>
      )}
    </div>
  );
};

export default EvaluationPage;
