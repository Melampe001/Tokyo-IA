const { db } = require('../modules/db');

try {
  const stmt = db.prepare('SELECT id, action_type, status, timestamp FROM tokyo_001_actions ORDER BY id DESC LIMIT 5');
  const rows = stmt.all();
  if (rows.length === 0) {
    console.log('ℹ️ No hay registros recientes en tokyo_001_actions.');
  } else {
    rows.forEach(r => {
      console.log(`  [ID: ${r.id}] [${r.timestamp}] Action: ${r.action_type} | Status: ${r.status}`);
    });
  }
} catch (e) {
  console.error('❌ Error leyendo la base de datos:', e.message);
}
