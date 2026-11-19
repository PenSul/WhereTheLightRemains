# Where the Light Remains

Current implementation brief, 19 November 2026. Unreal Engine 5.8.4.

## Premise and scope

A quiet, non-combat side-scrolling puzzle game. A flat, articulated paper Elias walks through a shallow 3D harbour set. Elias, an elderly widower, revisits a harbour neighbourhood and understands how Mara helped her neighbours during an evacuation. Past is remembered experience, not time travel or resurrection. The whole-game target is 15–30 minutes across four compact areas. This build includes the reusable systems and the complete first area, Lantern Street; Footbridge, Workshop, and House & Landing are outside this build.

## Current Echo rules

Aideen's mechanics and Lantern Street drawings, adopted by the team, replace the original three-type inventory. Elias can remember **one Echo** at a time and manifest no more than one object in the Present. Nearby eligible sources are resolved by distance within a fixed radius. Acquisition/replacement requires confirmation. Light, platform and sound are functional properties; the source object's class is not the puzzle rule. A candle supplies both light and heat. Heat only affects authored grass; there is no general fire simulation. A sky light is not an Echo source.

An assigned manifestation must be safely recalled before replacement. It cannot disappear underneath Elias. Completed obstacles become permanent physical routes so retrieving an Echo cannot strand the player. Ownership and completed state persist; later areas must not create extra simultaneous slots. Platform receivers check height and footprint, and sound receivers check the intended sound property. Keep source spacing and level topology readable so the nearest-source rule is predictable.

## Lantern Street

The western cottage has a stone doorstep at quay level. In the adjoining kitchen, a plate rack and pendulum clock sit beside the letter. Elias starts at home. In Past, Mara sits opposite at the table. A candle is the first source. In Present, the letter pinned to the writing cabinet beside the exit needs light; inspecting the illuminated letter permits departure. Outside, tall grass blocks the route, demonstrating the same candle's heat. A painted stair sign marks the missing route to the upper quay in both periods. In the Past, Elias can remember a packing crate. In the Present, its manifested steps let him reach the landing latch. Opening the latch and getting clear of the Echo on the upper quay automatically returns the crate to his locket and leaves permanent stone stairs. A separate optional two-candle arrangement accepts a third candle and reveals a small memory. Do not reveal the later game's final answer here.

The journal accepts a finding once all three local observations have been discovered. The player then selects the two that directly support the finding and one of three interpretations. A wrong answer keeps all evidence and permits another attempt. The whole game still targets nine required observations and three reconstructions. Later investigation content is not implemented in this first-area build.

## Presentation and controls

Paper Theatre uses layered shallow buildings, paper grain, readable silhouettes, cream, navy ink, muted brick, wood and brass. Present is cool and weathered; Past is warmer. Elias has grey hair/beard, a brown coat, ochre scarf, navy trousers and boots. Use subtle depth and restrained movement, not cinematic letterbox bars.

On launch, the camera settles on a lantern overlooking the quay. The tide and wick move while the title appears. On the first button press, the view pulls back from the same moving harbour image. The view settles on a harbour photograph in a standing walnut frame, beside the open notebook. Reduced Motion takes the player directly to the same desk. A page turns at the notebook's binding to open another spread. **Continue** shows the single saved journey, its last checkpoint and how many of the three Lantern Street observations Elias has collected. An empty page offers **Begin a new journey**. **New journey** opens a chapter page with an unchecked **Skip opening** box. An existing journey also shows a replacement warning. **Settings** turns to a spread where the player can adjust preferences and controls. **Back** turns to the desk again.

A new journey opens on a chapter page. Elias recalls supper with Mara before the flood, sees her returned notebook and its lantern sketch, then arrives in the same kitchen where the player takes control. Checking **Skip opening** before beginning goes directly to the kitchen. Escape also skips a cinematic already in progress. Loading an existing journey returns Elias directly to his last safe checkpoint. From **Pause → Save book**, the player can explicitly save progress in the Present while standing clear of a manifested Echo. Opening the book alone preserves the saved journey.

During play, a short question or observation under the period label follows the player's evidence and permanent puzzle progress. It updates when loading a checkpoint. The period and current hint use larger type than the action result. A short result appears on a pale diary-paper slip that fits its text. A prompt appears beside an interactive object. One illustrated brass locket at the lower right shows the remembered Echo. The interface uses the project's licensed Libre Baskerville typeface. Elias holds the Journal with both hands. Its left page lists observations and its right page presents the current question. The book rises and tilts into view. Reduced motion opens it directly. Closing with J or Escape returns to the previous screen and preserves the current period.

Default keyboard controls: A/D or arrows move, Space jumps, E interacts, Q changes Past/Present, F handles Echo acquisition/use, J opens the Journal, R recalls, Escape pauses/closes. Explain unavailable actions at the object. Settings cover text size, brightness, Master, Music, Sound Effects, Reduce Motion, Reduce Flashes and control rebinding. Save/checkpoint and puzzle restart must preserve already recorded evidence and never create a trapped state.

## Lantern Street presentation

A Light Left On is an original 32-bar instrumental for felt piano, plucked strings and bowed bass. It loops under the title and gameplay, and follows the Music and Master settings. Elias faces directly along the quay. His inked paper limbs pivot behind the coat. At rest, Elias breathes through his shoulders and arms while his boots stay planted. A short neck shows between his beard and coat collar. Reduce Motion softens the idle animation. The gait pauses in flight. Rising, falling and landing have distinct poses. Lanterns light the paving below them, and the manifested candle lights the letter beside the kitchen door. The door spans the playable passage at an angle, where the character meets its closed leaf. Reading the letter opens the passage permanently. The foreground quay, boats, birds and distant painted harbour move at different rates. Individual terns flap, bank and glide across the high sky. Reduce Motion steadies the boats and hides the circling terns. Reduce Flashes steadies candlelight, removes decorative glare and skips the tint when switching periods.

## Source status

The cottage and street share a continuous stone quay. At the eastern end, a timber service stair descends from the upper quay to a small mooring where a rowing boat is tied up. The rail marks the edge of Elias's route. Players finish the chapter at the sunburst door.

The notebook uses a light paper brush for selection and distinct sounds for accepting a choice or backing out. Elias’s boots sound different on stone and timber. The candle, crate, kitchen door and upper landing latch have their own sounds. Players can adjust these with Sound Effects independently of Music.

For the course presentation and final report, optional captions for off-screen sounds are a proposed accessibility update or DLC.

Aideen designed the adopted mechanics and first-level sketches. Credit third-party and AI-assisted production assets using the [asset register](ASSET-CREDITS.csv).
