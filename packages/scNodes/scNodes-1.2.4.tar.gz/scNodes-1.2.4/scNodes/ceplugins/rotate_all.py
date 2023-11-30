from scNodes.core.ceplugin import *


def create():
    return RotateAllPlugin()


class RotateAllPlugin(CEPlugin):
    title = "Rot 90"
    description = "..."
    enabled = True  # default is True. Set to False in order not to load the plugin upon booting the software.

    def __init__(self):
        pass

    def render(self):
        if imgui.button("ccw", 40, 40):
            for f in cfg.ce_frames:
                f.locked = False
                f.pivot_point = f.transform.translation
                ci = f.children
                f.children = []
                f.pivoted_rotation(f.pivot_point, 90.0)
                f.children = ci
        imgui.same_line()
        if imgui.button("cw", 40, 40):
            for f in cfg.ce_frames:
                f.locked = False
                f.pivot_point = f.transform.translation
                ci = f.children
                f.children = []
                f.pivoted_rotation(f.pivot_point, -90.0)
                f.children = ci
        imgui.same_line()
        if imgui.button("H", 40, 40):
            for f in cfg.ce_frames:
                f.flip()
        imgui.same_line()
        if imgui.button("V", 40, 40):
            for f in cfg.ce_frames:
                f.flip(horizontally=False)
