const form = document.getElementById("analyze-form");
const urlInput = document.getElementById("url-input");
const button = document.getElementById("analyze-button");

const inputWrapper = document.querySelector(".input-wrapper");
const buttonText = document.querySelector(".button-text");

const results = document.getElementById("results");
const errorMessage = document.getElementById("error-message");


form.addEventListener("submit", async (event) => {

    event.preventDefault();

    const url = urlInput.value.trim();

    errorMessage.textContent = "";

    startLoading();

    try {

        const response = await fetch(
            `/analyze?url=${encodeURIComponent(url)}`
        );

        const data = await response.json();

        if (!response.ok) {
            throw new Error(getErrorMessage(data));
        }

        displayResults(data);

    } catch (error) {

        errorMessage.textContent =
            error.message || "Something went wrong.";

    } finally {

        stopLoading();

    }
});


function startLoading() {

    button.disabled = true;
    buttonText.textContent = "Scanning";

    inputWrapper.classList.add("loading");
}


function stopLoading() {

    button.disabled = false;
    buttonText.textContent = "Analyze";

    inputWrapper.classList.remove("loading");
}


function displayResults(data) {

    document.getElementById("status-code").textContent =
        `${data.status_code} OK`;

    document.getElementById("response-time").textContent =
        `${Math.round(data.response_time_ms)} ms`;

    document.getElementById("h1-count").textContent =
        data.h1_count;

    document.getElementById("missing-alt").textContent =
        data.images_missing_alt;

    document.getElementById("word-count").textContent =
        Number(data.word_count).toLocaleString();

    document.getElementById("page-title").textContent =
        data.title || "Not found";

    document.getElementById("meta-description").textContent =
        data.meta_description || "Not found";

    try {

        const analyzedUrl = new URL(urlInput.value);

        document.getElementById("analyzed-url").textContent =
            analyzedUrl.hostname;

    } catch {

        document.getElementById("analyzed-url").textContent =
            urlInput.value;

    }

    results.classList.add("hidden");

    requestAnimationFrame(() => {

        results.classList.remove("hidden");

        results.scrollIntoView({
            behavior: "smooth",
            block: "center"
        });

    });
}


function getErrorMessage(data) {

    if (typeof data.detail === "string") {
        return data.detail;
    }

    if (Array.isArray(data.detail)) {
        return "Please enter a valid webpage URL.";
    }

    return "Unable to analyze this webpage.";
}