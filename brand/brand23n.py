"""23N AI Labs: brand kit for Field Test notebooks, charts, videos and covers.

The look matches https://23nlabs.com: a warm paper background, ink text, moss as the accent colour,
Bricolage Grotesque for headlines, IBM Plex Sans for body text and IBM Plex Mono for labels.

Use it in a notebook (Colab or Kaggle):

    import urllib.request
    urllib.request.urlretrieve(
        "https://raw.githubusercontent.com/23nlabs/field-tests/main/brand/brand23n.py", "brand23n.py")
    import brand23n as B
    B.setup()                      # fetches the fonts and applies the matplotlib style
    v = B.Video("ft05_video.mp4")  # a 1080x1080 H.264 writer; the saved file plays at 1.5x (VIDEO_SPEED)
    B.hook_card(v.fig, "05", "Can a small model ...?", "One-line context")
    v.hold(5)
    ...
    B.end_card(v.fig, "05"); v.hold(6); v.close()
    B.cover("ft05_cover.png", "05", "Title", "Subtitle", "+156%", "what the number means", image=None)

See BRAND.md in the repo root for the rules this file implements.
"""
from __future__ import annotations

import os
import subprocess
import textwrap
import urllib.request
from pathlib import Path

import numpy as np
import matplotlib
import matplotlib.patches
import matplotlib.pyplot as plt
from matplotlib import font_manager

# ---------------------------------------------------------------- identity
NAME = "23N AI Labs"              # always written exactly like this
SITE = "23nlabs.com"
DESCRIPTOR = "Applied AI research · 23°N"
COORDS = "23.2° N, 72.6° E"
SERIES = "23N Field Tests"
HASHTAGS = "#23NFieldTests"
STANCE = "Independent study on public data."

# Videos are authored on a 1x timeline (hook 0-5 s ... end card 52-58 s) and saved sped up by this factor, so a
# 58 s timeline becomes a ~39 s file. Override per video with B.Video(..., speed=1.0), or for a whole run with the
# environment variable B23N_VIDEO_SPEED=1.
VIDEO_SPEED = float(os.environ.get("B23N_VIDEO_SPEED", "1.5"))

# ---------------------------------------------------------------- colour tokens (from 23nlabs.com CSS)
PAPER = "#F4F1EA"   # background
INK = "#18201D"     # headlines and primary text
MOSS = "#52654D"    # accent: the one thing to look at
STONE = "#777871"   # secondary text, axes
AMBER = "#B58C57"   # second series, highlights
BODY = "#1C1A17"    # body text
MUTED = "#4A463F"   # mono labels / eyebrows
LINE = (24 / 255, 32 / 255, 29 / 255, 0.17)  # hairlines and grid
MOSS_LIGHT = "#A9B5A2"
PAPER_DEEP = "#E8E3D8"   # panels and cards on paper

# Categorical order for charts: moss first, then amber, ink and stone.
SERIES_COLORS = [MOSS, AMBER, INK, STONE, MOSS_LIGHT]
# Sequential map for choropleths and heatmaps: paper -> moss -> ink
SEQ_CMAP = matplotlib.colors.LinearSegmentedColormap.from_list("23n_seq", [PAPER_DEEP, MOSS_LIGHT, MOSS, INK])
# Diverging map, centred on paper
DIV_CMAP = matplotlib.colors.LinearSegmentedColormap.from_list("23n_div", [AMBER, PAPER, MOSS])

# ---------------------------------------------------------------- fonts
FONT_BASE = "https://raw.githubusercontent.com/23nlabs/field-tests/main/brand/fonts/"
FONT_FILES = {
    "display": "BricolageGrotesque-Medium.ttf",
    "display_bold": "BricolageGrotesque-SemiBold.ttf",
    "sans": "IBMPlexSans-Regular.ttf",
    "sans_bold": "IBMPlexSans-SemiBold.ttf",
    "mono": "IBMPlexMono-Regular.ttf",
    "mono_bold": "IBMPlexMono-Medium.ttf",
}
FP: dict[str, font_manager.FontProperties] = {}


def _font_dir() -> Path:
    here = Path(__file__).resolve().parent / "fonts"   # running from a clone of the repo
    return here if here.exists() else Path("brand_fonts")


def setup(style: bool = True) -> dict:
    """Make sure the brand fonts are available (download if needed), register them, and apply the chart style."""
    d = _font_dir(); d.mkdir(exist_ok=True)
    for key, fn in FONT_FILES.items():
        p = d / fn
        if not p.exists():
            urllib.request.urlretrieve(FONT_BASE + fn, p)
        font_manager.fontManager.addfont(str(p))
        FP[key] = font_manager.FontProperties(fname=str(p))
    if style:
        apply_style()
    return FP


def apply_style():
    plt.rcParams.update({
        "figure.facecolor": PAPER, "axes.facecolor": PAPER, "savefig.facecolor": PAPER,
        "text.color": BODY, "axes.labelcolor": STONE, "axes.edgecolor": LINE,
        "xtick.color": STONE, "ytick.color": STONE, "grid.color": LINE, "grid.linewidth": 0.8,
        "axes.grid": True, "axes.axisbelow": True, "axes.spines.top": False, "axes.spines.right": False,
        "axes.prop_cycle": matplotlib.cycler(color=SERIES_COLORS),
        "font.family": "IBM Plex Sans", "font.size": 12,
        "axes.titlesize": 16, "axes.titleweight": "medium", "axes.titlelocation": "left",
        "legend.frameon": False, "figure.dpi": 110,
    })


def chart_title(ax, title: str, subtitle: str | None = None):
    """A headline-style chart title in Bricolage, with an optional mono subtitle."""
    ax.set_title("")
    ax.text(0, 1.10 if subtitle else 1.04, title, transform=ax.transAxes, fontproperties=FP.get("display"),
            fontsize=18, color=INK, ha="left", va="bottom")
    if subtitle:
        ax.text(0, 1.03, subtitle.upper(), transform=ax.transAxes, fontproperties=FP.get("mono"),
                fontsize=9.5, color=MUTED, ha="left", va="bottom")


def source_note(fig, text: str):
    fig.text(0.01, 0.005, text, fontproperties=FP.get("mono"), fontsize=8, color=STONE, ha="left", va="bottom")


# ---------------------------------------------------------------- video
SQUARE = (1080, 1080)     # the original Field Test format
PORTRAIT = (1080, 1350)   # 4:5, takes more of the LinkedIn feed; the default for deep Field Tests (#13 on)

# The video formats a Field Test can use for its 5-40 s evidence section (see BRAND.md, "Video formats").
# Pick the one that fits the topic; the hook, headline and end cards stay the same in all of them.
VIDEO_FORMATS = {
    "chart": "animated charts of the result (FT01-FT12 style)",
    "overlay": "model output drawn on the real imagery: boxes, keypoints, 95% ellipses, masks (B.overlay_frame)",
    "mechanism": "the method as a step-by-step diagram, one step lit per frame (B.step_card)",
    "failure": "side by side, where the model holds and where it breaks (B.split_frame)",
}


class Video:
    """Streams matplotlib frames straight into ffmpeg (H.264, yuv420p, faststart).

    Frames are written on a 1x timeline (hold(5) = 5 s of story time). On close() the file is re-timed by `speed`
    (default VIDEO_SPEED = 1.5) and saved at `out`, still at `fps`. keep_1x=True also keeps the 1x file as *_1x.mp4.
    """

    def __init__(self, out: str, size=(1080, 1080), fps: int = 30, speed: float | None = None, keep_1x: bool = False):
        self.final, self.W, self.H, self.fps = out, size[0], size[1], fps
        self.speed = VIDEO_SPEED if speed is None else float(speed)
        if self.speed <= 0:
            raise ValueError("speed must be > 0")
        self.keep_1x = keep_1x
        p = Path(out)
        self.out = out if self.speed == 1 else str(p.with_name(p.stem + "_1x" + p.suffix))
        self.fig = plt.figure(figsize=(self.W / 100, self.H / 100), dpi=100, facecolor=PAPER)
        self.proc = subprocess.Popen(
            ["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{self.W}x{self.H}",
             "-r", str(fps), "-i", "-", "-c:v", "libx264", "-preset", "veryfast", "-pix_fmt", "yuv420p",
             "-movflags", "+faststart", self.out], stdin=subprocess.PIPE)
        self.frames = 0

    @property
    def duration(self) -> float:
        """Length of the saved file in seconds (after the speed-up)."""
        return self.frames / self.fps / self.speed

    def clear(self):
        self.fig.clf(); self.fig.set_facecolor(PAPER)

    def grab(self) -> bytes:
        self.fig.canvas.draw()
        return np.asarray(self.fig.canvas.buffer_rgba())[..., :3].tobytes()

    def frame(self):
        self.proc.stdin.write(self.grab()); self.frames += 1

    def hold(self, seconds: float, fade: float = 0.4):
        """Write the current figure for `seconds` (1x timeline), fading in from paper over `fade` seconds."""
        n = int(round(seconds * self.fps)); nf = int(round(fade * self.fps))
        img = np.frombuffer(self.grab(), np.uint8).reshape(self.H, self.W, 3).astype(np.float32)
        bg = np.array(matplotlib.colors.to_rgb(PAPER), np.float32) * 255
        for k in range(n):
            a = min(1.0, (k + 1) / nf) if nf else 1.0
            self.proc.stdin.write((img * a + bg * (1 - a)).astype(np.uint8).tobytes() if a < 1 else img.astype(np.uint8).tobytes())
            self.frames += 1

    def close(self) -> str:
        self.proc.stdin.close(); rc = self.proc.wait(); plt.close(self.fig)
        if rc != 0:
            raise RuntimeError("ffmpeg failed")
        if self.speed != 1:
            r = subprocess.run(
                ["ffmpeg", "-y", "-loglevel", "error", "-i", self.out, "-filter:v", f"setpts=PTS/{self.speed}",
                 "-r", str(self.fps), "-c:v", "libx264", "-preset", "veryfast", "-pix_fmt", "yuv420p",
                 "-movflags", "+faststart", "-an", self.final])
            if r.returncode != 0:
                raise RuntimeError("ffmpeg speed-up failed")
            if not self.keep_1x:
                os.remove(self.out)
        print(f"video: {self.final} · {self.duration:.1f}s at {self.speed:g}x "
              f"({self.frames / self.fps:.1f}s timeline)" + (f" · 1x copy: {self.out}" if self.speed != 1 and self.keep_1x else ""))
        return self.final


def _wrap(s: str, n: int) -> str:
    return "\n".join(textwrap.wrap(s, n))


def header(fig, ft_no: str):
    """Top band on every frame: wordmark on the left, series label on the right, hairline below."""
    fig.text(0.055, 0.955, NAME, fontproperties=FP.get("display_bold"), fontsize=24, color=INK, va="top")
    fig.text(0.055, 0.917, DESCRIPTOR, fontproperties=FP.get("mono"), fontsize=12, color=MUTED, va="top")
    fig.text(0.945, 0.952, f"FIELD TEST #{ft_no}", fontproperties=FP.get("mono_bold"), fontsize=14,
             color=MOSS, va="top", ha="right")
    fig.add_artist(plt.Line2D([0.055, 0.945], [0.885, 0.885], color=LINE, lw=1.2, transform=fig.transFigure))


def caption(fig, text: str, y: float = 0.065, size: int = 22):
    """Burned-in caption (most people watch muted). Ink on a slightly deeper paper panel."""
    fig.text(0.5, y, _wrap(text, 62), ha="center", va="center", fontproperties=FP.get("sans"), fontsize=size,
             color=INK, bbox=dict(boxstyle="round,pad=0.6", fc=PAPER_DEEP, ec="none"))


def hook_card(fig, ft_no: str, question: str, context: str = ""):
    """0-5 s: the question, big, with a moss accent on the last line."""
    header(fig, ft_no)
    lines = textwrap.wrap(question, 18)
    for i, line in enumerate(lines):
        fig.text(0.055, 0.70 - i * 0.105, line, fontproperties=FP.get("display"), fontsize=74,
                 color=MOSS if i == len(lines) - 1 else INK, va="top")
    if context:
        fig.text(0.055, 0.17, _wrap(context, 48).upper(), fontproperties=FP.get("mono"), fontsize=17,
                 color=MUTED, va="bottom", linespacing=1.5)


def headline_card(fig, ft_no: str, number: str, statement: str, how: str = ""):
    """The headline number: huge, in moss, with one plain sentence beneath it and the method as a mono line."""
    header(fig, ft_no)
    fig.text(0.055, 0.78, number, fontproperties=FP.get("display"), fontsize=170, color=MOSS, va="top")
    fig.text(0.055, 0.44, _wrap(statement, 30), fontproperties=FP.get("display"), fontsize=44, color=INK,
             va="top", linespacing=1.15)
    if how:
        fig.text(0.055, 0.10, _wrap("How: " + how, 64).upper(), fontproperties=FP.get("mono"), fontsize=13,
                 color=MUTED, va="bottom", linespacing=1.5)


def end_card(fig, ft_no: str, data_credit: str = ""):
    """52-58 s: the sign-off, identical in every video."""
    fig.text(0.5, 0.60, NAME, fontproperties=FP.get("display"), fontsize=96, color=INK, ha="center", va="center")
    fig.text(0.5, 0.50, DESCRIPTOR.upper(), fontproperties=FP.get("mono"), fontsize=18, color=MUTED, ha="center")
    fig.text(0.5, 0.40, f"Field Test #{ft_no}  ·  open notebook in comments", fontproperties=FP.get("sans"),
             fontsize=26, color=MOSS, ha="center")
    fig.text(0.5, 0.32, SITE, fontproperties=FP.get("display_bold"), fontsize=36, color=INK, ha="center")
    fig.add_artist(plt.Line2D([0.3, 0.7], [0.26, 0.26], color=LINE, lw=1.2, transform=fig.transFigure))
    foot = STANCE + (f"  ·  {data_credit}" if data_credit else "")
    fig.text(0.5, 0.075, _wrap(foot, 80), fontproperties=FP.get("mono"), fontsize=12, color=STONE, ha="center")
    fig.text(0.5, 0.035, COORDS, fontproperties=FP.get("mono"), fontsize=12, color=STONE, ha="center")


def cover(out: str, ft_no: str, title: str, subtitle: str, number: str, number_caption: str,
          image=None, size=(1080, 1350), data_credit: str = "") -> str:
    """1080x1350 cover/thumbnail. `image` is an optional RGB array or a callable(ax) that draws into the panel."""
    fig = plt.figure(figsize=(size[0] / 100, size[1] / 100), dpi=100, facecolor=PAPER)
    fig.text(0.055, 0.965, NAME, fontproperties=FP.get("display_bold"), fontsize=24, color=INK, va="top")
    fig.text(0.945, 0.962, f"FIELD TEST #{ft_no}", fontproperties=FP.get("mono_bold"), fontsize=14, color=MOSS,
             va="top", ha="right")
    t_lines = textwrap.wrap(title, 22)
    t = fig.text(0.055, 0.915, "\n".join(t_lines), fontproperties=FP.get("display"), fontsize=58, color=INK,
                 va="top", linespacing=1.05)
    fig.canvas.draw()   # measure the title so the subtitle always sits below it
    y_sub = t.get_window_extent().transformed(fig.transFigure.inverted()).y0 - 0.018
    fig.text(0.055, y_sub, subtitle.upper(), fontproperties=FP.get("mono"), fontsize=15, color=MUTED, va="top")
    top = y_sub - 0.035
    ax = fig.add_axes([0.055, 0.30, 0.89, max(0.2, top - 0.30)]); ax.set_axis_off()
    if callable(image):
        image(ax)
    elif image is not None:
        ax.imshow(image); ax.set_aspect("auto")
    else:
        ax.add_patch(plt.Rectangle((0, 0), 1, 1, color=PAPER_DEEP, transform=ax.transAxes))
    fig.text(0.055, 0.255, number, fontproperties=FP.get("display"), fontsize=110, color=MOSS, va="top")
    fig.text(0.055, 0.115, _wrap(number_caption, 40), fontproperties=FP.get("sans"), fontsize=24, color=INK, va="top")
    fig.text(0.055, 0.03, f"{SITE}  ·  {STANCE}" + (f"  ·  {data_credit}" if data_credit else ""),
             fontproperties=FP.get("mono"), fontsize=11, color=STONE)
    fig.savefig(out, dpi=100, facecolor=PAPER); plt.close(fig)
    return out


# ---------------------------------------------------------------- evidence frames for the newer video formats
def _panel(fig, rect):
    ax = fig.add_axes(rect); ax.set_axis_off(); return ax


def blur_regions(img, boxes, k: int = 25):
    """Privacy: pixelate faces and number plates before an image is shown anywhere. boxes = [(x0, y0, x1, y1), ...]
    in pixels. Returns a copy. Every published frame of people or vehicles must go through this (BUILD.md)."""
    out = np.array(img, copy=True)
    for x0, y0, x1, y1 in boxes:
        x0, y0, x1, y1 = [int(round(v)) for v in (x0, y0, x1, y1)]
        x0, y0 = max(0, x0), max(0, y0); x1, y1 = min(out.shape[1], x1), min(out.shape[0], y1)
        if x1 <= x0 or y1 <= y0:
            continue
        reg = out[y0:y1, x0:x1]
        h, w = reg.shape[:2]; step = max(1, min(h, w) // max(1, min(k, min(h, w))) or 1)
        step = max(step, max(h, w) // 8 or 1)
        small = reg[::step, ::step]
        out[y0:y1, x0:x1] = np.repeat(np.repeat(small, step, 0), step, 1)[:h, :w]
    return out


def cov_ellipse(ax, mean, cov, p: float = 0.95, color: str | None = None, lw: float = 2.0, fill: bool = True):
    """Draw the p-probability ellipse of a 2D Gaussian (mean, 2x2 covariance) on `ax`, in data coordinates."""
    from matplotlib.patches import Ellipse
    cov = np.asarray(cov, float); vals, vecs = np.linalg.eigh(cov)
    vals = np.clip(vals, 0, None); k = np.sqrt(-2 * np.log(1 - p))          # chi-square, 2 dof
    ang = np.degrees(np.arctan2(vecs[1, 1], vecs[0, 1]))
    c = color or MOSS
    e = Ellipse(mean, 2 * k * np.sqrt(vals[1]), 2 * k * np.sqrt(vals[0]), angle=ang, ec=c, lw=lw,
                fc=matplotlib.colors.to_rgba(c, 0.18) if fill else "none")
    ax.add_patch(e); return e


def overlay_frame(fig, ft_no: str, image, boxes=(), points=(), ellipses=(), mask=None, title: str = "",
                  label: str = "", caption_text: str = ""):
    """Format "overlay": real imagery with the model's output drawn on it.

    boxes    = [(x0, y0, x1, y1, text, kind), ...]  kind "ok" (moss), "flag" (amber) or "unsure" (stone, dashed)
    points   = [(x, y, kind), ...]                  keypoints
    ellipses = [(mean_xy, cov_2x2, kind), ...]      95% uncertainty ellipses
    mask     = HxW bool/float array drawn as a translucent moss layer (e.g. flooded pixels)
    """
    header(fig, ft_no)
    col = {"ok": MOSS, "flag": AMBER, "unsure": STONE}
    top = 0.865
    if title:
        fig.text(0.055, 0.865, title, fontproperties=FP.get("display"), fontsize=34, color=INK, va="top")
        top = 0.80
    if label:
        fig.text(0.945, 0.865 if title else 0.865, label.upper(), fontproperties=FP.get("mono"), fontsize=12,
                 color=MUTED, va="top", ha="right")
        top = min(top, 0.835)
    bottom = 0.15 if caption_text else 0.06
    ax = _panel(fig, [0.055, bottom, 0.89, top - bottom - 0.015])
    img = np.asarray(image); ax.imshow(img, aspect="equal")
    if mask is not None:
        m = np.asarray(mask, float); rgba = np.zeros(m.shape + (4,))
        rgba[..., :3] = matplotlib.colors.to_rgb(MOSS); rgba[..., 3] = 0.45 * np.clip(m, 0, 1)
        ax.imshow(rgba, aspect="equal")
    for b in boxes:
        x0, y0, x1, y1 = b[:4]; text = b[4] if len(b) > 4 else ""; kind = b[5] if len(b) > 5 else "ok"
        c = col.get(kind, MOSS)
        ax.add_patch(plt.Rectangle((x0, y0), x1 - x0, y1 - y0, fill=False, ec=c, lw=3,
                                   ls="--" if kind == "unsure" else "-"))
        if text:
            ax.text(x0, y0 - 4, text.upper(), fontproperties=FP.get("mono_bold"), fontsize=11, color=PAPER,
                    va="bottom", ha="left", bbox=dict(boxstyle="square,pad=0.25", fc=c, ec="none"))
    for mean, cov, *kind in ellipses:
        cov_ellipse(ax, mean, cov, color=col.get(kind[0] if kind else "ok", MOSS))
    for x, y, *kind in points:
        ax.plot([x], [y], "o", ms=7, mfc=col.get(kind[0] if kind else "ok", MOSS), mec=PAPER, mew=1.5)
    ax.set_xlim(0, img.shape[1]); ax.set_ylim(img.shape[0], 0)
    if caption_text:
        caption(fig, caption_text)
    return ax


def split_frame(fig, ft_no: str, left, right, left_label: str, right_label: str, left_kind: str = "ok",
                right_kind: str = "flag", title: str = "", caption_text: str = ""):
    """Format "failure": two panels side by side, e.g. clear day vs fog, where the model holds vs where it breaks.
    `left` / `right` are RGB arrays or callables(ax) that draw into the panel (use overlay-style drawing there)."""
    header(fig, ft_no)
    col = {"ok": MOSS, "flag": AMBER, "unsure": STONE}
    top = 0.865
    if title:
        fig.text(0.055, 0.865, title, fontproperties=FP.get("display"), fontsize=34, color=INK, va="top")
        top = 0.80
    bottom = 0.15 if caption_text else 0.06
    h = top - bottom - 0.06
    axes = []
    for i, (src, lab, kind) in enumerate([(left, left_label, left_kind), (right, right_label, right_kind)]):
        x = 0.055 + i * 0.455
        fig.text(x, top - 0.01, lab.upper(), fontproperties=FP.get("mono_bold"), fontsize=13,
                 color=col.get(kind, MOSS), va="top")
        ax = _panel(fig, [x, bottom, 0.435, h])
        if callable(src):
            src(ax)
        else:
            ax.imshow(np.asarray(src), aspect="auto")
        for sp in ("top", "bottom", "left", "right"):
            ax.spines[sp].set_visible(False)
        fig.add_artist(plt.Rectangle((x, bottom), 0.435, h, fill=False, ec=col.get(kind, MOSS), lw=3,
                                     transform=fig.transFigure))
        axes.append(ax)
    if caption_text:
        caption(fig, caption_text)
    return axes


def step_card(fig, ft_no: str, steps, active: int, title: str = "", notes=None, caption_text: str = ""):
    """Format "mechanism": the method as a vertical pipeline of steps; step `active` (0-based) is lit in moss,
    earlier steps in ink, later ones in stone. `notes` = optional one-line mono note per step."""
    header(fig, ft_no)
    y = 0.865
    if title:
        fig.text(0.055, y, title, fontproperties=FP.get("display"), fontsize=38, color=INK, va="top")
        y = 0.78
    bottom = 0.17 if caption_text else 0.08
    n = len(steps); gap = (y - bottom) / max(n, 1)
    bh = min(0.105, gap * 0.72)
    for i, s in enumerate(steps):
        yy = y - i * gap - bh
        on, done = i == active, i < active
        fc = MOSS if on else (PAPER_DEEP if done else PAPER)
        ec = MOSS if on else (INK if done else STONE)
        fig.add_artist(matplotlib.patches.FancyBboxPatch((0.055, yy), 0.89, bh, boxstyle="round,pad=0,rounding_size=0.012",
                       fc=fc, ec=ec, lw=1.6, transform=fig.transFigure))
        fig.text(0.085, yy + bh * (0.62 if notes else 0.5), f"{i + 1:02d}", fontproperties=FP.get("mono_bold"), fontsize=16,
                 color=PAPER if on else (INK if done else STONE), va="center")
        fig.text(0.15, yy + bh * (0.62 if notes else 0.5), s, fontproperties=FP.get("display"), fontsize=27,
                 color=PAPER if on else (INK if done else STONE), va="center")
        if notes and i < len(notes) and notes[i]:
            fig.text(0.15, yy + bh * 0.24, notes[i].upper(), fontproperties=FP.get("mono"), fontsize=11,
                     color=PAPER if on else MUTED, va="center")
        if i < n - 1:
            fig.add_artist(matplotlib.patches.FancyArrowPatch((0.5, yy - 0.004), (0.5, yy - (gap - bh) + 0.004),
                           arrowstyle="-|>", mutation_scale=16, color=STONE, lw=1.4, transform=fig.transFigure))
    if caption_text:
        caption(fig, caption_text)


# ---------------------------------------------------------------- calibration charts (deep Field Tests)
def reliability_chart(ax, confidence, correct, bins: int = 10, label: str = "model"):
    """Reliability diagram: stated confidence vs observed accuracy, with the diagonal. Returns the ECE."""
    conf = np.asarray(confidence, float); corr = np.asarray(correct, float)
    edges = np.linspace(0, 1, bins + 1); idx = np.clip(np.digitize(conf, edges) - 1, 0, bins - 1)
    xs, ys, ws = [], [], []
    for b in range(bins):
        m = idx == b
        if m.any():
            xs.append(conf[m].mean()); ys.append(corr[m].mean()); ws.append(m.mean())
    ece = float(np.sum(np.array(ws) * np.abs(np.array(xs) - np.array(ys)))) if xs else float("nan")
    ax.plot([0, 1], [0, 1], color=STONE, lw=1, ls="--", label="perfectly calibrated")
    ax.plot(xs, ys, "o-", color=MOSS, lw=2.2, label=f"{label} (ECE {ece:.3f})")
    ax.set_xlim(0, 1); ax.set_ylim(0, 1); ax.set_xlabel("stated confidence"); ax.set_ylabel("observed accuracy")
    ax.legend(loc="upper left")
    return ece


def coverage_chart(ax, nominal, observed, labels=None):
    """Coverage diagnostic: nominal level (e.g. 50/80/90/95%) vs the share of true values that fell inside.
    `observed` may be one sequence or a list of sequences (one per condition, e.g. clear vs fog)."""
    nominal = np.asarray(nominal, float)
    obs = observed if (len(observed) and np.ndim(observed[0]) > 0) else [observed]
    labels = labels or ["observed"] * len(obs)
    ax.plot([0, 1], [0, 1], color=STONE, lw=1, ls="--", label="ideal")
    for o, lab, c in zip(obs, labels, SERIES_COLORS):
        ax.plot(nominal, np.asarray(o, float), "o-", color=c, lw=2.2, label=lab)
    lo = max(0.0, min(float(nominal.min()), min(float(np.min(o)) for o in obs)) - 0.05)
    ax.set_xlim(lo, 1); ax.set_ylim(lo, 1); ax.set_xlabel("nominal coverage"); ax.set_ylabel("observed coverage")
    ax.legend(loc="upper left")


def selective_chart(ax, confidence, correct, label: str = "model", target: float | None = None):
    """Selective prediction: accuracy on the cases the model keeps vs the share it keeps (abstains on the rest).
    With `target` (e.g. 0.95), marks the largest share that still meets it and returns that share."""
    conf = np.asarray(confidence, float); corr = np.asarray(correct, float)
    order = np.argsort(-conf); acc = np.cumsum(corr[order]) / np.arange(1, len(conf) + 1)
    share = np.arange(1, len(conf) + 1) / len(conf)
    ax.plot(share, acc, color=MOSS, lw=2.2, label=label)
    ax.set_xlim(0, 1); ax.set_xlabel("share of cases handled automatically"); ax.set_ylabel("accuracy on those cases")
    best = None
    if target is not None:
        ok = np.where(acc >= target)[0]
        best = float(share[ok.max()]) if len(ok) else 0.0
        ax.axhline(target, color=AMBER, lw=1.2, ls="--", label=f"target {target:.0%}")
        if best:
            ax.axvline(best, color=MOSS, lw=1, ls=":")
    ax.legend(loc="lower left")
    return best


def post_signature(ft_no: str) -> str:
    """The closing lines used on every LinkedIn/X post."""
    return f"{SERIES} #{ft_no} · {NAME}, Gandhinagar · {SITE}\n{STANCE}\n{HASHTAGS}"
