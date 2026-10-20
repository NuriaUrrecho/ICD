param([string]$BaseUrl = "http://localhost:5000")
$ErrorActionPreference = "Stop"

function Confirmar($condicion, $mensaje) {
    if (-not $condicion) { throw "FALLO: $mensaje" }
    Write-Host "OK  $mensaje" -ForegroundColor Green
}

Write-Host "Probando $BaseUrl"
$health = Invoke-RestMethod "$BaseUrl/api/health"
Confirmar ($health.status -eq "ok" -and $health.database -eq "connected") "Flask responde y MariaDB está conectada"

$serial = "TEST-$([DateTimeOffset]::UtcNow.ToUnixTimeSeconds())"
$body = @{
    nombre = "Portátil de validación"
    tipo = "Portátil"
    marca = "Lenovo"
    modelo = "ThinkPad"
    numero_serie = $serial
    estado = "Operativo"
    ubicacion = "Laboratorio"
    ip_address = "192.0.2.25"
} | ConvertTo-Json

$created = Invoke-RestMethod "$BaseUrl/api/equipos" -Method Post -ContentType "application/json" -Body $body
Confirmar ($created.id -gt 0 -and $created.numero_serie -eq $serial) "CREATE devuelve 201 y el equipo creado"
$id = $created.id

$read = Invoke-RestMethod "$BaseUrl/api/equipos/$id"
Confirmar ($read.nombre -eq "Portátil de validación") "READ recupera el equipo"

$patch = @{ estado = "Mantenimiento" } | ConvertTo-Json
$updated = Invoke-RestMethod "$BaseUrl/api/equipos/$id" -Method Patch -ContentType "application/json" -Body $patch
Confirmar ($updated.estado -eq "Mantenimiento") "UPDATE modifica el estado"

$search = Invoke-RestMethod "$BaseUrl/api/equipos?q=$serial"
Confirmar ($search.total -eq 1) "El buscador encuentra el número de serie"

Invoke-RestMethod "$BaseUrl/api/equipos/$id" -Method Delete | Out-Null
try {
    Invoke-RestMethod "$BaseUrl/api/equipos/$id" | Out-Null
    throw "FALLO: DELETE no eliminó el equipo"
} catch {
    if ($_.Exception.Response.StatusCode.value__ -ne 404) { throw }
}
Write-Host "OK  DELETE elimina el equipo y una lectura posterior devuelve 404" -ForegroundColor Green
Write-Host "Todas las pruebas CRUD han pasado." -ForegroundColor Cyan

