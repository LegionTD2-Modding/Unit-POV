# Unit view

A [ProLeak](https://github.com/LegionTD2-Modding/ProLeak) plugin for Legion TD 2. Right-click
any unit and pick **First person view** or **Third person view**, or select it and press
**V** (first person) or **B** (third person).

- First person: the camera rides the unit at its head, looking where it faces.
- Third person: the camera follows the unit from behind and above. Drag with the middle mouse
  button to turn around it, and use the wheel to move closer or further.

Press the same key again, or **Escape**, to go back to the normal camera. Clicking the minimap
or using one of the game's camera shortcuts (lanes, king, bookmarks) also leaves the view and
moves the camera as the game would. During a wave a
placed fighter is hidden while another unit fights for it; the view follows that unit. The
view ends by itself when the unit leaves the game.

## Looking around in first person

Drag with the middle mouse button to look up, down, left and right, inside a cone around where
the unit faces (90 degrees each way by default, set in the plugin settings).

## Moving the camera in first person

| Key | Moves the camera |
|---|---|
| Right / Left arrow | right / left |
| Up / Down arrow | forward / back |
| Page Up / Page Down | up / down |
| Shift with any of these | a fifth of a step |
| Home | back to the head (or the top of the model) |

The offset is saved for the unit type, in the plugin's store
(`ProLeak/data/kidev.unit-pov/store.sqlite`). The next unit of that type starts from it.

## Third person

Leaving third person saves the distance and angle for the unit type, in the same store.
**Home** puts them back to the start.

## Settings

In the game, Mods > Unit view > Settings:

| Setting | Default | Effect |
|---|---|---|
| Show the unit | off | Keep the unit's model visible in first person. |
| First person key | `V` | The key that enters and leaves first person. |
| Third person key | `B` | The key that enters and leaves third person. |
| Menu on Alt + right-click | off | On: a plain right-click on a unit pings as usual, and Alt + right-click opens the view menu. |
| Look range, horizontal | 90 | Degrees the middle-button drag looks across, left to right; 0 turns it off. |
| Look range, vertical | 90 | Degrees the middle-button drag looks across, up to down; 0 turns it off. |
| Camera step | 0.1 | How far each key press moves the camera in first person. |

To change a key, click it in the form and press the new key.

Moving the camera needs the `actions` permission, which ProLeak gives in local games only.

## Installing

In the game, Mods > Browse lists it: press Install. ProLeak installs the latest release and
offers each update in the Mods tab.

To install it by hand, copy this folder into `ProLeak/plugins/` in the game folder, so that
`plugin.yml` sits at `ProLeak/plugins/kidev.unit-pov/plugin.yml`.

## License

GNU Affero General Public License v3.0; see [LICENSE](LICENSE).
