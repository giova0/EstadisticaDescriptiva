// Calculadora de Estadísticas para Hospital San Carlos
class StatisticsCalculator {
    constructor() {
        this.hospitalData = {
            patients: [],
            services: [],
            demographics: {}
        };
        this.init();
    }

    init() {
        this.generateSampleData();
        console.log('📊 Calculadora de estadísticas inicializada');
    }

    generateSampleData() {
        // Generar datos de muestra para el Hospital San Carlos
        this.hospitalData.patients = this.generatePatientData(300);
        this.hospitalData.services = this.generateServiceData();
        this.hospitalData.demographics = this.calculateDemographics();
    }

    generatePatientData(count) {
        const patients = [];
        const bloodTypes = ['O+', 'A+', 'B+', 'AB+', 'O-', 'A-', 'B-', 'AB-'];
        const genders = ['M', 'F'];
        const diagnoses = [
            'Hipertensión', 'Diabetes', 'Infección respiratoria', 
            'Fractura', 'Gastritis', 'Migraña', 'Apendicitis', 
            'Neumonía', 'Artritis', 'Dermatitis'
        ];

        for (let i = 1; i <= count; i++) {
            const age = this.normalDistribution(45, 18); // Media 45, desviación 18
            const gender = genders[Math.floor(Math.random() * genders.length)];
            
            patients.push({
                id: i,
                age: Math.max(1, Math.min(100, Math.round(age))), // Entre 1 y 100 años
                gender: gender,
                weight: Math.round(this.normalDistribution(70, 15)), // Media 70kg, desviación 15
                height: Math.round(this.normalDistribution(165, 10)), // Media 165cm, desviación 10
                bloodType: bloodTypes[Math.floor(Math.random() * bloodTypes.length)],
                diagnosis: diagnoses[Math.floor(Math.random() * diagnoses.length)],
                daysHospitalized: Math.max(1, Math.round(this.exponentialDistribution(0.3))), // Distribución exponencial
                systolicBP: Math.round(this.normalDistribution(120, 20)), // Presión sistólica
                diastolicBP: Math.round(this.normalDistribution(80, 15)), // Presión diastólica
                admissionDate: this.randomDate(new Date(2024, 0, 1), new Date())
            });
        }

        return patients;
    }

    generateServiceData() {
        return [
            { service: 'Urgencias', patients: 280, avgWaitTime: 45 },
            { service: 'Consulta Externa', patients: 450, avgWaitTime: 25 },
            { service: 'Hospitalización', patients: 180, avgWaitTime: 120 },
            { service: 'Cirugía', patients: 120, avgWaitTime: 180 },
            { service: 'Laboratorio', patients: 380, avgWaitTime: 15 },
            { service: 'Imagenología', patients: 220, avgWaitTime: 35 }
        ];
    }

    // Medidas de Tendencia Central
    calculateMean(data) {
        if (!Array.isArray(data) || data.length === 0) return 0;
        return data.reduce((sum, value) => sum + value, 0) / data.length;
    }

    calculateMedian(data) {
        if (!Array.isArray(data) || data.length === 0) return 0;
        const sorted = [...data].sort((a, b) => a - b);
        const mid = Math.floor(sorted.length / 2);
        
        return sorted.length % 2 === 0
            ? (sorted[mid - 1] + sorted[mid]) / 2
            : sorted[mid];
    }

    calculateMode(data) {
        if (!Array.isArray(data) || data.length === 0) return [];
        
        const frequency = {};
        data.forEach(value => {
            frequency[value] = (frequency[value] || 0) + 1;
        });

        const maxFrequency = Math.max(...Object.values(frequency));
        return Object.keys(frequency)
            .filter(key => frequency[key] === maxFrequency)
            .map(Number);
    }

    // Medidas de Dispersión
    calculateRange(data) {
        if (!Array.isArray(data) || data.length === 0) return 0;
        return Math.max(...data) - Math.min(...data);
    }

    calculateVariance(data, sample = true) {
        if (!Array.isArray(data) || data.length === 0) return 0;
        
        const mean = this.calculateMean(data);
        const sumSquares = data.reduce((sum, value) => sum + Math.pow(value - mean, 2), 0);
        
        return sample ? sumSquares / (data.length - 1) : sumSquares / data.length;
    }

    calculateStandardDeviation(data, sample = true) {
        return Math.sqrt(this.calculateVariance(data, sample));
    }

    calculateCoefficiateOfVariation(data) {
        const mean = this.calculateMean(data);
        const stdDev = this.calculateStandardDeviation(data);
        return mean !== 0 ? (stdDev / mean) * 100 : 0;
    }

    // Medidas de Posición
    calculatePercentile(data, percentile) {
        if (!Array.isArray(data) || data.length === 0) return 0;
        
        const sorted = [...data].sort((a, b) => a - b);
        const index = (percentile / 100) * (sorted.length - 1);
        
        if (Number.isInteger(index)) {
            return sorted[index];
        } else {
            const lower = Math.floor(index);
            const upper = Math.ceil(index);
            const weight = index - lower;
            return sorted[lower] * (1 - weight) + sorted[upper] * weight;
        }
    }

    calculateQuartiles(data) {
        return {
            Q1: this.calculatePercentile(data, 25),
            Q2: this.calculateMedian(data),
            Q3: this.calculatePercentile(data, 75),
            IQR: this.calculatePercentile(data, 75) - this.calculatePercentile(data, 25)
        };
    }

    // Análisis específicos del hospital
    analyzePatientAges() {
        const ages = this.hospitalData.patients.map(p => p.age);
        
        return {
            mean: this.calculateMean(ages),
            median: this.calculateMedian(ages),
            mode: this.calculateMode(ages),
            standardDeviation: this.calculateStandardDeviation(ages),
            quartiles: this.calculateQuartiles(ages),
            ageGroups: this.groupByAgeRanges(ages)
        };
    }

    analyzeByGender() {
        const males = this.hospitalData.patients.filter(p => p.gender === 'M');
        const females = this.hospitalData.patients.filter(p => p.gender === 'F');

        return {
            total: this.hospitalData.patients.length,
            males: {
                count: males.length,
                percentage: (males.length / this.hospitalData.patients.length) * 100,
                avgAge: this.calculateMean(males.map(p => p.age)),
                avgWeight: this.calculateMean(males.map(p => p.weight))
            },
            females: {
                count: females.length,
                percentage: (females.length / this.hospitalData.patients.length) * 100,
                avgAge: this.calculateMean(females.map(p => p.age)),
                avgWeight: this.calculateMean(females.map(p => p.weight))
            }
        };
    }

    analyzeHospitalizationDays() {
        const days = this.hospitalData.patients.map(p => p.daysHospitalized);
        
        return {
            mean: this.calculateMean(days),
            median: this.calculateMedian(days),
            standardDeviation: this.calculateStandardDeviation(days),
            maximum: Math.max(...days),
            minimum: Math.min(...days),
            distribution: this.createFrequencyDistribution(days, 10)
        };
    }

    analyzeBloodPressure() {
        const systolic = this.hospitalData.patients.map(p => p.systolicBP);
        const diastolic = this.hospitalData.patients.map(p => p.diastolicBP);

        return {
            systolic: {
                mean: this.calculateMean(systolic),
                standardDeviation: this.calculateStandardDeviation(systolic),
                normal: systolic.filter(bp => bp >= 90 && bp <= 140).length,
                high: systolic.filter(bp => bp > 140).length,
                low: systolic.filter(bp => bp < 90).length
            },
            diastolic: {
                mean: this.calculateMean(diastolic),
                standardDeviation: this.calculateStandardDeviation(diastolic),
                normal: diastolic.filter(bp => bp >= 60 && bp <= 90).length,
                high: diastolic.filter(bp => bp > 90).length,
                low: diastolic.filter(bp => bp < 60).length
            }
        };
    }

    // Funciones auxiliares
    groupByAgeRanges(ages) {
        const ranges = {
            '0-17': 0, '18-25': 0, '26-35': 0, '36-45': 0,
            '46-55': 0, '56-65': 0, '66-75': 0, '76+': 0
        };

        ages.forEach(age => {
            if (age < 18) ranges['0-17']++;
            else if (age <= 25) ranges['18-25']++;
            else if (age <= 35) ranges['26-35']++;
            else if (age <= 45) ranges['36-45']++;
            else if (age <= 55) ranges['46-55']++;
            else if (age <= 65) ranges['56-65']++;
            else if (age <= 75) ranges['66-75']++;
            else ranges['76+']++;
        });

        return ranges;
    }

    createFrequencyDistribution(data, bins) {
        const min = Math.min(...data);
        const max = Math.max(...data);
        const binWidth = (max - min) / bins;
        
        const distribution = {};
        
        for (let i = 0; i < bins; i++) {
            const binStart = min + i * binWidth;
            const binEnd = binStart + binWidth;
            const binLabel = `${binStart.toFixed(1)}-${binEnd.toFixed(1)}`;
            distribution[binLabel] = 0;
        }

        data.forEach(value => {
            const binIndex = Math.min(Math.floor((value - min) / binWidth), bins - 1);
            const binStart = min + binIndex * binWidth;
            const binEnd = binStart + binWidth;
            const binLabel = `${binStart.toFixed(1)}-${binEnd.toFixed(1)}`;
            distribution[binLabel]++;
        });

        return distribution;
    }

    // Distribuciones para generar datos realistas
    normalDistribution(mean, stdDev) {
        // Box-Muller transformation
        const u1 = Math.random();
        const u2 = Math.random();
        const z0 = Math.sqrt(-2 * Math.log(u1)) * Math.cos(2 * Math.PI * u2);
        return z0 * stdDev + mean;
    }

    exponentialDistribution(lambda) {
        return -Math.log(1 - Math.random()) / lambda;
    }

    randomDate(start, end) {
        return new Date(start.getTime() + Math.random() * (end.getTime() - start.getTime()));
    }

    calculateDemographics() {
        return {
            totalPatients: this.hospitalData.patients.length,
            genderAnalysis: this.analyzeByGender(),
            ageAnalysis: this.analyzePatientAges(),
            hospitalizationAnalysis: this.analyzeHospitalizationDays(),
            bloodPressureAnalysis: this.analyzeBloodPressure()
        };
    }

    // Método para obtener estadísticas resumidas
    getSummaryStatistics(variable) {
        let data;
        
        switch(variable) {
            case 'age':
                data = this.hospitalData.patients.map(p => p.age);
                break;
            case 'weight':
                data = this.hospitalData.patients.map(p => p.weight);
                break;
            case 'height':
                data = this.hospitalData.patients.map(p => p.height);
                break;
            case 'daysHospitalized':
                data = this.hospitalData.patients.map(p => p.daysHospitalized);
                break;
            case 'systolicBP':
                data = this.hospitalData.patients.map(p => p.systolicBP);
                break;
            case 'diastolicBP':
                data = this.hospitalData.patients.map(p => p.diastolicBP);
                break;
            default:
                return null;
        }

        return {
            count: data.length,
            mean: this.calculateMean(data),
            median: this.calculateMedian(data),
            mode: this.calculateMode(data),
            standardDeviation: this.calculateStandardDeviation(data),
            variance: this.calculateVariance(data),
            range: this.calculateRange(data),
            minimum: Math.min(...data),
            maximum: Math.max(...data),
            quartiles: this.calculateQuartiles(data),
            coefficientOfVariation: this.calculateCoefficiateOfVariation(data)
        };
    }
}

// Exportar para uso global
window.StatisticsCalculator = StatisticsCalculator;