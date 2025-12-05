# Requerimientos generales para la codificación de predicados

## Documentación de predicados
Agrega antes de cada predicado, una descripción del mismo, utilizando la
normativa definida en [PlDoc](https://www.swi-prolog.org/pldoc/doc_for?object=section(%27packages/pldoc.html%27)).

En particular, indica en el encabezado:
- type; p. ejemplo: atom, number, list, key-value-list (o lista_clave-valor)
- mode; p. ejemplo: +, -, ?
- determinism; p. ejemplo: det, semidet, failure, nondet, multi, undefined.


## Nombre de los predicados

### Predicados que describen relaciones
Esto aplica para
- relaciones representadas mediante facts en la base de datos de Prolog, como en
    ```prolog
    %% categoria_alimento(?Categoria:atom, ?Alimento:atom) is nondet.
    %
    % Ejemplos de alimentos pertenecientes a una categoría específica.
    ```
- relaciones para las que el predicado haga un cálculo a fin de generar instancias de un argumento con base en otros, como en
    ```prolog
    %% alimento_porciones_calorias(+Alimento:atom, +Porciones:number, -CaloriasTotales:number) is det.
    %
    % Calcula las calorías aproximadas basadas en el número de porciones.
    ```

En general, requerimos que el nombre de cualquier predicado esté formado por palabras que correspondan a los argumentos de los predicados, aun cuando el predicado haya sido escrito para realizar un cálculo.
Por ejemplo
% Obtener micronutrientes de un alimento (normalizado y lista)
alimento_micronutriente(+Alimento, +Micronutriente, -Cantidad).
alimento_micronutrientes(+Alimento, -ListaMicronutrientes).

% Calcular macronutrientes por porción (usando helper de lista)
alimento_porciones_macronutrientes(+Alimento, +Porciones, -MacronutrientesPorcion).

% Sumar micronutrientes de una receta completa (nomenclatura sugerida)
receta_totalMicronutrientes(+Receta, -MicronutrientesTotales).

% Verificar deficiencias nutricionales (nomenclatura sugerida)
comidas_requerimientosDiarios_deficiencias(+ListaComidas, +RequirimientosDiarios, -Deficiencias).

% Sugerir alimentos para cubrir deficiencias (nomenclatura sugerida)
nutriente_cantidad_alimentosSugeridos(+Nutriente, +CantidadNecesaria, -AlimentosSugeridos).

Nótese que palabras en plural sugerirían que el argumento correspondiente será una lista o alguna estructura como key-value pairs.

### Predicados que describen existencia o alguna propiedad de un único argumento
En casos como
```prolog
%% categoria(-Categoria:atom) is nondet.
%
% Declara la existencia de una Categoria.
% @param Categoria nombre de una categoría disponible
```
basta con una palabra que describa el elemento cuya existencia se declara.

En casos como
```prolog
%% alimento_con_porcion(-Alimento:atom) is nondet.
%
% Por reintentos (backtracking), genera Alimentos que cuentan con una porción definida.
% @param Alimento alimento con porcion definida.
```
o como
%% alimentos_con_porcion(-Alimentos:list) is det.
%
% Obtiene una lista de todos los alimentos que tienen porción definida.
% @param Alimentos Lista de alimentos con porciones definidas

es preferible que el predicado tenga una palabra o combinación de palabras que
describa la propiedad del argumento

### Predicados que definen acciones de efecto colateral
Como 
- inicializar_sistema/0,
- mostrar_ayuda/0,
- listar_categorias/0,
- listar_tipos_comida/0,
- verificar_integridad_datos/0

basta que el nombre del predicado tenga la forma de dos palabras: verbo_objeto,
en forma imperativa, como sugieren los ejemplos anteriores, 


## Tipos de argumentos
Los argumentos serán:
- átomos o números (atómicos)
- listas de elementos del mismo tipo
- key-value lists (as in library(pairs)), cuando el argumento esté compuesto por una diversidad de elementos, cada uno con un nombre y atributos posiblemente distintos, en cuanto a estructura o unidades de medida.

Ejemplo recomendado (normalizado + helper lista):
`alimento_macronutriente(Alimento, Nutriente, Cantidad)` y el helper `alimento_macronutrientes(Alimento, [proteinas-P, carbohidratos-C, grasas-G, fibra-F])`.
Para unidad de medida, usar `nutriente_unidadMedida(Nutriente, Unidad)` con valores como g, mg, μg o ui.

## Orden de los argumentos
Los argumentos de los predicados debe ser
- argumentos de entrada
- argumentos para cálculos intermedios
- argumentos de salida o calculados

## Declaración de predicados exportados de un módulo
Para efectos de conveniencia y brevedad
- se indicará una **lista de argumentos**, cada uno con un **nombre decriptivo**, como comentario, a la derecha de cada predicado exportado.
- el **modo** de cada argumento se indicará junto con su nombre 
```Prolog
:- module(alimento, [
    categoria/1,                  % ?Categoria
    categoria_alimento/2,         % ?Categoria, ?Alimento
    ...
]).
```

## Expresiones con calificaciones existenciales
Fórmulas con variables anónimas se preferirán antes que fórmulas con calificaciones existenciales.

Por ejemplo, en lugar de
`setof(Cat, Alim^categoria_alimento(Cat, Alim), Cats)`
habrá de usarse
```
findall(Cat, categoria_alimento(Cat, _Alim), CatL)
sort(CatL, Cats)
```
Esto, porque:
1. La calificación existencial es un poco más confusa de leer
2. `findall` produce una lista vacía ante la falta de soluciones, `bagof`, en el que `setof` está basado, simplemente falla en tal caso.
3. `findall` es más eficiente en términos de rendimiento, ya que no necesita crear un nuevo entorno de búsqueda.

## Uso de variables anónimas
El preservar el nombre del argumento existencial en la forma `_Nombre` se
preferirá a la utilización de un simple `_`

## Evitar uso de predicados que dependan de `bagof`, como `setof`
Estos predicados producen `fail` cuando no encuentran soluciones a su 
segundo argumento.

Por ello, en lugar de `bagof`, se preferirá usar `findall`,
de manera que en caso de no haber soluciones se produzca una lista vacía: `[]`.

Similarmente, en lugar de expresiones como
`setof(Cat, Alim^categoria_alimento(Cat, Alim), Cats)`
habrá de usarse
```
findall(Cat, categoria_alimento(Cat, _Alim), CatL)
sort(CatL, Cats)
```

## Escritura de estructuras específicas
### -> ;

Estas deben escribirse siguiendo este patrón, en donde el operador `->` aparece en una nueva línea, y el operador `;` también aparece en una nueva línea, alineado con el `->`:
```prolog
(test_1
->  test_1_is_true
;   (test_2
    ->  test_2_is_true_and_test_1_is_false
    ;   both_are_false
    )
)
```
