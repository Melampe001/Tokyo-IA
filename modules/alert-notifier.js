const https = require('https');

class AlertNotifier {
  static async sendCriticalAlert(errorDetails) {
    const webhookUrl = process.env.ALERT_WEBHOOK_URL;
    if (!webhookUrl) {
      console.log('ℹ️ AlertNotifier: Webhook no configurado. Registrando en log local.');
      return;
    }

    const payload = JSON.stringify({
      text: `🚨 *ALERTA CRÍTICA - RascacielosDigital* 🚨\n\n*Error:* ${errorDetails.message}\n*Ambiente:* ${process.env.NODE_ENV || 'production'}\n*Hora:* ${new Date().toISOString()}`,
      parse_mode: 'Markdown'
    });

    try {
      const req = https.request(webhookUrl, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' }
      });
      req.on('error', (err) => console.error('Error enviando alerta:', err.message));
      req.write(payload);
      req.end();
    } catch (err) {
      console.error('Fallo en el envío de telemetría:', err);
    }
  }
}

module.exports = { AlertNotifier };
