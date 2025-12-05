# Ejecución de Scripts

## Carga Obligatoria de init.pl

**REGLA FUNDAMENTAL**: Todo script de Prolog en este proyecto DEBE cargar el archivo `init.pl` al inicio de su ejecución.

### Comando Estándar

Para ejecutar cualquier script `.pl` en el proyecto:

```bash
cd /path/to/project && swipl -s init.pl -l archivo_target.pl -g "objetivo" -t halt
```

O alternativamente:

```bash
cd /path/to/project && swipl -s init.pl -g "ensure_loaded('archivo_target.pl'), objetivo" -t halt
```

### Razones para esta Práctica

#### 1. **Configuración de Rutas de Búsqueda**
El archivo `init.pl` establece las rutas de búsqueda críticas para el proyecto:
- `file_search_path(module, 'src/module')` - Para módulos de producción
- `file_search_path(testdata, 'test/data')` - Para módulos de datos de prueba
- `file_search_path(src, 'src')` - Para código fuente general

Sin estas rutas, el sistema no puede resolver correctamente las declaraciones como:
- `use_module(module(alimento_fact), [...])`
- `use_module(testdata(nutricion_fact), [...])`

#### 2. **Inyección de Dependencias**
Los módulos que usan `injectable_module/2` dependen de que las rutas estén configuradas para:
- Localizar módulos de producción (`module/nombre`)
- Localizar módulos de prueba (`testdata/nombre`) 
- Permitir la sustitución automática durante testing

#### 3. **Variables de Entorno**
Muchos módulos requieren que `MENUS_PROJECT_ROOT` esté definida correctamente, lo cual se gestiona desde `init.pl`.

#### 4. **Consistencia del Entorno**
Garantiza que todos los scripts se ejecuten en el mismo entorno configurado, independientemente de:
- El directorio actual de trabajo
- El shell usado
- Las variables de entorno del usuario

### Ejemplos de Uso Correcto

#### Ejecutar Tests
```bash
cd /home/calang/proyects/calang/menus && swipl -s init.pl -l test/test_nutricion.pl -g "run_tests" -t halt
```

#### Ejecutar Tests Específicos
```bash
cd /home/calang/proyects/calang/menus && swipl -s init.pl -l test/test_nutricion.pl -g "run_tests(basicos)" -t halt
```

#### Cargar y Consultar Módulos
```bash
cd /home/calang/proyects/calang/menus && swipl -s init.pl -l src/nutricion.pl -g "alimento_macronutrientes(pollo, X), write(X)" -t halt
```

### Error Común

❌ **INCORRECTO**:
```bash
swipl -s test/test_nutricion.pl -g "run_tests" -t halt
```

✅ **CORRECTO**:
```bash
cd /path/to/project && swipl -s init.pl -l test/test_nutricion.pl -g "run_tests" -t halt
```

### Verificación

Para verificar que `init.pl` está cargado correctamente, se puede comprobar:
```prolog
?- file_search_path(module, Path).
Path = 'src/module'.
```

Si esto falla, es señal de que `init.pl` no se cargó apropiadamente.

## Integración con IDEs y Herramientas

### SWI-Prolog IDE
Configurar el IDE para que siempre cargue `init.pl` como primer archivo.

### Scripts de Automatización
Todos los scripts de build, test y despliegue deben seguir este patrón de carga.

### CI/CD Pipelines
Los pipelines de integración continua deben incluir la carga de `init.pl` en todos los pasos de prueba.