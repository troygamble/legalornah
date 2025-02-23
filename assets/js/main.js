document.addEventListener("DOMContentLoaded", function() {
    const randomButton = document.querySelector(".random-question-btn");
    const questionsList = document.getElementById("questions-list");

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

    // ✅ Populate the "Browse All Questions" list dynamically
    if (questionsList) {
        fetch("/sitemap.xml")
            .then((response) => response.text())
            .then((data) => {
                const parser = new DOMParser();
                const xml = parser.parseFromString(data, "text/xml");
                const urls = xml.getElementsByTagName("loc");

                for (let i = 0; i < urls.length; i++) {
                    const url = urls[i].textContent;
                    if (url.includes("/questions/") && url !== window.location.href) {
                        const title = decodeURIComponent(
                            url.split("/").filter(Boolean).pop().replace(/-/g, " ")
                        );
                        const li = document.createElement("li");
                        li.innerHTML = `<a href="${url}">${title}</a>`;
                        questionsList.appendChild(li);
                    }
                }
            })
            .catch((error) => console.error("Error loading sitemap:", error));
    }
});
