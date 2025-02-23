function getRandomQuestion() {
    const questions = window.siteQuestions || [];
    if (questions.length > 0) {
        window.location.href = questions[Math.floor(Math.random() * questions.length)];
    }
}
