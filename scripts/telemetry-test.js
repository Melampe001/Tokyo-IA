const { MonitorAgent } = require('../agents/monitor-agent');

function testTelemetry() {
  console.log('📊 [PRUEBA DE TELEMETRÍA] Verificando métricas de salud del sistema...');
  const monitor = new MonitorAgent({ memoryThresholdMB: 150 });
  const metrics = monitor.checkHealth();
  console.log(`Estado: [${metrics.status}] | Uptime: ${metrics.uptimeSeconds}s | Heap: ${metrics.heapUsedMB} MB`);
}

testTelemetry();
