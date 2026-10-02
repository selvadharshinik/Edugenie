/**
 * EduGenie Interactive 3D Flashcard Engine
 * Controls 3D card flips, study progress, mastery counts, and deck navigation.
 */

class FlashcardEngine {
    constructor(containerId) {
        this.container = document.getElementById(containerId);
        this.cards = [];
        this.currentIndex = 0;
        this.mastered = 0;
        this.needsReview = 0;
        this.isFlipped = false;
    }

    startDeck(data) {
        if (!data || !data.cards || data.cards.length === 0) return;
        this.cards = data.cards;
        this.currentIndex = 0;
        this.mastered = 0;
        this.needsReview = 0;
        this.isFlipped = false;

        this.renderCard();
    }

    renderCard() {
        if (!this.container) return;
        const total = this.cards.length;
        const card = this.cards[this.currentIndex];
        this.isFlipped = false;

        this.container.innerHTML = `
            <div class="flashcard-deck-wrapper glass-panel fade-in">
                <div class="deck-header">
                    <div class="deck-stats">
                        <span class="stat-badge stat-mastered">✅ Mastered: ${this.mastered}</span>
                        <span class="stat-badge stat-review">🧠 Needs Review: ${this.needsReview}</span>
                    </div>
                    <span class="deck-progress">Card ${this.currentIndex + 1} of ${total}</span>
                </div>

                <div class="flashcard-3d-scene" id="flashcard-scene">
                    <div class="flashcard-3d-card" id="flashcard-card">
                        <!-- FRONT -->
                        <div class="flashcard-face flashcard-front">
                            <span class="card-side-label">TERM / CONCEPT</span>
                            <div class="card-main-text">${this.escapeHtml(card.term)}</div>
                            <div class="card-hint-prompt">💡 Click or press Space to Flip Card</div>
                        </div>

                        <!-- BACK -->
                        <div class="flashcard-face flashcard-back">
                            <span class="card-side-label">DEFINITION & EXPLANATION</span>
                            <div class="card-main-text">${this.escapeHtml(card.definition)}</div>
                            ${card.example ? `<div class="card-example-box"><strong>Example:</strong> ${this.escapeHtml(card.example)}</div>` : ''}
                        </div>
                    </div>
                </div>

                <div class="deck-controls">
                    <button type="button" class="btn btn-secondary" id="btn-prev-card" ${this.currentIndex === 0 ? 'disabled' : ''}>
                        ← Previous
                    </button>
                    
                    <button type="button" class="btn btn-review-action" id="btn-mark-review">
                        🧠 Needs Review
                    </button>

                    <button type="button" class="btn btn-master-action" id="btn-mark-master">
                        ✅ Know It!
                    </button>

                    <button type="button" class="btn btn-secondary" id="btn-next-card" ${this.currentIndex + 1 >= total ? 'disabled' : ''}>
                        Next →
                    </button>
                </div>
            </div>
        `;

        // Card flip listener
        const scene = this.container.querySelector('#flashcard-scene');
        const cardEl = this.container.querySelector('#flashcard-card');

        if (scene && cardEl) {
            scene.addEventListener('click', () => {
                this.isFlipped = !this.isFlipped;
                cardEl.classList.toggle('is-flipped', this.isFlipped);
            });
        }

        // Button handlers
        const prevBtn = this.container.querySelector('#btn-prev-card');
        if (prevBtn) prevBtn.addEventListener('click', (e) => { e.stopPropagation(); this.prevCard(); });

        const nextBtn = this.container.querySelector('#btn-next-card');
        if (nextBtn) nextBtn.addEventListener('click', (e) => { e.stopPropagation(); this.nextCard(); });

        const markMaster = this.container.querySelector('#btn-mark-master');
        if (markMaster) markMaster.addEventListener('click', (e) => { e.stopPropagation(); this.markMastered(); });

        const markReview = this.container.querySelector('#btn-mark-review');
        if (markReview) markReview.addEventListener('click', (e) => { e.stopPropagation(); this.markReview(); });
    }

    markMastered() {
        this.mastered++;
        // Update stats widget if present
        const masteredWidget = document.getElementById('stat-mastered-count');
        if (masteredWidget) {
            let current = parseInt(masteredWidget.textContent || '0', 10);
            masteredWidget.textContent = (current + 1).toString();
        }
        this.nextCard();
    }

    markReview() {
        this.needsReview++;
        this.nextCard();
    }

    nextCard() {
        if (this.currentIndex + 1 < this.cards.length) {
            this.currentIndex++;
            this.renderCard();
        } else {
            this.renderDeckComplete();
        }
    }

    prevCard() {
        if (this.currentIndex > 0) {
            this.currentIndex--;
            this.renderCard();
        }
    }

    renderDeckComplete() {
        this.container.innerHTML = `
            <div class="glass-panel text-center fade-in" style="padding: 2.5rem;">
                <div style="font-size: 3rem; margin-bottom: 0.5rem;">🏆</div>
                <h2>Flashcard Deck Complete!</h2>
                <p style="color: var(--text-secondary); margin-bottom: 1.5rem;">
                    Mastered: <strong>${this.mastered}</strong> | Needs Review: <strong>${this.needsReview}</strong>
                </p>
                <button type="button" class="btn btn-primary" onclick="FlashcardEngine.resetFlashcards()">
                    🔄 Study Deck Again
                </button>
            </div>
        `;
    }

    static resetFlashcards() {
        const inputContainer = document.getElementById('flashcard-input-container');
        const deckContainer = document.getElementById('flashcard-deck-container');
        if (inputContainer) inputContainer.style.display = 'block';
        if (deckContainer) {
            deckContainer.style.display = 'none';
            deckContainer.innerHTML = '';
        }
    }

    escapeHtml(text) {
        if (!text) return '';
        return text.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/"/g, "&quot;");
    }
}
