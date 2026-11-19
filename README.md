# Where the Light Remains

A quiet, side-view 3D puzzle game. Elias, an elderly widower, returns to a harbour neighbourhood and pieces together how Mara helped her neighbours during an evacuation. The playable project covers Lantern Street and the systems shared by later areas. Aideen's revised design gives Elias one remembered Echo and one manifestation. A candle can light a letter and burn dry grass.

## Open and play

1. Use **Unreal Engine 5.8.4** on Windows. Open `WhereTheLightRemains.uproject` in this folder. Allow shaders to compile on the first launch.
2. The configured startup map is `/Game/WTLR/Maps/L_LanternStreet`. To open it manually, use the Content Browser under **Content → WTLR → Maps → L_LanternStreet**.
3. Choose **Play → New Editor Window (PIE)**. At the lantern overlooking the quay, press any button to open the notebook. Select **New journey**. On the chapter page, leave **Skip opening** unchecked to see why Elias returned home, or check it to begin in the kitchen. Press **Escape** to skip during the cinematic.
4. To resume, choose **Continue → Load journey**. The book shows your last checkpoint and the number of observations collected. During play, **Escape → Save book → Save progress** records your journey at its last safe checkpoint when Elias is in the Present and off his Echo.

| Action | Default key |
| --- | --- |
| Walk | A / D or left / right arrow |
| Jump | Space |
| Inspect an object or read a clue | E |
| Switch between Past and Present | Q |
| Remember or place an Echo | F |
| Recall the placed Echo | R |
| Open or close the Journal | J |
| Pause or go back | Escape |

**For an editor test**, use the same startup map and Play mode. To exercise the first puzzle, find the candle in the Past, confirm the memory, return to the Present and use it to read the door letter. After opening the door, recall the candle and use its heat at the grass. Keep a separate working copy when testing a fresh journey so your regular playthrough can be resumed.

## Development checkout

Install Unreal Engine 5.8.4, Git and Git LFS on Windows. Open PowerShell in the folder where you keep your projects and run

```powershell
git lfs install
git clone -c core.longpaths=true https://github.com/PenSul/WhereTheLightRemains.git
cd WhereTheLightRemains
git lfs pull
git lfs fsck
```

Open `WhereTheLightRemains.uproject`. The editor builds local shaders and caches on the first launch. Each checkout keeps its own save games.

For Blueprint work, open the Content Drawer and browse to **Content → WTLR**. `Player` contains Elias and his controller, `Core` contains the journey state and save classes, and `UI` contains the notebook widget. Edit the first chapter in `Maps/L_LanternStreet`.

## Design and attribution

Aideen’s mechanics and level drawings informed the team’s single-Echo rules and the opening in Elias’s home. The current design brief describes the playable area, controls and puzzle rules. [Current design](Docs/GAME-DESIGN.md)

For course submissions, credit each third-party and AI-assisted asset, including the original creator or provider, source, licence where applicable and team modifications. Preserve original licences alongside the source files. [Asset register](Docs/ASSET-CREDITS.csv) · [Asset conventions](Docs/ASSET-CONVENTIONS.md)

