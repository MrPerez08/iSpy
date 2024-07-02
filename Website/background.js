chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
    if (message.action === "copyQuery") {
        navigator.clipboard.writeText(message.query).then(() => {
            console.log("Query copied to clipboard");
            sendToVSCode(message.query);
        });
    }
});

function sendToVSCode(query) {
    const vscodeTerminalCommand = `code --execute-command workbench.action.terminal.sendSequence --args "${query}"`;
    chrome.runtime.sendNativeMessage("com.your_extension.native", { command: vscodeTerminalCommand }, response => {
        console.log("Response from native app:", response);
    });
}
