#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

#define MAX_FILA 100
#define MAX_COL 100
#define DIRECCIONES 4

// Direcciones posibles: arriba, abajo, izquierda, derecha
int direcciones[DIRECCIONES][2] = {{-1, 0}, {1, 0}, {0, -1}, {0, 1}};

// Estructura para el mapa
char mapa[MAX_FILA][MAX_COL];
int visitado[MAX_FILA][MAX_COL];
int filas, columnas;

void cargar_archivo(char *ruta_archivo) {
    FILE *archivo = fopen(ruta_archivo, "r");
    if (!archivo) {
        printf("Error al cargar el archivo\n");
        exit(1);
    }
    
    char linea[MAX_COL];
    filas = 0;
    
    while (fgets(linea, sizeof(linea), archivo)) {
        linea[strcspn(linea, "\n")] = '\0'; // Eliminar el salto de línea
        strcpy(mapa[filas], linea);
        filas++;
    }
    columnas = strlen(mapa[0]);
    
    fclose(archivo);
}

void imprimir_mapa() {
    printf("\nMapa del jardín:\n");
    for (int i = 0; i < filas; i++) {
        printf("%s\n", mapa[i]);
    }
    printf("\n");
}

int contar_lados(int fila, int col, int direccion_entrada, char tipo_planta) {
    int lados_totales = 0;
    
    for (int i = 0; i < DIRECCIONES; i++) {
        int nuevo_fila = fila + direcciones[i][0];
        int nuevo_col = col + direcciones[i][1];
        
        if (direccion_entrada == 0) {
            if (nuevo_fila < 0 || nuevo_fila >= filas || nuevo_col < 0 || nuevo_col >= columnas || mapa[nuevo_fila][nuevo_col] != tipo_planta) {
                lados_totales++;
            }
        } else if (direccion_entrada == i) {
            if (nuevo_fila < 0 || nuevo_fila >= filas || nuevo_col < 0 || nuevo_col >= columnas || mapa[nuevo_fila][nuevo_col] != tipo_planta) {
                lados_totales++;
            }
        }
    }
    
    return lados_totales;
}

void dfs(int fila, int col, char tipo_planta, int direccion_entrada, int *area, int *lados_totales) {
    int stack[MAX_FILA * MAX_COL][3]; // Pila para la DFS, guardando coordenadas y dirección de entrada
    int tope = -1;
    
    stack[++tope][0] = fila;
    stack[tope][1] = col;
    stack[tope][2] = direccion_entrada;
    
    visitado[fila][col] = 1;
    *area = 0;
    *lados_totales = 0;
    
    while (tope >= 0) {
        int x = stack[tope][0];
        int y = stack[tope][1];
        int dir = stack[tope][2];
        tope--;
        
        (*area)++;
        *lados_totales += contar_lados(x, y, dir, tipo_planta);
        
        for (int i = 0; i < DIRECCIONES; i++) {
            int nuevo_fila = x + direcciones[i][0];
            int nuevo_col = y + direcciones[i][1];
            
            if (nuevo_fila >= 0 && nuevo_fila < filas && nuevo_col >= 0 && nuevo_col < columnas && !visitado[nuevo_fila][nuevo_col] && mapa[nuevo_fila][nuevo_col] == tipo_planta) {
                visitado[nuevo_fila][nuevo_col] = 1;
                stack[++tope][0] = nuevo_fila;
                stack[tope][1] = nuevo_col;
                stack[tope][2] = i; // Dirección actual como entrada
            }
        }
    }
}

int calcular_costo_total() {
    int costo_total = 0;
    
    for (int i = 0; i < filas; i++) {
        for (int j = 0; j < columnas; j++) {
            if (!visitado[i][j]) {
                char tipo_planta = mapa[i][j];
                int area = 0, lados_totales = 0;
                dfs(i, j, tipo_planta, 0, &area, &lados_totales);
                int ap = area * lados_totales;
                costo_total += ap;
                printf("Tipo de planta '%c': Área = %d, Lados = %d, Costo = %d\n", tipo_planta, area, lados_totales, ap);
            }
        }
    }
    
    return costo_total;
}

int main(int argc, char *argv[]) {
    if (argc != 2) {
        printf("Uso: %s <archivo>\n", argv[0]);
        return 1;
    }
    
    clock_t start = clock();
    
    cargar_archivo(argv[1]);
    
    imprimir_mapa();
    
    int costo_total = calcular_costo_total();
    
    printf("El costo total de cercar todas las regiones es: %d\n", costo_total);
    printf("Tiempo de ejecución: %.2f ms\n", (double)(clock() - start) * 1000 / CLOCKS_PER_SEC);
    
    return 0;
}
