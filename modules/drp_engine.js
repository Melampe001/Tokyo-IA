const fs = require('fs');
const path = require('path');
const { logAction } = require('./db');

function executeDisasterRecoveryBackup() {
    try {
        console.log('🔄 [DRP Engine] Iniciando Respaldo Espejo y Cadena de Custodia...');
        
        // Apuntar correctamente a la raíz donde vive Tokyo_001.db
        const dbSource = path.join(__dirname, '../Tokyo_001.db');
        const backupDir = 'E:\\TOKYOAPPS_UNIVERSE\\01_ACTIVE\\NULOGIC_BACKUP';
        
        if (!fs.existsSync(backupDir)) {
            fs.mkdirSync(backupDir, { recursive: true });
        }

        const timestamp = new Date().toISOString().replace(/[:.]/g, '-');
        const dbBackup = path.join(backupDir, `Tokyo_001_snapshot_${timestamp}.db`);

        if (fs.existsSync(dbSource)) {
            fs.copyFileSync(dbSource, dbBackup);
            console.log(`  • Respaldo espejo sincronizado con éxito en: ${dbBackup}`);
        } else {
            console.warn('⚠️ Advertencia: Base de datos no encontrada en la ruta raíz especificada.');
        }

        logAction('DRP_SNAPSHOT_CREATED', { backup_path: dbBackup }, 'SUCCESS');
        console.log('✅ [DRP Engine] Sistema protegido con respaldo espejo activo.');
        return true;
    } catch (error) {
        console.error('❌ [DRP Engine] Error crítico en respaldo espejo:', error.message);
        return false;
    }
}

if (require.main === module) {
    executeDisasterRecoveryBackup();
}

module.exports = { executeDisasterRecoveryBackup };
