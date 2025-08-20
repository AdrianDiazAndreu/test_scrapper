from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from scrapper import ejecutar_tarea
import os, json, uuid
#sadasdads
app = FastAPI()
# Permitir peticiones desde WordPress
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.get("/scrape")

def scrape(query: str, tienda: str = "primor"):
    tarea_id = str(uuid.uuid4())
    os.makedirs("temp", exist_ok=True)

    # Configuración según tienda
    if tienda == "primor":
        url_query = f"https://www.primor.eu/catalogsearch/result/?q={query}"
        tarea_json = {
            "url": url_query,
            "selectors": [
                {"name": "producto", "selector": ".product-item-link"},
                {"name": "link", "selector": "a.product-item-photo", "attribute": "href"}
            ],
            "pagination": {"selector": ".pages-item-next a", "max_pages": 1}
        }

    elif tienda == "druni":
        url_query = f"https://www.druni.es/#8f52/fullscreen/m=and&p=2&q={query}"
        tarea_json = {
            "url": url_query,
            "selectors": [
                {"name": "producto", "selector": ".dfd-card-title"},
                {"name": "precio", "selector": ".dfd-card-price"},
                {"name": "link", "selector": ".dfd-card", "attribute": "dfd-value-link"},
                {"name": "imagen", "selector": ".dfd-card-thumbnail img", "attribute": "src"}
            ],
            "pagination": {"selector": ".next", "max_pages": 1}
        }

    elif tienda == "maquillalia":
        url_query = f"https://www.maquillalia.com/#23cd/embedded/m=and&q={query}"
        tarea_json = {
            "url": url_query,
            "selectors": [
                { "name": "producto", "selector": ".dfd-card-title" },
                { "name": "precio", "selector": ".dfd-card-price" },
                { "name": "link", "selector": ".dfd-card", "attribute": "dfd-value-link" },
                { "name": "imagen", "selector": ".dfd-card-thumbnail img", "attribute": "src" }
            ],
            "pagination": {
                "selector": ".next",
                "max_pages": 1
            }
        }
    elif tienda == "sephora":
        url_query = f"https://www.sephora.es/buscar/?q={query}"
        tarea_json = {
            "url": url_query,
            "selectors":[
                { "name": "producto", "selector": ".product-tile-link",  "attribute": "title"  },
                { "name": "precio", "selector": ".dfd-card-price" },
                { "name": "link", "selector": ".product-tile-link", "attribute": "href" },
                { "name": "imagen", "selector": ".dfd-card-thumbnail img", "attribute": "src" }
            ]
        }

    else:
        return {"error": f"Tienda '{tienda}' no soportada"}

    # Guardar tarea
    tarea_path = f"temp/tarea_{tarea_id}.json"
    salida_path = f"temp/resultados_{tarea_id}.json"
    with open(tarea_path, "w", encoding="utf-8") as f:
        json.dump(tarea_json, f)

    ejecutar_tarea(tarea_path, salida_path, tienda)

    with open(salida_path, "r", encoding="utf-8") as f:
        resultados = json.load(f)

    print(f"\n🟢 Consulta: {query} | Tienda: {tienda}")
    print("📦 Resultados:")
    print(json.dumps(resultados, indent=2, ensure_ascii=False))

    return {"resultados": resultados}

