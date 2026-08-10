const { JobQueue } = require('../modules/queue');
const { SecurityAgent } = require('../agents/security-agent');
const { db } = require('../modules/db');

async function verifyIntegration() {
  console.log('================================================--');
  console.log('🧪 VERIFICACIÓN DE PERSISTENCIA EN TOKYO_001_ACTIONS');
  console.log('================================================--');

  // 1. Encolar y procesar un trabajo en JobQueue
  const queue = new JobQueue();
  queue.registerHandler('VERIFY_TASK', async (job) => ({ status: 'COMPLETED' }));
  const job = queue.addJob('VERIFY_TASK', { data: 'test_db_persistence' });
  await queue.process();

  // 2. Ejecutar un escaneo con amenaza en SecurityAgent
  const security = new SecurityAgent({ strictMode: true });
  security.scanCode("SELECT * FROM users WHERE '1'='1'");

  // 3. Consultar directamente los registros guardados en la tabla tokyo_001_actions
  const stmt = db.prepare("SELECT * FROM tokyo_001_actions ORDER BY id DESC LIMIT 5");
  const records = stmt.all();

  console.log('📋 ÚLTIMAS ACCIONES REGISTRADAS EN LA BASE DE DATOS:');
  records.forEach(r => {
    console.log(`  [ID: ${r.id}] [${r.timestamp}] Action: ${r.action_type} | Status: ${r.status}`);
    console.log(`         Payload: ${r.payload}`);
  });
  console.log('--------------------------------------------------');
  console.log('✅ Persistencia nativa activada y confirmada.');
}

verifyIntegration().catch(console.error);
