const consoleElement = document.getElementById("console");

function pushLine(lineText) {
    const line = document.createElement("p");
    line.style.margin = 0;
    line.textContent = lineText;
    consoleElement.appendChild(line);
}