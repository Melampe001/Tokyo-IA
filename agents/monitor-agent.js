class MonitorAgent {
  constructor(options = {}) {
    this.memoryThresholdMB = options.memoryThresholdMB || 150;
    this.status = 'HEALTHY';
  }

  getMetrics() {
    const memory = process.memoryUsage();
    const heapUsedMB = (memory.heapUsed / 1024 / 1024).toFixed(2);
    const uptimeSeconds = process.uptime().toFixed(1);

    const isOverloaded = parseFloat(heapUsedMB) > this.memoryThresholdMB;
    this.status = isOverloaded ? 'DEGRADED' : 'HEALTHY';

    return {
      status: this.status,
      uptimeSeconds: Number(uptimeSeconds),
      heapUsedMB: Number(heapUsedMB),
      rssMB: Number((memory.rss / 1024 / 1024).toFixed(2)),
      timestamp: new Date().toISOString()
    };
  }

  checkHealth() {
    const metrics = this.getMetrics();
    if (metrics.status === 'DEGRADED') {
      console.warn(`⚠️ ALERTA: Consumo de memoria elevado (${metrics.heapUsedMB} MB).`);
    }
    return metrics;
  }
}

module.exports = { MonitorAgent };
