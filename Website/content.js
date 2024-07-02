document.addEventListener('keydown', (event) => {
    if (event.key === 'Enter') {
        let searchBox = document.querySelector('input[name="q"]');
        let query = searchBox.value;
        chrome.runtime.sendMessage({ action: "copyQuery", query: query });
    }
});
