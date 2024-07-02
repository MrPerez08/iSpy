document.getElementById('searchBox').addEventListener('keydown', function(event) {
    if (event.key === 'Enter') {
        let query = this.value;
        copyToClipboard(query);
        sendToVSCodeTerminal(query);
    }
});

function copyToClipboard(text) {
    const textarea = document.createElement('textarea');
    textarea.value = text;
    document.body.appendChild(textarea);
    textarea.select();
    document.execCommand('copy');
    document.body.removeChild(textarea);
    console.log('Query copied to clipboard:', text);
}

function sendToVSCodeTerminal(query) {
    fetch('http://localhost:3000/send-to-vscode', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ query: query })
    })
    .then(response => response.json())
    .then(data => {
        console.log('Response from server:', data);
    })
    .catch(error => {
        console.error('Error:', error);
    });
}
