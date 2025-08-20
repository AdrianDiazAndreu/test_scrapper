import json
import os
#sadasdads
def generar_tarea_desde_plantilla(nombre_plantilla, valor_busqueda, ruta_salida):
    ruta_plantilla = f"templates/{nombre_plantilla}.json"

    if not os.path.exists(ruta_plantilla):
        print(f"❌ Plantilla '{nombre_plantilla}' no encontrada.")
        return

    with open(ruta_plantilla, 'r', encoding='utf-8') as f:
        plantilla = json.load(f)

    url = plantilla["url_pattern"].replace("{query}", valor_busqueda)
    tarea = {
        "url": url,
        "selectors": plantilla["selectors"],
        "pagination": plantilla.get("pagination", None)
    }

    with open(ruta_salida, 'w', encoding='utf-8') as f:
        json.dump(tarea, f, indent=2, ensure_ascii=False)

    print(f"✅ Tarea generada con éxito en: {ruta_salida}")
