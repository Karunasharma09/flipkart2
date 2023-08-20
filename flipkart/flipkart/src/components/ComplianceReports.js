import React from 'react';

function ComplianceReports() {
  const fakeComplianceReport = `compliance_report.txt`; // Replace with actual report content

  const handleDownload = () => {
    const blob = new Blob([fakeComplianceReport], { type: 'text/plain' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = './downloads/compliance_report.txt'; // Change the filename as needed
    a.click();
    URL.revokeObjectURL(url);
  };

  return (
    <div className="section">
      <h2 className="text-xl font-semibold mb-4">Compliance Reports</h2>
      <button
        onClick={handleDownload}
        className="bg-green-500 text-white px-4 py-2 rounded hover:bg-green-600 transition"
      >
        Download Compliance Report
      </button>
    </div>
  );
}

export default ComplianceReports;
