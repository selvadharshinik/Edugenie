/**
 * EduGenie Application Core Controller
 * Orchestrates views, sidebar, themes, forms, markdown rendering, export suite, TTS, and local history.
 */

document.addEventListener('DOMContentLoaded', () => {
    // Global Engine Instances
    window.quizEngine = new QuizEngine('quiz-interactive-container');
    window.flashcardEngine = new FlashcardEngine('flashcard-deck-container');

    const EduGenieApp = {
        activeView: 'dashboard',
        theme: localStorage.getItem('edugenie_theme') || 'dark',

        init() {
            this.applyTheme(this.theme);
            this.setupNavigation();
            this.setupThemeToggle();
            this.setupMobileMenu();
            this.setupFormSubmissions();
            this.setupQuickActions();
            this.setupPomodoroTimer();
            this.loadRecentActivity();
        },

        // Theme Toggle
        applyTheme(theme) {
            this.theme = theme;
            document.documentElement.setAttribute('data-theme', theme);
            localStorage.setItem('edugenie_theme', theme);
            
            const themeBtn = document.getElementById('btn-theme-toggle');
            if (themeBtn) {
                themeBtn.innerHTML = theme === 'dark' 
                    ? `<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 3v1m0 16v1m9-9h-1M4 12H3m15.364 6.364l-.707-.707M6.343 6.343l-.707-.707m12.728 0l-.707.707M6.343 17.657l-.707.707M16 12a4 4 0 11-8 0 4 4 0 018 0z"/></svg> Light` 
                    : `<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 12.79A9 9 0 1111.21 3 7 7 0 0021 12.79z"/></svg> Dark`;
            }
        },

        setupThemeToggle() {
            const themeBtn = document.getElementById('btn-theme-toggle');
            if (themeBtn) {
                themeBtn.addEventListener('click', () => {
                    const newTheme = this.theme === 'dark' ? 'light' : 'dark';
                    this.applyTheme(newTheme);
                });
            }
        },

        // Navigation & Views
        setupNavigation() {
            const navLinks = document.querySelectorAll('[data-view-target]');
            navLinks.forEach(link => {
                link.addEventListener('click', (e) => {
                    e.preventDefault();
                    const target = link.getAttribute('data-view-target');
                    this.switchView(target);

                    const sidebar = document.getElementById('sidebar');
                    if (sidebar && sidebar.classList.contains('mobile-open')) {
                        sidebar.classList.remove('mobile-open');
                    }
                });
            });
        },

        switchView(viewName) {
            const views = document.querySelectorAll('.view-panel');
            views.forEach(v => v.classList.remove('active'));

            const targetView = document.getElementById(`view-${viewName}`);
            if (targetView) {
                targetView.classList.add('active');
                this.activeView = viewName;
            }

            const navLinks = document.querySelectorAll('.nav-item');
            navLinks.forEach(item => {
                if (item.getAttribute('data-view-target') === viewName) {
                    item.classList.add('active');
                } else {
                    item.classList.remove('active');
                }
            });

            window.scrollTo({ top: 0, behavior: 'smooth' });
        },

        setupMobileMenu() {
            const hamburger = document.getElementById('btn-mobile-menu');
            const sidebar = document.getElementById('sidebar');
            const overlay = document.getElementById('sidebar-overlay');

            if (hamburger && sidebar) {
                hamburger.addEventListener('click', () => {
                    sidebar.classList.toggle('mobile-open');
                    if (overlay) overlay.classList.toggle('active');
                });
            }

            if (overlay && sidebar) {
                overlay.addEventListener('click', () => {
                    sidebar.classList.remove('mobile-open');
                    overlay.classList.remove('active');
                });
            }
        },

        setupQuickActions() {
            const cards = document.querySelectorAll('.quick-action-card');
            cards.forEach(card => {
                card.addEventListener('click', () => {
                    const target = card.getAttribute('data-target-view');
                    if (target) {
                        this.switchView(target);
                    }
                });
            });

            const heroForm = document.getElementById('hero-prompt-form');
            if (heroForm) {
                heroForm.addEventListener('submit', (e) => {
                    e.preventDefault();
                    const heroInput = document.getElementById('hero-prompt-input');
                    if (heroInput && heroInput.value.trim()) {
                        const query = heroInput.value.trim();
                        heroInput.value = '';
                        this.switchView('qa');
                        const qaInput = document.getElementById('qa-question-input');
                        if (qaInput) {
                            qaInput.value = query;
                            this.handleQASubmit(query);
                        }
                    }
                });
            }
        },

        // Form Handlers
        setupFormSubmissions() {
            // Core 5
            const qaForm = document.getElementById('form-qa');
            if (qaForm) qaForm.addEventListener('submit', (e) => { e.preventDefault(); const val = document.getElementById('qa-question-input').value.trim(); if (val) this.handleQASubmit(val); });

            const explainForm = document.getElementById('form-explain');
            if (explainForm) explainForm.addEventListener('submit', (e) => { e.preventDefault(); const val = document.getElementById('explain-topic-input').value.trim(); if (val) this.handleExplainSubmit(val); });

            const quizForm = document.getElementById('form-quiz');
            if (quizForm) quizForm.addEventListener('submit', (e) => { e.preventDefault(); const val = document.getElementById('quiz-text-input').value.trim(); if (val) this.handleQuizSubmit(val); });

            const summarizeForm = document.getElementById('form-summarize');
            if (summarizeForm) summarizeForm.addEventListener('submit', (e) => { e.preventDefault(); const val = document.getElementById('summarize-text-input').value.trim(); if (val) this.handleSummarizeSubmit(val); });

            const learnForm = document.getElementById('form-learn');
            if (learnForm) learnForm.addEventListener('submit', (e) => { e.preventDefault(); const val = document.getElementById('learn-topic-input').value.trim(); if (val) this.handleLearningPathSubmit(val); });

            // New 4 Advanced Capabilities
            const flashcardForm = document.getElementById('form-flashcards');
            if (flashcardForm) flashcardForm.addEventListener('submit', (e) => {
                e.preventDefault();
                const topic = document.getElementById('flashcard-topic-input').value.trim();
                const count = parseInt(document.getElementById('flashcard-count-input').value, 10) || 5;
                if (topic) this.handleFlashcardSubmit(topic, count);
            });

            const codeForm = document.getElementById('form-code');
            if (codeForm) codeForm.addEventListener('submit', (e) => {
                e.preventDefault();
                const code = document.getElementById('code-input').value.trim();
                const lang = document.getElementById('code-lang-select').value;
                if (code) this.handleCodeSubmit(code, lang);
            });

            const mindmapForm = document.getElementById('form-mindmap');
            if (mindmapForm) mindmapForm.addEventListener('submit', (e) => {
                e.preventDefault();
                const topic = document.getElementById('mindmap-topic-input').value.trim();
                if (topic) this.handleMindMapSubmit(topic);
            });

            const studyPlanForm = document.getElementById('form-study-plan');
            if (studyPlanForm) studyPlanForm.addEventListener('submit', (e) => {
                e.preventDefault();
                const topic = document.getElementById('study-topic-input').value.trim();
                const days = parseInt(document.getElementById('study-days-input').value, 10) || 7;
                const hours = parseFloat(document.getElementById('study-hours-input').value) || 2.0;
                if (topic) this.handleStudyPlanSubmit(topic, days, hours);
            });
        },

        // Core 1: Q&A
        async handleQASubmit(question) {
            const outputCard = document.getElementById('qa-result-card');
            const outputBody = document.getElementById('qa-result-body');
            const submitBtn = document.getElementById('btn-qa-submit');

            this.showLoading(outputCard, outputBody, submitBtn, "✦ EduGenie is thinking...");

            try {
                const res = await API.askQuestion(question);
                this.hideLoading(submitBtn);

                outputBody.innerHTML = `<div class="response-content">${this.formatMarkdown(res.answer)}</div>`;
                this.setupCardActions(outputCard, res.answer, () => this.handleQASubmit(question));
                this.addRecentActivity('Q&A', question);
            } catch (err) {
                this.renderError(outputCard, outputBody, submitBtn, err.message, () => this.handleQASubmit(question));
            }
        },

        // Core 2: Explanation
        async handleExplainSubmit(topic) {
            const outputCard = document.getElementById('explain-result-card');
            const outputBody = document.getElementById('explain-result-body');
            const submitBtn = document.getElementById('btn-explain-submit');

            this.showLoading(outputCard, outputBody, submitBtn, "✦ EduGenie is crafting your explanation...");

            try {
                const res = await API.explainTopic(topic);
                this.hideLoading(submitBtn);

                outputBody.innerHTML = `
                    <div class="response-content">
                        <div class="topic-header">
                            <span class="topic-badge">Topic</span>
                            <h3 class="topic-title">${this.escapeHtml(res.topic)}</h3>
                        </div>
                        ${this.formatMarkdown(res.explanation)}
                    </div>
                `;

                this.setupCardActions(outputCard, res.explanation, () => this.handleExplainSubmit(topic));
                this.addRecentActivity('Explanation', topic);
            } catch (err) {
                this.renderError(outputCard, outputBody, submitBtn, err.message, () => this.handleExplainSubmit(topic));
            }
        },

        // Core 3: Quiz
        async handleQuizSubmit(text) {
            const inputContainer = document.getElementById('quiz-input-container');
            const interactiveContainer = document.getElementById('quiz-interactive-container');
            const submitBtn = document.getElementById('btn-quiz-submit');

            if (submitBtn) {
                submitBtn.disabled = true;
                submitBtn.innerHTML = `<span class="spinner"></span> Generating Quiz...`;
            }

            interactiveContainer.style.display = 'block';
            interactiveContainer.innerHTML = `
                <div class="glass-panel skeleton-loader fade-in">
                    <div class="thinking-indicator">
                        <span class="sparkle-icon">✦</span> EduGenie is building your 3-question quiz...
                    </div>
                </div>
            `;

            try {
                const res = await API.generateQuiz(text);

                if (submitBtn) {
                    submitBtn.disabled = false;
                    submitBtn.innerHTML = `⚡ Generate Quiz`;
                }

                inputContainer.style.display = 'none';
                window.quizEngine.startQuiz(res, text);
                this.addRecentActivity('Quiz', text.slice(0, 40) + '...');
            } catch (err) {
                if (submitBtn) {
                    submitBtn.disabled = false;
                    submitBtn.innerHTML = `⚡ Generate Quiz`;
                }

                interactiveContainer.innerHTML = `
                    <div class="glass-panel error-card fade-in">
                        <div class="error-icon">⚠️</div>
                        <h4>Quiz Generation Error</h4>
                        <p>${this.escapeHtml(err.message)}</p>
                        <button type="button" class="btn btn-secondary" onclick="EduGenieApp.resetQuizInput()">Try Again</button>
                    </div>
                `;
            }
        },

        resetQuizInput() {
            const inputContainer = document.getElementById('quiz-input-container');
            const interactiveContainer = document.getElementById('quiz-interactive-container');
            if (inputContainer) inputContainer.style.display = 'block';
            if (interactiveContainer) {
                interactiveContainer.style.display = 'none';
                interactiveContainer.innerHTML = '';
            }
        },

        // Core 4: Summary
        async handleSummarizeSubmit(text) {
            const outputCard = document.getElementById('summarize-result-card');
            const outputBody = document.getElementById('summarize-result-body');
            const submitBtn = document.getElementById('btn-summarize-submit');

            this.showLoading(outputCard, outputBody, submitBtn, "✦ EduGenie is summarizing text...");

            try {
                const res = await API.summarizeText(text);
                this.hideLoading(submitBtn);

                outputBody.innerHTML = `<div class="response-content">${this.formatMarkdown(res.summary)}</div>`;
                this.setupCardActions(outputCard, res.summary, () => this.handleSummarizeSubmit(text));
                this.addRecentActivity('Summary', text.slice(0, 40) + '...');
            } catch (err) {
                this.renderError(outputCard, outputBody, submitBtn, err.message, () => this.handleSummarizeSubmit(text));
            }
        },

        // Core 5: Learning Path
        async handleLearningPathSubmit(topic) {
            const outputCard = document.getElementById('learn-result-card');
            const outputBody = document.getElementById('learn-result-body');
            const submitBtn = document.getElementById('btn-learn-submit');

            this.showLoading(outputCard, outputBody, submitBtn, "✦ EduGenie is charting your learning roadmap...");

            try {
                const res = await API.generateLearningPath(topic);
                this.hideLoading(submitBtn);

                outputBody.innerHTML = this.renderRoadmapUI(res);
                this.setupCardActions(outputCard, JSON.stringify(res, null, 2), () => this.handleLearningPathSubmit(topic));
                this.addRecentActivity('Learning Path', topic);
            } catch (err) {
                this.renderError(outputCard, outputBody, submitBtn, err.message, () => this.handleLearningPathSubmit(topic));
            }
        },

        // New Feature 6: Flashcards Deck
        async handleFlashcardSubmit(topic, count) {
            const inputContainer = document.getElementById('flashcard-input-container');
            const deckContainer = document.getElementById('flashcard-deck-container');
            const submitBtn = document.getElementById('btn-flashcard-submit');

            if (submitBtn) {
                submitBtn.disabled = true;
                submitBtn.innerHTML = `<span class="spinner"></span> Generating Flashcards...`;
            }

            deckContainer.style.display = 'block';
            deckContainer.innerHTML = `
                <div class="glass-panel skeleton-loader fade-in">
                    <div class="thinking-indicator">
                        <span class="sparkle-icon">✦</span> EduGenie is creating ${count} interactive flashcards...
                    </div>
                </div>
            `;

            try {
                const res = await API.generateFlashcards(topic, count);

                if (submitBtn) {
                    submitBtn.disabled = false;
                    submitBtn.innerHTML = `🎴 Generate Flashcards`;
                }

                inputContainer.style.display = 'none';
                window.flashcardEngine.startDeck(res);
                this.addRecentActivity('Flashcards', topic);
            } catch (err) {
                if (submitBtn) {
                    submitBtn.disabled = false;
                    submitBtn.innerHTML = `🎴 Generate Flashcards`;
                }

                deckContainer.innerHTML = `
                    <div class="glass-panel error-card fade-in">
                        <div class="error-icon">⚠️</div>
                        <h4>Flashcard Error</h4>
                        <p>${this.escapeHtml(err.message)}</p>
                        <button type="button" class="btn btn-secondary" onclick="FlashcardEngine.resetFlashcards()">Try Again</button>
                    </div>
                `;
            }
        },

        // New Feature 7: Code Explainer
        async handleCodeSubmit(code, lang) {
            const outputCard = document.getElementById('code-result-card');
            const outputBody = document.getElementById('code-result-body');
            const submitBtn = document.getElementById('btn-code-submit');

            this.showLoading(outputCard, outputBody, submitBtn, "✦ EduGenie is analyzing your code...");

            try {
                const res = await API.explainCode(code, lang);
                this.hideLoading(submitBtn);

                outputBody.innerHTML = `
                    <div class="response-content">
                        <div class="code-meta-bar">
                            <span class="badge badge-complexity">⏱️ Time: ${this.escapeHtml(res.time_complexity)}</span>
                            <span class="badge badge-complexity">💾 Space: ${this.escapeHtml(res.space_complexity)}</span>
                        </div>

                        <h4 style="margin-top: 1rem;">Summary</h4>
                        <p>${this.escapeHtml(res.summary)}</p>

                        <h4 style="margin-top: 1.5rem;">Line-by-Line Breakdown</h4>
                        <div class="code-line-list">
                            ${(res.line_by_line || []).map(line => `
                                <div class="code-line-item">
                                    <span class="code-chunk-label">${this.escapeHtml(line.line_or_section)}</span>
                                    <p class="code-chunk-desc">${this.escapeHtml(line.explanation)}</p>
                                </div>
                            `).join('')}
                        </div>

                        ${res.optimizations && res.optimizations.length ? `
                            <h4 style="margin-top: 1.5rem;">💡 Optimizations & Tips</h4>
                            <ul>
                                ${res.optimizations.map(opt => `<li>${this.escapeHtml(opt)}</li>`).join('')}
                            </ul>
                        ` : ''}

                        ${res.refactored_code ? `
                            <h4 style="margin-top: 1.5rem;">✨ Refactored Code</h4>
                            <pre><code>${this.escapeHtml(res.refactored_code)}</code></pre>
                        ` : ''}
                    </div>
                `;

                this.setupCardActions(outputCard, res.summary + "\n\n" + (res.refactored_code || ""), () => this.handleCodeSubmit(code, lang));
                this.addRecentActivity('Code Analysis', code.slice(0, 30) + '...');
            } catch (err) {
                this.renderError(outputCard, outputBody, submitBtn, err.message, () => this.handleCodeSubmit(code, lang));
            }
        },

        // New Feature 8: Mind Map Graph
        async handleMindMapSubmit(topic) {
            const outputCard = document.getElementById('mindmap-result-card');
            const outputBody = document.getElementById('mindmap-result-body');
            const submitBtn = document.getElementById('btn-mindmap-submit');

            this.showLoading(outputCard, outputBody, submitBtn, "✦ EduGenie is building your mind map...");

            try {
                const res = await API.generateMindMap(topic);
                this.hideLoading(submitBtn);

                outputBody.innerHTML = this.renderMindMapTree(res);
                this.setupCardActions(outputCard, JSON.stringify(res, null, 2), () => this.handleMindMapSubmit(topic));
                this.addRecentActivity('Mind Map', topic);
            } catch (err) {
                this.renderError(outputCard, outputBody, submitBtn, err.message, () => this.handleMindMapSubmit(topic));
            }
        },

        renderMindMapTree(data) {
            const nodes = data.nodes || [];
            const root = nodes.find(n => !n.parent_id) || nodes[0];
            const children = nodes.filter(n => n.parent_id === (root ? root.id : null));

            return `
                <div class="mindmap-container">
                    <div class="mindmap-root-node glass-panel">
                        <span class="root-badge">CENTRAL TOPIC</span>
                        <h3>${this.escapeHtml(data.topic)}</h3>
                        <p>${this.escapeHtml(root ? root.description : '')}</p>
                    </div>

                    <div class="mindmap-branches-grid">
                        ${children.map(child => {
                            const leafNodes = nodes.filter(n => n.parent_id === child.id);
                            return `
                                <div class="mindmap-branch-card glass-panel fade-in">
                                    <div class="branch-header">
                                        <h4>💡 ${this.escapeHtml(child.label)}</h4>
                                        <p>${this.escapeHtml(child.description)}</p>
                                    </div>
                                    ${leafNodes.length ? `
                                        <div class="leaf-list">
                                            ${leafNodes.map(leaf => `
                                                <div class="leaf-item">
                                                    <strong>• ${this.escapeHtml(leaf.label)}:</strong> ${this.escapeHtml(leaf.description)}
                                                </div>
                                            `).join('')}
                                        </div>
                                    ` : ''}
                                </div>
                            `;
                        }).join('')}
                    </div>
                </div>
            `;
        },

        // New Feature 9: Study Schedule
        async handleStudyPlanSubmit(topic, days, hours) {
            const outputCard = document.getElementById('study-result-card');
            const outputBody = document.getElementById('study-result-body');
            const submitBtn = document.getElementById('btn-study-submit');

            this.showLoading(outputCard, outputBody, submitBtn, `✦ EduGenie is building your ${days}-day study plan...`);

            try {
                const res = await API.generateStudyPlan(topic, days, hours);
                this.hideLoading(submitBtn);

                outputBody.innerHTML = `
                    <div class="study-plan-wrapper">
                        <div class="study-plan-header">
                            <h3>Exam / Topic: <span class="highlight">${this.escapeHtml(res.topic)}</span></h3>
                            <p><strong>Strategy Overview:</strong> ${this.escapeHtml(res.strategy_overview)}</p>
                        </div>

                        <div class="study-days-list">
                            ${(res.schedule || []).map(day => `
                                <div class="study-day-card glass-panel fade-in">
                                    <div class="day-badge">Day ${day.day}</div>
                                    <div class="day-details">
                                        <h4 class="day-focus">🎯 ${this.escapeHtml(day.focus_area)}</h4>
                                        <ul class="day-tasks">
                                            ${(day.tasks || []).map(t => `<li><input type="checkbox"> <span>${this.escapeHtml(t)}</span></li>`).join('')}
                                        </ul>
                                        <span class="day-break">⏱️ ${this.escapeHtml(day.break_strategy)}</span>
                                    </div>
                                </div>
                            `).join('')}
                        </div>
                    </div>
                `;

                this.setupCardActions(outputCard, res.strategy_overview, () => this.handleStudyPlanSubmit(topic, days, hours));
                this.addRecentActivity('Study Plan', topic);
            } catch (err) {
                this.renderError(outputCard, outputBody, submitBtn, err.message, () => this.handleStudyPlanSubmit(topic, days, hours));
            }
        },

        // Renderers & Utilities
        renderRoadmapUI(data) {
            const stages = data.stages || [];
            return `
                <div class="roadmap-header text-center">
                    <span class="topic-badge">Custom Roadmap</span>
                    <h2>Learning Journey: <span class="highlight">${this.escapeHtml(data.topic)}</span></h2>
                    <p>Follow this step-by-step path from core concepts to advanced mastery.</p>
                </div>

                <div class="roadmap-timeline">
                    ${stages.map((stage, idx) => `
                        <div class="roadmap-stage-card glass-panel fade-in">
                            <div class="stage-number">0${stage.order || idx + 1}</div>
                            <div class="stage-content">
                                <div class="stage-badge stage-${(stage.level || 'beginner').toLowerCase()}">${this.escapeHtml(stage.level)}</div>
                                <h3 class="stage-title">${this.escapeHtml(stage.title)}</h3>
                                <p class="stage-desc">${this.escapeHtml(stage.description)}</p>

                                <div class="stage-section">
                                    <h5>📚 Core Topics</h5>
                                    <div class="chips-group">
                                        ${(stage.topics || []).map(t => `<span class="chip chip-topic">${this.escapeHtml(t)}</span>`).join('')}
                                    </div>
                                </div>

                                <div class="stage-section">
                                    <h5>💡 Key Concepts</h5>
                                    <div class="chips-group">
                                        ${(stage.concepts || []).map(c => `<span class="chip chip-concept">${this.escapeHtml(c)}</span>`).join('')}
                                    </div>
                                </div>

                                ${stage.practical_activities && stage.practical_activities.length ? `
                                    <div class="stage-section">
                                        <h5>🛠️ Practical Activities</h5>
                                        <ul class="roadmap-list">
                                            ${stage.practical_activities.map(act => `<li>${this.escapeHtml(act)}</li>`).join('')}
                                        </ul>
                                    </div>
                                ` : ''}

                                ${stage.resources && stage.resources.length ? `
                                    <div class="stage-section">
                                        <h5>📖 Useful Resources</h5>
                                        <ul class="roadmap-list resources-list">
                                            ${stage.resources.map(res => `<li>🔗 ${this.escapeHtml(res)}</li>`).join('')}
                                        </ul>
                                    </div>
                                ` : ''}
                            </div>
                        </div>
                    `).join('<div class="timeline-connector">↓</div>')}
                </div>
            `;
        },

        // Pomodoro Timer Widget
        setupPomodoroTimer() {
            let timerInterval = null;
            let secondsLeft = 25 * 60;
            let isRunning = false;

            const display = document.getElementById('timer-display');
            const startBtn = document.getElementById('btn-timer-start');
            const resetBtn = document.getElementById('btn-timer-reset');

            if (!display || !startBtn || !resetBtn) return;

            const updateDisplay = () => {
                const mins = Math.floor(secondsLeft / 60);
                const secs = secondsLeft % 60;
                display.textContent = `${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
            };

            startBtn.addEventListener('click', () => {
                if (isRunning) {
                    clearInterval(timerInterval);
                    isRunning = false;
                    startBtn.textContent = '▶ Start Study Session';
                } else {
                    isRunning = true;
                    startBtn.textContent = '⏸ Pause';
                    timerInterval = setInterval(() => {
                        if (secondsLeft > 0) {
                            secondsLeft--;
                            updateDisplay();
                        } else {
                            clearInterval(timerInterval);
                            isRunning = false;
                            alert('⏱️ Pomodoro Study Session Complete! Take a 5-minute break.');
                            secondsLeft = 25 * 60;
                            updateDisplay();
                            startBtn.textContent = '▶ Start Study Session';
                        }
                    }, 1000);
                }
            });

            resetBtn.addEventListener('click', () => {
                clearInterval(timerInterval);
                isRunning = false;
                secondsLeft = 25 * 60;
                updateDisplay();
                startBtn.textContent = '▶ Start Study Session';
            });
        },

        // Card Actions (Copy, TTS Speech Reader, Download Markdown)
        setupCardActions(card, contentToCopy, regenerateFn) {
            if (!card) return;

            // Copy
            const copyBtn = card.querySelector('.btn-copy');
            if (copyBtn) {
                copyBtn.replaceWith(copyBtn.cloneNode(true));
                const newCopyBtn = card.querySelector('.btn-copy');
                newCopyBtn.addEventListener('click', () => {
                    navigator.clipboard.writeText(contentToCopy).then(() => {
                        const originalText = newCopyBtn.innerHTML;
                        newCopyBtn.innerHTML = `✓ Copied!`;
                        setTimeout(() => { newCopyBtn.innerHTML = originalText; }, 2000);
                    });
                });
            }

            // Regenerate
            const regenBtn = card.querySelector('.btn-regenerate');
            if (regenBtn && regenerateFn) {
                regenBtn.replaceWith(regenBtn.cloneNode(true));
                const newRegenBtn = card.querySelector('.btn-regenerate');
                newRegenBtn.addEventListener('click', regenerateFn);
            }

            // Text to Speech
            const ttsBtn = card.querySelector('.btn-tts');
            if (ttsBtn) {
                ttsBtn.replaceWith(ttsBtn.cloneNode(true));
                const newTtsBtn = card.querySelector('.btn-tts');
                newTtsBtn.addEventListener('click', () => {
                    if ('speechSynthesis' in window) {
                        window.speechSynthesis.cancel();
                        const utterance = new SpeechSynthesisUtterance(contentToCopy.slice(0, 500));
                        utterance.rate = 1.0;
                        window.speechSynthesis.speak(utterance);
                        newTtsBtn.innerHTML = '🔊 Speaking...';
                        utterance.onend = () => { newTtsBtn.innerHTML = '🔊 Listen'; };
                    } else {
                        alert('Text-to-speech is not supported by your browser.');
                    }
                });
            }

            // Export Markdown Download
            const exportBtn = card.querySelector('.btn-export');
            if (exportBtn) {
                exportBtn.replaceWith(exportBtn.cloneNode(true));
                const newExportBtn = card.querySelector('.btn-export');
                newExportBtn.addEventListener('click', () => {
                    const blob = new Blob([contentToCopy], { type: 'text/markdown' });
                    const url = URL.createObjectURL(blob);
                    const a = document.createElement('a');
                    a.href = url;
                    a.download = `edugenie-export-${Date.now()}.md`;
                    a.click();
                    URL.revokeObjectURL(url);
                });
            }
        },

        // Helpers
        showLoading(card, body, button, text) {
            if (button) {
                button.disabled = true;
                button.dataset.originalText = button.innerHTML;
                button.innerHTML = `<span class="spinner"></span> Processing...`;
            }
            if (card) card.style.display = 'block';
            if (body) {
                body.innerHTML = `
                    <div class="thinking-indicator skeleton-pulse">
                        <span class="sparkle-icon">✦</span> ${text}
                    </div>
                `;
            }
        },

        hideLoading(button) {
            if (button) {
                button.disabled = false;
                if (button.dataset.originalText) {
                    button.innerHTML = button.dataset.originalText;
                }
            }
        },

        renderError(card, body, button, message, retryFn) {
            this.hideLoading(button);
            if (card) card.style.display = 'block';
            if (body) {
                body.innerHTML = `
                    <div class="error-banner">
                        <div class="error-icon">⚠️</div>
                        <div class="error-details">
                            <h4>Oops! Couldn't generate response</h4>
                            <p>${this.escapeHtml(message)}</p>
                            <button type="button" class="btn btn-secondary btn-sm btn-retry">🔄 Try Again</button>
                        </div>
                    </div>
                `;
                const retryBtn = body.querySelector('.btn-retry');
                if (retryBtn && retryFn) retryBtn.addEventListener('click', retryFn);
            }
        },

        addRecentActivity(type, query) {
            let history = JSON.parse(localStorage.getItem('edugenie_history') || '[]');
            history.unshift({
                type,
                query,
                time: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
            });
            history = history.slice(0, 10);
            localStorage.setItem('edugenie_history', JSON.stringify(history));
            this.loadRecentActivity();
        },

        loadRecentActivity() {
            const container = document.getElementById('recent-activity-container');
            if (!container) return;

            const history = JSON.parse(localStorage.getItem('edugenie_history') || '[]');
            if (history.length === 0) {
                container.innerHTML = `<p class="empty-state">No recent activities yet. Start learning!</p>`;
                return;
            }

            container.innerHTML = `
                <div class="activity-list">
                    ${history.map(item => `
                        <div class="activity-item">
                            <span class="activity-type-badge">${this.escapeHtml(item.type)}</span>
                            <span class="activity-query">${this.escapeHtml(item.query)}</span>
                            <span class="activity-time">${this.escapeHtml(item.time)}</span>
                        </div>
                    `).join('')}
                </div>
            `;
        },

        formatMarkdown(text) {
            if (!text) return '';
            let html = this.escapeHtml(text);
            html = html.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
            html = html.replace(/\*(.*?)\*/g, '<em>$1</em>');
            html = html.replace(/^### (.*$)/gim, '<h3>$1</h3>');
            html = html.replace(/^## (.*$)/gim, '<h2>$1</h2>');
            html = html.replace(/^# (.*$)/gim, '<h1>$1</h1>');
            html = html.replace(/```([\s\S]*?)```/g, '<pre><code>$1</code></pre>');
            html = html.replace(/`([^`]+)`/g, '<code>$1</code>');
            html = html.replace(/^\- (.*$)/gim, '<li>$1</li>');
            html = html.replace(/(<li>.*<\/li>)/gim, '<ul>$1</ul>');
            html = html.replace(/\n\n/g, '</p><p>');
            return `<p>${html}</p>`;
        },

        escapeHtml(text) {
            if (!text) return '';
            return text.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/"/g, "&quot;").replace(/'/g, "&#039;");
        }
    };

    window.EduGenieApp = EduGenieApp;
    EduGenieApp.init();
});
