const { logAction } = require('../modules/db');

class SecurityAgent {
  constructor(options = {}) {
    this.strictMode = options.strictMode || false;
  }

  scanCode(code) {
    const patterns = [
      /SELECT.*FROM/i,
      /<script\b[^>]*>/i,
      /process\.env/i
    ];

    let vulnerabilitiesFound = 0;
    for (const pattern of patterns) {
      if (pattern.test(code)) {
        vulnerabilitiesFound++;
      }
    }

    if (vulnerabilitiesFound > 0) {
      logAction('SECURITY_THREAT_BLOCKED', {
        threatsDetected: vulnerabilitiesFound,
        snippet: code.substring(0, 100)
      }, 'BLOCKED');
    }

    return { vulnerabilitiesFound };
  }
}

module.exports = { SecurityAgent };
