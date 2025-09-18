const { spawn } = require('node:child_process');
const path = require('node:path');
const fs = require('node:fs');

// Clear CSV files on start

function clearCSV() {
    for (const file of ['accelerometer_data.csv', 'gyroscope_data.csv']) {
    try {
        const p = path.join(__dirname, file);
        fs.writeFileSync(p, '');
    } catch (err) {
        console.warn(`Could not clear ${file}:`, err.message);
    }
    }
}

clearCSV();

// Resolve venv python
const python = process.platform === 'win32'
  ? path.join(__dirname, '.venv', 'Scripts', 'python.exe')
  : path.join(__dirname, '.venv', 'bin', 'python');

function runPy(script, name) {
  const cp = spawn(python, [script], {
    cwd: __dirname,
    stdio: 'inherit',
    shell: false,
  });
  cp.once('error', (err) => {
    console.error(`[${name}] failed to start:`, err);
  });
  cp.once('close', (code, signal) => {
    console.log(`[${name}] exited code=${code} signal=${signal || 'none'}`);
  });
  return cp;
}

function runAnalyze() {
  return new Promise((resolve) => {
    const cp = spawn(python, ['analyze.py'], {
      cwd: __dirname,
      stdio: 'inherit',
      shell: false,
    });
    cp.once('error', (err) => {
      console.error(`[Analyze] failed to start:`, err);
      resolve();
    });
    cp.once('close', (code, signal) => {
      console.log(`Analysis finished cleaning up...`);
      try {
          const ts = new Date().toISOString().replace(/[:.]/g, '-');

          const renameWithTs = (file) => {
              const src = path.join(__dirname, file);
              if (!fs.existsSync(src)) return;
              const ext = path.extname(file);
              const base = path.basename(file, ext);
              const dst = path.join(__dirname, `${base}_${ts}${ext}`);
              try {
                  fs.renameSync(src, dst);
              } catch (e) {
                  console.warn(`Failed to rename ${file}:`, e.message);
              }
          };

          // Two CSV files
          ['accelerometer_data.csv', 'gyroscope_data.csv'].forEach(renameWithTs);

          // Three HTML files (pick up to three found in current directory)
          const htmlFiles = fs
              .readdirSync(__dirname)
              .filter((f) => /\.html$/i.test(f))
              .slice(0, 3);

          htmlFiles.forEach(renameWithTs);
      } catch (e) {
          console.warn('Post-analysis renaming encountered an error:', e.message);
      } finally {
          resolve();
      }
    });
  });
}

// Start both servers in parallel
const acc = runPy('server_acc.py', 'accelerometer');
const gy = runPy('server_gy.py', 'gyroscope');

function whenClosed(cp) {
  return new Promise((resolve) => {
    if (!cp || cp.killed || cp.exitCode !== null) return resolve();
    cp.once('close', () => resolve());
  });
}

let shuttingDownPromise = null;
// Graceful shutdown: on Ctrl+C / termination, kill children, await analyze
async function shutdown() {
  if (shuttingDownPromise) return shuttingDownPromise;
  shuttingDownPromise = (async () => {
    console.log('Starting analysis...');

    if (acc && !acc.killed) {
      acc.kill();
    }
    if (gy && !gy.killed) {
      gy.kill();
    }

    // Wait for children to exit (or timeout after 1s)
    await Promise.race([
      Promise.all([whenClosed(acc), whenClosed(gy)]),
      new Promise((r) => setTimeout(r, 3000)),
    ]);

    //wait 1s to ensure files are flushed
    await new Promise((r) => setTimeout(r, 1000));

    // Run analyze and wait for it to complete
    await runAnalyze();
    console.log('Analysis complete.');
  })();
  return shuttingDownPromise;
}

process.once('SIGINT', () => {
  shutdown().then(() => process.exit(0));
});
process.once('SIGTERM', () => {
  shutdown().then(() => process.exit(0));
});
// Do not use 'exit' for async work; optionally ensure shutdown on beforeExit
process.once('beforeExit', (code) => {
  if (!shuttingDownPromise) {
    // Kick off shutdown; Node will keep the event loop alive until promises resolve
    shutdown();
  }
});