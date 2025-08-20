from task_generator import generar_tarea_desde_plantilla
from scrapper import ejecutar_tarea
import sys
#sadasdads
if __name__ == "__main__":
    if len(sys.argv) == 4 and sys.argv[1] == "--plantilla":
        nombre_plantilla = sys.argv[2]
        query = sys.argv[3]
        ruta_tarea = f"tasks/{nombre_plantilla}_{query}.json"
        generar_tarea_desde_plantilla(nombre_plantilla, query, ruta_tarea)
        ejecutar_tarea(ruta_tarea, "output/resultados.json")

    elif len(sys.argv) == 2:
        tarea_path = sys.argv[1]
        ejecutar_tarea(tarea_path, "output/resultados.json")
    else:
        print("Uso:")
        print("  python main.py tasks/mi_tarea.json")
        print("  python main.py --plantilla primor perfume")
