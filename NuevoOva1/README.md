# 🏥 OVA 1: Estadística Descriptiva - Hospital San Carlos Bogotá

## 📋 Descripción del Proyecto

**Objeto Virtual de Aprendizaje (OVA)** de Bioestadística con temática del Hospital San Carlos en Bogotá, diseñado con estética **pixel art** para estudiantes de Ciencias de la Salud de la Universidad Antonio Nariño (UAN).

### 🎯 Objetivos de Aprendizaje

- **Comprender** conceptos fundamentales de estadística descriptiva
- **Calcular** medidas de tendencia central y dispersión
- **Interpretar** datos de pacientes hospitalarios
- **Crear** visualizaciones de datos médicos
- **Aplicar** conocimientos estadísticos en contextos de salud

## 🚀 Funcionalidades Implementadas

### ✅ Características Principales

#### 🎮 Interfaz Pixel Art
- Diseño retro pixelado con temática hospitalaria
- Efectos visuales inmersivos (partículas médicas, scanlines)
- Paleta de colores inspirada en monitores hospitalarios
- Animaciones fluidas y transiciones suaves

#### 📚 Contenido Educativo
- **Sección Introducción**: Presentación del hospital y objetivos
- **Conceptos Básicos**: Población vs muestra, tipos de variables
- **Medidas Descriptivas**: Tendencia central y dispersión
- **Visualización**: Gráficos interactivos con Chart.js
- **Ejercicios**: 5 actividades interactivas diferentes
- **Evaluación**: Quiz de 5 preguntas con feedback detallado

#### 🧮 Calculadora Estadística Integrada
- Generación automática de datos de 300 pacientes
- Cálculos en tiempo real de media, mediana, moda
- Análisis de dispersión (rango, varianza, desviación estándar)
- Datos contextualizados del Hospital San Carlos

#### 📊 Visualizaciones Interactivas
- **Gráfico de Barras**: Distribución por edad y género
- **Gráfico Circular**: Servicios médicos más utilizados
- **Datos Realistas**: Basados en estadísticas hospitalarias de Bogotá

#### 🎯 Ejercicios Interactivos
1. **Calculadora de Media**: Práctica con pesos de pacientes
2. **Clasificación de Variables**: Drag & drop cuantitativas/cualitativas
3. **Calculadora Dinámica**: Selector de variables y estadísticas
4. **Interpretación**: Preguntas sobre distribución normal
5. **Análisis de Datos**: Tablas de frecuencia hospitalaria

#### 📝 Sistema de Evaluación
- Quiz de 5 preguntas categorizadas
- Feedback inmediato con explicaciones
- Resumen detallado por categorías
- Recomendaciones personalizadas
- Puntuación y progreso guardado

## 🗂️ Estructura del Proyecto

```
📁 Hospital-San-Carlos-OVA/
├── 📄 index.html                    # Página principal
├── 📁 css/
│   ├── 🎨 pixel-style.css         # Estilos pixel art base
│   └── 🏥 hospital-theme.css      # Temática hospitalaria
├── 📁 js/
│   ├── 🎮 main.js                 # Controlador principal
│   ├── 🧮 statistics-calculator.js # Calculadora estadística
│   ├── 🎯 interactive-exercises.js # Ejercicios interactivos
│   ├── 📝 quiz-system.js          # Sistema de evaluación
│   └── ✨ pixel-engine.js         # Motor de efectos visuales
└── 📋 README.md                    # Documentación
```

## 🔧 Tecnologías Utilizadas

- **HTML5**: Estructura semántica y accesible
- **CSS3**: Animaciones, gradientes y efectos pixelados
- **JavaScript ES6+**: Programación orientada a objetos
- **Chart.js**: Visualizaciones de datos interactivas
- **Google Fonts**: Tipografía Press Start 2P (pixel perfect)

## 🎨 Características de Diseño

### Paleta de Colores
- **Primario**: `#00ff41` (Verde hospital)
- **Secundario**: `#3282b8` (Azul médico)
- **Fondo**: `#1a1a2e` (Oscuro para contraste)
- **Acento**: `#bbe1fa` (Azul claro)

### Efectos Visuales
- Partículas médicas flotantes (🏥💊🔬📊)
- Scanlines de monitor CRT
- Efectos de hover con partículas
- Transiciones pixeladas entre secciones
- Cursores parpadeantes en monitores

## 📊 Datos Simulados

### 👥 Población de Pacientes (n=300)
- **Edades**: Distribución normal (μ=45, σ=18)
- **Géneros**: Masculino/Femenino balanceado
- **Pesos**: Normal (μ=70kg, σ=15kg)
- **Alturas**: Normal (μ=165cm, σ=10cm)
- **Días hospitalización**: Exponencial (λ=0.3)

### 🏥 Servicios Médicos
- **Urgencias**: 280 pacientes (28%)
- **Consulta Externa**: 450 pacientes (45%)
- **Hospitalización**: 180 pacientes (18%)
- **Cirugía**: 120 pacientes (12%)
- **Laboratorio**: 380 pacientes
- **Imagenología**: 220 pacientes

## 🎯 URIs Funcionales

### Navegación Principal
- `/` - Página principal
- `#intro` - Introducción y objetivos
- `#conceptos` - Conceptos básicos
- `#medidas` - Medidas descriptivas
- `#graficos` - Visualizaciones
- `#ejercicios` - Ejercicios interactivos
- `#evaluacion` - Quiz final

### Funciones JavaScript
```javascript
// Navegación
hospitalOVA.showSection(sectionId)

// Calculadora
statisticsCalculator.getSummaryStatistics(variable)
statisticsCalculator.calculateMean(data)
statisticsCalculator.calculateMedian(data)

// Ejercicios
checkAnswer(exerciseId, correctAnswer)
interactiveExercises.checkInterpretation()

// Quiz
quizSystem.submitQuiz()
quizSystem.restartQuiz()

// Efectos
pixelEngine.createHoverEffect(element)
pixelEngine.adjustIntensity(level)
```

## 🎮 Instrucciones de Uso

### Para Estudiantes
1. **Navegación**: Usa los botones superiores para moverte entre secciones
2. **Ejercicios**: Completa las actividades interactivas en orden
3. **Calculadora**: Experimenta con diferentes variables y estadísticas
4. **Quiz**: Responde todas las preguntas antes de enviar
5. **Progreso**: El sistema guarda tu avance automáticamente

### Para Profesores
- **Seguimiento**: Revisa las puntuaciones guardadas en localStorage
- **Personalización**: Modifica datos en `statistics-calculator.js`
- **Contenido**: Actualiza preguntas en `quiz-system.js`

## 📚 Próximas Funcionalidades

### 🔄 Fase II - Probabilidad (Pendiente)
- [ ] Conceptos de probabilidad básica
- [ ] Distribuciones de probabilidad
- [ ] Teorema de Bayes aplicado a diagnósticos
- [ ] Simulaciones Monte Carlo

### 🔄 Fase III - Inferencia Estadística (Pendiente)
- [ ] Pruebas de hipótesis médicas
- [ ] Intervalos de confianza
- [ ] Comparación de tratamientos
- [ ] Análisis de supervivencia

### 🔄 Fase IV - Síntesis (Pendiente)
- [ ] Proyecto integrador
- [ ] Análisis de casos reales
- [ ] Presentación de resultados
- [ ] Certificación de competencias

## 📈 Recomendaciones de Desarrollo

### Prioridad Alta
1. **Integración con LMS**: Conectar con plataforma educativa UAN
2. **Base de Datos**: Implementar persistencia de datos real
3. **Accesibilidad**: Mejorar compatibilidad con lectores de pantalla
4. **Mobile First**: Optimizar para dispositivos móviles

### Prioridad Media
1. **Gamificación**: Sistema de puntos y logros
2. **Colaborativo**: Funciones multijugador
3. **Personalización**: Perfiles de usuario
4. **Analytics**: Seguimiento de aprendizaje

### Prioridad Baja
1. **Realidad Virtual**: Experiencia inmersiva hospitalaria
2. **IA Integrada**: Tutor virtual inteligente
3. **Exportación**: Generar reportes PDF
4. **API Externa**: Datos hospitalarios reales

## 🌟 Contexto Hospitalario Bogotá

### Hospital San Carlos (Simulado)
- **Ubicación**: Bogotá D.C., Colombia
- **Capacidad**: 15,000 pacientes/año
- **Servicios**: Urgencias, consulta externa, hospitalización, cirugía
- **Población**: Diversa, todas las edades y estratos socioeconómicos
- **Especialidades**: Medicina general, cardiología, pediatría, ginecología

### Datos Contextuales
- **EPS Principales**: Sura, Sanitas, Compensar, Nueva EPS
- **Patologías Frecuentes**: Hipertensión, diabetes, infecciones respiratorias
- **Indicadores**: Mortalidad, morbilidad, tiempos de espera
- **Calidad**: Certificación ISO 9001, habilitación ministerial

## 👥 Equipo de Desarrollo

**Desarrollado para la Universidad Antonio Nariño**
- **Programa**: Ciencias de la Salud
- **Materia**: Bioestadística
- **Modalidad**: Blended Learning (70% virtual, 30% presencial)
- **Fase**: I de IV (Estadística Descriptiva)

## 📄 Licencia

Proyecto educativo desarrollado específicamente para la Universidad Antonio Nariño (UAN) como parte del ecosistema Blended Learning de Bioestadística para Ciencias de la Salud.

---

### 🏥 ¡Bienvenido al Hospital San Carlos! 
**Donde los datos salvan vidas y las estadísticas curan conocimientos** 📊✨