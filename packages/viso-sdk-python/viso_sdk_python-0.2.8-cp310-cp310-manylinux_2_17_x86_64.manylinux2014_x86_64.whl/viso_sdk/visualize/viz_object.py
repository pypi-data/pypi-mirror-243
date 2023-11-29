import cv2
import numpy as np

from PIL import ImageDraw, Image
from viso_sdk.constants import KEY

from viso_sdk.visualize.palette import get_rgba_color_with_palette_id, get_rgba_color
from viso_sdk.visualize import utils


def trace_to_pts(trace):
    pts = []
    for tlwh in trace:
        x, y, w, h = tlwh
        pts.append([x + w / 2, y + h / 2])
    return pts


class VizObjectDraw:
    def __init__(self, bbox_color, bbox_thickness, text_size, text_color=utils.DEFAULT_TXT_COLOR):
        self.bbox_color = get_rgba_color(bbox_color)
        self.bbox_thickness = bbox_thickness

        self.default_font = utils.init_font(font_size=text_size)
        self.text_color = get_rgba_color(text_color)

    def _draw_objs_(
            self,
            draw,  # ImageDraw.Draw,
            objs,  # list
            random_color=False,
            show_label=True,
            show_confidence=True,
            show_class_id=False
    ):
        img_w, img_h = draw.im.size[:2]
        for obj in objs:
            tlwh = obj[KEY.TLWH]

            if tlwh[2] < 1.0:
                x, y, w, h = (np.array(tlwh) * np.array([img_w, img_h, img_w, img_h])).astype(int).tolist()
                # is_relative_coord = True
            else:
                x, y, w, h = np.array(tlwh).astype(int).tolist()
                # is_relative_coord = False

            if random_color:
                bbox_color = get_rgba_color_with_palette_id(palette_id=obj.get(KEY.CLASS_ID, 0))
            else:
                bbox_color = self.bbox_color if self.bbox_color is not None else utils.DEFAULT_ROI_OUTLINE_COLOR

            # put object boundary bbox
            draw.rectangle(xy=[(x, y), (x + w, y + h)], fill=None, outline=bbox_color, width=self.bbox_thickness)

            if show_label:
                label = ""

                if show_class_id and KEY.CLASS_ID in obj.keys():
                    label += f"{obj.get(KEY.CLASS_ID, '')} "

                label += f"{obj.get(KEY.LABEL, '')}"

                if show_confidence:
                    label += f" {float(obj.get(KEY.SCORE)):.2f}"

                # get text label
                if show_label:
                    utils.put_text(
                        font=self.default_font,
                        draw=draw,
                        pos=(x, y),
                        text=label,
                        show_bg=True,
                        bg_thickness=-1,
                        bg_color=bbox_color,
                        # show_shadow=True
                    )

        return draw

    def draw_detections(
            self,
            img,
            detections,
            random_color=False,
            show_label=True,
            show_confidence=True):
        # Convert the image to RGB (OpenCV uses BGR)
        cv_im_rgba = cv2.cvtColor(img.copy(), cv2.COLOR_BGR2RGBA)

        # Pass the image to PIL
        pil_base_im = Image.fromarray(cv_im_rgba, "RGBA")

        pil_viz_im = Image.new("RGBA", pil_base_im.size, (255, 255, 255, 0))
        draw = ImageDraw.Draw(pil_viz_im, "RGBA")

        self._draw_objs_(
            draw=draw,
            objs=detections,
            random_color=random_color,
            show_label=show_label,
            show_confidence=show_confidence)

        pil_out = Image.alpha_composite(pil_base_im, pil_viz_im)
        cv_im_processed = cv2.cvtColor(np.array(pil_out), cv2.COLOR_RGBA2BGR)
        return cv_im_processed

    def draw_tracks(
            self,
            img,
            tracks,
            random_color=False,
            show_detection=True,
            show_track_id=False,
            show_trace=True,
            trace_length_to_show=5
    ):
        img_h, img_w, = img.shape[:2]

        for obj in tracks:
            tid = obj[KEY.TID]
            tlwh = obj[KEY.TLWH]
            trace = obj[KEY.TRACE]
            # status = obj[KEY.STATUS]

            if tlwh[2] < 1.0:
                # x, y, w, h = (np.asarray(tlwh) * np.asarray([img_w, img_h, img_w, img_h])).astype(int).tolist()
                is_relative_coord = True
            else:
                # x, y, w, h = np.asarray(tlwh).astype(int).tolist()
                is_relative_coord = False

            if random_color:
                # status == TrackState.Tracked:
                bbox_color = get_rgba_color_with_palette_id(int(tid % 256))
            else:
                bbox_color = self.bbox_color if self.bbox_color is not None else utils.DEFAULT_ROI_OUTLINE_COLOR

            new_label = ""
            if show_track_id:
                new_label += f"tid {tid}"
            if show_detection:
                new_label += f" {obj[KEY.LABEL]} {float(obj[KEY.SCORE]):.2}"
            obj[KEY.LABEL] = new_label if len(new_label) != 0 else obj[KEY.LABEL]

            if show_trace:
                pts = trace_to_pts(trace)[-trace_length_to_show:]
                for i in range(len(pts) - 1):
                    if is_relative_coord:
                        _pt0 = (int(pts[i][0] * img_w), int(pts[i][1] * img_h))
                        _pt1 = (int(pts[i + 1][0] * img_w), int(pts[i + 1][1] * img_h))
                    else:
                        _pt0 = (int(pts[i][0]), int(pts[i][1]))
                        _pt1 = (int(pts[i + 1][0]), int(pts[i + 1][1]))
                    cv2.line(img=img, pt1=_pt0, pt2=_pt1, color=bbox_color,
                             thickness=self.bbox_thickness * 2)

        if show_trace or show_track_id or show_detection:
            img = self.draw_detections(img=img, detections=tracks,
                                       random_color=random_color,
                                       show_label=show_detection or show_track_id,
                                       show_confidence=False)

        return img
