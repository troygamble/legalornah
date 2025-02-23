---
layout: default
title: Search Results
description: "Search results for your query."
---

<!-- ✅ search.md for results -->
<section class="search-results">
  <h2>Search Results</h2>
  <ul id="search-results-list"></ul>
</section>

<script>
  const urlParams = new URLSearchParams(window.location.search);
  const query = urlParams.get("query")?.toLowerCase();
  const resultsList = document.getElementById("search-results-list");

  async function loadSearchIndex() {
    const response = await fetch('/search.json'); // 👈 Ensure this is generated!
    return response.json();
  }

  async function searchSite(query) {
    const index = await loadSearchIndex();

    const fuse = new Fuse(index, {
      keys: ['title', 'content'],
      threshold: 0.3, // 🔍 Adjust for fuzziness
    });

    const results = fuse.search(query);

    if (results.length === 0) {
      resultsList.innerHTML = `<li>No results found for "<strong>${query}</strong>".</li>`;
    } else {
      resultsList.innerHTML = results
        .map(({ item }) => `<li><a href="${item.url}">${item.title}</a></li>`)
        .join('');
    }
  }

  if (query) {
    resultsList.innerHTML = `<li>Searching for "<strong>${query}</strong>"...</li>`;
    searchSite(query);
  } else {
    resultsList.innerHTML = "<li>No search query provided.</li>";
  }
</script>
