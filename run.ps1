param(
    [switch]$Install
)

# Ruta esperada del entorno conda local dentro del repo
$envPath = Join-Path $PSScriptRoot ".conda"
$condaExe = "C:/Users/Lenovo/anaconda3/Scripts/conda.exe"

function Run-With-Conda {
    param($cmdArgs)
    & $condaExe run -p $envPath --no-capture-output $cmdArgs
}

if (Test-Path $condaExe -PathType Leaf -ErrorAction SilentlyContinue) {
    if ($Install) {
        Write-Output "Instalando dependencias en el entorno local (.conda)..."
        Run-With-Conda "python -m pip install -r \"$PSScriptRoot\\requirements.txt\""
    }
    Write-Output "Iniciando la aplicación con el entorno local (.conda)..."
    Run-With-Conda "python \"$PSScriptRoot\\main.py\""
} else {
    Write-Output "No se encontró conda en: $condaExe"
    Write-Output "Intentando ejecutar con el `python` disponible en PATH..."
    if ($Install) {
        python -m pip install -r (Join-Path $PSScriptRoot 'requirements.txt')
    }
    python (Join-Path $PSScriptRoot 'main.py')
}
