const { spawn } = require('child_process');

const childPython = spawn('python', ['discord_navigator.py']);
childPython.stdout.on('data',(data) => {
    console.log(`stdout: ${data}`);
});

childPython.stderr.on('data',(data) => {
    console.log(`stderr: ${data}`);
});

childPython.stdout.on('close',(code) => {
    console.log(`child process exited with code: ${code}`);
});





