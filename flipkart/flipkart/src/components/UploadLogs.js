import React, { useState } from 'react';
import ComplianceReports from './ComplianceReports';
import axios from 'axios';

function UploadLogs() {
  const [selectedFile, setSelectedFile] = useState(null);
  const [selectedFileType, setSelectedFileType] = useState('.txt');
  const [uploadStatus, setUploadStatus] = useState('');

  const handleFileChange = (event) => {
    setSelectedFile(event.target.files[0]);
  };

  const handleUpload = async() => {
    if (!selectedFile) {
      setUploadStatus('Please select a file.');
      return;
    }

    // You can add code here to send the file to the server for processing
    // and handle the server's response.
    const formData = new FormData();
    formData.append('file', selectedFile);

    try {
      const response = await axios.post('/api/process_input_data', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
      setUploadStatus('File uploaded successfully.');
    } catch (error) {
      console.error('Error uploading file:', error);
    }
    
  };

  return (
    <div className="section">
      <h2 className="text-xl font-semibold mb-4">Upload Logs</h2>
      <div className='py-10 flex justify-evenly'>
      
      <div className="flex space-x-28 pt-20">
      <div className="mt-4">
        <label className="block font-semibold mb-2">Select File Type:</label>
        <select
          value={selectedFileType}
          onChange={(e) => setSelectedFileType(e.target.value)}
          className="border rounded py-1 px-2 text-gray-600 bg-gray-100 focus:outline-none focus:border-blue-400"
        >
          <option value=".txt">text</option>
          <option value=".csv">csv</option>
          <option value=".json">json</option>
          <option value=".pdf">pdf</option>
        </select>
      </div>
        <input
          type="file"
          accept={selectedFileType}
          onChange={handleFileChange}
          className="border rounded py-2 px-4 w-2/3 text-gray-600  focus:outline-none focus:border-blue-400"
        />
        <button
          onClick={handleUpload}
          className="bg-blue-500 text-white px-6 py-2 rounded hover:bg-blue-600 transition"
        >
          Upload
        </button>
      </div>
      </div>
      {uploadStatus && (
        <p className="text-red-500 mt-2">
          {uploadStatus}
        </p>
      )}
      
      <div className="mt-8 w-2/4  mx-auto">
      <button
          className="bg-green-500 w-full  text-white px-6 py-2 rounded hover:bg-blue-600 transition"
        >Generate Compliance Report</button>
      </div>
    </div>
  );
}

export default UploadLogs;
