---
layout: default
title: Search Results
description: "Search results for your query."
---

<!-- ✅ Search Page Layout -->
<section class="search-results">
  <h2>Search Results</h2>
  <ul id="search-results-list" class="fade-in"></ul>
</section>

<!-- ✅ Trending Searches Section -->
<section class="trending-searches">
  <h3>Trending Legal Questions</h3>
  <ul id="trending-search-list">
    <li><a href="/questions/is-it-legal-to-sleep-in-your-car-in-los-angeles/">Is it legal to sleep in your car in Los Angeles?</a></li>
    <li><a href="/questions/is-it-legal-to-fly-a-drone-in-london-without-a-permit/">Is it legal to fly a drone in London without a permit?</a></li>
    <li><a href="/questions/is-it-legal-to-own-exotic-pets-in-texas/">Is it legal to own exotic pets in Texas?</a></li>
  </ul>
</section>

<script>
  const urlParams = new URLSearchParams(window.location.search);
  const query = urlParams.get("query")?.toLowerCase();
  const resultsList = document.getElementById("search-results-list");
  const trendingSearches = document.querySelector(".trending-searches");

  async function loadSearchIndex() {
    const response = await fetch('/search.json');
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
      resultsList.innerHTML = results.map(({ item }) => 
        `<li><a href="${item.url}">${highlightMatch(item.title, query)}</a></li>`
      ).join('');
    }
    
    // Hide trending searches when searching
    if (query) {
      trendingSearches.style.display = 'none';
    }
  }

  function highlightMatch(text, query) {
    const regex = new RegExp(`(${query})`, 'gi');
    return text.replace(regex, '<span class="highlight">$1</span>');
  }

  if (query) {
    resultsList.innerHTML = `<li>Searching for "<strong>${query}</strong>"...</li>`;
    searchSite(query);
  }
</script>

