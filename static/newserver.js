const versionSelectElement = document.getElementById("minecraftVersionSelect");

// https://api.papermc.io/docs/swagger-ui/index.html?configUrl=/openapi/swagger-config
// Fetch latest available minecraft versions (https://api.papermc.io/v2/projects/paper).
async function getJSON(url) {
    return fetch(url)
            .then((response) => response.json())
            .then((json) => { return json });
}

// Fetch a list of all paper supported minecraft versions.
async function fetchPaperVersions() {
    const response = await getJSON("https://api.papermc.io/v2/projects/paper");
    return response["versions"];
}

async function updateForm() {
    const paperVersions = await fetchPaperVersions();

    // Append new options to version select element.
    for (let index = 0; index < paperVersions.length; index++) {
        const version = paperVersions[index];
        const option = document.createElement("option");
        option.value = version;
        option.textContent = version;

        versionSelectElement.appendChild(option);
    }

    // Select latest version by default.
    const latestVersion = paperVersions[paperVersions.length - 1];
    versionSelectElement.value = latestVersion;
    console.log(latestVersion);

    paperVersions.forEach((version) => {
        const option = document.createElement("option");
        option.value = version;
        option.textContent = version;
        versionSelectElement.appendChild(option);
    });
}

updateForm();