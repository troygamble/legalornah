---
layout: default
title: Search Results
description: "Search results for your query."
---

<section class="search-results">
  <h2>Search Results</h2>
  <ul id="search-results-list"></ul>
</section>

<script>
  const urlParams = new URLSearchParams(window.location.search);
  const query = urlParams.get("query");
  const resultsList = document.getElementById("search-results-list");

  if (query) {
    resultsList.innerHTML = `<li>Showing results for '<strong>${query}</strong>' (functionality coming soon)</li>`;
  } else {
    resultsList.innerHTML = "<li>No search query provided.</li>";
  }
</script>