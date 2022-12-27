const consoleElement = document.getElementById("console");
const serverIndex = parseInt(consoleElement.getAttribute("data-server-index"));

function createLine(text) {
    const line = document.createElement("p");
    line.style.margin = 0;
    line.textContent = text;
    return line;
}

function pushLine(text) {
    const line = createLine(text);
    consoleElement.appendChild(line);
}

function pushLineAtStart(text) {
    const line = createLine(text);
    consoleElement.insertBefore(line, consoleElement.children[0]);
}

async function fetchOldLogs() {
    const response = await fetch(`${location.protocol}//${location.host}/api/server/${serverIndex}/oldLogs/0`)
        .then((response) => response.json())
        .then((json) => { return json });
    const success = response["result"];
    
    // Check if request was successful.
    if (!success) return [];

    return response["logs"];
}

function showOldLogs() {
    fetchLatestLogs().then((latestLogs) => latestLogs.forEach((line) => pushLine(line)));
}

// Initialize SocketIO
const socket = io(`ws://${location.host}/logs`);

socket.emit("request-last-logs", serverIndex);

socket.on("last-logs", (logs) => {
    logs.forEach((log) => pushLine(log));
});
