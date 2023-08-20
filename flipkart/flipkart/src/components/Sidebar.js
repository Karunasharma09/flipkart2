import React from 'react';
import logof from "../logof.png"

function Sidebar({ setActiveSection }) {
  const sections = [
    { id: 'rules', label: 'Rules Configuration' },
    { id: 'upload', label: 'Upload Logs' },
    { id: 'reports', label: 'Compliance Reports' },
  ];

  return (
    <aside className="sidebar bg-blue-500 w-1/4 h-full border-r  border-gray-300">
      <div className="flex items-center justify-center p-8">
        <p className=' text-5xl font-semibold text-white italic'>Flipkart</p>
        <img src={logof} alt="Flipkart Logo" className="w-20 h-20" />
      </div>
      <ul className="space-y-3 p-10">
        {sections.map((section) => (
          <li key={section.id}>
            <button
              className="block text-slate-300 text-lg py-3 hover:text-gray-700 transition duration-500"
              onClick={() => setActiveSection(section.id)}
            >
              {section.label}
            </button>
          </li>
        ))}
      </ul>
    </aside>
  );
}

export default Sidebar;
