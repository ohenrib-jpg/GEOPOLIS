// GEOPOLIS Unified Server
// Compatible with Flask backend and rss_aggregator (Render)
// Simplified and stable for current architecture

const express = require('express');
const axios = require('axios');
const fs = require('fs');
const path = require('path');
const chalk = require('chalk');

const app = express();
const PORT = 4000;

const FLASK_URL = 'http://localhost:5000/api/status';
const RSS_URL = 'https://rss-aggregator-l7qj.onrender.com/api/rss/status';
const RETRY_DELAY = 5000; // 5 sec retry delay

function logInfo(msg) {
    console.log(chalk.blue(`[${new Date().toISOString()}] INFO:`), msg);
}

function logWarn(msg) {
    console.warn(chalk.yellow(`[${new Date().toISOString()}] WARN:`), msg);
}

function logError(msg) {
    console.error(chalk.red(`[${new Date().toISOString()}] ERROR:`), msg);
}

// Check if a service is reachable
async function checkService(url) {
    try {
        const res = await axios.get(url, { timeout: 4000 });
        return res.status === 200;
    } catch (err) {
        return false;
    }
}

// Wait for both Flask backend and rss_aggregator to be ready
async function waitForServices() {
    let flaskReady = false;
    let rssReady = false;
    logInfo('Checking services availability...');
    while (!(flaskReady && rssReady)) {
        flaskReady = await checkService(FLASK_URL);
        rssReady = await checkService(RSS_URL);
        if (flaskReady && rssReady) break;
        if (!flaskReady) logWarn('Flask backend not ready yet...');
        if (!rssReady) logWarn('RSS Aggregator not ready yet...');
        await new Promise(r => setTimeout(r, RETRY_DELAY));
    }
    logInfo('All services are reachable, starting main tasks.');
}

// Example periodic job
async function runTasks() {
    try {
        const res = await axios.post('https://rss-aggregator-l7qj.onrender.com/api/rss/fetch', { urls: [] });
        logInfo(`RSS Aggregator responded: ${res.status}`);
        fs.mkdirSync(path.join(__dirname, 'data', 'logs'), { recursive: true });
        fs.appendFileSync(path.join(__dirname, 'data', 'logs', 'server.log'),
            `[${new Date().toISOString()}] Fetch OK (${res.status})\n`);
    } catch (err) {
        logError(`Failed to fetch RSS: ${err.message}`);
    }
}

async function main() {
    await waitForServices();
    runTasks();
    setInterval(runTasks, 10 * 60 * 1000); // every 10 minutes
}

app.get('/', (req, res) => {
    res.send('GEOPOLIS Node service is running.');
});

app.listen(PORT, () => {
    logInfo(`Server listening on http://localhost:${PORT}`);
    main();
});
