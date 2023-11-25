import sys
import asyncio
import json

from platform import window, is_browser

from pathlib import Path

# =================================================
# do no change import order for *thread*
# patching threading.Thread
import aio.gthread

# patched module
from threading import Thread

# =================================================
# original module

import pygame

# ====================================================================
# replace non working native function.

print(
    """\
https://github.com/pygame-web/pygbag/issues/16
    applying: use aio green thread for pygame.time.set_timer
"""
)

# build the event and send it directly in the queue
# caveats :
#   - could be possibly very late
#   - delay cannot be less than frametime at device refresh rate.


def patch_set_timer(cust_event_no, millis, loops=0):
    dlay = float(millis) / 1000
    cevent = pygame.event.Event(cust_event_no)

    async def fire_event():
        while true:
            await asyncio.sleep(dlay)
            if aio.exit:
                break
            pygame.event.post(cevent)

    Thread(target=fire_event).start()


pygame.time.set_timer = patch_set_timer

# ====================================================================
# pygame.quit is too hard on gc, and re-importing pygame is problematic
# if interpreter is not fully renewed.
# so just clear screen cut music and hope for the best.


def patch_pygame_quit():
    pygame.mixer.music.stop()
    pygame.mixer.music.unload()
    try:
        pygame.display.update()
    except:
        pass


pygame.quit = patch_pygame_quit


# =====================================================================
# we want fullscreen-windowed template for games as a default
# so call javascript to resize canvas viewport to fill the current
# window each time mode is changed, also remove the "scaled" option

__pygame_display_set_mode__ = pygame.display.set_mode


def patch_pygame_display_set_mode(size=(0, 0), flags=0, depth=0, display=0, vsync=0):
    # apparently no need to remove scaled.
    if size != (0, 0):
        if (sys.platform == "emscripten") and is_browser:
            try:
                window.window_resize()
            except:
                print("ERROR: browser host does not provide window_resize() function", file=sys.__stderr__)

    return __pygame_display_set_mode__(size, flags, depth, display, vsync)


pygame.display.set_mode = patch_pygame_display_set_mode


# =======================================================================
# pygame.mixer.music
#
# replace sdl thread music playing by browser native player
#

tracks = {"current": 0}


def patch_pygame_mixer_music_stop_pause_unload():
    last = tracks["current"]
    if last:
        window.MM.stop(last)
        tracks["current"] = 0


pygame.mixer.music.unload = patch_pygame_mixer_music_stop_pause_unload


def patch_pygame_mixer_music_load(fileobj, namehint=""):
    global tracks

    # stop previously loaded track
    patch_pygame_mixer_music_stop_pause_unload()

    tid = tracks.get(fileobj, None)

    # track was never loaded before
    if tid is None:
        track = patch_pygame_mixer_sound(fileobj, auto=False)
        tid = track.trackid

    # set new current track
    tracks["current"] = tid


pygame.mixer.music.load = patch_pygame_mixer_music_load


# TODO various buffer input
# FIXME tracks hash key
def patch_pygame_mixer_sound(data, auto=False):
    global tracks
    if isinstance(data, (Path, str)):
        data = str(data)
        trackid = tracks.get(data, None)
        if trackid is not None:
            return tracks[trackid]
    else:
        pdb(__file__, "137 TODO buffer types !")

    if Path(data).is_file():
        transport = "fs"
    else:
        transport = "url"

    cfg = {"url": data, "type": "audio", "auto": auto, "io": transport}

    track = window.MM.prepare(data, json.dumps(cfg))

    if track.error:
        pdb("ERROR: on track", cfg)
        # TODO stub track
        return "stub track"

    tracks[data] = track.trackid
    tracks[track.trackid] = track
    window.MM.load(track.trackid)
    return track


BUFFERSIZE = 2048


def patch_pygame_mixer_music_set_volume(vol: float):
    if vol < 0:
        return
    if vol > 1:
        vol = 1.0
    trackid = window.MM.current_trackid or tracks["current"]
    if trackid:
        window.MM.set_volume(trackid, vol)
    else:
        pdb(__file__, "ERROR 175: no track is loaded")


pygame.mixer.music.set_volume = patch_pygame_mixer_music_set_volume


def patch_pygame_mixer_music_get_volume():
    trackid = tracks["current"]
    return float(window.MM.get_volume(trackid))


pygame.mixer.music.get_volume = patch_pygame_mixer_music_get_volume


def patch_pygame_mixer_music_play(loops=0, start=0.0, fade_ms=0):
    trackid = tracks["current"]
    if trackid:
        window.MM.pause(trackid)
        window.MM.play(trackid, loops)
    else:
        pdb(__file__, "ERROR 184: no track is loaded")


pygame.mixer.music.play = patch_pygame_mixer_music_play


def patch_pygame_mixer_music_get_pos():
    trackid = window.MM.current_trackid or tracks["current"]
    if trackid:
        return int(1000 * float(window.MM.get_pos(trackid)))
    return -1


pygame.mixer.music.get_pos = patch_pygame_mixer_music_get_pos


def patch_pygame_mixer_music_queue(fileobj, namehint="", loops=0) -> None:
    window.MM.next = str(fileobj)
    window.MM.next_hint = str(namehint)
    window.MM.next_loops = int(loops)

    tid = tracks.get(fileobj, None)

    # track was never loaded before
    if tid is None:
        track = patch_pygame_mixer_sound(fileobj, auto=False)
        tid = track.trackid

    window.MM.next_tid = tid


pygame.mixer.music.queue = patch_pygame_mixer_music_queue


def patch_pygame_mixer_music_pause():
    last = window.MM.current_trackid or tracks["current"]
    if last:
        window.MM.pause(last)


def patch_pygame_mixer_music_unpause():
    last = window.MM.current_trackid or tracks["current"]
    if last:
        window.MM.unpause(last)


def patch_pygame_mixer_music_stop():
    last = window.MM.current_trackid or tracks["current"]
    if last:
        window.MM.stop(last)


pygame.mixer.music.stop = patch_pygame_mixer_music_stop
pygame.mixer.music.pause = patch_pygame_mixer_music_pause
pygame.mixer.music.unpause = patch_pygame_mixer_music_unpause

# TODO:
# https://www.pygame.org/docs/ref/music.html#pygame.mixer.music.fadeout

# =======================================================================
# pygame.mixer.Sound


# 0.2.0+ use huge buffer size instead of patching whole module.
# pro: full code compatibility
# con: sound lag
pygame.mixer.pre_init(buffer=BUFFERSIZE)

if 0:
    # 0.1.6 used to force soundpatch
    def patch_pygame_mixer_SoundPatch():
        print("pygame mixer SFX patch is already active you can remove this call")

else:

    def patch_pygame_mixer_SoundPatch():
        pygame.mixer.Sound = patch_pygame_mixer_sound
        print("pygame mixer SFX patch is now active")

    __pygame_mixer_init = pygame.mixer.init

    def patch_pygame_mixer_init(frequency=44100, size=-16, channels=2, buffer=512, devicename=None, allowedchanges=0) -> None:
        global BUFFERSIZE
        buffer = BUFFERSIZE
        print(f"pygame mixer init {frequency=}, {size=}, {channels=}, {buffer=}")
        __pygame_mixer_init(frequency, size, channels, buffer)

    pygame.mixer.init = patch_pygame_mixer_init

pygame.mixer.SoundPatch = patch_pygame_mixer_SoundPatch

# ====================================================================
import platform_wasm.pygame.vidcap


# ====================================================================
print("\n\n")
print(open("/data/data/org.python/assets/pygame.six").read())

print(sys._emscripten_info)
