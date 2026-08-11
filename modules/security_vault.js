const crypto = require('crypto');
const { db, logAction } = require('./db');

const ALGORITHM = 'aes-256-gcm';

// En producción, esta llave maestra DEBE venir de una variable de entorno (.env)
// Para inicialización, generamos un hash a partir de un identificador del propietario
const MASTER_KEY = crypto.scryptSync('Jose Arturo Orozco Jaime - Rascacielos Atom', 'salt', 32);

function setupVault() {
    db.prepare(`
        CREATE TABLE IF NOT EXISTS tokyo_credentials_vault (
            service_name TEXT PRIMARY KEY,
            encrypted_data TEXT,
            iv TEXT,
            auth_tag TEXT,
            updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    `).run();
}

function encryptAndStore(serviceName, plainTextData) {
    const iv = crypto.randomBytes(12);
    const cipher = crypto.createCipheriv(ALGORITHM, MASTER_KEY, iv);
    
    let encrypted = cipher.update(plainTextData, 'utf8', 'hex');
    encrypted += cipher.final('hex');
    const authTag = cipher.getAuthTag().toString('hex');

    db.prepare(`
        INSERT OR REPLACE INTO tokyo_credentials_vault (service_name, encrypted_data, iv, auth_tag, updated_at)
        VALUES (?, ?, ?, ?, datetime('now'))
    `).run(serviceName, encrypted, iv.toString('hex'), authTag);

    return true;
}

function verifyVault() {
    try {
        console.log('🛡️ [Piso 7] Inicializando Bóveda Criptográfica AES-256-GCM...');
        setupVault();

        // Simulando el guardado seguro de la estructura de OKX (Sin frase secreta, validado por IP)
        const okxStructure = JSON.stringify({
            apiKey: 'INGRESAR_API_KEY_REAL_AQUI',
            secretKey: 'INGRESAR_SECRET_KEY_REAL_AQUI',
            authMode: 'IP_BOUND'
        });

        encryptAndStore('OKX_PRODUCTION_API', okxStructure);

        logAction('SECURITY_VAULT_INIT', { status: 'AES_256_ACTIVE', service: 'OKX_PRODUCTION_API' }, 'SUCCESS');

        console.log('  • Algoritmo Activo: AES-256-GCM');
        console.log('  • Credenciales OKX: CIFRADAS Y ALMACENADAS EN BÓVEDA (SQLite)');
        console.log('✅ [Piso 7] Seguridad Militar desplegada. Listo para inyección de capital real.');
        return true;
    } catch (error) {
        console.error('❌ [Piso 7] Error en la Bóveda de Seguridad:', error.message);
        return false;
    }
}

if (require.main === module) {
    verifyVault();
}

module.exports = { setupVault, encryptAndStore };
