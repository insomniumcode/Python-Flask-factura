1.- Correr api cliente : dotnet run --urls="http://localhost:7777"  --project C:\prueba\2024_ASY5131_IntegracionPlataformas\API-Csharp\InversionesLtda.API



2.- Correr api producto : dotnet run --project C:\prueba\2024_ASY5131_IntegracionPlataformas\InversionesLtdaProductos.API



3 .- api flask : flask --app api-boleta.py --debug run --port=5001


4.- para entra a la vista de bodeguero usar la ruta http://127.0.0.1:5001/bodeguero (obviamente una vez agregada la factura) y apareceran las facturas agregadas


5.- api logistica en puerto 6000 : dotnet run --urls="http://localhost:6000" --project C:\Proyecto\Python-Flask-factura\2024_ASY5131_IntegracionPlataformas\InversionesLtdaLogistica.API\InversionesLtdaLogistica.API
