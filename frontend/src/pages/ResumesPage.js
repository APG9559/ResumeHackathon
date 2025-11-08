import React, { useState, useEffect } from 'react';
import { resumeAPI } from '../services/api';

const ResumesPage = () => {
  const [resumes, setResumes] = useState([]);
  const [loading, setLoading] = useState(false);
  const [uploading, setUploading] = useState(false);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  const [dragActive, setDragActive] = useState(false);

  useEffect(() => {
    fetchResumes();
  }, []);

  const fetchResumes = async () => {
    setLoading(true);
    try {
      const response = await resumeAPI.getAll();
      setResumes(response.data);
    } catch (err) {
      setError(err.response?.data?.message || 'Failed to fetch resumes');
    } finally {
      setLoading(false);
    }
  };

  const handleFileUpload = async (file) => {
    if (!file) return;

    const allowedTypes = ['application/pdf', 'text/plain'];
    if (!allowedTypes.includes(file.type)) {
      setError('Only PDF and TXT files are allowed');
      return;
    }

    if (file.size > 5 * 1024 * 1024) {
      setError('File size must be less than 5MB');
      return;
    }

    setUploading(true);
    setError('');
    setSuccess('');

    try {
      await resumeAPI.upload(file);
      setSuccess('Resume uploaded successfully!');
      fetchResumes();
    } catch (err) {
      setError(err.response?.data?.message || 'Failed to upload resume');
    } finally {
      setUploading(false);
    }
  };

  const handleFileChange = (e) => {
    const file = e.target.files[0];
    handleFileUpload(file);
  };

  const handleDrag = (e) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === 'dragenter' || e.type === 'dragover') {
      setDragActive(true);
    } else if (e.type === 'dragleave') {
      setDragActive(false);
    }
  };

  const handleDrop = (e) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);
    
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      handleFileUpload(e.dataTransfer.files[0]);
    }
  };

  const handleDelete = async (id) => {
    if (!window.confirm('Are you sure you want to delete this resume?')) return;

    try {
      await resumeAPI.delete(id);
      setSuccess('Resume deleted successfully!');
      fetchResumes();
    } catch (err) {
      setError(err.response?.data?.message || 'Failed to delete resume');
    }
  };

  return (
    <div className="px-4 py-6">
      <h2 className="text-2xl font-bold text-gray-800 mb-6">Resume Management</h2>

      {error && (
        <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-4">
          {error}
        </div>
      )}

      {success && (
        <div className="bg-green-100 border border-green-400 text-green-700 px-4 py-3 rounded mb-4">
          {success}
        </div>
      )}

      <div
        className={`border-2 border-dashed rounded-lg p-8 mb-6 text-center ${
          dragActive ? 'border-blue-500 bg-blue-50' : 'border-gray-300'
        }`}
        onDragEnter={handleDrag}
        onDragLeave={handleDrag}
        onDragOver={handleDrag}
        onDrop={handleDrop}
      >
        <input
          type="file"
          id="file-upload"
          className="hidden"
          accept=".pdf,.txt"
          onChange={handleFileChange}
          disabled={uploading}
        />
        <label htmlFor="file-upload" className="cursor-pointer">
          <div className="text-gray-600">
            {uploading ? (
              <p className="text-lg">Uploading...</p>
            ) : (
              <>
                <p className="text-lg mb-2">Drag and drop your resume here, or click to browse</p>
                <p className="text-sm text-gray-500">Supported formats: PDF, TXT (Max 5MB)</p>
              </>
            )}
          </div>
        </label>
      </div>

      <div className="bg-white shadow-md rounded-lg overflow-hidden">
        <div className="px-6 py-4 border-b border-gray-200">
          <h3 className="text-lg font-semibold text-gray-800">Uploaded Resumes</h3>
        </div>
        
        {loading ? (
          <div className="p-6 text-center text-gray-600">Loading...</div>
        ) : resumes.length === 0 ? (
          <div className="p-6 text-center text-gray-600">No resumes uploaded yet</div>
        ) : (
          <ul className="divide-y divide-gray-200">
            {resumes.map((resume) => (
              <li key={resume.id} className="px-6 py-4 flex justify-between items-center hover:bg-gray-50">
                <div>
                  <p className="text-sm font-medium text-gray-900">{resume.filename}</p>
                  <p className="text-sm text-gray-500">
                    Uploaded: {new Date(resume.uploaded_at).toLocaleDateString()}
                  </p>
                </div>
                <button
                  onClick={() => handleDelete(resume.id)}
                  className="text-red-600 hover:text-red-800 text-sm font-medium"
                >
                  Delete
                </button>
              </li>
            ))}
          </ul>
        )}
      </div>
    </div>
  );
};

export default ResumesPage;
