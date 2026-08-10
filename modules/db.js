const { DatabaseSync } = require('node:sqlite');
const path = require('path');
const fs = require('fs');

const dbPath = process.env.TOKYO_DB_PATH || path.join(__dirname, '..', 'data', 'Tokyo_001.db');
const dataDir = path.dirname(dbPath);

if (!fs.existsSync(dataDir)) {
  fs.mkdirSync(dataDir, { recursive: true });
}

let db = null;
try {
  db = new DatabaseSync(dbPath);
  db.exec(`
    CREATE TABLE IF NOT EXISTS tokyo_001_actions (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      action_type TEXT NOT NULL,
      payload TEXT,
      status TEXT DEFAULT 'SUCCESS',
      timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    );
  `);
} catch (error) {
  console.error(`❌ Error al inicializar SQLite (${dbPath}): ${error.message}`);
}

function logAction(actionType, payload = {}, status = 'SUCCESS') {
  if (!db) return false;
  try {
    const stmt = db.prepare(`
      INSERT INTO tokyo_001_actions (action_type, payload, status)
      VALUES (?, ?, ?)
    `);
    const payloadStr = typeof payload === 'object' ? JSON.stringify(payload) : String(payload);
    stmt.run(actionType, payloadStr, status);
    return true;
  } catch (err) {
    console.error(`❌ Error grabando en Tokyo_001: ${err.message}`);
    return false;
  }
}

function inspectDatabase() {
  if (!db) return [];
  try {
    const stmt = db.prepare("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'");
    const tables = stmt.all();
    const summary = [];

    for (const table of tables) {
      const tableName = table.name;
      const countStmt = db.prepare(`SELECT COUNT(*) as total FROM "${tableName}"`);
      const countResult = countStmt.get();
      const infoStmt = db.prepare(`PRAGMA table_info("${tableName}")`);
      const columns = infoStmt.all().map(c => c.name);

      summary.push({
        tabla: tableName,
        registros: countResult.total,
        columnas: columns
      });
    }
    return summary;
  } catch (e) {
    console.error(`Error inspeccionando DB: ${e.message}`);
    return [];
  }
}

module.exports = { db, logAction, inspectDatabase };
