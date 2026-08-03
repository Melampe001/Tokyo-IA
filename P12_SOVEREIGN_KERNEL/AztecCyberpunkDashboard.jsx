import React, { useState, useEffect } from 'react';
import './AztecCyberpunkDashboard.css';

const AztecCyberpunkDashboard = () => {
  const [metrics, setMetrics] = useState({
    systemStatus: 'ONLINE',
    latency: '3.4ms',
    activeTier: 'P12_SOVEREIGN_KERNEL',
    auditSeal: 'VERIFIED_100%'
  });

  useEffect(() => {
    const interval = setInterval(() => {
      setMetrics(prev => ({
        ...prev,
        latency: ` + (Math.random() * 2 + 2).toFixed(1) + ms
      }));
    }, 2000);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="aztec-cyber-container">
      <header className="aztec-header">
        <div className="glyph-symbol">☀️</div>
        <div className="title-block">
          <h1>NULOGIC // FLAGGSHIP APPS</h1>
          <p className="subtitle">SINC360° ESFERA — TITULAR: TOKYO M.</p>
        </div>
        <div className="status-badge cyberpunk-glow">
          {metrics.systemStatus}
        </div>
      </header>

      <div className="dashboard-grid">
        <div className="cyber-card">
          <h3>LATENCIA DE RED (P7)</h3>
          <p className="metric-value neon-cyan">{metrics.latency}</p>
          <span className="card-footer">Bybit / Alta Frecuencia</span>
        </div>

        <div className="cyber-card">
          <h3>NÚCLEO ACTIVO (P8)</h3>
          <p className="metric-value neon-gold">{metrics.activeTier}</p>
          <span className="card-footer">Estrategia: Potencia y Aceleracion</span>
        </div>

        <div className="cyber-card">
          <h3>AUDIT SEAL (P11)</h3>
          <p className="metric-value neon-green">{metrics.auditSeal}</p>
          <span className="card-footer">Inmutable & Cifrado</span>
        </div>
      </div>
    </div>
  );
};

export default AztecCyberpunkDashboard;
