// Ejercicios Interactivos - Hospital San Carlos OVA
class InteractiveExercises {
    constructor() {
        this.exercises = [];
        this.currentExercise = 0;
        this.score = 0;
        this.attempts = {};
        
        this.init();
    }

    init() {
        this.setupDragAndDrop();
        this.createAdditionalExercises();
        console.log('🎮 Sistema de ejercicios interactivos inicializado');
    }

    setupDragAndDrop() {
        const variableItems = document.querySelectorAll('.variable-item');
        const dropZones = document.querySelectorAll('.drop-zone');

        variableItems.forEach(item => {
            item.addEventListener('dragstart', (e) => {
                e.dataTransfer.setData('text/plain', e.target.getAttribute('data-type'));
                e.dataTransfer.setData('text/html', e.target.outerHTML);
                e.target.style.opacity = '0.5';
            });

            item.addEventListener('dragend', (e) => {
                e.target.style.opacity = '1';
            });
        });

        dropZones.forEach(zone => {
            zone.addEventListener('dragover', (e) => {
                e.preventDefault();
                zone.classList.add('drag-over');
            });

            zone.addEventListener('dragleave', (e) => {
                zone.classList.remove('drag-over');
            });

            zone.addEventListener('drop', (e) => {
                e.preventDefault();
                zone.classList.remove('drag-over');
                
                const draggedType = e.dataTransfer.getData('text/plain');
                const draggedHTML = e.dataTransfer.getData('text/html');
                const expectedCategory = zone.getAttribute('data-category');
                
                if (draggedType === expectedCategory) {
                    const newElement = document.createElement('div');
                    newElement.innerHTML = draggedHTML;
                    newElement.firstChild.style.background = '#00ff41';
                    newElement.firstChild.style.color = '#000';
                    newElement.firstChild.style.margin = '5px 0';
                    newElement.firstChild.style.padding = '8px';
                    newElement.firstChild.style.border = '2px solid #000';
                    newElement.firstChild.draggable = false;
                    
                    zone.appendChild(newElement.firstChild);
                    
                    // Feedback positivo
                    this.showFeedback(zone, '✅ ¡Correcto!', 'success');
                } else {
                    // Feedback negativo
                    this.showFeedback(zone, '❌ Categoría incorrecta', 'error');
                }
            });
        });
    }

    showFeedback(element, message, type) {
        const feedback = document.createElement('div');
        feedback.className = `feedback-message ${type}`;
        feedback.textContent = message;
        feedback.style.cssText = `
            position: absolute;
            top: -30px;
            left: 50%;
            transform: translateX(-50%);
            background: ${type === 'success' ? '#00ff41' : '#ff4444'};
            color: ${type === 'success' ? '#000' : '#fff'};
            padding: 5px 10px;
            border-radius: 4px;
            font-size: 10px;
            font-family: 'Press Start 2P', monospace;
            z-index: 1000;
            animation: feedbackPop 2s ease-out forwards;
        `;

        element.style.position = 'relative';
        element.appendChild(feedback);

        setTimeout(() => {
            if (feedback.parentNode) {
                feedback.parentNode.removeChild(feedback);
            }
        }, 2000);
    }

    createAdditionalExercises() {
        // Crear ejercicios adicionales dinámicamente
        this.addCalculatorExercise();
        this.addInterpretationExercise();
        this.addDataAnalysisExercise();
    }

    addCalculatorExercise() {
        const exerciseContainer = document.querySelector('.exercise-container');
        if (!exerciseContainer) return;

        const calculatorExercise = document.createElement('div');
        calculatorExercise.className = 'exercise-card';
        calculatorExercise.innerHTML = `
            <h3>Ejercicio 3: Calculadora Interactiva</h3>
            <p>Utiliza los datos del Hospital San Carlos para calcular estadísticas:</p>
            
            <div class="calculator-interface">
                <div class="data-selector">
                    <label>Selecciona variable:</label>
                    <select id="variable-selector" class="pixel-input">
                        <option value="age">Edad de pacientes</option>
                        <option value="weight">Peso de pacientes</option>
                        <option value="daysHospitalized">Días de hospitalización</option>
                        <option value="systolicBP">Presión sistólica</option>
                    </select>
                </div>
                
                <div class="calculation-buttons">
                    <button class="pixel-btn" onclick="this.calculateStatistic('mean')">Media</button>
                    <button class="pixel-btn" onclick="this.calculateStatistic('median')">Mediana</button>
                    <button class="pixel-btn" onclick="this.calculateStatistic('stdDev')">Desv. Est.</button>
                    <button class="pixel-btn" onclick="this.calculateStatistic('range')">Rango</button>
                </div>
                
                <div class="calculation-result" id="calc-result">
                    <div class="result-display">Selecciona una variable y un cálculo</div>
                </div>
            </div>
        `;

        exerciseContainer.appendChild(calculatorExercise);
    }

    addInterpretationExercise() {
        const exerciseContainer = document.querySelector('.exercise-container');
        if (!exerciseContainer) return;

        const interpretationExercise = document.createElement('div');
        interpretationExercise.className = 'exercise-card';
        interpretationExercise.innerHTML = `
            <h3>Ejercicio 4: Interpretación de Resultados</h3>
            <p>En el Hospital San Carlos, la edad promedio de los pacientes es 45.2 años con una desviación estándar de 18.3 años.</p>
            
            <div class="interpretation-questions">
                <div class="question-item">
                    <p><strong>¿Qué porcentaje de pacientes está entre 27 y 63 años?</strong></p>
                    <div class="answer-options">
                        <label><input type="radio" name="q1" value="50"> 50%</label>
                        <label><input type="radio" name="q1" value="68"> 68%</label>
                        <label><input type="radio" name="q1" value="95"> 95%</label>
                        <label><input type="radio" name="q1" value="99"> 99%</label>
                    </div>
                </div>
                
                <div class="question-item">
                    <p><strong>¿Cuál es la interpretación correcta de la desviación estándar?</strong></p>
                    <div class="answer-options">
                        <label><input type="radio" name="q2" value="a"> Los datos están muy concentrados</label>
                        <label><input type="radio" name="q2" value="b"> Hay moderada variabilidad en las edades</label>
                        <label><input type="radio" name="q2" value="c"> Los datos son extremadamente dispersos</label>
                        <label><input type="radio" name="q2" value="d"> No se puede determinar</label>
                    </div>
                </div>
            </div>
            
            <button class="pixel-btn primary" onclick="this.checkInterpretation()">Verificar Interpretación</button>
            <div class="feedback" id="interpretation-feedback"></div>
        `;

        exerciseContainer.appendChild(interpretationExercise);
    }

    addDataAnalysisExercise() {
        const exerciseContainer = document.querySelector('.exercise-container');
        if (!exerciseContainer) return;

        const analysisExercise = document.createElement('div');
        analysisExercise.className = 'exercise-card';
        analysisExercise.innerHTML = `
            <h3>Ejercicio 5: Análisis de Datos Hospitalarios</h3>
            <p>Analiza la siguiente tabla de frecuencias del Hospital San Carlos:</p>
            
            <div class="data-table">
                <table class="hospital-table">
                    <thead>
                        <tr>
                            <th>Servicio</th>
                            <th>Número de Pacientes</th>
                            <th>Porcentaje</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr><td>Urgencias</td><td>280</td><td>28%</td></tr>
                        <tr><td>Consulta Externa</td><td>450</td><td>45%</td></tr>
                        <tr><td>Hospitalización</td><td>180</td><td>18%</td></tr>
                        <tr><td>Cirugía</td><td>90</td><td>9%</td></tr>
                    </tbody>
                </table>
            </div>
            
            <div class="analysis-tasks">
                <div class="task-item">
                    <label>¿Cuál es el total de pacientes?</label>
                    <input type="number" id="total-patients-answer" class="pixel-input" placeholder="Respuesta">
                </div>
                
                <div class="task-item">
                    <label>¿Cuál es la moda en esta distribución?</label>
                    <select id="mode-answer" class="pixel-input">
                        <option value="">Seleccionar...</option>
                        <option value="urgencias">Urgencias</option>
                        <option value="consulta">Consulta Externa</option>
                        <option value="hospitalizacion">Hospitalización</option>
                        <option value="cirugia">Cirugía</option>
                    </select>
                </div>
            </div>
            
            <button class="pixel-btn primary" onclick="this.checkDataAnalysis()">Verificar Análisis</button>
            <div class="feedback" id="analysis-feedback"></div>
        `;

        exerciseContainer.appendChild(analysisExercise);
    }

    calculateStatistic(type) {
        const variable = document.getElementById('variable-selector').value;
        const resultDiv = document.getElementById('calc-result');
        
        if (!window.hospitalOVA || !window.hospitalOVA.statisticsCalculator) {
            // Crear calculadora si no existe
            const calc = new StatisticsCalculator();
            window.hospitalOVA.statisticsCalculator = calc;
        }

        const stats = window.hospitalOVA.statisticsCalculator.getSummaryStatistics(variable);
        
        if (!stats) {
            resultDiv.innerHTML = '<div class="error">Error al calcular estadística</div>';
            return;
        }

        let result;
        switch(type) {
            case 'mean':
                result = `Media: ${stats.mean.toFixed(2)}`;
                break;
            case 'median':
                result = `Mediana: ${stats.median.toFixed(2)}`;
                break;
            case 'stdDev':
                result = `Desviación Estándar: ${stats.standardDeviation.toFixed(2)}`;
                break;
            case 'range':
                result = `Rango: ${stats.range}`;
                break;
            default:
                result = 'Cálculo no válido';
        }

        resultDiv.innerHTML = `
            <div class="result-display success">
                <strong>${result}</strong>
                <div class="additional-info">
                    Variable: ${this.getVariableName(variable)}<br>
                    n = ${stats.count} pacientes
                </div>
            </div>
        `;
        
        // Efecto visual
        resultDiv.style.animation = 'fadeInUp 0.5s ease';
    }

    getVariableName(variable) {
        const names = {
            'age': 'Edad (años)',
            'weight': 'Peso (kg)',
            'daysHospitalized': 'Días de hospitalización',
            'systolicBP': 'Presión sistólica (mmHg)'
        };
        return names[variable] || variable;
    }

    checkInterpretation() {
        const q1Answer = document.querySelector('input[name="q1"]:checked');
        const q2Answer = document.querySelector('input[name="q2"]:checked');
        const feedback = document.getElementById('interpretation-feedback');
        
        let score = 0;
        let messages = [];
        
        // Pregunta 1: Regla empírica (68% en ±1 desviación estándar)
        if (q1Answer && q1Answer.value === '68') {
            score++;
            messages.push('✅ Correcto: ~68% de los datos están dentro de ±1 desviación estándar');
        } else {
            messages.push('❌ Incorrecto: La regla empírica indica que ~68% está en ±1σ de la media');
        }
        
        // Pregunta 2: Interpretación de desviación estándar
        if (q2Answer && q2Answer.value === 'b') {
            score++;
            messages.push('✅ Correcto: Una desviación de 18.3 años indica moderada variabilidad');
        } else {
            messages.push('❌ Incorrecto: Con σ=18.3 años hay moderada variabilidad en las edades');
        }
        
        feedback.innerHTML = `
            <div class="score-summary">
                <strong>Puntuación: ${score}/2</strong>
            </div>
            <div class="detailed-feedback">
                ${messages.map(msg => `<p>${msg}</p>`).join('')}
            </div>
        `;
        
        feedback.style.cssText = `
            background: ${score === 2 ? 'rgba(0, 255, 65, 0.1)' : 'rgba(255, 68, 68, 0.1)'};
            border: 2px solid ${score === 2 ? '#00ff41' : '#ff4444'};
            padding: 15px;
            margin-top: 15px;
            border-radius: 4px;
        `;
    }

    checkDataAnalysis() {
        const totalAnswer = parseInt(document.getElementById('total-patients-answer').value);
        const modeAnswer = document.getElementById('mode-answer').value;
        const feedback = document.getElementById('analysis-feedback');
        
        let score = 0;
        let messages = [];
        
        // Verificar total (280 + 450 + 180 + 90 = 1000)
        if (totalAnswer === 1000) {
            score++;
            messages.push('✅ Correcto: Total de pacientes = 1000');
        } else {
            messages.push('❌ Incorrecto: Total = 280 + 450 + 180 + 90 = 1000 pacientes');
        }
        
        // Verificar moda (Consulta Externa tiene mayor frecuencia)
        if (modeAnswer === 'consulta') {
            score++;
            messages.push('✅ Correcto: Consulta Externa es la moda (mayor frecuencia)');
        } else {
            messages.push('❌ Incorrecto: Consulta Externa tiene la mayor frecuencia (450 pacientes)');
        }
        
        feedback.innerHTML = `
            <div class="score-summary">
                <strong>Puntuación: ${score}/2</strong>
            </div>
            <div class="detailed-feedback">
                ${messages.map(msg => `<p>${msg}</p>`).join('')}
            </div>
        `;
        
        feedback.style.cssText = `
            background: ${score === 2 ? 'rgba(0, 255, 65, 0.1)' : 'rgba(255, 68, 68, 0.1)'};
            border: 2px solid ${score === 2 ? '#00ff41' : '#ff4444'};
            padding: 15px;
            margin-top: 15px;
            border-radius: 4px;
        `;
    }
}

// Estilos CSS adicionales para ejercicios
const exerciseStyles = document.createElement('style');
exerciseStyles.textContent = `
    .exercise-card {
        background: linear-gradient(135deg, #16213e, #1a1a2e);
        border: 2px solid #3282b8;
        padding: 20px;
        margin: 20px 0;
        border-radius: 0;
    }

    .exercise-card h3 {
        color: #00ff41;
        font-family: 'Press Start 2P', monospace;
        font-size: 12px;
        margin-bottom: 15px;
        text-align: center;
    }

    .calculator-interface {
        display: grid;
        gap: 15px;
        margin: 15px 0;
    }

    .calculation-buttons {
        display: flex;
        gap: 10px;
        flex-wrap: wrap;
        justify-content: center;
    }

    .calculation-result {
        min-height: 60px;
        background: #000;
        border: 2px solid #00ff41;
        padding: 15px;
        color: #00ff41;
        font-family: 'Press Start 2P', monospace;
        font-size: 10px;
        display: flex;
        align-items: center;
        justify-content: center;
    }

    .result-display.success {
        text-align: center;
        line-height: 1.5;
    }

    .additional-info {
        font-size: 8px;
        margin-top: 10px;
        color: #bbe1fa;
    }

    .hospital-table {
        width: 100%;
        border-collapse: collapse;
        margin: 15px 0;
        background: #000;
        color: #00ff41;
        font-family: 'Press Start 2P', monospace;
        font-size: 9px;
    }

    .hospital-table th,
    .hospital-table td {
        border: 1px solid #00ff41;
        padding: 8px;
        text-align: center;
    }

    .hospital-table th {
        background: #003300;
        color: #00ff41;
    }

    .question-item,
    .task-item {
        margin: 15px 0;
        padding: 10px;
        background: rgba(0, 255, 65, 0.05);
        border-left: 3px solid #00ff41;
    }

    .answer-options {
        display: grid;
        gap: 8px;
        margin-top: 10px;
    }

    .answer-options label {
        display: flex;
        align-items: center;
        gap: 8px;
        font-family: Arial, sans-serif;
        font-size: 11px;
        cursor: pointer;
        padding: 5px;
        transition: background 0.2s;
    }

    .answer-options label:hover {
        background: rgba(0, 255, 65, 0.1);
    }

    .drop-zone {
        min-height: 100px;
        border: 3px dashed #3282b8;
        padding: 15px;
        text-align: center;
        transition: all 0.3s ease;
        position: relative;
    }

    .drop-zone.drag-over {
        border-color: #00ff41;
        background: rgba(0, 255, 65, 0.1);
    }

    .variable-item {
        background: linear-gradient(45deg, #0f4c75, #3282b8);
        color: #fff;
        padding: 10px;
        margin: 5px;
        cursor: move;
        border: 2px solid #bbe1fa;
        font-size: 10px;
        transition: all 0.2s;
    }

    .variable-item:hover {
        transform: scale(1.05);
        box-shadow: 0 4px 8px rgba(0, 255, 65, 0.3);
    }

    @keyframes feedbackPop {
        0% { opacity: 0; transform: translateX(-50%) scale(0.8); }
        20% { opacity: 1; transform: translateX(-50%) scale(1.1); }
        100% { opacity: 0; transform: translateX(-50%) scale(1); }
    }
`;

document.head.appendChild(exerciseStyles);

// Exportar para uso global
window.InteractiveExercises = InteractiveExercises;