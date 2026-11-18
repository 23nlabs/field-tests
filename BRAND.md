# 23N AI Labs brand rules for Field Tests

Field Test #05 onwards follows these rules everywhere: notebooks, charts, videos, covers, posts and the GitHub Pages site. The look matches [23nlabs.com](https://23nlabs.com). Code that implements it is in [`brand/brand23n.py`](brand/brand23n.py).

FT01–FT04 keep their original videos, which used the earlier dark, saffron-accented look.

## Identity
- **Name:** always **23N AI Labs**, never 23N Labs, 23nlabs or 23N AI Lab.
- **Website:** **23nlabs.com**, on every end card, cover and post.
- **Descriptor:** *Applied AI research · 23°N*. The coordinates motif is **23.2° N, 72.6° E** (Gandhinagar).
- **Positioning:** deep-tech AI research for sovereign, regulated work. We study how small language models and agentic systems behave under real constraints (Indian languages, limited compute, data residency), and we publish what we measure.
- **Series:** *23N Field Tests*, numbered with two digits (#05, #06 …). Hashtag **#23NFieldTests**.

## Voice
- Measured, technical and evidence-led. The number leads, and the method is always one line away.
- Every headline number is computed in the notebook. State assumptions and limits plainly.
- Avoid hype words: *revolutionary*, *game-changing*, *disrupt*, *magic*. Avoid emoji in titles, and use at most one in a post.
- Always add the stance line: *Independent study on public data.* Never imply a partnership with a company or government body we analyse.

## Colour (tokens from 23nlabs.com)
| Token | Hex | Use |
|---|---|---|
| Paper | `#F4F1EA` | Background everywhere (charts, video, cover, web) |
| Ink | `#18201D` | Headlines, primary text |
| Moss | `#52654D` | The accent, used for one thing per frame: the key number, the highlighted series, the last line of a question |
| Amber | `#B58C57` | Second series, a comparison |
| Stone | `#777871` | Axes, secondary text, footers |
| Muted | `#4A463F` | Mono labels and eyebrows |
| Line | `rgba(24,32,29,.17)` | Hairlines, grids |
| Paper deep | `#E8E3D8` | Caption panels, cards |

Chart order: Moss, Amber, Ink, Stone. Sequential maps run from Paper deep through Moss to Ink; diverging maps from Amber through Paper to Moss. Don't use saturated reds, blues or rainbow colour maps.

## Type
- **Headlines:** Bricolage Grotesque, Medium (500). Use SemiBold (600) for the wordmark.
- **Body:** IBM Plex Sans, Regular or SemiBold.
- **Labels, eyebrows and source lines:** IBM Plex Mono, set in UPPERCASE with slight letter-spacing.
- **Hindi and other Indian scripts:** Noto Sans Devanagari or the matching Noto font, rendered with shaping (Pillow + libraqm).
- The fonts are in `brand/fonts/` (SIL OFL 1.1). The Bricolage files are static instances of the variable font.

## Video (1080×1080, 30 fps, H.264, captions burned in, saved at 1.5× speed)
The timings below are the 1× timeline (45–60 s). `B.Video` saves the file at 1.5× by default, so a 58 s timeline plays in about 39 s. Use `B.Video(..., speed=1.0)` for a normal-speed cut.
1. **0–5 s hook:** the question in large Bricolage, with the last line in Moss and a mono context line beneath.
2. **5–40 s evidence:** real data from the run, with the standard header band on every frame (wordmark left, `FIELD TEST #NN` right, hairline).
3. **40–52 s headline:** the number huge in Moss, one plain sentence beneath, and a mono "How:" line.
4. **52–58 s end card:** identical in every video. It reads **23N AI Labs**, then *Applied AI research · 23°N*, then *Field Test #NN · open notebook in comments*, then **23nlabs.com**, then the stance and data credit, then the coordinates.

## Cover (1080×1350)
The wordmark and Field Test number go on top, then the title (Bricolage) and a mono subtitle. Below them sit one visual from the run, then the headline number in Moss and a caption. The footer reads 23nlabs.com, the stance and the data credit.

## Posts
- **LinkedIn:** the question, the headline, three bullets (how, result, limit), then the signature. Keep it at or under 1,300 characters.
- **Signature:** `23N Field Tests #NN · 23N AI Labs, Gandhinagar · 23nlabs.com`, then a new line with `Independent study on public data.`, then `#23NFieldTests` plus at most three topical hashtags.
- **Comments:** put the notebook link in the first comment, not the post.

## Using the kit in a notebook
```python
import urllib.request
urllib.request.urlretrieve("https://raw.githubusercontent.com/23nlabs/field-tests/main/brand/brand23n.py", "brand23n.py")
import brand23n as B
B.setup()                          # fonts + chart style
v = B.Video("ft05_video.mp4")
B.hook_card(v.fig, "05", "Your question here?", "dataset · method · scale"); v.hold(5)
v.clear(); B.header(v.fig, "05"); ...; v.frame()   # animated evidence frames
v.clear(); B.headline_card(v.fig, "05", "+42%", "One plain sentence.", "method in one line"); v.hold(12)
v.clear(); B.end_card(v.fig, "05", "Data: <source, licence>"); v.hold(6)
v.close()
B.cover("ft05_cover.png", "05", "Title", "subtitle", "+42%", "what the number means")
print(B.post_signature("05"))
```
