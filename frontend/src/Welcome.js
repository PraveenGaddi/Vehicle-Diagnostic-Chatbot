import React from 'react';

const Welcome = ({ onStartChat }) => {
  return (
    <div className="flex flex-col items-center justify-center w-full h-full p-6">
      <div className="w-full max-w-xl mx-auto p-8 rounded-2xl shadow-xl transition-all duration-300 transform bg-white dark:bg-gray-800">
        <div className="text-center">
          <h1 className="text-3xl font-bold mb-2 text-gray-800 dark:text-white">
           Hello! 👋 Welcome to the Vehicle Diagnostics Chatbot
          </h1>
          <p className="text-gray-600 dark:text-gray-400">Your personal assistant for car problems.</p>
        </div>
        <div className="mt-8 space-y-6 text-gray-700 dark:text-gray-300">
          <div className="p-4 bg-gray-100 dark:bg-gray-700 rounded-lg">
            <h2 className="text-lg font-semibold mb-2 text-gray-800 dark:text-white">About Our Bot</h2>
            <p className="text-sm">
              Our chatbot is powered by an advanced AI model fine-tuned on a comprehensive dataset of vehicle issues and solutions. It's designed to provide preliminary diagnostics in a conversational, easy-to-understand format.
            </p>
          </div>
          <div className="p-4 bg-gray-100 dark:bg-gray-700 rounded-lg">
            <h2 className="text-lg font-semibold mb-2 text-gray-800 dark:text-white">Services</h2>
            <ul className="text-sm space-y-2 list-disc list-inside">
              <li>Engine Diagnostics:Interpret common check engine light codes like P0300, P0420, etc.</li>
              <li>Symptom Analysis:Provide insights into problems like strange noises, leaks, or performance issues.</li>
              <li>Troubleshooting:Guide you through basic steps to identify the root cause of a problem.</li>
            </ul>
          </div>
        </div>
        <div className="mt-8 text-center">
          <button
            onClick={onStartChat}
            className="w-full py-3 px-6 bg-blue-600 text-white rounded-full font-bold shadow-lg transform transition-all duration-200 hover:bg-blue-700 hover:scale-105"
          >
            Access the Chatbot
          </button>
        </div>
      </div>
    </div>
  );
};

export default Welcome;
