const { exec } = require('child_process');

process.stdin.on('data', (data) => {
    let message = JSON.parse(data);
    exec(message.command, (error, stdout, stderr) => {
        if (error) {
            console.error(`Error: ${error.message}`);
            return;
        }
        if (stderr) {
            console.error(`Stderr: ${stderr}`);
            return;
        }
        console.log(`Stdout: ${stdout}`);
    });
});
