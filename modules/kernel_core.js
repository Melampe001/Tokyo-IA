const { db, logAction } = require('./db');

function initializeKernel() {
    try {
        // Verificar integridad de tablas base
        db.prepare(`
            CREATE TABLE IF NOT EXISTS tokyo_kernel_state (
                key TEXT PRIMARY KEY,
                value TEXT,
                updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        `).run();

        // Registrar latido del Kernel Cognitivo
        db.prepare(`
            INSERT OR REPLACE INTO tokyo_kernel_state (key, value, updated_at)
            VALUES ('kernel_status', 'ACTIVE_SECURE', datetime('now'))
        `).run();

        logAction('KERNEL_COGNITIVO_INIT', { status: 'ONLINE', version: '1.0.0' }, 'SUCCESS');
        console.log('✅ [Piso 1] Kernel Cognitivo verificado y sincronizado con éxito.');
        return true;
    } catch (error) {
        console.error('❌ [Piso 1] Error crítico en el Kernel Cognitivo:', error.message);
        return false;
    }
}

if (require.main === module) {
    initializeKernel();
}

module.exports = { initializeKernel };
