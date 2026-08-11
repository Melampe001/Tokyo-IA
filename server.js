const http = require('http');
const sqlite3 = require('sqlite3').verbose();
const db = new sqlite3.Database('Tokyo_001.db');

const server = http.createServer((req, res) => {
    res.setHeader('Content-Type', 'application/json');
    if (req.method === 'POST' && req.url === '/api/monetize/execute') {
        db.run('INSERT INTO actions (timestamp, action, status) VALUES (datetime(\'now\'), ?, ?)', ['MONETIZE_EXEC', 'SUCCESS'], (err) => {
            res.writeHead(200);
            res.end(JSON.stringify({ 
                status: 'SUCCESS', 
                platform: 'FlaggsShip Apps', 
                tx_id: 'TXN_' + Date.now(), 
                revenue: '.99 USD' 
            }));
        });
    } else {
        res.writeHead(404);
        res.end(JSON.stringify({ status: 'ERROR', message: 'Not Found' }));
    }
});

server.listen(3000, '127.0.0.1', () => {
    console.log('[SERVER RUNNING ON 3000]');
});
