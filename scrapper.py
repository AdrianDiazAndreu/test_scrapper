from playwright.sync_api import sync_playwright
import json
#sadasdads
def ejecutar_tarea(tarea_path: str, salida_path: str, tienda: str):
    with open(tarea_path, 'r', encoding='utf-8') as f:
        config = json.load(f)

    url = config['url']
    selectors = config['selectors']
    pagination = config.get('pagination', None)
    max_pages = pagination.get('max_pages', 1) if pagination else 1

    resultados = {s['name']: [] for s in selectors}

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)  # Cambia a False si deseas ver el navegador
        context = browser.new_context(user_agent="Mozilla/5.0 (X11; Linux x86_64)")
        page = context.new_page()
        page.goto(url, timeout=60000)

        # Esperar a que cargue completamente
        page.wait_for_load_state("networkidle")

        # Cerrar el modal de cookies si aparece
        try:
            if page.locator("button.ambar-btn-decline").is_visible():
                print("🍪 Modal de cookies detectado. Cerrando...")
                page.locator("button.ambar-btn-decline").click()
                page.wait_for_timeout(30000)
        except Exception as e:
            print(f"⚠️ No se pudo cerrar el modal de cookies: {e}")
        # Cerrar el modal de cookies si aparece

        current_page = 1
        while True:
            print(f"\n📄 Página {current_page}: {page.url}")
            page.wait_for_load_state("networkidle")

            # Scroll para cargar contenido dinámico (lazy load)
            page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
            page.wait_for_timeout(1000)

            for sel in selectors:
                name = sel['name']
                selector = sel['selector']
                datos = []

                try:
                    page.wait_for_selector(selector, timeout=10000)
                    elementos = page.locator(selector).all()

                    if 'attribute' in sel:
                        for e in elementos:
                            attr = e.get_attribute(sel['attribute'])
                            if attr:
                                datos.append(attr)
                            else:
                                datos.append(None)
                    else:
                        datos = [e.inner_text() for e in elementos]

                    resultados[name].extend(datos)
                    print(f"✅ {name}: {len(datos)} elementos extraídos.")

                except Exception as e:
                    print(f"❌ Error extrayendo '{name}': {e}")

            # Paginación
            # if pagination and current_page < max_pages:
            #     next_selector = pagination['selector']
            #     next_button = page.locator(next_selector)
            #     if next_button.count() > 0 and next_button.first.is_enabled():
            #         print("➡️ Haciendo clic en 'Siguiente'")
            #         next_button.first.click()
            #         page.wait_for_load_state("networkidle")
            #         current_page += 1
            #     else:
            #         print("🚫 No hay más páginas o botón no encontrado.")
            #         break
            # else:
            #     break

            browser.close()

    with open(salida_path, 'w', encoding='utf-8') as f:
        json.dump(resultados, f, ensure_ascii=False, indent=2)

    print(f"\n✅ Tarea completada. Resultados guardados en '{salida_path}'")

