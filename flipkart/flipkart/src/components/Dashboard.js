import React from 'react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';

function Dashboard({ totalComplianceBreaches, pendingActions, breachData }) {
  return (
    <div className="section">
      <h2 className="text-xl font-semibold mb-4">Dashboard</h2>
      <div className="grid grid-cols-2 gap-4">
        <div className="bg-white p-4 rounded shadow">
          <h3 className="text-lg font-semibold mb-2">Total Compliance Breaches</h3>
          <p className="text-gray-600">{totalComplianceBreaches} breaches detected</p>
        </div>
        {/* <div className="bg-white p-4 rounded shadow col-span-2">
          <h3 className="text-lg font-semibold mb-2">Breach Distribution</h3>
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={breachData} margin={{ top: 20, right: 30, left: 0, bottom: 20 }}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="name" />
              <YAxis />
              <Tooltip />
              <Bar dataKey="count" fill="#8884d8" />
            </BarChart>
          </ResponsiveContainer>
        </div> */}
        {/* Add more dashboard widgets as needed */}
      </div>
    </div>
  );
}

export default Dashboard;
