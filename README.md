# Renfe Cercanías — Archivo de posición en tiempo real

Descarga la posición en tiempo real de los trenes de Cercanías de Renfe cada minuto.

## Fuente de datos

`https://tiempo-real.renfe.com/renfe-visor/flota.json`

## Estructura

Los datos se guardan en CSV diarios en `data/YYYY/MM/flota-YYYY-MM-DD.csv` con las siguientes columnas:

| Columna | Descripción |
|---|---|
| `timestamp_utc` | Momento de la captura (UTC) |
| `tripId` | Identificador del viaje |
| `codTren` | Código del tren |
| `codLinea` | Línea de Cercanías (C1, C2, etc.) |
| `retrasoMin` | Retraso en minutos |
| `codEstAct` | Código estación actual |
| `codEstSig` | Código siguiente estación |
| `horaLlegadaSigEst` | Hora estimada llegada siguiente estación |
| `codEstDest` | Código estación destino |
| `codEstOrig` | Código estación origen |
| `porAvanc` | Indicador de avance |
| `latitud` | Latitud GPS |
| `longitud` | Longitud GPS |
| `nucleo` | Núcleo de Cercanías |
| `accesible` | Accesibilidad |
| `via` | Vía actual |
| `nextVia` | Siguiente vía |
