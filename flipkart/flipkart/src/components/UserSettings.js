import React, { useState } from 'react';

function UserSettings() {
  const [username, setUsername] = useState('');
  const [email, setEmail] = useState('');
  const [notificationEnabled, setNotificationEnabled] = useState(true);
  const [savedMessage, setSavedMessage] = useState('');

  const handleSaveSettings = () => {
    // You can add code here to save user settings to the server or a database
    setSavedMessage('Settings saved successfully.');
  };

  return (
    <div className="section">
      <h2 className="text-xl font-semibold mb-4">User Settings</h2>
      <div className="mb-4">
        <label className="block font-semibold mb-1">Username:</label>
        <input
          type="text"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
          className="border rounded py-2 px-4 w-full text-gray-600 focus:outline-none focus:border-blue-400"
        />
      </div>
      <div className="mb-4">
        <label className="block font-semibold mb-1">Email:</label>
        <input
          type="email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          className="border rounded py-2 px-4 w-full text-gray-600 focus:outline-none focus:border-blue-400"
        />
      </div>
      <div className="mb-4">
        <label className="block font-semibold mb-1">Notification Enabled:</label>
        <input
          type="checkbox"
          checked={notificationEnabled}
          onChange={(e) => setNotificationEnabled(e.target.checked)}
          className="text-blue-500"
        />
      </div>
      <button
        onClick={handleSaveSettings}
        className="bg-blue-500 text-white px-6 py-2 rounded hover:bg-blue-600 transition"
      >
        Save Settings
      </button>
      {savedMessage && <p className="text-green-500 mt-2">{savedMessage}</p>}
    </div>
  );
}

export default UserSettings;
