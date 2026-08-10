const http = require('http');
const { SecurityAgent } = require('./agents/security-agent');
const { MonitorAgent } = require('./agents/monitor-agent');
const { JobQueue } = require('./modules/queue');
const { logAction } = require('./modules/db');

const PORT = process.env.PORT || 3000;
const security = new SecurityAgent({ strictMode: true });
const monitor = new MonitorAgent({ memoryThresholdMB: 150 });
const queue = new JobQueue({ concurrency: 50 });

queue.registerHandler('API_TASK', async (job) => {
  return { status: 'PROCESSED', jobId: job.id };
});

const server = http.createServer(async (req, res) => {
  if (req.method === 'GET' && req.url === '/health') {
    const metrics = monitor.getMetrics();
    logAction('HEALTH_CHECK', metrics);
    res.writeHead(200, { 'Content-Type': 'application/json' });
    return res.end(JSON.stringify(metrics));
  }

  if (req.method === 'POST' && req.url === '/api/v1/execute') {
    let body = '';
    req.on('data', chunk => { body += chunk.toString(); });
    req.on('end', async () => {
      const scan = security.scanCode(body);
      if (scan.vulnerabilitiesFound > 0) {
        res.writeHead(400, { 'Content-Type': 'application/json' });
        return res.end(JSON.stringify({
          error: 'Payload bloqueado por políticas de seguridad.',
          threats: scan.vulnerabilitiesFound
        }));
      }

      try {
        const payload = JSON.parse(body || '{}');
        const job = queue.addJob('API_TASK', payload);
        await queue.process();
        res.writeHead(200, { 'Content-Type': 'application/json' });
        return res.end(JSON.stringify({ status: 'SUCCESS', message: 'Trabajo procesado en la cola', jobId: job.id }));
      } catch (e) {
        logAction('INVALID_JSON_PAYLOAD', { error: e.message }, 'REJECTED');
        res.writeHead(400, { 'Content-Type': 'application/json' });
        return res.end(JSON.stringify({ error: 'JSON inválido' }));
      }
    });
    return;
  }

  res.writeHead(404, { 'Content-Type': 'application/json' });
  res.end(JSON.stringify({ error: 'Ruta no encontrada' }));
});

server.listen(PORT, () => {
  logAction('SERVER_STARTUP', { port: PORT });
  console.log(`🚀 Servidor NULOGIC_CORE activo en puerto ${PORT}`);
});
