---
layout: default
title: Is It Legal?
description: "A fun Q&A site answering weird and interesting 'Is it legal...?' questions."
affiliate_asin: B08XYZ1234  # Replace with the actual product ASIN
affiliate_title: "Weird Laws: The Funniest Legal Curiosities"
affiliate_text: "Check out this awesome book about bizarre legal cases:"
---

<!-- Hero Banner Section -->
<div class="hero-banner">
  <h1 style="font-size: 48px; margin-bottom: 20px;">Welcome to Is It Legal?</h1>
  <p style="font-size: 20px; margin-bottom: 30px;">Where bizarre legal questions get surprising answers!</p>
  <div class="hero-buttons">
    <a href="/questions/" class="btn hero-btn">Browse All Questions</a>
    <a href="javascript:void(0);" onclick="location.href=getRandomQuestion();" class="btn hero-btn">Random Question</a>
  </div>
</div>




<!-- Main Content -->
<section class="content-section">
  <h2>Featured Questions</h2>
  <div class="featured-grid">
    {% assign featured_questions = site.questions | sample:6 %}
    {% for question in featured_questions %}
      <div class="featured-item">
        <a href="{{ question.url }}">
          <div class="featured-item-inner">
            <h3>{{ question.title }}</h3>
          </div>
        </a>
      </div>
    {% endfor %}
  </div>
</section>

<!-- Popular Topics -->
<section class="topics-section">
  <h2>Popular Topics</h2>
  <ul class="topics-list">
    <li>✅ <span class="topic-icon">&#128161;</span> Weird Laws</li>
    <li>✅ <span class="topic-icon">&#128293;</span> Obscure Legal Loopholes</li>
    <li>✅ <span class="topic-icon">&#127979;</span> State-Specific Laws</li>
    <li>✅ <span class="topic-icon">&#128218;</span> Bizarre Historical Laws</li>
  </ul>
</section>

<!-- Amazon Affiliate Section -->
<section class="affiliate-section">
  {% include affiliate.html %}
</section>

<!-- Disclaimer & Call-to-Action -->
<section class="disclaimer-section">
  <p class="disclaimer">This site is for entertainment purposes only. Laws vary by region. Always consult a legal professional for real legal advice.</p>
  <p class="call-to-action">Bookmark us & check back often for new legal insights!</p>
</section>

<script>
  // Collect all question URLs from the site into an array
  function getRandomQuestion() {
    var questions = [
      {% for question in site.questions %}
        "{{ question.url }}",
      {% endfor %}
    ];
    return questions[Math.floor(Math.random() * questions.length)];
  }
</script>
