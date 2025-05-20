'use client';

import { useState, FormEvent } from 'react';

export default function Home() {
  const [phoneNumber, setPhoneNumber] = useState('');
  const [waitForAnswer, setWaitForAnswer] = useState(true);
  const [isLoading, setIsLoading] = useState(false);
  const [result, setResult] = useState<{
    success?: boolean;
    message?: string;
  } | null>(null);

  const handleSubmit = async (e: FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    
    if (!phoneNumber) {
      setResult({
        success: false,
        message: 'Please enter a phone number',
      });
      return;
    }

    if (!phoneNumber.startsWith('+')) {
      setResult({
        success: false,
        message: 'Phone number must start with + (e.g., +18005551234)',
      });
      return;
    }

    setIsLoading(true);
    setResult(null);

    try {
      const response = await fetch('/api/call', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          phone_number: phoneNumber,
          wait_for_answer: waitForAnswer,
        }),
      });

      const data = await response.json();

      if (response.ok) {
        setResult({
          success: true,
          message: data.message,
        });
        setPhoneNumber('');
      } else {
        setResult({
          success: false,
          message: data.detail || 'Failed to make call',
        });
      }
    } catch (error) {
      setResult({
        success: false,
        message: 'An error occurred while making the call',
      });
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="max-w-md mx-auto mt-10">
      <div className="bg-white shadow-md rounded-lg p-6">
        <h2 className="text-2xl font-bold mb-6 text-center">Make an Outbound Call</h2>
        
        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label htmlFor="phoneNumber" className="block text-sm font-medium text-gray-700 mb-1">
              Phone Number
            </label>
            <input
              type="text"
              id="phoneNumber"
              value={phoneNumber}
              onChange={(e) => setPhoneNumber(e.target.value)}
              placeholder="+18005551234"
              className="w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary"
              disabled={isLoading}
            />
            <p className="mt-1 text-sm text-gray-500">
              Format: +[country code][number], e.g., +18005551234
            </p>
          </div>

          <div className="flex items-center">
            <input
              type="checkbox"
              id="waitForAnswer"
              checked={waitForAnswer}
              onChange={(e) => setWaitForAnswer(e.target.checked)}
              className="h-4 w-4 text-primary focus:ring-primary border-gray-300 rounded"
              disabled={isLoading}
            />
            <label htmlFor="waitForAnswer" className="ml-2 block text-sm text-gray-700">
              Wait for answer before returning
            </label>
          </div>

          <button
            type="submit"
            disabled={isLoading}
            className={`w-full py-2 px-4 rounded-md text-white font-medium ${
              isLoading
                ? 'bg-gray-400 cursor-not-allowed'
                : 'bg-primary hover:bg-primary-dark'
            }`}
          >
            {isLoading ? 'Calling...' : 'Make Call'}
          </button>
        </form>

        {result && (
          <div
            className={`mt-4 p-3 rounded-md ${
              result.success
                ? 'bg-green-50 text-green-800 border border-green-200'
                : 'bg-red-50 text-red-800 border border-red-200'
            }`}
          >
            <p>{result.message}</p>
          </div>
        )}
      </div>
    </div>
  );
}
