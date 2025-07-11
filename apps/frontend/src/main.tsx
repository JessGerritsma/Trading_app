import React from 'react';
import ReactDOM from 'react-dom/client';
import TradingDashboard from './App';
import './index.css'; 

const root = ReactDOM.createRoot(
  document.getElementById('root') as HTMLElement
);

root.render(
  <React.StrictMode>
    <TradingDashboard />
  </React.StrictMode>
);