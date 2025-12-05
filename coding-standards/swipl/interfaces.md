# Interfaces

Estándares para la escritura del archivo docs/interfaces.md,
describiendo
- los módulos y sus predicados exportados
- relaciones entre módulos
- uso del sistema

## Enumeración de predicados exportados
Es innecesario indicar el nombre del predicado exportado y la cantidad de argumentos,
cuando al mismo tiempo se da un ejemplo de
- nombre del predicado y cantidad de argumentos
- typo de cada argumento
- modo de cada argumento

Por ejemplo, en lugar de
```text
Predicados exportados:

receta/3 - receta(?Nombre, ?Comida, ?Instrucciones)
tipoComida_recetas/2 - tipocomida_recetas(+TipoComida, -Recetas)
```
deberá producirse
```text
Predicados exportados:

receta(?Nombre, ?Comida, ?Instrucciones)
tipocomida_recetas(+TipoComida, -Recetas)
```
