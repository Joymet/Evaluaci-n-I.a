# Evaluaci-n-I.a
Hago este repositorio porque es parte de la evaluacion


encia](#licencia)

## Demostración
La serpiente solida se mueve de forma autónoma: en cada iteración se calcula la ruta más corta (en número de celdas) hasta la manzana, evitando el cuerpo actual de la serpiente y los bordes.

## Ejecución
```bash
# 1) Crear y activar entorno
python -m venv .venv
# Windows
.venv\Scripts\activate
# Linux/Mac
source .venv/bin/activate

# 2) Instalar dependencias
pip install pygame

# 3) Ejecutar
python "Snake Max Delgado y Leandro Velazques.py"
```

> **Nota:** para pruebas automáticas/benchmarks en entornos headless (sin pantalla), usar SDL en modo **dummy**:
> ```bash
> # Linux/Mac
> SDL_VIDEODRIVER=dummy python "Snake Max Delgado y Leandro Velazques.py"
> # Windows PowerShell
> $env:SDL_VIDEODRIVER="dummy"; python "Snake Max Delgado y Leandro Velazques.py"
> ```

## Controles
- **Espacio/Enter** en `GAME OVER` → reiniciar
- **Click** en botón `RESET` → reiniciar
- (El movimiento es automático por BFS; no hay controles de dirección manual.)

## Estructura
- `Snake` (clase): cuerpo, dirección, crecimiento, colisiones
- `draw_board(snake, food, score)`: dibuja serpiente, comida y puntaje
- `generate_food(snake)`: genera manzanas en celdas libres
- `bfs(snake, food)`: calcula ruta más corta evitando el cuerpo
- `game_over_screen(score, elapsed_time)`: UI de fin de juego + botón reset
- `game_loop()`: bucle principal (render, BFS → `set_direction`, `move`, colisiones)


## Algoritmo: BFS
Se usa **Búsqueda en Amplitud** sobre la grilla para hallar un camino válido desde la cabeza de la serpiente hasta la comida.  
- **Estados**: celdas `(x, y)` del tablero.
- **Vecinos**: cuatro direcciones ortogonales `UP, DOWN, LEFT, RIGHT` dentro de los límites.
- **Obstáculos**: el **cuerpo actual** de la serpiente (excepto la cabeza).
- **Meta**: la celda de comida.

## Complejidad y costos
- **Tiempo** de BFS: en el peor caso **O(W·H)**, donde `W=WIDTH` y `H=HEIGHT`.
- **Espacio**: también **O(W·H)** por `visited` y la cola.
- **Juego en tiempo real**: se ejecuta BFS **por frame** (hasta 80 FPS). En esta grilla (30×25=750 celdas), BFS es lo bastante rápido en hardware común, pero el costo crece linealmente con el área del tablero.

### Métricas sugeridas
En [`PERFORMANCE.md`](./PERFORMANCE.md) se detalla cómo medir:
- Tiempo promedio de `bfs()` (ms) y desviación estándar
- FPS efectivo con y sin renderizado
- Uso de CPU promedio
- Relación entre **longitud de la serpiente** y tiempo de `bfs()`
- Diferencia entre **tablero vacío** vs. **obstáculos densos**

## Decisiones de diseño
- **Greedy por frame**: recalcular la ruta cada frame simplifica la IA y responde a cambios del entorno (el cuerpo se mueve).
- **Obstáculos = cuerpo**: se evita autocolisión modelando el cuerpo actual como celdas bloqueadas.
- **UI minimalista**: marcador y pantalla de `GAME OVER` con botón `RESET` y atajos de teclado.

## Limitaciones
- **Miopía temporal**: no planifica a futuro; puede encerrarse al crecer (no usa evasión de cola ni caminos hamiltonianos).
- **Sin heurística**: BFS no usa prioridades; en tableros grandes convendría **A\*** con heurística Manhattan.
- **Render dependiente de Pygame**: los benchmarks completos requieren configurar `SDL_VIDEODRIVER=dummy` si no hay display.

## Mejoras Futuras
- A\* o IDA\* con heurística y penalización por cercanía a la cola.
- Modo **headless** con bandera `--no-gui` para benchmarks.
- Evitación de trampas: seguir la cola en ausencia de ruta segura (estrategia tipo “zig-zag”/Hamiltoniano).
- Persistencia de récords, niveles y paredes dinámicas.
- Tests unitarios del BFS y generación controlada de escenarios.
- Perfilado con `cProfile` (ver `PERFORMANCE.md`).

## Créditos
- Código base: *Max Delgado y Leandro Velázquez*.
- Tecnologías: Python, Pygame, .

## Licencia
MIT. Ver `LICENSE`.
