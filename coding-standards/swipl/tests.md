# Testing Standards

## Test file correspondence

Each module, say `<mod>.pl`, must have a corresponding test file called `test_<mod>.pl`.

Test files must follow the standards outlined in the [SWI-Prolog PLUnit documentation](https://www.swi-prolog.org/pldoc/doc_for?object=section(%27packages/plunit.html%27)).

`test_<mod>.pl` must have tests verifying the correctness of each predicate in `<mod>.pl`, including all cases where the predicate is queried under any condition matching its PlDoc.

When numeric arguments are used, tests must cover critical and extreme values.

## **Testing Architecture: Dependency Injection with Testdata**

### **Primary Strategy: Term Expansion with Dynamic Facts**

This project uses `term_expansion/2` to automatically substitute static fact modules with dynamic testdata modules:

```prolog
% In test files: Automatic module substitution
term_expansion(
    injectable_module(module_fact, module(module_fact)),
    injectable_module(module_fact, testdata(module_fact))
).
```

**Benefits proven in practice:**
- ✅ **Total control** over test data
- ✅ **Complete isolation** between tests  
- ✅ **Zero changes** required in production code
- ✅ **Maximum flexibility** for complex scenarios
- ✅ **30 tests implemented** with 100% success rate

### **Project Structure**

```
project/
├── init.pl                     # Configure search paths
├── src/module/                 # Production modules
│   └── module_rule.pl         # With injectable_module declarations
├── test/data/                  # Testdata modules with dynamic predicates
│   └── module_fact.pl         # Same interface, dynamic predicates
└── test/
    └── test_module.pl         # Tests with term_expansion
```

### **Implementation Example**

#### Step 1: Rule Module (Production)
```prolog
% In src/module/alimento_rule.pl
:- module(alimento_rule, [categorias/1, categoria_alimentos/2]).

% Initialize environment
:-  getenv('MENUS_PROJECT_ROOT', Root),
    atom_concat(Root, '/init', InitFile),
    ensure_loaded(InitFile).

% Injectable dependency declaration (production default)
injectable_module(alimento_fact, module(alimento_fact)).

% Load module (real or substituted)
:-  injectable_module(alimento_fact, ModAlimentoFact),
    use_module(ModAlimentoFact, [categoria/1, categoria_alimento/2]).

% Rules using dependencies (unchanged)
categorias(CategoriasUnicas) :-
    findall(Categoria, categoria(Categoria), CategoriaList),
    sort(CategoriaList, CategoriasUnicas).
```

#### Step 2: Testdata Module (Dynamic)
```prolog
% In test/data/alimento_fact.pl
:- module(alimento_fact, [categoria/1, categoria_alimento/2]).

% CRITICAL: Dynamic predicates for test manipulation
:- dynamic categoria/1.
:- dynamic categoria_alimento/2.

% Initial facts (optional, can be modified by tests)
% categoria(proteina).
% categoria_alimento(proteina, pollo).
```

#### Step 3: Test File (Injection)
```prolog
% In test/test_alimento.pl
#!/usr/bin/env swipl

% Initialize environment
:-  getenv('MENUS_PROJECT_ROOT', Root),
    atom_concat(Root, '/init', InitFile),
    ensure_loaded(InitFile).

% DEPENDENCY INJECTION: Substitute static facts with dynamic testdata
term_expansion(
    injectable_module(alimento_fact, module(alimento_fact)),
    injectable_module(alimento_fact, testdata(alimento_fact))
).

:- use_module(library(plunit)).
:- use_module(module(alimento_rule), [categorias/1, categoria_alimentos/2]).

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%% GLOBAL TESTING HELPERS
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

% Helper to clean test facts
cleanup_facts_test :-
    retractall(alimento_fact:categoria(_)),
    retractall(alimento_fact:categoria_alimento(_, _)).

% Helper to setup basic facts
setup_facts_basicos :-
    cleanup_facts_test,
    asserta(alimento_fact:categoria(proteina)),
    asserta(alimento_fact:categoria(vegetal)),
    asserta(alimento_fact:categoria_alimento(proteina, pollo)),
    asserta(alimento_fact:categoria_alimento(vegetal, lechuga)).
```
## **Recommended Test Suite Organization**

### **1. Basic Tests** (Required)
```prolog
:- begin_tests(basicos).

test(caso_tipico, [
    setup(setup_facts_basicos),
    cleanup(cleanup_facts_test),
    true(Resultado == [esperado, orden])
]) :-
    predicado_principal(Resultado).

:- end_tests(basicos).
```

### **2. Edge Cases** (Required)
```prolog
:- begin_tests(casos_limite).

test(sistema_vacio, [
    setup(cleanup_facts_test),
    cleanup(cleanup_facts_test),
    true(Resultado == [])
]) :-
    predicado_principal(Resultado).

test(entrada_invalida, [
    setup(setup_facts_basicos),
    cleanup(cleanup_facts_test),
    true(Resultado == [])
]) :-
    predicado_principal(entrada_inexistente, Resultado).

:- end_tests(casos_limite).
```

### **3. Realistic Configurations** (Recommended)
```prolog
:- begin_tests(configuraciones_realistas).

test(escenario_real_usuario, [
    setup(setup_escenario_real),
    cleanup(cleanup_facts_test)
]) :-
    predicado_principal(EntradaReal),
    validar_resultado_realista(EntradaReal).

:- end_tests(configuraciones_realistas).
```

### **4. Property-Based Tests** (Recommended)
```prolog
:- begin_tests(propiedades).

test(resultado_siempre_ordenado, [
    setup(setup_facts_basicos),
    cleanup(cleanup_facts_test)
]) :-
    predicado_principal(Resultado),
    sort(Resultado, ResultadoOrdenado),
    Resultado == ResultadoOrdenado.

test(consistencia_con_facts, [
    setup(setup_facts_basicos),
    cleanup(cleanup_facts_test)
]) :-
    predicado_principal(Resultado),
    forall(member(Item, Resultado), (
        module_fact:fact_relacionado(Item)
    )).

:- end_tests(propiedades).
```

### **5. Regression Tests** (Required for critical modules)
```prolog
:- begin_tests(regresion).

test(manejo_duplicados, [
    setup(setup_facts_con_duplicados),
    cleanup(cleanup_facts_test)
]) :-
    predicado_principal(Resultado),
    sort(Resultado, ResultadoLimpio),
    length(Resultado, N1),
    length(ResultadoLimpio, N2),
    N1 =:= N2.  % No debe haber duplicados

:- end_tests(regresion).
```

### **6. Performance Tests** (For critical modules)
```prolog
:- begin_tests(performance).

test(tiempo_ejecucion_aceptable, [
    setup(setup_facts_basicos),
    cleanup(cleanup_facts_test),
    true(Time =< 0.1)
]) :-
    get_time(Start),
    predicado_principal(_),
    get_time(End),
    Time is End - Start.

:- end_tests(performance).
```

### **7. Use Case Tests** (Domain-specific)
```prolog
:- begin_tests(casos_uso).

test(caso_uso_especifico, [
    setup(setup_caso_uso_real),
    cleanup(cleanup_facts_test),
    true(cumple_requisitos_dominio(Resultado))
]) :-
    predicado_principal(Resultado).

:- end_tests(casos_uso).
```

### **8. Integrity Tests** (Data validation)
```prolog
:- begin_tests(integridad).

test(no_datos_huerfanos, [
    setup(setup_facts_basicos),
    cleanup(cleanup_facts_test)
]) :-
    predicado_principal(Resultado),
    forall(member(Item, Resultado), (
        validar_integridad_item(Item)
    )).

:- end_tests(integridad).
```

## **Specialized Helper Patterns**

### **Scenario-specific helpers**
```prolog
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%% HELPERS FOR SCENARIO CONFIGURATION
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

% Helper for specific domain scenario
setup_escenario_vegano :-
    cleanup_facts_test,
    asserta(module_fact:categoria(vegetal)),
    asserta(module_fact:categoria(fruta)),
    asserta(module_fact:categoria_alimento(vegetal, lechuga)),
    asserta(module_fact:categoria_alimento(fruta, manzana)).

% Helper for scalability scenarios
setup_escenario_escalabilidad(N) :-
    cleanup_facts_test,
    forall(between(1, N, I), (
        atom_concat(categoria_, I, Cat),
        asserta(module_fact:categoria(Cat)),
        atom_concat(item_, I, Item),
        asserta(module_fact:categoria_alimento(Cat, Item))
    )).

% Helper for edge case scenarios
setup_escenario_duplicados :-
    cleanup_facts_test,
    asserta(module_fact:categoria(proteina)),
    asserta(module_fact:categoria(proteina)),  % Intentional duplicate
    asserta(module_fact:categoria_alimento(proteina, pollo)),
    asserta(module_fact:categoria_alimento(proteina, pollo)).  % Intentional duplicate
```

## **Success Case Study: test_alimento.pl**

**Implemented structure:**
- ✅ **30 tests total** - all passing
- ✅ **8 test suites** covering different aspects
- ✅ **Dependency injection** with testdata
- ✅ **Complete isolation** between tests
- ✅ **Domain-specific scenarios** (vegan diet, keto diet, etc.)
- ✅ **Property verification** (ordering, consistency)
- ✅ **Performance testing** for scalability

**Test suite breakdown:**
1. `basicos` (3 tests) - Core functionality
2. `casos_limite` (5 tests) - Edge cases and boundaries  
3. `configuraciones_realistas` (5 tests) - Real-world scenarios
4. `propiedades` (3 tests) - Invariant properties
5. `regresion` (4 tests) - Preventing regressions
6. `performance` (3 tests) - Performance validation
7. `casos_uso` (3 tests) - Domain-specific use cases
8. `integridad` (4 tests) - Data integrity validation

## **Best Practices (Updated)**

### **Mandatory Requirements**
1. ✅ **Use dependency injection** with `term_expansion` for fact-dependent modules
2. ✅ **Create testdata modules** with dynamic predicates
3. ✅ **Implement global helpers** (`cleanup_facts_test`, `setup_facts_basicos`)
4. ✅ **Use setup/cleanup** in every test suite
5. ✅ **Test edge cases** (empty data, invalid input, scalability)
6. ✅ **Organize into logical test suites** (basic, limits, realistic, properties, etc.)

### **Strongly Recommended**
7. ✅ **Include property-based tests** for invariants
8. ✅ **Test realistic domain scenarios** reflecting actual usage
9. ✅ **Add performance tests** for critical operations
10. ✅ **Use descriptive test and suite names**
11. ✅ **Document test purpose** in comments
12. ✅ **Verify both positive and negative cases**

### **Configuration Requirements**
13. ✅ **Configure init.pl** with proper search paths:
    ```prolog
    :- asserta(user:file_search_path(testdata, 'test/data')).
    :- asserta(user:file_search_path(module, 'src/module')).
    ```

### **Quality Standards**
14. ✅ **All tests must pass** before committing
15. ✅ **Maintain test isolation** - no test dependencies
16. ✅ **Test execution time** should be reasonable (< 0.1s per test typically)
17. ✅ **Cover all public predicates** of the module

## **Legacy Techniques (Deprecated)**

The following techniques are now **not recommended** in favor of dependency injection:

~~**Strategy 1**: Direct setup/cleanup with module facts~~ 
- **Problem**: Modifies production module state
- **Replaced by**: Testdata modules with dependency injection

~~**Strategy 2**: Parameterized tests without injection~~
- **Problem**: Complex parameter passing, brittle tests  
- **Replaced by**: Scenario-specific helper functions

~~**Strategy 3**: Integration tests with real facts only~~
- **Problem**: Lack of control, non-deterministic results
- **Replaced by**: Controlled integration tests with testdata

The **dependency injection with testdata** technique has proven superior in all aspects: control, isolation, maintainability, and flexibility.
