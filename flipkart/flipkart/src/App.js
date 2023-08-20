// import logo from './logo.svg';
// import './App.css';

// function App() {
//   return (
//     <div className="App">
      
//     </div>
//   );
// }

// export default App;

import React, { useState } from 'react';

// Components
import Sidebar from './components/Sidebar';
import Dashboard from './components/Dashboard';
import RulesConfiguration from './components/RulesConfiguration';
import UploadLogs from './components/UploadLogs';
import ComplianceReports from './components/ComplianceReports';
import UserSettings from './components/UserSettings';

import './App.css';

function App() {
  const [activeSection, setActiveSection] = useState('dashboard');

  const renderSection = () => {
    switch (activeSection) {
      case 'dashboard':
        return <Dashboard />;
      case 'rules':
        return <RulesConfiguration />;
      case 'upload':
        return <UploadLogs />;
      case 'reports':
        return <ComplianceReports />;
      case 'settings':
        return <UserSettings />;
      default:
        return null;
    }
  };

  return (
    <div className="app flex h-screen">
      <Sidebar setActiveSection={setActiveSection} />
      <main className="main-content w-3/4 p-10">{renderSection()}</main>
    </div>
  );
}

export default App;
