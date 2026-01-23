// Main Application Controller - Hospital San Carlos OVA
class HospitalOVA {
    constructor() {
        this.currentSection = 'intro';
        this.patientCount = 0;
        this.overallProgress = 0;
        this.completedSections = new Set();
        
        this.init();
    }

    init() {
        this.setupNavigation();
        this.setupProgressTracking();
        this.startPixelEffects();
        this.loadPatientData();
        this.updatePatientCounter();
        
        // Initialize sections
        this.showSection('intro');
        
        console.log('🏥 Hospital San Carlos OVA iniciado correctamente');
    }

    setupNavigation() {
        const navButtons = document.querySelectorAll('.nav-btn');
        
        navButtons.forEach(btn => {
            btn.addEventListener('click', (e) => {
                const section = e.target.getAttribute('data-section');
                this.showSection(section);
                this.updateNavigation(e.target);
            });
        });
    }

    showSection(sectionId) {
        // Hide all sections
        document.querySelectorAll('.ova-section').forEach(section => {
            section.classList.remove('active');
        });

        // Show target section
        const targetSection = document.getElementById(sectionId);
        if (targetSection) {
            targetSection.classList.add('active');
            this.currentSection = sectionId;
            
            // Initialize section-specific functionality
            this.initializeSectionFeatures(sectionId);
            
            // Mark section as visited
            this.markSectionCompleted(sectionId);
            this.updateProgress();
        }
    }

    updateNavigation(activeBtn) {
        document.querySelectorAll('.nav-btn').forEach(btn => {
            btn.classList.remove('active');
        });
        activeBtn.classList.add('active');
    }

    initializeSectionFeatures(sectionId) {
        switch(sectionId) {
            case 'conceptos':
                this.initializeConceptsSection();
                break;
            case 'medidas':
                this.initializeMeasuresSection();
                break;
            case 'graficos':
                this.initializeChartsSection();
                break;
            case 'ejercicios':
                this.initializeExercisesSection();
                break;
            case 'evaluacion':
                this.initializeEvaluationSection();
                break;
        }
    }

    initializeConceptsSection() {
        // Animación de población vs muestra
        this.animatePopulationDemo();
        
        // Interactividad en tarjetas de conceptos
        const conceptCards = document.querySelectorAll('.concept-card');
        conceptCards.forEach(card => {
            card.addEventListener('click', () => {
                card.style.transform = 'scale(1.02)';
                setTimeout(() => {
                    card.style.transform = '';
                }, 200);
            });
        });
    }

    animatePopulationDemo() {
        const totalElement = document.getElementById('total-patients');
        const sampleElement = document.getElementById('sample-patients');
        
        if (totalElement && sampleElement) {
            let total = 0;
            let sample = 0;
            const targetTotal = 15000;
            const targetSample = 300;
            
            const interval = setInterval(() => {
                total += 150;
                sample += 3;
                
                totalElement.textContent = total.toLocaleString();
                sampleElement.textContent = sample;
                
                if (total >= targetTotal) {
                    clearInterval(interval);
                    totalElement.textContent = targetTotal.toLocaleString();
                    sampleElement.textContent = targetSample;
                }
            }, 50);
        }
    }

    initializeMeasuresSection() {
        const generateBtn = document.getElementById('generate-data');
        if (generateBtn) {
            generateBtn.addEventListener('click', () => {
                this.generateNewPatientData();
            });
        }
        
        // Calcular medidas iniciales
        this.calculateMeasures();
    }

    generateNewPatientData() {
        // Generar datos aleatorios de edades de pacientes
        const ages = [];
        for (let i = 0; i < 10; i++) {
            ages.push(Math.floor(Math.random() * 60) + 18); // Edades entre 18 y 78
        }
        
        // Mostrar nuevos datos
        document.getElementById('patient-ages').textContent = ages.join(', ');
        
        // Recalcular medidas
        this.calculateMeasuresFromArray(ages);
        
        // Efecto visual
        document.getElementById('patient-ages').style.background = '#00ff41';
        document.getElementById('patient-ages').style.color = '#000';
        setTimeout(() => {
            document.getElementById('patient-ages').style.background = '';
            document.getElementById('patient-ages').style.color = '';
        }, 1000);
    }

    calculateMeasures() {
        const dataText = document.getElementById('patient-ages').textContent;
        const ages = dataText.split(', ').map(num => parseInt(num.trim()));
        this.calculateMeasuresFromArray(ages);
    }

    calculateMeasuresFromArray(ages) {
        // Calcular media
        const mean = ages.reduce((sum, age) => sum + age, 0) / ages.length;
        document.getElementById('media-result').textContent = mean.toFixed(1);
        
        // Calcular mediana
        const sortedAges = [...ages].sort((a, b) => a - b);
        const median = sortedAges.length % 2 === 0
            ? (sortedAges[sortedAges.length / 2 - 1] + sortedAges[sortedAges.length / 2]) / 2
            : sortedAges[Math.floor(sortedAges.length / 2)];
        document.getElementById('mediana-result').textContent = median;
        
        // Calcular moda
        const frequency = {};
        ages.forEach(age => frequency[age] = (frequency[age] || 0) + 1);
        const maxFreq = Math.max(...Object.values(frequency));
        const modes = Object.keys(frequency).filter(age => frequency[age] === maxFreq);
        document.getElementById('moda-result').textContent = maxFreq > 1 ? modes.join(', ') : 'N/A';
        
        // Calcular rango
        const range = Math.max(...ages) - Math.min(...ages);
        document.getElementById('rango-result').textContent = range;
        
        // Calcular desviación estándar
        const variance = ages.reduce((sum, age) => sum + Math.pow(age - mean, 2), 0) / (ages.length - 1);
        const stdDev = Math.sqrt(variance);
        document.getElementById('desviacion-result').textContent = stdDev.toFixed(1);
        document.getElementById('varianza-result').textContent = variance.toFixed(1);
    }

    initializeChartsSection() {
        this.createAgeChart();
        this.createServicesChart();
    }

    createAgeChart() {
        const ctx = document.getElementById('age-chart');
        if (ctx && typeof Chart !== 'undefined') {
            new Chart(ctx, {
                type: 'bar',
                data: {
                    labels: ['18-25', '26-35', '36-45', '46-55', '56-65', '65+'],
                    datasets: [{
                        label: 'Hombres',
                        data: [45, 67, 89, 72, 56, 34],
                        backgroundColor: '#3282b8',
                        borderColor: '#0f4c75',
                        borderWidth: 2
                    }, {
                        label: 'Mujeres',
                        data: [52, 78, 95, 83, 68, 41],
                        backgroundColor: '#bbe1fa',
                        borderColor: '#3282b8',
                        borderWidth: 2
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        title: {
                            display: true,
                            text: 'Distribución de Pacientes por Edad y Género',
                            color: '#00ff41',
                            font: { family: 'Press Start 2P', size: 10 }
                        },
                        legend: {
                            labels: { color: '#fff', font: { family: 'Arial', size: 12 } }
                        }
                    },
                    scales: {
                        y: {
                            beginAtZero: true,
                            ticks: { color: '#00ff41' },
                            grid: { color: '#3282b8' }
                        },
                        x: {
                            ticks: { color: '#00ff41' },
                            grid: { color: '#3282b8' }
                        }
                    }
                }
            });
        }
    }

    createServicesChart() {
        const ctx = document.getElementById('services-chart');
        if (ctx && typeof Chart !== 'undefined') {
            new Chart(ctx, {
                type: 'pie',
                data: {
                    labels: ['Urgencias', 'Consulta Externa', 'Hospitalización', 'Cirugía', 'Laboratorio', 'Imagenología'],
                    datasets: [{
                        data: [280, 450, 180, 120, 380, 220],
                        backgroundColor: [
                            '#ff4444', '#00ff41', '#3282b8', 
                            '#bbe1fa', '#ff9966', '#ffcc99'
                        ],
                        borderColor: '#000',
                        borderWidth: 3
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        title: {
                            display: true,
                            text: 'Servicios Médicos más Utilizados (Mensual)',
                            color: '#00ff41',
                            font: { family: 'Press Start 2P', size: 10 }
                        },
                        legend: {
                            labels: { color: '#fff', font: { family: 'Arial', size: 11 } }
                        }
                    }
                }
            });
        }
    }

    initializeExercisesSection() {
        // Los ejercicios se manejan en interactive-exercises.js
        console.log('Sección de ejercicios inicializada');
    }

    initializeEvaluationSection() {
        // La evaluación se maneja en quiz-system.js
        console.log('Sección de evaluación inicializada');
    }

    markSectionCompleted(sectionId) {
        this.completedSections.add(sectionId);
    }

    updateProgress() {
        const totalSections = 6; // intro, conceptos, medidas, graficos, ejercicios, evaluacion
        const progress = (this.completedSections.size / totalSections) * 100;
        this.overallProgress = Math.round(progress);
        
        const progressElement = document.getElementById('overall-progress');
        if (progressElement) {
            progressElement.textContent = `${this.overallProgress}%`;
        }
    }

    setupProgressTracking() {
        // Tracking automático del progreso
        setInterval(() => {
            this.updatePatientCounter();
        }, 30000); // Actualizar cada 30 segundos
    }

    updatePatientCounter() {
        // Simular pacientes llegando al hospital
        this.patientCount += Math.floor(Math.random() * 3) + 1;
        const counterElement = document.getElementById('patient-count');
        if (counterElement) {
            counterElement.textContent = `Pacientes: ${this.patientCount}`;
        }
    }

    startPixelEffects() {
        // Efectos pixelados adicionales
        const glowElements = document.querySelectorAll('.pixel-glow');
        glowElements.forEach(element => {
            element.classList.add('pixel-glow');
        });

        // Efecto de scanlines
        document.body.classList.add('scanlines');
    }

    loadPatientData() {
        // Simular carga de datos de pacientes
        console.log('📊 Cargando datos del Hospital San Carlos...');
        
        setTimeout(() => {
            console.log('✅ Datos cargados: 300 pacientes en muestra');
            this.patientCount = 300;
            this.updatePatientCounter();
        }, 1000);
    }
}

// Función para verificar respuestas de ejercicios
function checkAnswer(exerciseId, correctAnswer) {
    const userAnswer = parseFloat(document.getElementById(`answer-${exerciseId}`).value);
    const feedbackElement = document.getElementById(`feedback-${exerciseId}`);
    
    if (Math.abs(userAnswer - correctAnswer) < 0.1) {
        feedbackElement.innerHTML = '<span style="color: #00ff41;">✅ ¡Correcto! Excelente trabajo.</span>';
        feedbackElement.style.background = 'rgba(0, 255, 65, 0.1)';
    } else {
        feedbackElement.innerHTML = `<span style="color: #ff4444;">❌ Incorrecto. La respuesta correcta es ${correctAnswer}</span>`;
        feedbackElement.style.background = 'rgba(255, 68, 68, 0.1)';
    }
    
    // Efecto visual
    feedbackElement.style.padding = '10px';
    feedbackElement.style.border = '2px solid';
    feedbackElement.style.borderColor = Math.abs(userAnswer - correctAnswer) < 0.1 ? '#00ff41' : '#ff4444';
}

// Inicializar la aplicación cuando el DOM esté listo
document.addEventListener('DOMContentLoaded', () => {
    window.hospitalOVA = new HospitalOVA();
});

// Exportar para uso global
window.HospitalOVA = HospitalOVA;