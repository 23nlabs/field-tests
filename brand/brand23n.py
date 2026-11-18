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


def post_signature(ft_no: str) -> str:
    """The closing lines used on every LinkedIn/X post."""
    return f"{SERIES} #{ft_no} · {NAME}, Gandhinagar · {SITE}\n{STANCE}\n{HASHTAGS}"
