// Pixel Engine - Efectos visuales pixelados para Hospital San Carlos OVA
class PixelEngine {
    constructor() {
        this.effects = [];
        this.isRunning = false;
        this.animationFrame = null;
        
        this.init();
    }

    init() {
        this.createPixelEffects();
        this.setupEventListeners();
        this.startEngine();
        
        console.log('🎮 Pixel Engine iniciado');
    }

    createPixelEffects() {
        // Efecto de partículas médicas
        this.createMedicalParticles();
        
        // Efectos de monitor hospitalario
        this.createMonitorEffects();
        
        // Animaciones de datos
        this.createDataAnimations();
        
        // Efectos de hover pixelados
        this.setupPixelHovers();
    }

    createMedicalParticles() {
        const particleContainer = document.createElement('div');
        particleContainer.className = 'medical-particles';
        particleContainer.style.cssText = `
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            pointer-events: none;
            z-index: 1;
            overflow: hidden;
        `;
        
        document.body.appendChild(particleContainer);

        // Crear partículas médicas (cruces, píldoras, etc.)
        for (let i = 0; i < 15; i++) {
            setTimeout(() => {
                this.createMedicalParticle(particleContainer);
            }, i * 2000);
        }
    }

    createMedicalParticle(container) {
        const particle = document.createElement('div');
        const symbols = ['🏥', '💊', '🔬', '📊', '💉', '🩺'];
        const symbol = symbols[Math.floor(Math.random() * symbols.length)];
        
        particle.innerHTML = symbol;
        particle.style.cssText = `
            position: absolute;
            font-size: 16px;
            opacity: 0.3;
            animation: floatMedical ${15 + Math.random() * 10}s linear infinite;
            left: ${Math.random() * 100}%;
            top: 100%;
            filter: pixelated;
            image-rendering: pixelated;
        `;
        
        container.appendChild(particle);
        
        // Remover partícula después de la animación
        setTimeout(() => {
            if (particle.parentNode) {
                particle.parentNode.removeChild(particle);
            }
        }, 25000);
    }

    createMonitorEffects() {
        const monitors = document.querySelectorAll('.pixel-monitor');
        
        monitors.forEach(monitor => {
            // Efecto de scanlines
            this.addScanlines(monitor);
            
            // Efecto de parpadeo del cursor
            this.addBlinkingCursor(monitor);
            
            // Efecto de ruido de monitor
            this.addMonitorNoise(monitor);
        });
    }

    addScanlines(element) {
        const scanlines = document.createElement('div');
        scanlines.className = 'scanlines-overlay';
        scanlines.style.cssText = `
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: repeating-linear-gradient(
                0deg,
                transparent 0px,
                rgba(0, 255, 65, 0.03) 1px,
                transparent 2px,
                transparent 4px
            );
            pointer-events: none;
            animation: scanlineMove 0.1s linear infinite;
        `;
        
        element.style.position = 'relative';
        element.appendChild(scanlines);
    }

    addBlinkingCursor(element) {
        const cursor = document.createElement('span');
        cursor.innerHTML = '_';
        cursor.style.cssText = `
            color: #00ff41;
            animation: pixel-blink 1s infinite;
            font-family: 'Press Start 2P', monospace;
        `;
        
        element.appendChild(cursor);
    }

    addMonitorNoise(element) {
        // Agregar ruido sutil de monitor cada pocos segundos
        setInterval(() => {
            element.style.filter = 'brightness(1.1) contrast(1.05)';
            setTimeout(() => {
                element.style.filter = '';
            }, 100);
        }, 5000 + Math.random() * 10000);
    }

    createDataAnimations() {
        // Animaciones para mostrar datos llegando al hospital
        const dataElements = document.querySelectorAll('.data-display, .measure-value, .chart-section');
        
        dataElements.forEach(element => {
            const observer = new IntersectionObserver((entries) => {
                entries.forEach(entry => {
                    if (entry.isIntersecting) {
                        this.animateDataEntry(entry.target);
                    }
                });
            });
            
            observer.observe(element);
        });
    }

    animateDataEntry(element) {
        // Efecto de datos llegando pixel por pixel
        const originalText = element.textContent;
        element.textContent = '';
        
        let currentChar = 0;
        const interval = setInterval(() => {
            if (currentChar < originalText.length) {
                element.textContent += originalText[currentChar];
                currentChar++;
                
                // Efecto de sonido visual
                element.style.background = '#00ff41';
                element.style.color = '#000';
                setTimeout(() => {
                    element.style.background = '';
                    element.style.color = '';
                }, 50);
            } else {
                clearInterval(interval);
            }
        }, 50);
    }

    setupPixelHovers() {
        // Efectos de hover para elementos interactivos
        const interactiveElements = document.querySelectorAll(
            '.pixel-btn, .concept-card, .objective-card, .exercise-card, .option-label'
        );
        
        interactiveElements.forEach(element => {
            element.addEventListener('mouseenter', () => {
                this.createHoverEffect(element);
            });
            
            element.addEventListener('mouseleave', () => {
                this.removeHoverEffect(element);
            });
        });
    }

    createHoverEffect(element) {
        // Crear efecto de partículas en hover
        const rect = element.getBoundingClientRect();
        
        for (let i = 0; i < 5; i++) {
            setTimeout(() => {
                this.createHoverParticle(rect);
            }, i * 100);
        }
        
        // Efecto de glow
        element.style.boxShadow = '0 0 20px rgba(0, 255, 65, 0.5)';
        element.style.filter = 'brightness(1.1)';
    }

    removeHoverEffect(element) {
        element.style.boxShadow = '';
        element.style.filter = '';
    }

    createHoverParticle(rect) {
        const particle = document.createElement('div');
        particle.innerHTML = '+';
        particle.style.cssText = `
            position: fixed;
            color: #00ff41;
            font-family: 'Press Start 2P', monospace;
            font-size: 8px;
            pointer-events: none;
            z-index: 1000;
            left: ${rect.left + Math.random() * rect.width}px;
            top: ${rect.top + Math.random() * rect.height}px;
            animation: hoverParticle 1s ease-out forwards;
        `;
        
        document.body.appendChild(particle);
        
        setTimeout(() => {
            if (particle.parentNode) {
                particle.parentNode.removeChild(particle);
            }
        }, 1000);
    }

    startEngine() {
        this.isRunning = true;
        this.engineLoop();
    }

    stopEngine() {
        this.isRunning = false;
        if (this.animationFrame) {
            cancelAnimationFrame(this.animationFrame);
        }
    }

    engineLoop() {
        if (!this.isRunning) return;
        
        // Actualizar efectos cada frame
        this.updateEffects();
        
        this.animationFrame = requestAnimationFrame(() => this.engineLoop());
    }

    updateEffects() {
        // Actualizar efectos dinámicos
        this.updatePatientCounter();
        this.updateHospitalStatus();
    }

    updatePatientCounter() {
        // Efecto de contador animado
        const counters = document.querySelectorAll('[id*="patient"]');
        
        counters.forEach(counter => {
            if (Math.random() < 0.01) { // 1% de probabilidad por frame
                counter.style.color = '#fff';
                setTimeout(() => {
                    counter.style.color = '';
                }, 200);
            }
        });
    }

    updateHospitalStatus() {
        // Simular actividad del hospital
        const statusIndicators = document.querySelectorAll('.hospital-room::before');
        
        // El CSS ya maneja el parpadeo, solo necesitamos efectos adicionales ocasionales
    }

    setupEventListeners() {
        // Efectos especiales en eventos específicos
        document.addEventListener('click', (e) => {
            if (e.target.classList.contains('pixel-btn')) {
                this.createClickEffect(e.target, e.clientX, e.clientY);
            }
        });

        // Efectos en cambios de sección
        document.addEventListener('sectionChange', (e) => {
            this.createSectionTransitionEffect();
        });
    }

    createClickEffect(element, x, y) {
        // Crear efecto de "explosión" pixelada en click
        for (let i = 0; i < 8; i++) {
            const particle = document.createElement('div');
            particle.innerHTML = '■';
            particle.style.cssText = `
                position: fixed;
                color: #00ff41;
                font-size: 8px;
                pointer-events: none;
                z-index: 1000;
                left: ${x}px;
                top: ${y}px;
                animation: clickExplosion 0.6s ease-out forwards;
                animation-delay: ${i * 0.05}s;
                transform: rotate(${i * 45}deg);
            `;
            
            document.body.appendChild(particle);
            
            setTimeout(() => {
                if (particle.parentNode) {
                    particle.parentNode.removeChild(particle);
                }
            }, 600);
        }
    }

    createSectionTransitionEffect() {
        // Efecto de transición entre secciones
        const overlay = document.createElement('div');
        overlay.style.cssText = `
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: linear-gradient(90deg, 
                transparent 0%, 
                rgba(0, 255, 65, 0.1) 50%, 
                transparent 100%);
            z-index: 10000;
            pointer-events: none;
            animation: wipeTransition 0.5s ease-out;
        `;
        
        document.body.appendChild(overlay);
        
        setTimeout(() => {
            if (overlay.parentNode) {
                overlay.parentNode.removeChild(overlay);
            }
        }, 500);
    }

    // Métodos públicos para controlar efectos
    enableEffect(effectName) {
        // Habilitar efectos específicos
        console.log(`Efecto habilitado: ${effectName}`);
    }

    disableEffect(effectName) {
        // Deshabilitar efectos específicos
        console.log(`Efecto deshabilitado: ${effectName}`);
    }

    adjustIntensity(level) {
        // Ajustar intensidad de efectos (0-1)
        const intensity = Math.max(0, Math.min(1, level));
        
        document.documentElement.style.setProperty('--effect-intensity', intensity);
        console.log(`Intensidad de efectos: ${intensity * 100}%`);
    }
}

// CSS para animaciones del Pixel Engine
const pixelEngineStyles = document.createElement('style');
pixelEngineStyles.textContent = `
    /* Variables CSS para efectos */
    :root {
        --effect-intensity: 1;
    }

    /* Animaciones de partículas médicas */
    @keyframes floatMedical {
        0% {
            transform: translateY(0) rotate(0deg);
            opacity: 0;
        }
        10% {
            opacity: 0.3;
        }
        90% {
            opacity: 0.3;
        }
        100% {
            transform: translateY(-100vh) rotate(360deg);
            opacity: 0;
        }
    }

    /* Animaciones de scanlines */
    @keyframes scanlineMove {
        0% { transform: translateY(-100%); }
        100% { transform: translateY(100vh); }
    }

    /* Animación de partículas de hover */
    @keyframes hoverParticle {
        0% {
            transform: scale(1) translateY(0);
            opacity: 1;
        }
        100% {
            transform: scale(0.5) translateY(-20px);
            opacity: 0;
        }
    }

    /* Animación de explosión en click */
    @keyframes clickExplosion {
        0% {
            transform: scale(1) translate(0, 0);
            opacity: 1;
        }
        100% {
            transform: scale(0.5) translate(var(--dx, 0), var(--dy, 0));
            opacity: 0;
        }
    }

    /* Animación de transición entre secciones */
    @keyframes wipeTransition {
        0% { transform: translateX(-100%); }
        100% { transform: translateX(100%); }
    }

    /* Efectos de parpadeo mejorados */
    @keyframes pixel-blink {
        0%, 50% { 
            opacity: calc(var(--effect-intensity) * 1); 
        }
        51%, 100% { 
            opacity: 0; 
        }
    }

    /* Efectos de glow mejorados */
    @keyframes pixel-glow {
        0%, 100% { 
            text-shadow: 
                2px 2px 0px #000, 
                0 0 calc(10px * var(--effect-intensity)) #00ff41; 
        }
        50% { 
            text-shadow: 
                2px 2px 0px #000, 
                0 0 calc(20px * var(--effect-intensity)) #00ff41, 
                0 0 calc(30px * var(--effect-intensity)) #00ff41; 
        }
    }

    /* Contenedor de partículas médicas */
    .medical-particles {
        opacity: calc(var(--effect-intensity) * 0.7);
    }

    /* Overlay de scanlines */
    .scanlines-overlay {
        opacity: calc(var(--effect-intensity) * 0.5);
    }

    /* Efectos de entrada de datos */
    .data-entry-effect {
        animation: dataEntry 0.5s ease-out;
    }

    @keyframes dataEntry {
        0% {
            transform: scaleX(0);
            background: #00ff41;
        }
        100% {
            transform: scaleX(1);
            background: transparent;
        }
    }

    /* Efectos de feedback */
    .feedback-effect {
        animation: feedbackPulse 0.3s ease-out;
    }

    @keyframes feedbackPulse {
        0% { transform: scale(1); }
        50% { transform: scale(1.05); }
        100% { transform: scale(1); }
    }

    /* Modo de bajo rendimiento */
    .low-performance .medical-particles,
    .low-performance .scanlines-overlay {
        display: none;
    }

    .low-performance * {
        animation-duration: 0s !important;
        transition-duration: 0s !important;
    }

    /* Accesibilidad - respeto por preferencias de movimiento reducido */
    @media (prefers-reduced-motion: reduce) {
        .medical-particles {
            display: none;
        }
        
        * {
            animation-duration: 0.01ms !important;
            animation-iteration-count: 1 !important;
            transition-duration: 0.01ms !important;
        }
    }
`;

document.head.appendChild(pixelEngineStyles);

// Auto-inicialización con detección de rendimiento
document.addEventListener('DOMContentLoaded', () => {
    // Detectar capacidades del dispositivo
    const isLowPerformance = /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent) ||
                            navigator.hardwareConcurrency < 4 ||
                            navigator.deviceMemory < 4;
    
    if (isLowPerformance) {
        document.body.classList.add('low-performance');
    }
    
    // Inicializar Pixel Engine
    window.pixelEngine = new PixelEngine();
    
    // Ajustar intensidad basada en rendimiento
    if (isLowPerformance) {
        window.pixelEngine.adjustIntensity(0.3);
    }
});

// Exportar para uso global
window.PixelEngine = PixelEngine;