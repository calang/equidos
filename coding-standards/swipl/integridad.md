# Pruebas de integridad

## Referencias
Cuandoquiera que un predicado (fact) utilice átomos que 
identifiquen entidades definidas o creadas mediante otros predicados,
deberá haber predicados que comprueben la integridad de estas referencias.

Esta verificación de referencias entre predicados es semejante a la revisión
que uno haría en una base de datos relacional, asegurando que las llaves foráneas
(foreign keys) presentes en algún registro tengan valores presentes
en los campos llave de la tabla a la que se estén refiriendo.

## Sistema de comprobación

Sistema que utiliza predicados genéricos para realizar las verificaciones de integridad.

### Base de datos de dependencias

Por aparte, se forma una lista o tabla, a partir de un predicado Prolog, `dependencia`
que indica en cada una de sus cláusulas, una las dependencias entre predicados.

Cada dependencia (o cláusula del predicado `dependencia`) deberá indicar:
- módulo origen
- predicado origen
- posición y nombre del argumento que apunta a la referencia
- módulo destino
- predicado destino
- posición y nombre del argumento sobre el que se da la dependencia.

Por ejemplo, siendo que un predicado
```
preferencia(Tipo, Alimento)
```
definido en un módulo A,
dependa de que el alimento mencionado esté presente en una cláusula como
```
comida(Alimento, Clase)
```
definido en un módulo B,
entonces habrá de haber una cláusula para el predicado `dependencia` como
```
dependencia('A', preferencia, 2-'Alimento', 'B', comida, 1-'Alimento')
```

### Predicado genéricos de verificación

El predicado `verif_deps/1` toma la información de cada dependencia
representada en una cláusula del predicado `dependencia`,
produciendo una lista Prolog indicando cuáles predicados destino,
y en qué módulos destino, tienen qué valores ausentes en su argumento de referencia.

P. ejemplo, `verif_deps/1` produce una lista en su único argumento de salida, con la estructura siguiente:
```
[   ('A', preferencia, 2-'Alimento', 'B', comida, 1-'Alimento')-[pescado, carne, chuleta],
    ...
]
```
En este ejemplo se indica que en el argumento número `1`, llamado `Alimento`,
del predicado `comida` en el módulo `B`
hacen falta cláusulas con los valores `pescado`, `carne`, `chuleta`,
las cuales se utilizan en el predicado preferencia, del módulo `A`,
desde el argumento número `2`, llamado también `Alimento`.

Nótese en particular, que la notación N-'Dato' significa que 
el valor buscado, correspondiente a un 'Dato', está en la posición
número N (contando a partir de 1) del predicado.

Semejantemente, habrá elementos adicionales en la misma lista describiendo otros
posible faltantes en los predicados de referencia.
