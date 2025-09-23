// Sistema de Quiz - Hospital San Carlos OVA
class QuizSystem {
    constructor() {
        this.questions = [];
        this.currentQuestion = 0;
        this.userAnswers = [];
        this.score = 0;
        this.totalQuestions = 0;
        this.isQuizActive = false;
        
        this.init();
    }

    init() {
        this.createQuestions();
        this.setupQuizInterface();
        console.log('📝 Sistema de evaluación inicializado');
    }

    createQuestions() {
        this.questions = [
            {
                id: 1,
                question: "En el Hospital San Carlos, si tenemos 15,000 pacientes al año y seleccionamos 300 para análisis, ¿cuál es el concepto correcto?",
                options: [
                    "Los 15,000 son la muestra y los 300 la población",
                    "Los 15,000 son la población y los 300 la muestra",
                    "Ambos grupos son muestras",
                    "No se puede determinar sin más información"
                ],
                correctAnswer: 1,
                explanation: "La población son todos los pacientes (15,000) y la muestra es el grupo seleccionado para análisis (300).",
                category: "conceptos"
            },
            {
                id: 2,
                question: "¿Cuál de las siguientes variables del Hospital San Carlos es cuantitativa continua?",
                options: [
                    "Tipo de sangre del paciente",
                    "Número de cirugías realizadas",
                    "Peso del paciente en kilogramos",
                    "Estado civil del paciente"
                ],
                correctAnswer: 2,
                explanation: "El peso es una variable cuantitativa continua ya que puede tomar cualquier valor dentro de un rango.",
                category: "conceptos"
            },
            {
                id: 3,
                question: "Si las edades de 5 pacientes son: 25, 30, 35, 40, 45 años, ¿cuál es la media aritmética?",
                options: [
                    "30 años",
                    "35 años", 
                    "40 años",
                    "32.5 años"
                ],
                correctAnswer: 1,
                explanation: "Media = (25 + 30 + 35 + 40 + 45) ÷ 5 = 175 ÷ 5 = 35 años",
                category: "medidas"
            },
            {
                id: 4,
                question: "En una distribución de días de hospitalización: 2, 3, 3, 4, 5, 5, 5, 6 días, ¿cuál es la moda?",
                options: [
                    "3 días",
                    "4 días",
                    "5 días",
                    "No hay moda"
                ],
                correctAnswer: 2,
                explanation: "La moda es 5 días, ya que es el valor que aparece con mayor frecuencia (3 veces).",
                category: "medidas"
            },
            {
                id: 5,
                question: "¿Qué tipo de gráfico sería MÁS apropiado para mostrar la distribución de tipos de sangre en el hospital?",
                options: [
                    "Histograma",
                    "Gráfico de barras",
                    "Gráfico de dispersión",
                    "Gráfico de líneas"
                ],
                correctAnswer: 1,
                explanation: "Un gráfico de barras es ideal para variables categóricas como los tipos de sangre (A, B, AB, O).",
                category: "graficos"
            }
        ];
        
        this.totalQuestions = this.questions.length;
    }

    setupQuizInterface() {
        const quizContainer = document.getElementById('quiz-container');
        const nextBtn = document.getElementById('next-question');
        const prevBtn = document.getElementById('prev-question');
        const submitBtn = document.getElementById('submit-quiz');
        const restartBtn = document.getElementById('restart-quiz');

        if (!quizContainer) return;

        // Event listeners
        if (nextBtn) nextBtn.addEventListener('click', () => this.nextQuestion());
        if (prevBtn) prevBtn.addEventListener('click', () => this.previousQuestion());
        if (submitBtn) submitBtn.addEventListener('click', () => this.submitQuiz());
        if (restartBtn) restartBtn.addEventListener('click', () => this.restartQuiz());

        // Inicializar primer pregunta
        this.loadQuestion(0);
    }

    loadQuestion(questionIndex) {
        const quizContainer = document.getElementById('quiz-container');
        const questionCounter = document.getElementById('question-counter');
        const progressFill = document.getElementById('quiz-progress');
        
        if (!quizContainer || questionIndex >= this.questions.length) return;

        this.currentQuestion = questionIndex;
        const question = this.questions[questionIndex];

        // Actualizar contador y progreso
        if (questionCounter) {
            questionCounter.textContent = `Pregunta ${questionIndex + 1} de ${this.totalQuestions}`;
        }
        
        if (progressFill) {
            const progress = ((questionIndex + 1) / this.totalQuestions) * 100;
            progressFill.style.width = `${progress}%`;
        }

        // Crear HTML de la pregunta
        quizContainer.innerHTML = `
            <div class="quiz-question">
                <div class="question-header">
                    <h4>Pregunta ${questionIndex + 1}</h4>
                    <span class="category-badge">${this.getCategoryName(question.category)}</span>
                </div>
                
                <div class="question-text">
                    ${question.question}
                </div>
                
                <div class="question-options">
                    ${question.options.map((option, index) => `
                        <div class="option-item">
                            <label class="option-label">
                                <input type="radio" name="answer-${question.id}" value="${index}" 
                                       ${this.userAnswers[questionIndex] === index ? 'checked' : ''}>
                                <span class="option-text">${option}</span>
                            </label>
                        </div>
                    `).join('')}
                </div>
                
                ${this.userAnswers[questionIndex] !== undefined ? `
                    <div class="answer-feedback">
                        ${this.createFeedback(question, this.userAnswers[questionIndex])}
                    </div>
                ` : ''}
            </div>
        `;

        // Event listener para respuestas
        const radioInputs = quizContainer.querySelectorAll('input[type="radio"]');
        radioInputs.forEach(input => {
            input.addEventListener('change', (e) => {
                this.recordAnswer(questionIndex, parseInt(e.target.value));
            });
        });

        // Actualizar botones de navegación
        this.updateNavigationButtons();
    }

    recordAnswer(questionIndex, answerIndex) {
        this.userAnswers[questionIndex] = answerIndex;
        const question = this.questions[questionIndex];
        
        // Mostrar feedback inmediato
        const feedbackContainer = document.querySelector('.answer-feedback') || 
                                 document.createElement('div');
        feedbackContainer.className = 'answer-feedback';
        feedbackContainer.innerHTML = this.createFeedback(question, answerIndex);
        
        if (!document.querySelector('.answer-feedback')) {
            document.querySelector('.question-options').insertAdjacentElement('afterend', feedbackContainer);
        }

        // Efectos visuales
        this.highlightAnswers(question, answerIndex);
    }

    createFeedback(question, userAnswer) {
        const isCorrect = userAnswer === question.correctAnswer;
        
        return `
            <div class="feedback-content ${isCorrect ? 'correct' : 'incorrect'}">
                <div class="feedback-header">
                    ${isCorrect ? '✅ ¡Correcto!' : '❌ Incorrecto'}
                </div>
                <div class="feedback-explanation">
                    ${question.explanation}
                </div>
            </div>
        `;
    }

    highlightAnswers(question, userAnswer) {
        const optionItems = document.querySelectorAll('.option-item');
        
        optionItems.forEach((item, index) => {
            const label = item.querySelector('.option-label');
            
            // Resetear clases
            label.classList.remove('correct-answer', 'incorrect-answer', 'user-answer');
            
            // Marcar respuesta correcta
            if (index === question.correctAnswer) {
                label.classList.add('correct-answer');
            }
            
            // Marcar respuesta del usuario si es incorrecta
            if (index === userAnswer && userAnswer !== question.correctAnswer) {
                label.classList.add('incorrect-answer', 'user-answer');
            }
        });
    }

    nextQuestion() {
        if (this.currentQuestion < this.totalQuestions - 1) {
            this.loadQuestion(this.currentQuestion + 1);
        }
    }

    previousQuestion() {
        if (this.currentQuestion > 0) {
            this.loadQuestion(this.currentQuestion - 1);
        }
    }

    updateNavigationButtons() {
        const nextBtn = document.getElementById('next-question');
        const prevBtn = document.getElementById('prev-question');
        const submitBtn = document.getElementById('submit-quiz');

        if (prevBtn) {
            prevBtn.style.display = this.currentQuestion > 0 ? 'inline-block' : 'none';
        }

        if (nextBtn) {
            nextBtn.style.display = this.currentQuestion < this.totalQuestions - 1 ? 'inline-block' : 'none';
        }

        if (submitBtn) {
            submitBtn.style.display = this.currentQuestion === this.totalQuestions - 1 ? 'inline-block' : 'none';
        }
    }

    submitQuiz() {
        // Verificar que todas las preguntas estén respondidas
        const unanswered = this.questions.findIndex((_, index) => this.userAnswers[index] === undefined);
        
        if (unanswered !== -1) {
            alert(`Por favor responde la pregunta ${unanswered + 1} antes de enviar.`);
            this.loadQuestion(unanswered);
            return;
        }

        // Calcular puntuación
        this.calculateScore();
        
        // Mostrar resultados
        this.showResults();
    }

    calculateScore() {
        this.score = 0;
        
        this.questions.forEach((question, index) => {
            if (this.userAnswers[index] === question.correctAnswer) {
                this.score++;
            }
        });
    }

    showResults() {
        const percentage = Math.round((this.score / this.totalQuestions) * 100);
        const quizContainer = document.getElementById('quiz-container');
        const quizControls = document.querySelector('.quiz-controls');
        const quizResults = document.getElementById('quiz-results');
        const finalScore = document.getElementById('final-score');
        const scoreMessage = document.getElementById('score-message');

        // Ocultar quiz y controles
        if (quizContainer) quizContainer.style.display = 'none';
        if (quizControls) quizControls.style.display = 'none';

        // Mostrar resultados
        if (quizResults) {
            quizResults.style.display = 'block';
            
            if (finalScore) finalScore.textContent = percentage;
            if (scoreMessage) scoreMessage.textContent = this.getScoreMessage(percentage);

            // Crear resumen detallado
            this.createDetailedSummary(quizResults, percentage);
        }

        // Registrar completación
        this.recordCompletion(percentage);
    }

    getScoreMessage(percentage) {
        if (percentage >= 90) return "¡Excelente! Dominas los conceptos de estadística descriptiva.";
        if (percentage >= 80) return "¡Muy bien! Tienes un buen entendimiento del tema.";
        if (percentage >= 70) return "Bien. Revisa algunos conceptos para mejorar.";
        if (percentage >= 60) return "Suficiente. Te recomendamos repasar el material.";
        return "Necesitas estudiar más. Revisa todo el contenido antes de continuar.";
    }

    createDetailedSummary(container, percentage) {
        const summaryDiv = document.createElement('div');
        summaryDiv.className = 'detailed-summary';
        summaryDiv.innerHTML = `
            <h4>Resumen Detallado</h4>
            <div class="summary-stats">
                <div class="stat-item">
                    <span class="stat-label">Respuestas Correctas:</span>
                    <span class="stat-value">${this.score}/${this.totalQuestions}</span>
                </div>
                <div class="stat-item">
                    <span class="stat-label">Porcentaje:</span>
                    <span class="stat-value">${percentage}%</span>
                </div>
            </div>
            
            <div class="category-performance">
                <h5>Rendimiento por Categoría:</h5>
                ${this.getCategoryPerformance()}
            </div>
            
            <div class="recommendations">
                <h5>Recomendaciones:</h5>
                ${this.getRecommendations(percentage)}
            </div>
        `;
        
        container.appendChild(summaryDiv);
    }

    getCategoryPerformance() {
        const categories = {};
        
        this.questions.forEach((question, index) => {
            const category = question.category;
            if (!categories[category]) {
                categories[category] = { correct: 0, total: 0 };
            }
            categories[category].total++;
            if (this.userAnswers[index] === question.correctAnswer) {
                categories[category].correct++;
            }
        });

        return Object.entries(categories).map(([category, data]) => {
            const percentage = Math.round((data.correct / data.total) * 100);
            return `
                <div class="category-item">
                    <span>${this.getCategoryName(category)}: </span>
                    <span class="category-score">${data.correct}/${data.total} (${percentage}%)</span>
                </div>
            `;
        }).join('');
    }

    getRecommendations(percentage) {
        const recommendations = [];
        
        if (percentage < 70) {
            recommendations.push("Revisa los conceptos básicos de población vs muestra");
            recommendations.push("Practica más el cálculo de medidas de tendencia central");
        }
        
        if (percentage < 80) {
            recommendations.push("Estudia los tipos de variables y sus aplicaciones");
            recommendations.push("Practica la interpretación de gráficos estadísticos");
        }
        
        if (percentage >= 90) {
            recommendations.push("¡Excelente trabajo! Estás listo para el siguiente módulo");
            recommendations.push("Considera ayudar a tus compañeros con las dudas");
        } else {
            recommendations.push("Continúa practicando con los ejercicios interactivos");
            recommendations.push("Consulta el material de apoyo para reforzar conceptos");
        }

        return recommendations.map(rec => `<li>${rec}</li>`).join('');
    }

    getCategoryName(category) {
        const names = {
            'conceptos': 'Conceptos Básicos',
            'medidas': 'Medidas Descriptivas',
            'graficos': 'Gráficos y Visualización'
        };
        return names[category] || category;
    }

    recordCompletion(percentage) {
        // Registrar en el progreso general de la OVA
        if (window.hospitalOVA) {
            window.hospitalOVA.markSectionCompleted('evaluacion');
            window.hospitalOVA.updateProgress();
        }

        // Guardar en localStorage para persistencia
        const completionData = {
            timestamp: new Date().toISOString(),
            score: this.score,
            totalQuestions: this.totalQuestions,
            percentage: percentage,
            answers: this.userAnswers
        };
        
        localStorage.setItem('hospitalOVA_quiz_completion', JSON.stringify(completionData));
        
        console.log(`🎓 Quiz completado: ${percentage}% (${this.score}/${this.totalQuestions})`);
    }

    restartQuiz() {
        // Resetear variables
        this.currentQuestion = 0;
        this.userAnswers = [];
        this.score = 0;
        this.isQuizActive = false;

        // Mostrar elementos del quiz
        const quizContainer = document.getElementById('quiz-container');
        const quizControls = document.querySelector('.quiz-controls');
        const quizResults = document.getElementById('quiz-results');

        if (quizContainer) quizContainer.style.display = 'block';
        if (quizControls) quizControls.style.display = 'flex';
        if (quizResults) quizResults.style.display = 'none';

        // Remover resumen detallado si existe
        const detailedSummary = document.querySelector('.detailed-summary');
        if (detailedSummary) {
            detailedSummary.remove();
        }

        // Cargar primera pregunta
        this.loadQuestion(0);
        
        console.log('🔄 Quiz reiniciado');
    }
}

// Estilos CSS adicionales para el quiz
const quizStyles = document.createElement('style');
quizStyles.textContent = `
    .quiz-question {
        background: linear-gradient(135deg, #16213e, #1a1a2e);
        border: 2px solid #3282b8;
        padding: 25px;
        border-radius: 0;
        margin: 20px 0;
    }

    .question-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 20px;
        padding-bottom: 10px;
        border-bottom: 1px solid #3282b8;
    }

    .question-header h4 {
        color: #00ff41;
        font-family: 'Press Start 2P', monospace;
        font-size: 12px;
    }

    .category-badge {
        background: #0f4c75;
        color: #bbe1fa;
        padding: 5px 10px;
        font-size: 8px;
        border: 1px solid #3282b8;
    }

    .question-text {
        font-size: 13px;
        line-height: 1.6;
        margin: 20px 0;
        color: #eee;
        font-family: Arial, sans-serif;
    }

    .question-options {
        margin: 20px 0;
    }

    .option-item {
        margin: 10px 0;
    }

    .option-label {
        display: flex;
        align-items: flex-start;
        gap: 10px;
        padding: 12px;
        background: linear-gradient(135deg, #0f1419, #1a1a2e);
        border: 2px solid #3282b8;
        cursor: pointer;
        transition: all 0.3s ease;
        font-family: Arial, sans-serif;
        font-size: 12px;
        line-height: 1.4;
    }

    .option-label:hover {
        border-color: #00ff41;
        background: linear-gradient(135deg, #1a1a2e, #16213e);
    }

    .option-label.correct-answer {
        border-color: #00ff41;
        background: linear-gradient(135deg, #003300, #006600);
        color: #00ff41;
    }

    .option-label.incorrect-answer {
        border-color: #ff4444;
        background: linear-gradient(135deg, #330000, #660000);
        color: #ff4444;
    }

    .option-text {
        flex: 1;
    }

    .answer-feedback {
        margin-top: 20px;
        padding: 15px;
        border-radius: 0;
        animation: fadeInUp 0.5s ease;
    }

    .feedback-content.correct {
        background: rgba(0, 255, 65, 0.1);
        border: 2px solid #00ff41;
        color: #00ff41;
    }

    .feedback-content.incorrect {
        background: rgba(255, 68, 68, 0.1);
        border: 2px solid #ff4444;
        color: #ff4444;
    }

    .feedback-header {
        font-family: 'Press Start 2P', monospace;
        font-size: 10px;
        margin-bottom: 10px;
    }

    .feedback-explanation {
        font-family: Arial, sans-serif;
        font-size: 11px;
        line-height: 1.5;
        color: #eee;
    }

    .progress-bar {
        width: 100%;
        height: 20px;
        background: #000;
        border: 2px solid #00ff41;
        position: relative;
        overflow: hidden;
    }

    .progress-fill {
        height: 100%;
        background: repeating-linear-gradient(
            90deg,
            #00ff41 0px,
            #00ff41 4px,
            #00cc33 4px,
            #00cc33 8px
        );
        transition: width 0.5s ease;
        width: 0%;
    }

    .quiz-controls {
        display: flex;
        justify-content: center;
        gap: 15px;
        margin: 20px 0;
    }

    .score-circle {
        width: 120px;
        height: 120px;
        border: 4px solid #00ff41;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        margin: 0 auto 20px;
        background: radial-gradient(circle, #003300, #001100);
    }

    .score-circle span {
        font-family: 'Press Start 2P', monospace;
        font-size: 24px;
        color: #00ff41;
    }

    .detailed-summary {
        background: linear-gradient(135deg, #0f1419, #1a1a2e);
        border: 2px solid #3282b8;
        padding: 20px;
        margin-top: 20px;
        font-family: Arial, sans-serif;
        font-size: 12px;
    }

    .detailed-summary h4,
    .detailed-summary h5 {
        color: #00ff41;
        font-family: 'Press Start 2P', monospace;
        font-size: 10px;
        margin-bottom: 15px;
    }

    .summary-stats,
    .category-performance,
    .recommendations {
        margin: 15px 0;
    }

    .stat-item,
    .category-item {
        display: flex;
        justify-content: space-between;
        margin: 8px 0;
        padding: 5px 0;
        border-bottom: 1px solid #3282b8;
    }

    .stat-value,
    .category-score {
        color: #00ff41;
        font-weight: bold;
    }

    .recommendations ul {
        list-style: none;
        padding: 0;
    }

    .recommendations li {
        padding: 5px 0;
        border-left: 3px solid #00ff41;
        padding-left: 10px;
        margin: 8px 0;
        background: rgba(0, 255, 65, 0.05);
    }
`;

document.head.appendChild(quizStyles);

// Exportar para uso global
window.QuizSystem = QuizSystem;