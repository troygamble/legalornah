function getRandomQuestion() {
    var questions = [
      {% for question in site.questions %}
        "{{ question.url }}",
      {% endfor %}
    ];
    return questions[Math.floor(Math.random() * questions.length)];
}
