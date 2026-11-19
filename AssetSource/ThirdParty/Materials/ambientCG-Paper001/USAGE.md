# Paper001 grain for Paper Theatre

Use the original Paper001_1K-PNG_Color.png for notebook pages, trace slips, cream card panels, and small paper signs. Its near-white, even fibers match the calm Paper Theatre references. The image has no writing, strong stains, folds or baked hard shadows.

The source is 1024 x 600 RGB PNG despite the 1K pack label. Its bytes match the archive member exactly. Keep the image unchanged. Use Cream #F4E7CC, GrainAmount 0.08, and BaseColor = Cream * lerp(1, PaperColor.rgb, GrainAmount), with sRGB enabled. Keep Metallic 0 and Roughness 1. No normal or displacement map is needed for this shared shallow-card use.

For a fixed UI card, import into the UI texture group with NoMipmaps and Clamp addressing. For a world card that needs mips, use Unreal's Pad to Power of Two setting and padding color #F4F3F2, producing a 1024 x 1024 backing texture during import. Sample only the original 600-row region: source-content UV scale is (1, 0.5859375). Check the import preview and card at normal camera distance before assigning it broadly. These import settings are a documented recipe; they were not applied to a live engine project.

Only the Color member is accepted. The original full ZIP remains in the local downloads folder. The ZIP contains no license file. CC0-1.0.txt and LICENSE-SOURCE.html preserve the official CC0 legal text and ambientCG licensing declaration supplied separately, with hashes in SOURCE.json. CC0 allows commercial use, modification and sharing the raw files with the team. Attribution is optional; the creator credit is recorded in CREDIT-ROW.json.

Creator: Lennart Demes / ambientCG. Asset: https://ambientcg.com/view?id=Paper001
License declaration: https://docs.ambientcg.com/license/
Texture import reference: https://dev.epicgames.com/documentation/en-us/unreal-engine/texture-properties?application_version=4.27
