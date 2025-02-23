document.addEventListener("DOMContentLoaded", function() {
    const randomButton = document.querySelector(".random-question-btn");

    async function getRandomQuestion() {
        try {
            const response = await fetch('/sitemap.xml');
            const text = await response.text();
            const parser = new DOMParser();
            const xmlDoc = parser.parseFromString(text, "application/xml");
            const urls = Array.from(xmlDoc.getElementsByTagName("loc"))
                .map(loc => loc.textContent)
                .filter(url => url.includes('/questions/') && !url.endsWith('/questions/'));

            if (urls.length > 0) {
                const randomIndex = Math.floor(Math.random() * urls.length);
                window.location.href = urls[randomIndex];
            } else {
                console.error("No question URLs found in sitemap.");
            }
        } catch (error) {
            console.error("Error fetching sitemap:", error);
        }
    }

    if (randomButton) {
        randomButton.addEventListener("click", getRandomQuestion);
    }
});
