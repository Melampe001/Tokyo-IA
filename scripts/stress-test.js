const { JobQueue } = require('../modules/queue');

async function runStressTest() {
  console.log('⚡ [PRUEBA DE CARGA] Procesando 10,000 trabajos masivos...');
  const queue = new JobQueue({ concurrency: 100 });
  queue.registerHandler('STRESS_TASK', async (job) => ({ processedId: job.id }));

  const totalJobs = 10000;
  const startTime = Date.now();

  for (let i = 0; i < totalJobs; i++) {
    queue.addJob('STRESS_TASK', { payload: `packet_${i}` }, { priority: i % 5 });
  }

  await queue.process();
  const duration = (Date.now() - startTime) / 1000;
  const memory = process.memoryUsage();

  console.log(`✅ Resultado: ${totalJobs.toLocaleString()} trabajos completados.`);
  console.log(`⏱️ Tiempo total: ${duration.toFixed(2)}s | Rendimiento: ${(totalJobs / duration).toFixed(0)} jobs/s`);
  console.log(`🧠 Memoria Heap Utilizada: ${(memory.heapUsed / 1024 / 1024).toFixed(2)} MB`);
}

runStressTest().catch(console.error);
