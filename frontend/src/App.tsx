import React, { useState, useEffect } from 'react';
import logo from './logo.svg';
import './App.css';
import { apiClient, API_CONFIG } from './config/api';

interface HealthStatus {
  status: string;
  timestamp: string;
}

function App() {
  const [healthStatus, setHealthStatus] = useState<HealthStatus | null>(null);
  const [isConnected, setIsConnected] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    checkBackendHealth();
  }, []);

  const checkBackendHealth = async () => {
    try {
      const response = await apiClient.get<HealthStatus>(
        API_CONFIG.ENDPOINTS.HEALTH,
      );
      setHealthStatus(response);
      setIsConnected(true);
      setError(null);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Unknown error');
      setIsConnected(false);
    }
  };

  return (
    <div className="App">
      <header className="App-header">
        <img src={logo} className="App-logo" alt="logo" />
        <h1>Multi-Blog Publishing Platform</h1>

        <div className="backend-status">
          <h2>Backend Connection Status</h2>
          <p>
            <strong>API URL:</strong> {API_CONFIG.BASE_URL}
          </p>

          {isConnected ? (
            <div className="status-success">
              <p>✅ Connected to backend server</p>
              {healthStatus && (
                <div>
                  <p>
                    <strong>Status:</strong> {healthStatus.status}
                  </p>
                  <p>
                    <strong>Timestamp:</strong> {healthStatus.timestamp}
                  </p>
                </div>
              )}
            </div>
          ) : (
            <div className="status-error">
              <p>❌ Failed to connect to backend</p>
              {error && (
                <p>
                  <strong>Error:</strong> {error}
                </p>
              )}
            </div>
          )}

          <button onClick={checkBackendHealth} className="retry-button">
            Retry Connection
          </button>
        </div>

        <div className="api-links">
          <h3>API Documentation</h3>
          <a
            className="App-link"
            href={`${API_CONFIG.BASE_URL}/docs`}
            target="_blank"
            rel="noopener noreferrer"
          >
            Swagger UI
          </a>
          <a
            className="App-link"
            href={`${API_CONFIG.BASE_URL}/redoc`}
            target="_blank"
            rel="noopener noreferrer"
          >
            ReDoc
          </a>
        </div>
      </header>
    </div>
  );
}

export default App;
