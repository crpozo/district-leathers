# District Leathers · Fitting Room & Hide Calculator

Contexto para Claude Code. Lee esto antes de tocar nada.

## Qué es
Herramienta que vive dentro de la tienda Shopify de District Leathers (districtleathers.com, proveedor de cuero en el Garment District, NY). El cliente elige un cuero real en stock, describe lo que quiere hacer (prenda, bolso, mueble, asiento de auto), la IA genera la imagen del producto en ese cuero, y de ahí sigue a: molde base más parecido → cuántas pieles por talla → mismo lote → carrito. Lo técnico del cuero (caída, grosor, costuras, mapa de corte) es el diferenciador; ninguna tienda de cuero lo muestra.

Brief original: `docs/Brief_Desarrollador_District.pdf` (Martín Flores, oct 2026, v3). Es confidencial (NDA) y está ignorado por git: el repo es público, el PDF se guarda solo en local. El código, repo y cuentas van a nombre de la empresa de Martín; la IP es de esa empresa.

## Estado actual (oct 2026)
- `demo/index.html`: prototipo navegable de una sola página, datos fijos, sin Shopify. Es lo que se enseña a los dueños (Alex y Stephen). Todo embebido (fuentes de Google, fotos en base64). Se construye con `python3 build.py` desde `src/demo.html` + `src/img/` (no editar `demo/index.html` a mano).
- Publicado con GitHub Pages desde `main` (root). URL: `https://crpozo.github.io/district-leathers/demo/`. `index.html` en la raíz redirige a `/demo/`.
- Pantallas de la demo (numeración del brief): 0 página de producto · fitting room (1, 2, 10, 11 en un flujo de 3 pasos) · 3 calculadora · 8 comparar caída y ficha técnica · 9 mapa de corte (pantalón mujer M, lamb vs cow) · 5 proyecto a medida (cierre del flujo Corvette) · "More": 4 cuenta, 6 panel, 7 seguimiento como mockups estáticos. Sin barra de navegación: la demo abre en el fitting room y el resto se llega desde los botones del flujo (o por hash: `#product`, `#calc`, `#compare`, `#cutmap`, `#project`, `#more`).
- Ejemplos obligatorios cubiertos: bomber jacket (Nappa Lamb) y Corvette 1967 (dos asientos delanteros en cognac, Semi-Aniline Cow, termina en el formulario de proyecto con estimado de 2 pieles enteras).
- Fase 1 (producción en su Shopify) no ha empezado. Falta cotización aprobada.

## Flujo del fitting room (dentro de la demo)
1. **Pick a leather**: cinco tarjetas estilo "Best sellers" de su web (foto real del cuero teñida por color, nombre, tagline, precio, estrellas, muestras redondas con foto). Tocar un color tiñe la foto y muestra "Continue with [color]".
2. **Describe your idea**: textarea + "Or pick a District base pattern" (Jacket, Pants, Chair/Sofa, Car seat) + ejemplos rápidos (bomber, wide-leg pants, two-seat sofa, 1967 Corvette). Aviso en vivo con el molde base detectado. Talla (Women/Men, XS–XXL) y merma (20/25/30%). Se ocultan para tapicería. **Subir archivo** (punto 7 de las correcciones del 14 oct): tres tipos. Foto de una pieza: funciona en la demo con una foto de ejemplo embebida (bomber de algodón beige sobre modelo, `src/img/sample_jacket.jpg`) o una foto del iPad; el paso 3 muestra "Your photo" junto al resultado (bomber en el cuero elegido; con key de IA, edita la foto real con la foto del cuero como referencia). Boceto y molde (DXF/PDF) llevan etiqueta "Final version" y solo explican qué harán. Después de la imagen sigue igual: pieles, lote, carrito.
3. **See it & buy**: imagen grande (prenda sobre modelo, frente/espalda para el pantalón) + panel "How many hides?" (rango, recomendado, mismo lote, descuento por volumen, envío gratis $250, aviso de pieza larga, nudge de piel extra, carrito). Debajo: "Change the leather", "Suggested palettes", "Compare 2 leathers", y para el pantalón "Drape & spec sheet" (pantalla 8). Para tapicería: estimado desde tabla + "Send to a District expert" (pantalla 5).

## Decisiones de diseño
- Replicar el estilo de districtleathers.com, no inventar: barra amarilla neón `#e9f33b` texto oscuro peso normal; cabecera `#333638` de 90px con monograma LD (L y D superpuestas), menú mayúsculas peso 500; fuente Raleway; títulos de producto mayúsculas peso 500; botones negros con texto blanco letterspaced; estrellas amarillas `#f2c21b`; muestras redondas con aro gris, negro la seleccionada.
- Sin burbuja de chat ni etiquetas "New" en la demo.
- UI en inglés (vive en su web). Conversación con Carlos en español.
- Imágenes: todas son fotos generadas con IA (Figma `generate_image`, modelo gemini-3.1-flash-image), nunca siluetas SVG. Carlos quiere siempre este nivel: foto de producto o prenda sobre modelo, fondo blanco. Hay dos tipos: planas (bomber, pantalón fluido, pantalón estructurado, asientos Corvette, sofá) recortadas del fondo y en escala de grises con alfa; y sobre modelo (bomber, pantalón frente y espalda) generadas en gris neutro con una máscara solo de la prenda. El color del cuero se aplica en el navegador con canvas (`PH.render` en `src/demo.html`): cada píxel de la prenda toma el color objetivo escalado por su luminancia relativa a la media de la prenda, así se conservan sombras y brillos en negro, navy u off white. La foto del cuero (muestras y tarjetas) sí usa CSS `mix-blend-mode: multiply`. El recorte y las máscaras se generan con `src/process_images.py` (PIL: distancia al blanco para las planas; baja saturación + flood fill + recorte arriba/abajo para las de modelo).
- Resolución: las fotos están a resolución completa (1024 px planas, 896×1200 sobre modelo) en `src/img/fullres/`. El entorno de Claude bloquea www.figma.com, así que se bajaron con el workflow `.github/workflows/fetch-figma-assets.yml` (corre en un runner de GitHub y hace commit). Para nuevas imágenes: generar con Figma, añadir la URL a `src/img/figma-fullres-urls.txt`, disparar el workflow, `git pull`, `python3 src/process_images.py`, `python3 build.py`.
- IA en vivo: la demo puede generar en vivo si se guarda una API key en el dispositivo (5 toques en el logo LD o `#setup`): Gemini (`gemini-2.5-flash-image`, con la foto del cuero teñida como referencia) u OpenAI (`gpt-image-1` edits). Si no hay key, no hay internet, falla o tarda más de 75 s, cae a las imágenes pregeneradas sin que se note (misma animación de "Generating"). La key vive en localStorage del iPad, nunca en el repo. No está probado con una key real: probar antes de la demo con "Test now".
- Cálculo: `sq ft = área de la prenda (tabla) × (1 + merma)`; `pieles = sq ft ÷ tamaño de piel`. Mínimo = con la piel promedio; recomendado = con la piel chica del rango (6–9 sq ft en lamb); ambos hacia arriba. Así chaqueta M = 4–5 (rec. 5) y pantalón M = 4–5 (rec. 5), como en el brief. Cow: combinación más barata que alcance (entera o medias). Tapicería: 1 yarda = 18 sq ft o tabla por mueble/auto. Las áreas por prenda en la demo son estimadas; las reales las dan Martín y Dan.
- Cueros en la demo (5): Italian Nappa Lamb $64.99, 0.8 mm, 6–9 sq ft, 122 reseñas; Bambino Cow Lightweight $499.99, 1.2 mm, 32–40 sq ft; New England Thin Garment Weight Cow $529.99, 0.5 mm, 34–44 sq ft (datos reales de su web, del brief); Kid Skin Goat ($54.99) y Bambino Semi-Aniline Cow ($449.99, tapicería/auto) son nombres reales de su catálogo con precio, tamaño y caída de ejemplo, a confirmar. Lotes, stock, reseñas de goat/cow, paletas, pieza más larga y áreas por prenda son ejemplo. districtleathers.com no es accesible desde el entorno de Claude (DNS bloqueado), por eso no se pudieron verificar.

## Arquitectura decidida para Fase 1
- NO es una web nueva ni rediseño. Se extiende su tema actual.
- UI: modificar el tema de Shopify (duplicar el tema, trabajar en la copia; secciones Liquid + JS). Bloque de app en la página de producto debajo de "Buy more, save more!"; galería "Made with this leather"; pantallas de la herramienta.
- Puente al backend: **custom app** (privada, una sola tienda, sin revisión del App Store) con app proxy `/apps/fitting-room`, para firmar llamadas y saber qué cliente es. No app pública.
- Backend: AWS serverless (API, cálculo, generación de imágenes con referencia de imagen, proyectos guardados, panel, administración). DB para cueros, colores, lotes, stock, tablas de consumo, pieza más larga, mapas de corte, paletas.
- Integraciones: Shopify (productos, variantes, stock, cuentas de cliente, tags/metafields "I am a…", lote como propiedad de línea en carrito), su app de descuentos (leer niveles), Shopify Inbox (chat prellenado), Loox (reseñas con foto y galería por producto; construir solo lo que Loox no cubra), email de seguimiento post-compra.
- IA: servicio de generación de imágenes existente, prompt fijo ("product made of [cuero], studio photo, plain background"), foto del cuero como referencia, filtro de logos, límite diario por usuario. Imágenes privadas del diseñador.
- Parser de moldes DXF (CLO3D/Gerber/Optitex) y PDF: parte técnica más incierta; aislar como módulo.
- Fase 1 debe quedar lista para conectar la Fase 2 (creador por partes, foto de moldes de papel, 3D, AR, probador sobre el cuerpo) sin rehacer nada.

## Dependencias de District / Martín (condición de inicio de Fase 1)
Tabla de consumo (prenda × mujer/hombre × XS–XXL), tabla de tapicería, pieza más larga por talla, mapas de corte (Dan), caída 1–5 y estiramiento por cuero, fotos de cueros, niveles de descuento, acceso de colaborador a la tienda, tienda de desarrollo, Shopify Partner de la empresa de Martín, NDA firmado.

## Pendientes inmediatos
- Probar en el iPad real (Safari): el recorrido se probó en Chromium a 1024×768 y 768×1024 sin errores de consola.
- Probar la IA en vivo con una key real (Gemini u OpenAI) y medir el tiempo; decidir si se usa en la demo o solo las pregeneradas.
- Confirmar con Martín precios y datos de Kid Skin Goat y Semi-Aniline Cow.
- Cotización: precio cerrado de demo y de Fase 1, fecha más corta para cada una.

## Convenciones
- Commits directos a `main`; Pages publica solo. Sin PRs.
- Mantener `demo/index.html` autocontenido (un archivo, assets embebidos) hasta que empiece la Fase 1. Editar `src/demo.html` y correr `python3 build.py`.
- No usar em dashes en textos que vea el cliente.
