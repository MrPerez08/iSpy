const express = require('express');
const { exec } = require('child_process');
const app = express();
const port = 3000;

app.use(express.json());

app.post('/send-to-vscode', (req, res) => {
    const query = req.body.query;
    const vscodeCommand = `code --execute-command workbench.action.terminal.sendSequence --args "${query}\\n"`;
    
    exec(vscodeCommand, (error, stdout, stderr) => {
        if (error) {
            console.error(`Error: ${error.message}`);
            return res.status(500).json({ error: error.message });
        }
        if (stderr) {
            console.error(`Stderr: ${stderr}`);
            return res.status(500).json({ stderr: stderr });
        }
        console.log(`Stdout: ${stdout}`);
        res.json({ message: 'Query sent to VS Code terminal' });
    });
});

app.listen(port, () => {
    console.log(`Server running at http://localhost:${port}`);
});
