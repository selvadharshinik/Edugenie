/**
 * EduGenie API Client
 * Centralized wrapper for backend HTTP requests.
 */

const API = {
    async request(endpoint, payload = null, method = 'POST') {
        const options = {
            method: method,
            headers: {
                'Content-Type': 'application/json',
                'Accept': 'application/json'
            }
        };

        if (payload && (method === 'POST' || method === 'PUT')) {
            options.body = JSON.stringify(payload);
        }

        try {
            const response = await fetch(endpoint, options);
            const contentType = response.headers.get("content-type");
            
            let data;
            if (contentType && contentType.includes("application/json")) {
                data = await response.json();
            } else {
                const text = await response.text();
                data = { message: text };
            }

            if (!response.ok) {
                const errorMessage = data.message || data.error || `Request failed with status ${response.status}`;
                const error = new Error(errorMessage);
                error.status = response.status;
                error.details = data.details || null;
                throw error;
            }

            return data;
        } catch (error) {
            console.error(`[API Error] ${method} ${endpoint}:`, error);
            if (error.name === 'TypeError' && error.message.includes('fetch')) {
                throw new Error("Unable to connect to EduGenie server. Please ensure the backend is running.");
            }
            throw error;
        }
    },

    async checkHealth() {
        return this.request('/health', null, 'GET');
    },

    async askQuestion(question) {
        return this.request('/qa', { question });
    },

    async explainTopic(topic) {
        return this.request('/explain', { topic });
    },

    async generateQuiz(text) {
        return this.request('/quiz', { text });
    },

    async summarizeText(text) {
        return this.request('/summarize', { text });
    },

    async generateLearningPath(topic) {
        return this.request('/learn/recommendations', { topic });
    },

    async generateFlashcards(topic, count = 5) {
        return this.request('/flashcards', { topic, count });
    },

    async explainCode(code_or_topic, language = "python") {
        return this.request('/code-explain', { code_or_topic, language });
    },

    async generateMindMap(topic) {
        return this.request('/mindmap', { topic });
    },

    async generateStudyPlan(exam_or_topic, days_remaining = 7, hours_per_day = 2.0) {
        return this.request('/study-plan', { exam_or_topic, days_remaining, hours_per_day });
    }
};
