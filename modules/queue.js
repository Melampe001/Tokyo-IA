const { logAction } = require('./db');

class JobQueue {
  constructor(options = {}) {
    this.concurrency = options.concurrency || 100;
    this.handlers = new Map();
    this.queue = [];
  }

  registerHandler(type, handler) {
    this.handlers.set(type, handler);
  }

  addJob(type, payload, options = {}) {
    const jobId = Math.random().toString(36).substring(2, 9);
    const job = {
      id: jobId,
      type,
      payload,
      priority: options.priority || 0
    };
    this.queue.push(job);
    logAction('JOB_QUEUED', { jobId, type, priority: job.priority });
    return job;
  }

  async process() {
    this.queue.sort((a, b) => b.priority - a.priority);
    const chunkSize = this.concurrency;
    for (let i = 0; i < this.queue.length; i += chunkSize) {
      const chunk = this.queue.slice(i, i + chunkSize);
      await Promise.all(
        chunk.map(async (job) => {
          const handler = this.handlers.get(job.type);
          if (handler) {
            try {
              const result = await handler(job);
              logAction('JOB_PROCESSED', { jobId: job.id, type: job.type, result });
              return result;
            } catch (err) {
              logAction('JOB_FAILED', { jobId: job.id, type: job.type, error: err.message }, 'FAILED');
              throw err;
            }
          }
        })
      );
    }
    this.queue = [];
  }
}

module.exports = { JobQueue };
