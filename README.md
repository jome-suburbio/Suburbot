# Suburbot

Sistema de reservas para un hotel pequeno.

## Paso actual

Esta primera parte implementa:

- Conexion a Google Sheets con una cuenta de servicio.
- Funcion para consultar disponibilidad por rango de fechas.
- Script local para probar la consulta.
- Pruebas unitarias de la logica de disponibilidad sin conectarse a Google.

## Estructura esperada de Google Sheets

Crea una pestaña, por ejemplo `Disponibilidad`, con esta estructura:

| habitacion | 2026-04-10 | 2026-04-11 | 2026-04-12 |
| --- | --- | --- | --- |
| H1 | disponible | ocupado | disponible |
| H2 | disponible | disponible | disponible |
| H3 | ocupado | disponible | disponible |

Reglas:

- La primera fila contiene fechas.
- La primera columna contiene el nombre o codigo de la habitacion.
- Las celdas deben usar `disponible` u `ocupado`.
- El check-out no cuenta como noche ocupada. Por ejemplo, del `2026-04-10` al `2026-04-12` revisa las noches `2026-04-10` y `2026-04-11`.

## Instalacion local

1. Instala dependencias:

```bash
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -r requirements.txt
```

2. Crea el archivo `.env`:

```bash
cp .env.example .env
```

3. Configura Google Sheets:

- Crea un proyecto en Google Cloud.
- Activa la Google Sheets API.
- Crea una cuenta de servicio.
- Descarga su JSON de credenciales.
- Comparte tu Google Sheet con el email de la cuenta de servicio, con permiso de editor.
- Agrega el `GOOGLE_SHEETS_SPREADSHEET_ID` y `GOOGLE_SHEETS_TAB_NAME` a `.env`.
- Usa una de estas opciones:
  - `GOOGLE_APPLICATION_CREDENTIALS=./credentials/google-service-account.json`
  - `GOOGLE_SERVICE_ACCOUNT_JSON={...json completo...}`

## Probar disponibilidad

```bash
python3 scripts/check_availability.py --check-in 2026-04-10 --check-out 2026-04-12
```

Salida esperada:

```json
{
  "check_in": "2026-04-10",
  "check_out": "2026-04-12",
  "nights": ["2026-04-10", "2026-04-11"],
  "available_rooms": ["H2"]
}
```

## Pruebas

```bash
python3 -m unittest discover -s test
```

Estas pruebas validan la logica de disponibilidad con datos simulados.

## Variables de entorno necesarias

- `GOOGLE_SHEETS_SPREADSHEET_ID`: ID del Google Sheet.
- `GOOGLE_SHEETS_TAB_NAME`: nombre de la pestaña con disponibilidad.
- `GOOGLE_APPLICATION_CREDENTIALS`: ruta al JSON de cuenta de servicio, o
- `GOOGLE_SERVICE_ACCOUNT_JSON`: JSON completo de cuenta de servicio.
