const { inspectDatabase, logAction } = require('../modules/db');

console.log('================================================--');
console.log('🔍 ANÁLISIS Y ALINEACIÓN DE ESQUEMA TOKYO_001.DB');
console.log('================================================--');

const summary = inspectDatabase();

if (Array.isArray(summary) && summary.length > 0) {
  summary.forEach(item => {
    console.log(`📋 TABLA: [${item.tabla}]`);
    console.log(`   🔢 Registros Totales: ${item.registros.toLocaleString()}`);
    console.log(`   🛠️  Columnas (${item.columnas.length}): ${item.columnas.join(', ')}`);
    console.log('--------------------------------------------------');
  });
} else {
  console.log('ℹ️ Base de datos inicializada correctamente. Tabla tokyo_001_actions activa.');
  console.log('--------------------------------------------------');
}

logAction('SYSTEM_ALIGNMENT_ROOT', {
  system: 'RascacielosDigital',
  owner: 'Jose Arturo Orozco Jaime',
  path: process.cwd(),
  status: 'UNIFIED_ROOT_SUCCESS'
});

console.log('✅ Acción guardada automáticamente en la tabla tokyo_001_actions.');
