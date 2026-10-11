# District Leathers · Fitting Room & Hide Calculator

Contexto para Claude Code. Lee esto antes de tocar nada.

## Qué es
Herramienta que vive dentro de la tienda Shopify de District Leathers (districtleathers.com, proveedor de cuero en el Garment District, NY). El cliente elige un cuero real en stock, describe lo que quiere hacer (prenda, bolso, mueble, asiento de auto), la IA genera la imagen del producto en ese cuero, y de ahí sigue a: molde base más parecido → cuántas pieles por talla → mismo lote → carrito. Lo técnico del cuero (caída, grosor, costuras, mapa de corte) es el diferenciador; ninguna tienda de cuero lo muestra.

Brief original: `docs/Brief_Desarrollador_District.pdf` (Martín Flores, oct 2026, v3). Es confidencial (NDA) y está ignorado por git: el repo es público, el PDF se guarda solo en local. El código, repo y cuentas van a nombre de la empresa de Martín; la IP es de esa empresa.

## Estado actual (oct 2026)
- `demo/index.html`: prototipo navegable de una sola página, 3 pasos, datos fijos, sin Shopify. Es lo que se enseña a los dueños (Alex y Stephen). Todo embebido (fuentes de Google, fotos en base64).
- Publicado con GitHub Pages desde `main` (root). URL: `https://crpozo.github.io/district-leathers/demo/`. `index.html` en la raíz redirige a `/demo/`.
- Fase 1 (producción en su Shopify) no ha empezado. Falta cotización aprobada.

## Flujo de la demo
1. **Pick a leather**: tres tarjetas estilo "Best sellers" de su web (foto real del cuero teñida por color, nombre, tagline, precio, estrellas, muestras redondas). Tocar un color tiñe la foto y muestra "Continue with [color]" abajo a la derecha.
2. **Describe your idea**: textarea + grilla "Or pick a District base pattern" (Jacket, Pants, Skirt, Bag, Chair/Sofa, Car seat) + ejemplos rápidos (bomber, wide-leg pants, two-seat sofa, 1967 Corvette seats). Aviso en vivo con el molde base detectado. Talla (Women/Men, XS–XXL) y merma (20/25/30%). Se ocultan para tapicería.
3. **See it & buy**: imagen grande + panel "How many hides?" (rango, recomendado, mismo lote, descuento por volumen, envío gratis $250, nudge de piel extra, carrito). Debajo: "Change the leather" (muestras de todos los cueros en stock, regenera al tocar) y "Suggested palettes" (Classic, Coastal, Fall 26 → dos cueros lado a lado). Para tapicería: estimado desde tabla + formulario corto "Send to a District expert".

## Decisiones de diseño
- Replicar el estilo de districtleathers.com, no inventar: barra amarilla neón `#e9f33b` texto oscuro peso normal; cabecera `#333638` de 90px con monograma LD (L y D superpuestas), menú mayúsculas peso 500; fuente Raleway; títulos de producto mayúsculas peso 500; botones negros con texto blanco letterspaced; estrellas amarillas `#f2c21b`; muestras redondas con aro gris, negro la seleccionada.
- Sin burbuja de chat ni etiquetas "New" en la demo.
- UI en inglés (vive en su web). Conversación con Carlos en español.
- Imágenes: la chaqueta es una foto real recortada del fondo, en escala de grises y teñida con el color del cuero (CSS `mix-blend-mode: multiply` con máscara). El resto de prendas aún son SVG; reemplazar por fotos reales cuando Carlos las mande (pantalón, falda, bolso, sofá, asiento). Generación de IA en vivo NO es posible en una página estática publicada; para la demo se usan imágenes pregeneradas. Figma `generate_image` dio buena calidad (prueba: bomber cognac) pero el entorno de Claude.ai no puede descargar de figma.com.
- Cálculo: `sq ft = área de la prenda (tabla) × (1 + merma)`; `pieles = sq ft ÷ tamaño promedio de piel`. Mínimo = merma 5 puntos menos; ambos redondeados hacia arriba. Cow: combinación más barata que alcance (entera o medias). Tapicería: 1 yarda = 18 sq ft o tabla por mueble/auto. Las áreas por prenda en la demo son estimadas; las reales las dan Martín y Dan.
- Datos reales de su web usados en la demo: Italian Nappa Lamb $64.99, 0.8 mm, 6–10 sq ft, 122 reseñas; Bambino Cow Lightweight $499.99, 1.2 mm, 32–40 sq ft; New England Thin Cow $529.99, 0.5 mm, 34–44 sq ft. Lotes, stock, paletas y "Upholstery Cow" son ejemplo.

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
- Fotos reales de pantalón, falda, bolso, sofá y asiento para reemplazar los SVG.
- Imágenes IA pregeneradas (3–4 ideas de respaldo por si falla internet en la demo).
- Probar en iPad (es donde la van a enseñar).
- Cotización: precio cerrado de demo y de Fase 1, fecha más corta para cada una.

## Convenciones
- Commits directos a `main`; Pages publica solo. Sin PRs.
- Mantener `demo/index.html` autocontenido (un archivo, assets embebidos) hasta que empiece la Fase 1.
- No usar em dashes en textos que vea el cliente.
