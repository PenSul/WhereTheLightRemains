# M0 lantern development sources

These are the editable sources for the lantern sample in the accepted movement/camera room, **not approved finished production art**. The project-created geometry was made with OpenAI-assisted procedural Blender authoring; it is not a downloaded third-party mesh or a Tripo generation. Specific underlying model identifiers were not returned/retained.

- `WTLR_Lantern_Source-v01.blend`: Blender 5.2.2 LTS source. Select scene `WTLR_Lantern_M01` for the editable named lantern parts; preview walls, lights and cameras are reference-only. A retained factory scene is not an export selection.
- [Past FBX](../../../Exports/Dev/M01/SM_Lantern_Past-v01.fbx) and [Present FBX](../../../Exports/Dev/M01/SM_Lantern_Present-v01.fbx): one static mesh each, four material slots, 1,256 triangles / 668 vertices. No gameplay collision or lights are included.
- Dimensions: **44 × 73.5 × 111 cm**. Pivot: wall mount at source origin. Source object scale: 1. Source bracket projects along −Y; orient it to the actual side camera in Unreal without negative scaling.

FBX recipe: global scale 1, apply units, `FBX_SCALE_UNITS`, −Y forward / Z up. Verify 100 Unreal units per metre and material-slot order after import. Fresh Blender readback matched both source exports before M0; the project team also checked the in-editor room and lantern visibility during M0.

Material roles: `M01_WoodBrown`, `M01_InkIron`, `M01_Brass`, and either `M01_PaperAmber` (Past) or `M01_PaperUnlit` (Present). Recreate these roles in UE4. The Blender graph is a look reference, not a portable game shader. Keep emission separate from the actual bounded game light and from any gameplay influence region. Current Unreal sample materials remain placeholders.

The packed paper image is **Paper001 by Lennart Demes / ambientCG, CC0**, also retained at `AssetSource/ThirdParty/Materials/ambientCG-Paper001/`. Keep its original notice and [asset-credit entry](../../../../Docs/ASSET-CREDITS.csv). The source file is self-contained for its packed image; packaging a texture does not replace its attribution record.

Reimport the existing development mesh assets from these shared exports through the Editor and save their import metadata. Do not recreate or edit `.uasset` files as binary data. Runtime play must not depend on a private source path or an authoring helper.
