1. FuncLang - Mini intérprete

Este proyecto es el examen práctico de la asignatura Compiladores (Grupo B).

El programa implementa un intérprete básico que permite

Definir funciones matemáticas con la palabra func.

- Ejecutar funciones usando print.
- Usar operaciones: +, -, \*, /, ^.
- Manejar errores léxicos, sintácticos y semánticos

Archivos del proyecto

- mini\_func.py  Código del intérprete.
- codigo.txt  Archivo con las funciones de prueba (correctas y con errores).

Ejemplo de uso

Entrada (\`codigo.txt\`)

func suma(a, b) = a + b;

func cuadrado(x) = x \* x;

func potencia(x, y) = x ^ y;

print suma(4,5);

print cuadrado(3);

print potencia(2,4);

print potencia(3, suma(2,2));

Salida esperada

9

9

16

81

errores  q detecta

* Símbolo desconocido.
* Función no definida.
* Número incorrecto de parámetros.
* División por cero.
* Variable no declarada.
* Paréntesis desbalanceados.

ejecucion

python mini_func.py
