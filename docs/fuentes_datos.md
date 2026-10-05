# Fuentes de datos

## Principios

- No usar scraping de plataformas si sus terminos no lo permiten.
- Guardar la fuente de cada dato importado.
- Diferenciar datos manuales, oficiales y de proveedor autorizado.
- Empezar con carga manual/CSV hasta decidir productos concretos.

## Fuentes candidatas

### Oficiales

- Banco de Espana: series macro y estadisticas.
- Banco Central Europeo: tipos oficiales y series monetarias.
- INE: IPC e inflacion.
- CNMV: registros oficiales de entidades, fondos y gestoras.
- Tesoro Publico: informacion de deuda publica.

### De mercado

Los precios de fondos, ETFs y bonos pueden tener licencias especificas. Para el MVP se usaran datos manuales o importados por fichero.

## Campos minimos por dato

- producto_id
- fecha
- valor/precio
- divisa
- fuente
- tipo_fuente: manual, oficial, proveedor, broker_export
- fecha de carga
