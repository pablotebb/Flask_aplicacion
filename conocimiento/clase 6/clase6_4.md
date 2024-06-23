> Y para volver sólo a la anterior?

Para volver solo a la migración anterior (una posición atrás), puedes usar el comando `flask db downgrade` sin necesidad de especificar el identificador único. Flask-Migrate tiene una opción de conveniencia que permite retroceder una migración a la vez. Aquí están los pasos:

1. **Retroceder una migración**:
   Usa el comando `flask db downgrade` con el argumento `-1` para retroceder una migración.

   En consola, dentro de tu proyecto Flask, ejecuta:

   ```bash
   flask db downgrade -1
   ```

Este comando revertirá la base de datos al estado anterior a la última migración aplicada.

### Ejemplo Paso a Paso

1. **Aplicar migraciones**:
   Supongamos que actualmente has aplicado las siguientes migraciones:

   ```
   abcd1234 -> efg56789 (head), "Add campo4 to Usuario and Tarea"
   1234abcd -> abcd1234, "Add campo3 to Tarea"
   7890efgh -> 1234abcd, "Add Tarea"
   efgh5678 -> 7890efgh, "Add campo3 to Usuario"
   4567abcd -> efgh5678, "Add User"
   ```

2. **Retroceder una migración**:
   Si actualmente estás en la migración `efg56789` (la más reciente), ejecutar el siguiente comando te llevará a la migración `abcd1234`:

   ```bash
   flask db downgrade -1
   ```

   Esto revertirá la última migración aplicada, volviendo a la base de datos al estado correspondiente a la migración "Add campo3 to Tarea".

Si necesitas retroceder más de una migración, puedes ejecutar el comando varias veces, una para cada migración que quieras revertir.

### Volver a la migración anterior específica

Si quieres volver a una migración específica que está justo antes de la actual, pero sabes su identificador, puedes usar:

```bash
flask db downgrade <identificador>
```

Este método requiere conocer el identificador de la migración a la que deseas volver. Para volver a la migración inmediatamente anterior, generalmente `flask db downgrade -1` es suficiente y más conveniente.

### Confirmar el Estado de la Migración

Puedes usar el comando `flask db current` para ver cuál es la migración actual aplicada:

```bash
flask db current
```

Esto te permitirá confirmar que has revertido correctamente a la migración anterior.
