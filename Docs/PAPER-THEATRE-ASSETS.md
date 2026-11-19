# Paper Theatre asset sources

This selection contains 24 environment modules, 15 ordinary props, one serif font family and one paper texture. Use the current Lantern Street map to compare colour, scale and silhouette.

| Source | Included selection | License | Intended use and small adjustments |
| --- | --- | --- | --- |
| [Quaternius Medieval Village MegaKit](https://quaternius.com/packs/medievalvillagemegakit.html), free Standard edition | 24 FBXs: plaster/wood walls, openings, trims, decks, rails, stairs and a compact roof | CC0 1.0 | Reuse the shallow geometry across four areas. Retint materials to cream, navy, muted brick and wood; soften stock normal maps, relink textures and check scale/pivots. Whole fantasy buildings and ornate towers were excluded. |
| [Quaternius Fantasy Props MegaKit](https://quaternius.com/packs/fantasypropsmegakit.html), free Standard edition | 11 FBXs: crate, barrel, bench, stool, rope coil, closed book, bottle, pot, peg rack, workbench and wall shelf | CC0 1.0 | Ordinary harbour, workshop and household objects. Adjust palette/paper surface and placement; no weapons or elaborate fantasy objects were selected. |
| [Kenney Furniture Kit](https://kenney.nl/assets/furniture-kit) | 3 self-contained GLBs: single bed, table and open bookcase | CC0 1.0 | House furniture with simple silhouettes. Edit in Blender and export FBX for the project. Retint their existing material colours and check dimensions. |
| [Quaternius Medieval Village Pack](https://quaternius.com/packs/medievalvillage.html) | One original bell FBX, with a simple suspension loop | CC0 1.0 | The street investigation bell. Correct the imported material opacity and use a simple or world-coordinate brass/paper material; the source has no UVs or external textures. |
| [Libre Baskerville](https://github.com/impallari/Libre-Baskerville), pinned upstream revision `9852edf75ece3af500a5ec61245f94788c3d4633` | Regular, Bold and Italic static TrueType fonts | SIL Open Font License 1.1 | Printed notebook text. Keep evidence readable and retain live 100/125/150% text scaling. The supplied usage recipe gives a small title-size adjustment if the wordmark is rebuilt. Font binaries are unmodified. |
| [ambientCG Paper 001](https://ambientcg.com/view?id=Paper001) by Lennart Demes | Original 1K colour PNG, **1024 × 600** | CC0 1.0 | A quiet grain blended at about 0.08 into cream; use the same surface vocabulary across cards and interface artwork. It is not a square texture: use UI Clamp/NoMipmaps or intentional padding and matching UVs for world materials. |

The [model source folder](../AssetSource/ThirdParty/Models/README.md), [font folder](../AssetSource/ThirdParty/Fonts/LibreBaskerville/USAGE.md), and [paper material folder](../AssetSource/ThirdParty/Materials/ambientCG-Paper001/USAGE.md) contain editable originals and import notes. Every pack's `SOURCE.json` records original URLs, file hashes, roles and permitted adjustments. License notices or documented creator grants remain beside the sources; [ASSET-CREDITS.csv](ASSET-CREDITS.csv) contains the shared attribution register. ambientCG's [official license declaration](https://docs.ambientcg.com/license/) permits raw files in a game project; its notice and full CC0 text are retained with the texture.

The approximate 80% suitability threshold is a visual selection judgment, not a numeric quality measurement. These files already provide the needed shapes; the remaining work is mostly materials, scale, pivots and texture relinking. Check the adjusted result in the game’s side camera. A source download does not establish that its imported material, collision or animation is production-ready.

## Import and teamwork

Keep third-party originals unchanged under `AssetSource/ThirdParty`. Save working `.blend` files in `AssetSource/Models` and clean exports in `AssetSource/Exports`. Use ASCII names and project prefixes for new Unreal assets, then import through the Content Browser into `Content/WTLR/Art`. Build simple collision separately, preserve walkable silhouettes and check 1 metre = 100 Unreal units. Shader nodes need corresponding Unreal materials or baked textures.

The editable notebook textures, UI artwork and Echo symbols are under `AssetSource/UI/`. Menu labels and other live text are assembled in the UMG widget.

Acquire LFS locks and coordinate ownership before editing shared source files. Include the creator license notices and font OFL when distributing source packages or a game build. CC0 attribution is recorded for provenance even though the license does not require credit; the OFL copyright and license notices must be retained.
