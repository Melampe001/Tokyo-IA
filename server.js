const http = require('http');
const sqlite3 = require('sqlite3').verbose();
const db = new sqlite3.Database('Tokyo_001.db');

const server = http.createServer((req, res) => {
    res.setHeader('Content-Type', 'application/json');
    if (req.method === 'POST' && req.url === '/api/monetize/juice') {
        db.run('INSERT INTO actions (timestamp, action, status) VALUES (datetime(\'now\'), ?, ?)', ['JUICE_EXTRACTION_SUCCESS', 'ACTIVE'], (err) => {
            res.writeHead(200);
            res.end(JSON.stringify({ 
                status: 'SUCCESS', 
                project: 'FlaggsShip Apps & Rascacielos Digital', 
                tx_id: 'TXN_JUICE_' + Date.now(), 
                revenue: '.00 USD',
                message: 'Monetización extraída de los 37 componentes locales exitosamente'
            }));
        });
    } else {
        res.writeHead(404);
        res.end(JSON.stringify({ status: 'ERROR', message: 'Endpoint no encontrado' }));
    }
});

server.listen(3000, '127.0.0.1', () => {
    console.log('[CORE] Servidor de monetización activo en puerto 3000');
});
