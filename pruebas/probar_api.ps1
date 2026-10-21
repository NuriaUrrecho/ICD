param([string]$BaseUrl = "http://localhost:5000")
$ErrorActionPreference = "Stop"

function Confirmar($condicion, $mensaje) {
    if (-not $condicion) { throw "FALLO: $mensaje" }
    Write-Host "OK  $mensaje" -ForegroundColor Green
}

Write-Host "Probando $BaseUrl"
$health = Invoke-RestMethod "$BaseUrl/health"
Confirmar ($health.status -eq "ok" -and $health.database -eq "connected") "Flask responde y MariaDB está conectada"

$body = @{
    titulo = "Aviso automatizado $([DateTimeOffset]::UtcNow.ToUnixTimeSeconds())"
    descripcion = "Aviso temporal creado por la prueba CRUD"
    categoria = "Mantenimiento"
    prioridad = "Media"
} | ConvertTo-Json

$created = Invoke-RestMethod "$BaseUrl/api/avisos" -Method Post -ContentType "application/json" -Body $body
Confirmar ($created.id -gt 0 -and $created.categoria -eq "Mantenimiento") "CREATE publica un aviso"
$id = $created.id

$read = Invoke-RestMethod "$BaseUrl/api/avisos/$id"
Confirmar ($read.titulo -like "Aviso automatizado*") "READ recupera el aviso"

$patch = @{ prioridad = "Alta" } | ConvertTo-Json
$updated = Invoke-RestMethod "$BaseUrl/api/avisos/$id" -Method Patch -ContentType "application/json" -Body $patch
Confirmar ($updated.prioridad -eq "Alta") "UPDATE modifica la prioridad"

$filtered = Invoke-RestMethod "$BaseUrl/api/avisos?prioridad=Alta"
Confirmar (@($filtered.items | Where-Object { $_.id -eq $id }).Count -eq 1) "El filtro encuentra el aviso actualizado"

Invoke-RestMethod "$BaseUrl/api/avisos/$id" -Method Delete | Out-Null
try {
    Invoke-RestMethod "$BaseUrl/api/avisos/$id" | Out-Null
    throw "FALLO: DELETE no eliminó el aviso"
} catch {
    if ($_.Exception.Response.StatusCode.value__ -ne 404) { throw }
}
Write-Host "OK  DELETE elimina el aviso y una lectura posterior devuelve 404" -ForegroundColor Green
Write-Host "Todas las pruebas CRUD han pasado." -ForegroundColor Cyan

