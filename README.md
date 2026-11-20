# Antonio Hernández Pinto · Perfil profesional QA Automation / SDET

Sitio web estático bilingüe (español e inglés) preparado para GitHub Pages con dominio propio **antoniohernandezpinto.com**.

**Versión revisada: 20 de noviembre de 2026 (v5)**

## Qué se ha corregido

- Se identifica **Telefónica Tech** como único empleador desde abril de 2019 hasta la actualidad.
- Se muestran dos etapas bajo ese mismo empleador: **QA Automation / SDET (abril 2019–septiembre 2026)** y **proyecto Thanos para BBVA (octubre 2026–actualidad)**, con trabajo en playbooks de Google SecOps. Thanos/BBVA figura como proyecto, no como nueva empresa.
- Se rediseñaron con tipografía más legible y distribución optimizada los **cuatro PDF** (completo de dos páginas y ejecutivo de una, ambos en español e inglés) con la misma cronología, enlaces públicos y formación que la web.
- Se actualizó asimismo el PDF de **compatibilidad** `assets/cv/Antonio_Hernandez_Pinto_RESUME_linkedIn_version.pdf`, para que un enlace antiguo no siga mostrando datos anteriores.
- Formación: **Maestro en Educación Primaria (Diplomatura)**, 1998–2001, Centro Fray Luis de León; **Técnico Superior en Desarrollo de Aplicaciones Informáticas**, 2001–2003, Centro Gregorio Fernández, ambos en Valladolid.
- Contacto público único: **antoniohernandezpinto.com** y **LinkedIn** (`https://www.linkedin.com/in/antonio-hernandez-pinto/`). Se han eliminado los correos personales de la web, del código fuente y de los PDF, incluidos enlaces `mailto:`.
- SEO: descripciones para compartir en redes, alternancia de idiomas y fecha del sitemap revisadas; se conserva el dominio canónico.
- La sección Experiencia muestra las **dos etapas bajo una misma entrada** con un diseño compatible con móviles y tema oscuro/claro.

No se han añadido métricas, responsabilidades ni certificaciones no documentadas. Comprueba que puedes hacer públicos los detalles de clientes/proyectos antes de publicarlos.

## Publicar en GitHub Pages

1. **Descomprime el ZIP**. Sube el contenido de la carpeta a la **raíz** de la rama `main` del repositorio `antoniohernandezpinto/professional-profile`, reemplazando los archivos antiguos.
2. Conserva la estructura de carpetas (`en/`, `assets/cv/`, `assets/img/`, `assets/site.js`) y `CNAME` en la raíz.
3. Puedes hacerlo con `git` desde una copia local del repositorio:

   ```bash
   git add -A
   git commit -m "Polish responsive website and bilingual CV layouts - Nov 2026"
   git push origin main
   ```

4. Tras publicar, comprueba en modo incógnito las páginas `https://antoniohernandezpinto.com/` y `https://antoniohernandezpinto.com/en/` y los **cuatro** enlaces de descarga PDF.
5. Comprueba el antiguo enlace `https://antoniohernandezpinto.com/assets/cv/Antonio_Hernandez_Pinto_RESUME_linkedIn_version.pdf`; deberá mostrar la versión actualizada.
6. En caso de caché, vuelve a cargar forzando actualización. Mantén `CNAME` con `antoniohernandezpinto.com`.

**Importante:** este ZIP **no está publicado automáticamente** en GitHub. La subida al repositorio es un paso pendiente.

## Archivos principales

- `index.html`: español.
- `en/index.html`: inglés.
- `style.css`: diseño responsive, tema oscuro/claro.
- `assets/site.js`: menú móvil y alternancia de tema.
- `assets/img/`: fotografía y miniatura social.
- `assets/cv/`: cinco PDF (cuatro versiones + ruta de compatibilidad).
- `tools/build_cvs.py`: script fuente para regenerar los cuatro CV con información compartida.
- `tools/check_site.py`: verificación estática de enlaces, cronología, PDF y metadatos.
- `robots.txt`, `sitemap.xml`, `CNAME`: configuración de rastreo/dominio.

## Mantenimiento de los CV

Los cuatro PDF se generan desde `tools/build_cvs.py`, que guarda un modelo bilingüe común. Se necesita Python, `reportlab`, Pillow y la familia de tipografías Lato **instalada en el sistema**. El archivo ZIP no incluye fuentes de terceros. Edita el modelo de contenido en ese script para que los PDF no diverjan entre sí.

Tras cambios:

```bash
python tools/build_cvs.py
python tools/check_site.py
```

Antes de publicar cambios futuros, verifica manualmente que las fechas, roles, estudios y denominaciones de certificaciones sean correctas y autorizadas.

## Avisos

- La presentación profesional se centra en **QA Automation / SDET**. Google SecOps se presenta como especialización de proyecto.
- El sitio y los CV no publican ninguna dirección de correo ni enlaces `mailto:`. Los únicos enlaces de contacto públicos son la web y LinkedIn.
- El sitio no incluye analítica ni cookies de seguimiento.
- Validación realizada localmente: comprobación de ausencia de direcciones de correo en HTML, documentación y PDFs (texto y enlaces), y de enlaces de contacto únicamente al dominio personal y LinkedIn; archivos/anchors, contenido de PDF, tamaño de los CV y metadatos. Revisión visual realizada localmente en escritorio y móvil; comprueba también el sitio público después de desplegar.

© 2026 Antonio Hernández Pinto.
