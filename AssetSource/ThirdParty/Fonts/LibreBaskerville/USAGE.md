# Libre Baskerville for Paper Theatre

Use the original static Regular, Bold and Italic TTF files in this folder. They have TrueType glyph outlines, no variable-font tables, and unrestricted embedding bits. All originals and licensing documents match their upstream Git blob SHA-1; SOURCE.json records the pinned commit and SHA-256 hashes.

Regular supplies evidence body and quiet menu labels; Bold supplies notebook headings; Italic supplies short recollection quotations. Keep ink at #2B404D and evidence body at the reference 17 px, including the existing 100/125/150 percent text settings. The family is Latin; CJK localization needs a compatible fallback.

If the two-line wordmark is regenerated with this family, use Regular at 54 px with 1.1 px tracking for "Where the" and 78 px with -1.15 px tracking for "Light Remains". Keep the 800 x 280 canvas and existing line positions. Measured advances are 301.8 and 571.2 px, within 1 percent of the Georgia reference. No font outlines need editing.

In Unreal Engine 4.27, import the TTFs as Font Face assets and give one Composite Font explicit Regular, Bold and Italic faces. Assign Italic explicitly: its internal family name is "Libre Baskerville Italic". The source/rasterizer checks do not substitute for a later Unreal import/packaging check.

The SIL OFL permits commercial use, game embedding, modification and team redistribution. Keep OFL.txt and the copyright notice with redistributed fonts and game license notices. Font software stays under OFL; the game may use another license. A modified font derivative must use a new name because "Libre Baskerville" is reserved. Keep FONTLOG.txt with the font sources. Do not sell the font on its own. OFL.txt preserves its upstream Latin-1 text encoding and original line endings.

Creators: Pablo Impallari, Rodrigo Fuenzalida and Libre Baskerville Project contributors. Official source: https://github.com/impallari/Libre-Baskerville
