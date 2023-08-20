import React, { useState } from 'react';

function RulesConfiguration() {
  const [rules, setRules] = useState([
  ]);

  const [newRuleTitle, setNewRuleTitle] = useState('');
  const [newRuleDescription, setNewRuleDescription] = useState('');

  const handleAddRule = () => {
    if (!newRuleTitle) {
      return; // Prevent adding a rule with no title
    }

    const newRule = {
      id: Date.now(),
      title: newRuleTitle,
      description: newRuleDescription,
      parameters: {},
      isEditable: false, // Initially not editable
    };

    setRules([...rules, newRule]);
    setNewRuleTitle('');
    setNewRuleDescription('');
  };

  const handleDeleteRule = (id) => {
    const updatedRules = rules.filter((rule) => rule.id !== id);
    setRules(updatedRules);
  };

  const handleEditRule = (id) => {
    const updatedRules = rules.map((rule) =>
      rule.id === id ? { ...rule, isEditable: true } : rule
    );
    setRules(updatedRules);
  };

  const handleSaveRule = (id, updatedRule) => {
    const updatedRules = rules.map((rule) =>
      rule.id === id ? { ...updatedRule, isEditable: false } : rule
    );
    setRules(updatedRules);
  };

  return (
    <div className="section">
      <h2 className="text-xl font-semibold mb-4">Rules Configuration</h2>
      <div className="flex space-x-2 mb-2">
        <input
          type="text"
          placeholder="Rule title"
          value={newRuleTitle}
          onChange={(e) => setNewRuleTitle(e.target.value)}
          className="border rounded px-2 py-1 w-5/12"
        />
        <textarea
          placeholder="Rule description"
          value={newRuleDescription}
          onChange={(e) => setNewRuleDescription(e.target.value)}
          className="border rounded px-2 py-1 w-5/12"
        />
        <button
          onClick={handleAddRule}
          className="bg-blue-500 w-2/12 text-white px-4 py-2 rounded hover:bg-blue-600 transition"
        >
          Add Rule
        </button>
      </div>
      <ul className="space-y-4">
        {rules.map((rule) => (
          <li key={rule.id} className="border p-4 rounded bg-white shadow">
            <h3 className="font-semibold mb-2">
              {rule.isEditable ? (
                <input
                  type="text"
                  value={rule.title}
                  onChange={(e) => handleSaveRule(rule.id, { ...rule, title: e.target.value })}
                  className="border rounded px-2 py-1 w-full"
                />
              ) : (
                rule.title
              )}
            </h3>
            {rule.isEditable ? (
              <textarea
                value={rule.description}
                onChange={(e) =>
                  handleSaveRule(rule.id, { ...rule, description: e.target.value })
                }
                className="border rounded px-2 py-1 w-full h-20"
              />
            ) : (
              <p>{rule.description}</p>
            )}
            {rule.isEditable ? (
              <button
                onClick={() => handleSaveRule(rule.id, { ...rule })}
                className="bg-green-500 text-white px-2 py-1 rounded hover:bg-green-600 transition mt-2"
              >
                Save
              </button>
            ) : (
              <button
                onClick={() => handleEditRule(rule.id)}
                className="text-blue-500 hover:text-blue-600 transition mt-2"
              >
                Edit
              </button>
            )}
            <button
              onClick={() => handleDeleteRule(rule.id)}
              className="text-red-500 hover:text-red-600 transition mt-2 ml-2"
            >
              Delete
            </button>
          </li>
        ))}
      </ul>
    </div>
  );
}

export default RulesConfiguration;
