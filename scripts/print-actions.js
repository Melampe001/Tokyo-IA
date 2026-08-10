const { db } = require('../modules/db');
try {
  const stmt = db.prepare('SELECT id, action_type, status, timestamp FROM tokyo_001_actions ORDER BY id DESC LIMIT 5');
  const rows = stmt.all();
  rows.forEach(r => {
    console.log(`  [ID: ${r.id}] [${r.timestamp}] Action: ${r.action_type} | Status: ${r.status}`);
  });
} catch (e) {
  console.error('Error al leer acciones:', e.message);
}
