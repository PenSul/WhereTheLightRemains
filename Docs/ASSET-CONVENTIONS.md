# Asset conventions

## Unreal project layout

Author UE5.8.4 assets in `/Game/WTLR`. The playable map is `Maps/L_LanternStreet`. Shared session, save and mode Blueprints live in `Core`, the character and controller in `Player`, and the menu and Journal widget in `UI`. Lantern Street scenery is under `Art/LanternStreet`. The gameplay plane is X/Z, Y is depth and walking right follows positive X.

Match the existing Unreal prefixes, including `L_` for maps, `BP_` for gameplay Blueprints, `WBP_` for widgets, `SM_` for static meshes, `M_` for materials, `T_` for textures and `SW_` for sound waves. Keep package names descriptive and free of spaces. Use the Content Browser to move Unreal assets, fix redirectors and check references. Keep station IDs, phase tags and saved progression fields stable when editing scene art.

## Models and textures

Preserve editable originals and importable exports under `AssetSource/`. Elias's Blender source, part-pivot manifest and joint-centred FBX files are together under `Models/Characters/Elias/`. The Lantern Street set uses layered glTF meshes and a paper texture atlas under `Models/LanternStreet/`. Place third-party originals and their licence files in `ThirdParty/`. The current Lantern Street map shows the intended silhouette, colour palette and composition.

Use real-world scale. One metre should import as 100 Unreal centimetres. Test a representative part before a batch. In the editor, check dimensions, Z-up orientation, facing, material slots and the pivot with the matching adjacent piece. Check articulated limbs at the elbow, knee and shoulder in both movement directions. Keep the camera, capsule and visual facing independent.

Review assets from the side camera in both phases. Give paper cut-outs thickness where an edge can become visible, and maintain enough contrast around clues, hands and feet. Separate walkable geometry from decoration. After a scenery edit, check that restored routes and phase changes preserve the original collision and that recall cannot remove Elias's support.

## Credit and version control

Record third-party and AI-assisted assets in the course register. Include the source path or URL, creator or provider, licence, required attribution and changes. Keep the original licence notices with redistributed files. Credit Aideen when reproducing her mechanics and level drawings. [Asset register](ASSET-CREDITS.csv) · [AI-assisted asset references](AI-ASSET-REFERENCES.md)

Keep `.uasset`, `.umap`, source models and other large binary assets under the project's Git LFS rules when sharing through Git. Coordinate edits to the same map or Blueprint with the team. [Project setup and controls](../README.md)
