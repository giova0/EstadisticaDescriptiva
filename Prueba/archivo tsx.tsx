import { useState } from "react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { BarChart, PieChart, TrendingUp, Activity } from "lucide-react";

const DataVisualization = () => {
  const [selectedChart, setSelectedChart] = useState("bar");

  // Datos simulados del hospital
  const hospitalData = {
    patientsByAge: [
      { age: "0-18", count: 45, percentage: 15 },
      { age: "19-35", count: 90, percentage: 30 },
      { age: "36-50", count: 75, percentage: 25 },
      { age: "51-65", count: 60, percentage: 20 },
      { age: "65+", count: 30, percentage: 10 }
    ],
    diseaseDistribution: [
      { disease: "Hipertensión", count: 120, color: "#ef4444" },
      { disease: "Diabetes", count: 85, color: "#f97316" },
      { disease: "Cardiopatías", count: 65, color: "#eab308" },
      { disease: "Respiratorias", count: 45, color: "#22c55e" },
      { disease: "Otras", count: 85, color: "#3b82f6" }
    ],
    monthlyAdmissions: [
      { month: "Ene", admissions: 245 },
      { month: "Feb", admissions: 220 },
      { month: "Mar", admissions: 280 },
      { month: "Abr", admissions: 265 },
      { month: "May", admissions: 290 },
      { month: "Jun", admissions: 310 }
    ]
  };

  const renderBarChart = () => {
    const maxCount = Math.max(...hospitalData.patientsByAge.map(d => d.count));
    
    return (
      <div className="space-y-4">
        <h4 className="pixel-subtitle">Distribución de Pacientes por Edad</h4>
        <div className="space-y-3">
          {hospitalData.patientsByAge.map((item, index) => (
            <div key={index} className="flex items-center space-x-4">
              <div className="w-16 pixel-text text-xs">{item.age}</div>
              <div className="flex-1 bg-muted h-8 relative border-2 border-pixel-shadow">
                <div 
                  className="bg-primary h-full transition-all duration-500"
                  style={{ width: `${(item.count / maxCount) * 100}%` }}
                />
                <div className="absolute inset-0 flex items-center justify-center">
                  <span className="pixel-text text-xs text-white font-bold">
                    {item.count}
                  </span>
                </div>
              </div>
              <div className="w-12 pixel-text text-xs">{item.percentage}%</div>
            </div>
          ))}
        </div>
      </div>
    );
  };

  const renderPieChart = () => {
    const total = hospitalData.diseaseDistribution.reduce((sum, item) => sum + item.count, 0);
    let currentAngle = 0;

    return (
      <div className="space-y-4">
        <h4 className="pixel-subtitle">Distribución de Enfermedades</h4>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div className="relative">
            <svg width="200" height="200" className="mx-auto">
              <circle cx="100" cy="100" r="80" fill="none" stroke="#000" strokeWidth="4"/>
              {hospitalData.diseaseDistribution.map((item, index) => {
                const percentage = (item.count / total) * 100;
                const angle = (percentage / 100) * 360;
                const x1 = 100 + 80 * Math.cos((currentAngle - 90) * Math.PI / 180);
                const y1 = 100 + 80 * Math.sin((currentAngle - 90) * Math.PI / 180);
                const x2 = 100 + 80 * Math.cos((currentAngle + angle - 90) * Math.PI / 180);
                const y2 = 100 + 80 * Math.sin((currentAngle + angle - 90) * Math.PI / 180);
                
                const largeArcFlag = angle > 180 ? 1 : 0;
                const pathData = `M 100 100 L ${x1} ${y1} A 80 80 0 ${largeArcFlag} 1 ${x2} ${y2} Z`;
                
                currentAngle += angle;
                
                return (
                  <path
                    key={index}
                    d={pathData}
                    fill={item.color}
                    stroke="#000"
                    strokeWidth="2"
                  />
                );
              })}
            </svg>
          </div>
          <div className="space-y-2">
            {hospitalData.diseaseDistribution.map((item, index) => (
              <div key={index} className="flex items-center space-x-3">
                <div 
                  className="w-4 h-4 border-2 border-pixel-shadow"
                  style={{ backgroundColor: item.color }}
                />
                <span className="pixel-text text-xs flex-1">{item.disease}</span>
                <span className="pixel-text text-xs">{item.count}</span>
                <span className="pixel-text text-xs">
                  ({((item.count / total) * 100).toFixed(1)}%)
                </span>
              </div>
            ))}
          </div>
        </div>
      </div>
    );
  };

  const renderLineChart = () => {
    const maxAdmissions = Math.max(...hospitalData.monthlyAdmissions.map(d => d.admissions));
    const minAdmissions = Math.min(...hospitalData.monthlyAdmissions.map(d => d.admissions));
    
    return (
      <div className="space-y-4">
        <h4 className="pixel-subtitle">Ingresos Mensuales 2024</h4>
        <div className="bg-muted p-4 border-2 border-pixel-shadow">
          <svg width="100%" height="200" viewBox="0 0 400 200">
            {/* Grid lines */}
            {[0, 1, 2, 3, 4].map(i => (
              <line
                key={i}
                x1="50"
                y1={40 + i * 30}
                x2="350"
                y2={40 + i * 30}
                stroke="#ccc"
                strokeWidth="1"
                strokeDasharray="2,2"
              />
            ))}
            
            {/* Data line */}
            <polyline
              points={hospitalData.monthlyAdmissions.map((item, index) => {
                const x = 50 + (index * 50);
                const y = 160 - ((item.admissions - minAdmissions) / (maxAdmissions - minAdmissions)) * 120;
                return `${x},${y}`;
              }).join(' ')}
              fill="none"
              stroke="hsl(var(--primary))"
              strokeWidth="4"
            />
            
            {/* Data points */}
            {hospitalData.monthlyAdmissions.map((item, index) => {
              const x = 50 + (index * 50);
              const y = 160 - ((item.admissions - minAdmissions) / (maxAdmissions - minAdmissions)) * 120;
              return (
                <g key={index}>
                  <circle cx={x} cy={y} r="6" fill="hsl(var(--primary))" stroke="#000" strokeWidth="2"/>
                  <text x={x} y="185" textAnchor="middle" className="pixel-text text-xs">{item.month}</text>
                  <text x={x} y={y - 10} textAnchor="middle" className="pixel-text text-xs">{item.admissions}</text>
                </g>
              );
            })}
          </svg>
        </div>
      </div>
    );
  };

  return (
    <Card className="pixel-card">
      <CardHeader>
        <CardTitle className="pixel-title flex items-center">
          <Activity className="w-6 h-6 mr-2" />
          Visualización de Datos Hospitalarios
        </CardTitle>
      </CardHeader>
      <CardContent>
        <div className="space-y-6">
          {/* Chart Type Selector */}
          <div className="flex flex-wrap gap-2">
            <Button
              variant={selectedChart === "bar" ? "default" : "outline"}
              className="pixel-button text-xs"
              onClick={() => setSelectedChart("bar")}
            >
              <BarChart className="w-4 h-4 mr-2" />
              Barras
            </Button>
            <Button
              variant={selectedChart === "pie" ? "default" : "outline"}
              className="pixel-button text-xs"
              onClick={() => setSelectedChart("pie")}
            >
              <PieChart className="w-4 h-4 mr-2" />
              Circular
            </Button>
            <Button
              variant={selectedChart === "line" ? "default" : "outline"}
              className="pixel-button text-xs"
              onClick={() => setSelectedChart("line")}
            >
              <TrendingUp className="w-4 h-4 mr-2" />
              Líneas
            </Button>
          </div>

          {/* Chart Display */}
          <div className="pixel-card bg-card">
            {selectedChart === "bar" && renderBarChart()}
            {selectedChart === "pie" && renderPieChart()}
            {selectedChart === "line" && renderLineChart()}
          </div>

          {/* Statistical Summary */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div className="stats-display text-center">
              <div className="text-2xl font-bold text-primary">400</div>
              <div className="pixel-text text-xs">Total Pacientes</div>
            </div>
            <div className="stats-display text-center">
              <div className="text-2xl font-bold text-secondary">15%</div>
              <div className="pixel-text text-xs">Tasa Ocupación</div>
            </div>
            <div className="stats-display text-center">
              <div className="text-2xl font-bold text-accent">4.2</div>
              <div className="pixel-text text-xs">Estancia Promedio</div>
            </div>
          </div>

          {/* Interpretation */}
          <div className="pixel-card bg-muted">
            <h4 className="pixel-subtitle mb-3">Interpretación Estadística</h4>
            <div className="space-y-2 pixel-text text-sm">
              <p>• La distribución por edades muestra mayor concentración en adultos jóvenes (19-35 años)</p>
              <p>• La hipertensión es la patología más prevalente con 30% de los casos</p>
              <p>• Se observa tendencia creciente en ingresos durante el primer semestre</p>
              <p>• La variabilidad mensual sugiere factores estacionales en las admisiones</p>
            </div>
          </div>
        </div>
      </CardContent>
    </Card>
  );
};

export default DataVisualization;