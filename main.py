"""See the game from any unit: in first person from its head, or in third person orbiting it.
Right-click a unit, or select it and press a view key. The camera set for a unit type is kept
and used the next time a unit of that type is viewed."""
from proleak import camera, plugins, settings, store, ui, world
from proleak import input as keys
from proleak.errors import NotAllowedHere

from .controls import KEYS, nudge
from .offsets import ORBIT, ORIGIN, Cameras

SHOW_UNIT = settings.add("show_unit", False, label="Show the unit", subtitle="In first person")
VIEW_KEY = settings.add("view_key", "V", type="key", label="First person key",
                        help="With a unit selected, enters first person; press it again, or Escape, to leave.")
THIRD_KEY = settings.add("third_key", "B", type="key", label="Third person key",
                         help="With a unit selected, enters third person; press it again, or Escape, to leave. "
                              "Drag with the middle mouse button to turn around the unit, and use the wheel "
                              "to move closer or further.")
MENU_ALT = settings.add("menu_alt", False, label="Menu on Alt + right-click",
                        help="Off: a right-click on a unit opens the view menu, in place of the ping wheel. "
                             "On: a plain right-click pings as usual, and Alt + right-click opens the menu.")
LOOK_H = settings.add("look_horizontal", 90, min=0, max=180, label="Look range, horizontal",
                      subtitle="First person, in degrees",
                      help="Drag with the middle mouse button to look left and right, up to half this angle "
                           "each way. 0 turns it off.")
LOOK_V = settings.add("look_vertical", 90, min=0, max=180, label="Look range, vertical",
                      subtitle="First person, in degrees",
                      help="Drag with the middle mouse button to look up and down, up to half this angle "
                           "each way. 0 turns it off.")
STEP = settings.add("step", 0.1, min=0.01, max=2, label="Camera step", subtitle="First person",
                    help="How far each arrow, Page Up or Page Down press moves the camera. Hold Shift for a "
                         "fifth of a step.")

offsets = Cameras(store.table("first_person"), ORIGIN)
orbits = Cameras(store.table("third_person"), ORBIT)
view = None
viewed_type = ""
menu_entries = []


def on_load(ctx):
    keys.key(VIEW_KEY.value, lambda ev: toggle("first"))
    keys.key(THIRD_KEY.value, lambda ev: toggle("third"))
    menu_entries[:] = [ui.unit_menu.add("First person view", lambda unit: start(unit, "first"), alt=MENU_ALT.value),
                   ui.unit_menu.add("Third person view", lambda unit: start(unit, "third"), alt=MENU_ALT.value)]


@MENU_ALT.on_change
def menu_alt_changed(value):
    for entry in menu_entries:
        entry.alt = value


@VIEW_KEY.on_change
def view_key_changed(value):
    plugins.reload()                     # the key watches are set up at load


@THIRD_KEY.on_change
def third_key_changed(value):
    plugins.reload()


def active():
    return view is not None and view.alive


def end():
    if view.mode == "third":
        orbits.set(viewed_type, (view.distance, view.pitch))
    view.end()


def toggle(mode):
    if active():
        same = view.mode == mode
        end()
        if same:
            return
    me = world.player()
    selected = me.selected() if me is not None else []
    if not selected:
        ui.toast("Select a unit, then press the view key.", header="Unit view")
        return
    start(selected[0], mode)


def start(unit, mode):
    global view, viewed_type
    if active():
        end()
    viewed_type = unit.type
    try:
        if mode == "first":
            view = camera.pov(unit, offset=offsets.get(viewed_type), show_unit=SHOW_UNIT.value,
                               look=(LOOK_H.value, LOOK_V.value))
        else:
            distance, pitch = orbits.get(viewed_type)
            view = camera.third_person(unit, distance=distance, pitch=pitch)
    except NotAllowedHere:
        ui.toast("Moving the camera is not allowed on this server.", header="Unit view")
    except ValueError as e:              # another plugin holds the view, or the unit just left
        ui.toast(str(e), header="Unit view")


@keys.key("Escape")
def leave(ev):
    if active():
        end()


@LOOK_H.on_change
@LOOK_V.on_change
def look_changed(value):
    if active() and view.mode == "first":
        view.look = (LOOK_H.value, LOOK_V.value)


@SHOW_UNIT.on_change
def show_changed(value):
    if active() and view.mode == "first":
        view.show_unit = value


def move(ev, fine):
    if not active() or view.mode != "first":
        return
    view.offset = nudge(view.offset, ev.key, STEP.value, fine)
    offsets.set(viewed_type, view.offset)


def reset(ev):
    if not active():
        return
    if view.mode == "first":
        offsets.reset(viewed_type)
        view.offset = offsets.get(viewed_type)
    else:
        orbits.reset(viewed_type)
        view.distance, view.pitch = orbits.get(viewed_type)


for key in KEYS:
    keys.key(key, lambda ev: move(ev, False))
    keys.key(key, lambda ev: move(ev, True), shift=True)
keys.key("Home", reset)
