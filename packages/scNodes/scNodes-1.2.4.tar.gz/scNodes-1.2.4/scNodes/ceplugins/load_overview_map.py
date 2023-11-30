import imgui

from scNodes.core.ceplugin import *
import tifffile

def create():
    return OverviewMapPlugin()


class OverviewMapPlugin(CEPlugin):
    title = "Load overview map"
    description = "Work in progress"
    enabled = True  # default is True. Set to False in order not to load the plugin upon booting the software.


    def __init__(self):
        ## variables for settings can be initialized here.
        self.maximum_projection = True
        self.angle = 45.0

    def render(self):
        # body of the node goes here.
        # see ceplugin.py for a list of predefined widgets that may be useful.
        # these can be called as in the following examples:
        _, self.maximum_projection = imgui.checkbox("maximum projection", self.maximum_projection)
        imgui.push_item_width(60)
        imgui.align_text_to_frame_padding()
        _, self.angle = imgui.input_float("##angle", self.angle, 0.0, 0.0)
        imgui.same_line()
        imgui.text("relative angle")
        imgui.pop_item_width()
        self.maximum_projection = True  # only MIP for now.
        if self.widget_centred_button("Select map", 90, 20):
            d = filedialog.askdirectory()
            try:
                self.import_map(d)
            except Exception as e:
                cfg.set_error(e, "Couldn't import overview map")

    def import_map(self, d):
        # get a list of all frames from the metadata file.
        frames = list()
        sin = np.sin(self.angle / 180 * np.pi)
        cos = np.sin(self.angle / 180 * np.pi)

        with open(d+"/md.txt", "r") as csv:
            for line in csv:
                vals = line.strip().split(',')
                path = vals[0]
                title = vals[1]
                x = float(vals[2])
                y = float(vals[3])
                z = float(vals[4])
                c = (float(vals[5]), float(vals[6]), float(vals[7]), 1.0)
                pxs = float(vals[8])
                frames.append(MapFrame(
                    path=path,
                    title=title,
                    x=x,#-(sin * x + cos * y),
                    y=y,#cos * x + sin * y,
                    z=z,
                    c=c,
                    pxs=pxs
                ))
        # for every z-stack, load frames and make a ceframe of the MIP
        base_frame = CLEMFrame(np.zeros((10, 10)))
        base_frame.title = "Overview map"
        base_frame.colour = (0.0, 0.0, 0.0, 1.0)
        base_frame.lut = 0
        base_frame.update_lut()
        cfg.ce_frames.append(base_frame)
        channels = list()
        positions = list()
        for f in frames:
            if f.title not in channels:
                channels.append(f.title)
            if [f.x, f.y] not in positions:
                positions.append([f.x, f.y])

        new_frames = list()
        p_enum = 0
        for p in positions:
            ceframes_at_pos = list()
            p_enum += 1
            for c in channels:
                stack = [f for f in frames if f.title == c and [f.x, f.y] == p]
                pxd = list()
                for s in stack:
                    pxd.append(tifffile.imread(d+"/"+s.path))
                pxd = np.asarray(pxd)
                pxd = pxd.max(0)
                ceframe = CLEMFrame(pxd)
                ceframe.colour = stack[0].colour
                ceframe.lut = 0
                ceframe.update_lut()
                ceframe.transform.translation[0] = stack[0].x * 1000.0
                ceframe.transform.translation[1] = stack[1].y * 1000.0
                ceframe.transform.rotation = self.angle
                ceframe.pixel_size = stack[0].pxs
                ceframe.blend_mode = 0 if stack[0].title == channels[-1] else 1
                ceframe.locked = True
                ceframe.title = stack[0].title + f"_{p_enum}"
                ceframes_at_pos.append(ceframe)
                cfg.ce_frames.append(ceframe)
                new_frames.append(ceframe)
            for c in ceframes_at_pos:
                c.parent_to(ceframes_at_pos[-1])
            ceframes_at_pos[-1].parent_to(base_frame)

        x = 0
        y = 0
        xmin = new_frames[0].transform.translation[0]
        ymin = new_frames[0].transform.translation[1]
        xmax = new_frames[0].transform.translation[0]
        ymax = new_frames[0].transform.translation[1]
        n = 0
        for f in new_frames:
            _x = f.transform.translation[0]
            _y = f.transform.translation[1]
            x += _x
            y += _y
            xmin = min(xmin, _x)
            xmax = max(xmax, _x)
            ymin = min(ymin, _y)
            ymax = max(ymax, _y)
            n += 1
        x /= n
        y /= n
        for f in new_frames:
            f.transform.translation[0] -= x
            f.transform.translation[1] -= y

        f_width = new_frames[0].width * new_frames[0].pixel_size
        f_height = new_frames[0].height * new_frames[0].pixel_size
        total_width = (xmax - xmin) + f_width
        total_height = (ymax - ymin) + f_height
        base_frame.pixel_size = max(total_width, total_height) / 10.0
        base_frame.move_to_back()


class MapFrame:
    def __init__(self, path, title, x, y, z, c, pxs):
        self.path = path
        self.title = title
        self.x = x
        self.y = y
        self.z = z
        self.colour = c
        self.pxs = pxs

    def __str__(self):
        return self.path