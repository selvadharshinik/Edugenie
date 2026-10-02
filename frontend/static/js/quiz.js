/**
 * EduGenie Interactive Quiz Engine
 * Handles step-by-step quiz state, option selection, visual feedback, scoring, and resets.
 */

class QuizEngine {
    constructor(containerId) {
        this.container = document.getElementById(containerId);
        this.questions = [];
        this.currentIndex = 0;
        this.score = 0;
        this.userAnswers = [];
        this.selectedOption = null;
        this.isAnswered = false;
        this.originalText = "";
    }

    startQuiz(quizData, originalText = "") {
        if (!quizData || !quizData.questions || quizData.questions.length === 0) {
            console.error("Invalid quiz data provided.");
            return;
        }

        this.questions = quizData.questions;
        this.originalText = originalText;
        this.currentIndex = 0;
        this.score = 0;
        this.userAnswers = [];
        this.isAnswered = false;
        this.selectedOption = null;

        this.renderQuestion();
    }

    renderQuestion() {
        if (!this.container) return;

        const total = this.questions.length;
        const currentQ = this.questions[this.currentIndex];
        const progressPct = Math.round(((this.currentIndex + 1) / total) * 100);

        this.isAnswered = false;
        this.selectedOption = null;

        const optionLetters = ['A', 'B', 'C', 'D'];

        this.container.innerHTML = `
            <div class="quiz-card glass-panel fade-in">
                <div class="quiz-header">
                    <div class="quiz-progress-info">
                        <span class="quiz-step-badge">Question ${this.currentIndex + 1} of ${total}</span>
                        <span class="quiz-progress-text">${progressPct}% Completed</span>
                    </div>
                    <div class="quiz-progress-bar-bg">
                        <div class="quiz-progress-bar-fill" style="width: ${progressPct}%"></div>
                    </div>
                </div>

                <div class="quiz-body">
                    <h3 class="quiz-question-text">${this.escapeHtml(currentQ.question)}</h3>

                    <div class="quiz-options-grid" id="quiz-options-container">
                        ${currentQ.options.map((opt, idx) => `
                            <button type="button" class="quiz-option-btn" data-index="${idx}">
                                <span class="option-letter">${optionLetters[idx]}</span>
                                <span class="option-text">${this.escapeHtml(opt)}</span>
                                <span class="option-icon"></span>
                            </button>
                        `).join('')}
                    </div>
                </div>

                <div class="quiz-footer" id="quiz-footer" style="display: none;">
                    <div class="quiz-feedback-banner" id="quiz-feedback-banner"></div>
                    <button type="button" class="btn btn-primary" id="btn-next-question">
                        ${this.currentIndex + 1 < total ? 'Next Question →' : 'Complete Quiz ✨'}
                    </button>
                </div>
            </div>
        `;

        // Attach option click handlers
        const optionBtns = this.container.querySelectorAll('.quiz-option-btn');
        optionBtns.forEach(btn => {
            btn.addEventListener('click', (e) => {
                const optIndex = parseInt(btn.getAttribute('data-index'), 10);
                this.handleAnswerSelection(optIndex);
            });
        });

        // Next button handler
        const nextBtn = this.container.querySelector('#btn-next-question');
        if (nextBtn) {
            nextBtn.addEventListener('click', () => this.nextQuestion());
        }
    }

    handleAnswerSelection(selectedIndex) {
        if (this.isAnswered) return;

        this.isAnswered = true;
        const currentQ = this.questions[this.currentIndex];
        const selectedText = currentQ.options[selectedIndex];
        const correctAnswerText = currentQ.answer;

        const isCorrect = (selectedText.trim() === correctAnswerText.trim());

        if (isCorrect) {
            this.score++;
        }

        this.userAnswers.push({
            question: currentQ.question,
            selected: selectedText,
            correct: correctAnswerText,
            isCorrect: isCorrect
        });

        // Update Option UI states
        const optionBtns = this.container.querySelectorAll('.quiz-option-btn');
        optionBtns.forEach((btn, idx) => {
            btn.disabled = true;
            btn.classList.add('disabled');

            const optText = currentQ.options[idx].trim();

            if (optText === correctAnswerText.trim()) {
                btn.classList.add('correct');
                btn.querySelector('.option-icon').innerHTML = `
                    <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
                        <path d="M20 6L9 17l-5-5"/>
                    </svg>`;
            } else if (idx === selectedIndex && !isCorrect) {
                btn.classList.add('incorrect');
                btn.querySelector('.option-icon').innerHTML = `
                    <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
                        <path d="M18 6L6 18M6 6l12 12"/>
                    </svg>`;
            }
        });

        // Show feedback banner and next button
        const footer = this.container.querySelector('#quiz-footer');
        const feedbackBanner = this.container.querySelector('#quiz-feedback-banner');

        if (footer && feedbackBanner) {
            footer.style.display = 'flex';
            if (isCorrect) {
                feedbackBanner.className = 'quiz-feedback-banner feedback-correct';
                feedbackBanner.innerHTML = `✨ <strong>Correct!</strong> Well done.`;
            } else {
                feedbackBanner.className = 'quiz-feedback-banner feedback-incorrect';
                feedbackBanner.innerHTML = `💡 <strong>Incorrect.</strong> Correct answer: <em>${this.escapeHtml(correctAnswerText)}</em>`;
            }
        }
    }

    nextQuestion() {
        if (this.currentIndex + 1 < this.questions.length) {
            this.currentIndex++;
            this.renderQuestion();
        } else {
            this.renderResults();
        }
    }

    renderResults() {
        const total = this.questions.length;
        const percentage = Math.round((this.score / total) * 100);

        let badgeClass = "grade-good";
        let message = "Great effort! Keep practicing to master this concept.";
        let emoji = "🎉";

        if (percentage === 100) {
            badgeClass = "grade-perfect";
            message = "Outstanding! You got a perfect score!";
            emoji = "🏆";
        } else if (percentage >= 66) {
            badgeClass = "grade-good";
            message = "Good job! You have a solid grasp of this topic.";
            emoji = "🌟";
        } else {
            badgeClass = "grade-needs-work";
            message = "Keep learning! Review the concepts and try again.";
            emoji = "📚";
        }

        this.container.innerHTML = `
            <div class="quiz-results-card glass-panel fade-in">
                <div class="results-header text-center">
                    <div class="results-emoji">${emoji}</div>
                    <h2>Quiz Complete!</h2>
                    <p class="results-subtitle">${message}</p>
                </div>

                <div class="score-display">
                    <div class="score-circle ${badgeClass}">
                        <span class="score-number">${this.score} / ${total}</span>
                        <span class="score-percentage">${percentage}%</span>
                    </div>
                </div>

                <div class="answers-recap">
                    <h4>Question Breakdown</h4>
                    <div class="recap-list">
                        ${this.userAnswers.map((ua, idx) => `
                            <div class="recap-item ${ua.isCorrect ? 'recap-correct' : 'recap-incorrect'}">
                                <div class="recap-status-icon">
                                    ${ua.isCorrect ? '✓' : '✗'}
                                </div>
                                <div class="recap-details">
                                    <p class="recap-question"><strong>Q${idx + 1}:</strong> ${this.escapeHtml(ua.question)}</p>
                                    <p class="recap-answer">
                                        Your answer: <span class="ans-tag ${ua.isCorrect ? 'tag-correct' : 'tag-incorrect'}">${this.escapeHtml(ua.selected)}</span>
                                        ${!ua.isCorrect ? `<br>Correct: <span class="tag-correct">${this.escapeHtml(ua.correct)}</span>` : ''}
                                    </p>
                                </div>
                            </div>
                        `).join('')}
                    </div>
                </div>

                <div class="results-actions">
                    <button type="button" class="btn btn-secondary" id="btn-quiz-retry">
                        🔄 Try Again
                    </button>
                    <button type="button" class="btn btn-primary" id="btn-quiz-new">
                        ✨ Generate Another Quiz
                    </button>
                </div>
            </div>
        `;

        // Action handlers
        const retryBtn = this.container.querySelector('#btn-quiz-retry');
        if (retryBtn) {
            retryBtn.addEventListener('click', () => {
                this.currentIndex = 0;
                this.score = 0;
                this.userAnswers = [];
                this.renderQuestion();
            });
        }

        const newQuizBtn = this.container.querySelector('#btn-quiz-new');
        if (newQuizBtn) {
            newQuizBtn.addEventListener('click', () => {
                if (window.EduGenieApp && typeof window.EduGenieApp.resetQuizInput === 'function') {
                    window.EduGenieApp.resetQuizInput();
                } else {
                    location.reload();
                }
            });
        }
    }

    escapeHtml(text) {
        if (!text) return '';
        return text
            .replace(/&/g, "&amp;")
            .replace(/</g, "&lt;")
            .replace(/>/g, "&gt;")
            .replace(/"/g, "&quot;")
            .replace(/'/g, "&#039;");
    }
}
