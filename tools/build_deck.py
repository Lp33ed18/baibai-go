# -*- coding: utf-8 -*-
"""Build the BaiBai Go midterm deck (.pptx) and its speaker script (.md).

Usage (from the repo root):
    python tools/build_deck.py [OUT_PPTX] [OUT_MD] [GIF]

Defaults write build/Midterm_Presentation.pptx and build/Midterm_Script.md
(build/ is git-ignored) and embed assets/baibaigo_demo.gif. Speaker notes in
the deck and the script file come from the same text below.

The committed Midterm_Presentation.pptx has a few manual edits made in
PowerPoint (title-slide member names, one heading on slide 2) that this script
does not reproduce, so do not write over it without carrying those edits.
"""
import os
import sys
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.chart.data import XyChartData
from pptx.enum.chart import XL_CHART_TYPE

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BUILD = os.path.join(ROOT, "build")
OUT_PPTX = sys.argv[1] if len(sys.argv) > 1 else os.path.join(BUILD, "Midterm_Presentation.pptx")
OUT_MD = sys.argv[2] if len(sys.argv) > 2 else os.path.join(BUILD, "Midterm_Script.md")
os.makedirs(os.path.dirname(os.path.abspath(OUT_PPTX)), exist_ok=True)
os.makedirs(os.path.dirname(os.path.abspath(OUT_MD)), exist_ok=True)
GIF = sys.argv[3] if len(sys.argv) > 3 else os.path.join(ROOT, "assets", "baibaigo_demo.gif")

RED = RGBColor(0x9E, 0x2A, 0x2B)
DARK = RGBColor(0x2B, 0x1B, 0x17)
DARK2 = RGBColor(0x40, 0x2C, 0x26)
GOLD = RGBColor(0xE0, 0x9F, 0x3E)
TINT = RGBColor(0xF8, 0xEF, 0xE9)
GOLDT = RGBColor(0xFB, 0xEC, 0xD2)
GRAY = RGBColor(0x5F, 0x57, 0x54)
LGRAY = RGBColor(0xE9, 0xE4, 0xE1)
WHITE = RGBColor(0xFF, 0xFF, 0xFF)
HEAD, BODY = "Cambria", "Calibri"

prs = Presentation()
prs.slide_width, prs.slide_height = Inches(13.333), Inches(7.5)
TITLE_ONLY = prs.slide_layouts[5]


def box(s, x, y, w, h, fill=TINT, rounded=True, name=None):
    shp = s.shapes.add_shape(
        MSO_SHAPE.ROUNDED_RECTANGLE if rounded else MSO_SHAPE.RECTANGLE,
        Inches(x), Inches(y), Inches(w), Inches(h))
    if rounded:
        shp.adjustments[0] = 0.08
    shp.fill.solid()
    shp.fill.fore_color.rgb = fill
    shp.line.fill.background()
    shp.shadow.inherit = False
    if name:
        shp.name = name
    return shp


def text(s, x, y, w, h, paras, size=14, color=DARK, bold=False, align=PP_ALIGN.LEFT,
         anchor=MSO_ANCHOR.TOP, font=BODY, italic=False, space=4):
    """paras: str | list of (str | list of (text, {opts}))"""
    t = s.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    tf = t.text_frame
    tf.word_wrap = True
    tf.vertical_anchor = anchor
    for m in ("margin_left", "margin_right", "margin_top", "margin_bottom"):
        setattr(tf, m, Inches(0.04))
    if isinstance(paras, str):
        paras = [paras]
    for i, p in enumerate(paras):
        para = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        para.alignment = align
        para.space_after = Pt(space)
        runs = [(p, {})] if isinstance(p, str) else p
        for rt, o in runs:
            r = para.add_run()
            r.text = rt
            f = r.font
            f.name = o.get("font", font)
            f.size = Pt(o.get("size", size))
            f.bold = o.get("bold", bold)
            f.italic = o.get("italic", italic)
            f.color.rgb = o.get("color", color)
    return t


def badge(s, x, y, label, d=0.5, fill=RED, color=WHITE, size=16):
    c = s.shapes.add_shape(MSO_SHAPE.OVAL, Inches(x), Inches(y), Inches(d), Inches(d))
    c.fill.solid()
    c.fill.fore_color.rgb = fill
    c.line.fill.background()
    c.shadow.inherit = False
    tf = c.text_frame
    for m in ("margin_left", "margin_right", "margin_top", "margin_bottom"):
        setattr(tf, m, 0)
    tf.vertical_anchor = MSO_ANCHOR.MIDDLE
    p = tf.paragraphs[0]
    p.alignment = PP_ALIGN.CENTER
    r = p.add_run()
    r.text = label
    r.font.size, r.font.bold, r.font.name = Pt(size), True, HEAD
    r.font.color.rgb = color
    return c


def arrow(s, x, y, w=0.22, h=0.3, fill=GOLD):
    a = s.shapes.add_shape(MSO_SHAPE.CHEVRON, Inches(x), Inches(y), Inches(w), Inches(h))
    a.fill.solid()
    a.fill.fore_color.rgb = fill
    a.line.fill.background()
    a.shadow.inherit = False
    return a


def frame(sl, x, y, w, h, label):
    f = sl.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(x), Inches(y), Inches(w), Inches(h))
    f.adjustments[0] = 0.05
    f.fill.background()
    f.line.color.rgb = GOLD
    f.line.width = Pt(2)
    f.shadow.inherit = False
    text(sl, x + 0.25, y + 0.08, w - 0.5, 0.5, label, size=20, bold=True, color=RED, font=HEAD, anchor=MSO_ANCHOR.MIDDLE)


def new_slide(title, notes, dark=False):
    s = prs.slides.add_slide(TITLE_ONLY)
    if dark:
        bg = s.background.fill
        bg.solid()
        bg.fore_color.rgb = DARK
    t = s.shapes.title
    t.left, t.top, t.width, t.height = Inches(0.6), Inches(0.4), Inches(12.13), Inches(0.9)
    tf = t.text_frame
    tf.word_wrap = True
    tf.vertical_anchor = MSO_ANCHOR.MIDDLE
    tf.margin_left = Inches(0.04)
    tf.text = title
    p = tf.paragraphs[0]
    p.alignment = PP_ALIGN.LEFT
    r = p.runs[0]
    r.font.name, r.font.size, r.font.bold = HEAD, Pt(34), True
    r.font.color.rgb = WHITE if dark else DARK
    s.notes_slide.notes_text_frame.text = notes
    return s


SCRIPT = []  # (title, time, speaker, notes)


def add(title, time, speaker, notes, dark=False):
    SCRIPT.append((title, time, speaker, notes))
    return new_slide(title, notes, dark)


# ---------------------------------------------------------------- 1 Title
n1 = ("Good morning, everyone. Our final project is called BaiBai Go, a voice-first temple route "
      "companion for seniors. \"Bai-bai\" is how people in Taiwan say going to the temple to pray. "
      "In the next ten minutes we will introduce the problem, the methods we plan to use, how our "
      "five members share the work, and how the project connects to the USR competition.")
SCRIPT.append(("Title", "0:20", "Member E", n1))
s = prs.slides.add_slide(TITLE_ONLY)
s.background.fill.solid()
s.background.fill.fore_color.rgb = DARK
for d, x, y, col in ((5.2, 9.3, -1.2, DARK2), (3.0, 11.2, 4.9, DARK2), (1.1, 9.6, 4.3, GOLD)):
    c = s.shapes.add_shape(MSO_SHAPE.OVAL, Inches(x), Inches(y), Inches(d), Inches(d))
    c.fill.solid(); c.fill.fore_color.rgb = col; c.line.fill.background(); c.shadow.inherit = False
t = s.shapes.title
t.left, t.top, t.width, t.height = Inches(0.8), Inches(2.0), Inches(8.6), Inches(1.3)
t.text_frame.text = "BaiBai Go"
t.text_frame.vertical_anchor = MSO_ANCHOR.BOTTOM
p = t.text_frame.paragraphs[0]; p.alignment = PP_ALIGN.LEFT
r = p.runs[0]; r.font.name, r.font.size, r.font.bold = HEAD, Pt(66), True; r.font.color.rgb = WHITE
text(s, 0.8, 3.4, 8.4, 1.0, "A Voice-First Temple Route Companion for Seniors", size=26, color=GOLD, font=HEAD)
text(s, 0.8, 4.5, 8.4, 0.5, "Introduction to Multimedia Technologies  ·  Midterm Presentation", size=16, color=WHITE)
text(s, 0.8, 6.2, 8.4, 0.5, "Member A  ·  Member B  ·  Member C  ·  Member D  ·  Member E", size=16, color=LGRAY)
s.notes_slide.notes_text_frame.text = n1

# ---------------------------------------------------------------- 2 Problem
s = add("Seniors want to visit temples, but the trip is hard", "1:20", "Member E",
        "Many seniors in Taiwan love going to the temple. It is a habit, a social event, and for many "
        "of them it is the main reason to leave the house. But they often give up, for three simple "
        "reasons: they are not sure about the route, there are too many stairs, or they are afraid it "
        "is too far to walk. When they stop going, they also lose exercise and social contact.\n\n"
        "A map app could help, but typing and reading small text is difficult for them. Voice is the "
        "most natural interface: just say, \"I want to go to the temple.\"\n\n"
        "However, a voice assistant often fails in exactly this situation. Outdoors there is traffic, "
        "wind and temple music. Seniors often speak softly or hold the phone far away. And many of "
        "them have age-related hearing loss, so they cannot clearly hear the spoken answer.\n\n"
        "So our problem is not only route recommendation. It is how to make the voice channel itself "
        "work for seniors, in both directions. This idea comes from the Sinyi Charity Foundation's "
        "Gather Ideas platform.")
text(s, 0.6, 1.5, 3.7, 0.6, "Why seniors go out less", size=20, bold=True, color=RED, font=HEAD)
for i, (h, d) in enumerate((("Unfamiliar routes", "Not sure which way is easiest or safest"),
                            ("Too many stairs", "Steps on the way or at the gate"),
                            ("Fear of walking too far", "No idea where to rest or catch a bus"))):
    y = 2.2 + i * 1.3
    badge(s, 0.6, y + 0.1, str(i + 1))
    text(s, 1.25, y, 3.05, 1.2, [[(h, {"bold": True, "size": 18})], [(d, {"color": GRAY})]], size=16)
arrow(s, 4.38, 3.85, w=0.3, h=0.45)
text(s, 4.8, 1.5, 3.7, 0.6, "Our idea: ask by voice", size=20, bold=True, color=RED, font=HEAD)
box(s, 4.8, 2.2, 3.7, 3.75, fill=RED)
text(s, 5.05, 2.4, 3.2, 1.9, "“I want to go to the temple.”", size=26, bold=True, color=WHITE, font=HEAD)
text(s, 5.05, 4.35, 3.2, 1.5, ["One big voice button comes first.", "Typing and menus stay, as secondary options."],
     size=18, color=WHITE)
arrow(s, 8.6, 3.85, w=0.3, h=0.45)
text(s, 9.03, 1.5, 3.7, 0.6, "But voice fails outdoors", size=20, bold=True, color=RED, font=HEAD)
for i, (h, d) in enumerate((("Noisy surroundings", "Traffic, wind, temple music"),
                            ("Soft, distant voices", "Phone held far from the mouth"),
                            ("Age-related hearing loss", "High frequencies fade with age"))):
    y = 2.2 + i * 1.3
    box(s, 9.03, y, 3.7, 1.15)
    text(s, 9.2, y + 0.1, 3.4, 1.0, [[(h, {"bold": True, "size": 18})], [(d, {"color": GRAY})]], size=16)
text(s, 0.6, 6.45, 12.1, 0.5,
     "Idea source: Sinyi Charity Foundation, Gather Ideas platform, \"長輩專屬拜拜路線推薦\" (Senior-friendly temple route recommendation)",
     size=12, color=GRAY, italic=True)

# ---------------------------------------------------------------- 3 Objectives
s = add("Three objectives, one for each step of a conversation", "0:50", "Member E",
        "We set three objectives, and each one matches one step of a conversation.\n\n"
        "First, speak naturally. A senior should be able to ask in everyday words, with one big "
        "voice button as the main entry. Typing and menus are still available, but only as "
        "secondary options, so that new features can be added later.\n\n"
        "Second, be understood in noise. Before the recording goes to a speech recognition service, "
        "we clean it with our own audio pre-processing.\n\n"
        "Third, hear the answer clearly. Before the answer is played, we adjust the synthesized voice "
        "for older ears.\n\n"
        "The second and third objectives are where we apply what we learned in this course about "
        "digital audio.")
cols = (("1", "Speak naturally", "One big voice button comes first. Typing and menus stay as secondary options.", "App design"),
        ("2", "Be understood in noise", "Clean the recording before it reaches the speech recognition API.", "Input pre-processing"),
        ("3", "Hear the answer clearly", "Adapt the synthesized voice for older ears before playback.", "Output processing"))
for i, (n, h, d, tag) in enumerate(cols):
    x = 0.6 + i * 4.18
    box(s, x, 1.6, 3.77, 4.6)
    text(s, x + 0.3, 1.75, 3.2, 1.3, n, size=72, bold=True, color=RED, font=HEAD)
    text(s, x + 0.3, 3.1, 3.2, 0.6, h, size=22, bold=True, font=HEAD)
    text(s, x + 0.3, 4.1, 3.2, 1.2, d, size=16, color=GRAY)
    box(s, x + 0.3, 5.35, 3.17, 0.5, fill=RED if i else GRAY)
    text(s, x + 0.3, 5.35, 3.17, 0.5, tag, size=14, bold=True, color=WHITE, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)

# ---------------------------------------------------------------- 4 Scenario & pipeline
s = add("How it works: from microphone to speaker", "1:00", "Member A",
        "Here is a typical scenario. Grandma presses the big button and says, \"I want to go to the "
        "temple.\" The app recommends a nearby temple and a route with few stairs and places to rest. "
        "Everything after her request runs automatically. The app reads the directions aloud as the "
        "main guidance, and the route on the screen is a secondary aid. When she arrives, her family can receive a short "
        "safe-arrival message.\n\n"
        "Below is the system pipeline. The sound from the microphone first goes through our input "
        "pre-processing. Then we call an existing speech-to-text API. The app logic finds the intent "
        "and recommends a temple and a route. The reply is turned into speech by an existing "
        "text-to-speech API, and finally it goes through our output processing before it reaches the "
        "speaker.\n\n"
        "The two red blocks are what we implement ourselves. The gray blocks are off-the-shelf "
        "services. With about six weeks, we do not want to rebuild speech recognition. We want to "
        "make existing recognition work better for seniors.")
frame(s, 0.6, 1.45, 12.13, 2.35, "User flow")
steps = (("Ask", "\"I want to go to the temple.\""), ("Recommend", "A nearby temple and a low-barrier route"),
         ("Guide", "Spoken directions first, on-screen route second"), ("Arrive safely", "A short message tells the family"))
for i, (h, d) in enumerate(steps):
    x = 0.85 + i * 2.993
    box(s, x, 2.1, 2.65, 1.5)
    badge(s, x + 0.15, 2.2, str(i + 1), d=0.45, size=14)
    text(s, x + 0.7, 2.18, 1.9, 0.5, h, size=19, bold=True, font=HEAD, anchor=MSO_ANCHOR.MIDDLE)
    text(s, x + 0.15, 2.75, 2.4, 0.8, d, size=16, color=GRAY)
    if i < 3:
        arrow(s, x + 2.71, 2.7)
frame(s, 0.6, 3.95, 12.13, 2.75, "System pipeline")
pipe = (("Microphone", 0), ("Input pre-processing", 1), ("Speech-to-Text API", 0), ("App logic: intent and route", 0),
        ("Text-to-Speech API", 0), ("Output processing", 1), ("Speaker", 0))
for i, (lab, ours) in enumerate(pipe):
    x = 0.85 + i * 1.697
    box(s, x, 4.6, 1.45, 1.15, fill=RED if ours else LGRAY)
    text(s, x, 4.6, 1.45, 1.15, lab, size=15, bold=True, color=WHITE if ours else DARK,
         align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
    if i < 6:
        arrow(s, x + 1.48, 5.025, w=0.18)
box(s, 0.85, 6.05, 0.3, 0.3, fill=RED, rounded=False)
text(s, 1.25, 5.95, 5.0, 0.5, "Implemented by our team", size=16, anchor=MSO_ANCHOR.MIDDLE)
box(s, 6.9, 6.05, 0.3, 0.3, fill=LGRAY, rounded=False)
text(s, 7.3, 5.95, 5.2, 0.5, "Off-the-shelf services and app code", size=16, anchor=MSO_ANCHOR.MIDDLE)

# ---------------------------------------------------------------- 5 Prototype preview
s = add("Prototype preview: what the senior sees", "0:30", "Member E",
        "This short animation is a front-end mockup of the app, with demo data. The senior presses "
        "the big voice button and speaks. The app works automatically and reads the recommendation "
        "aloud. During the walk, the map shows the current position and the route, with a large turn "
        "card and spoken guidance on top. At the end, the family receives a safe-arrival message.")
pic = s.shapes.add_picture(GIF, Inches(1.5), Inches(1.5), height=Inches(5.5))
pic.name = "Prototype animation"
pic._element.nvPicPr.cNvPr.set("descr", "Animated mockup of the BaiBai Go app: ask by voice, recommendation, map guidance, safe arrival")
demo = (("Ask", "One big voice button; typing and menus are secondary"),
        ("Recommend", "The answer is read aloud first; the card and route come second"),
        ("Guide", "A map with the current position and route, plus a turn card and spoken guidance"),
        ("Arrive safely", "A message tells the family"))
for i, (h, d) in enumerate(demo):
    y = 1.5 + i * 1.2
    box(s, 5.3, y, 7.43, 1.05)
    badge(s, 5.5, y + 0.28, str(i + 1))
    text(s, 6.2, y + 0.04, 6.4, 1.0, [[(h, {"bold": True, "size": 20, "font": HEAD})], [(d, {"color": GRAY})]],
         size=17, space=0, anchor=MSO_ANCHOR.MIDDLE)
text(s, 5.3, 6.4, 7.43, 0.6, "Front-end mockup with demo data. The animation plays in slideshow mode.",
     size=14, color=GRAY, italic=True)

# ---------------------------------------------------------------- 6 Input
s = add("Methods 1: Cleaning the voice before recognition", "1:30", "Member B",
        "Now the input side. We plan four steps before calling the speech recognition API.\n\n"
        "Step one, format conversion. We convert the recording to 16 kilohertz, 16-bit, mono. As we "
        "learned from the Nyquist theorem, 16 kilohertz can represent frequencies up to 8 kilohertz, "
        "which covers speech and is the usual rate for speech recognition.\n\n"
        "Step two, voice activity detection. We split the signal into short frames and compute the "
        "energy of each frame in decibels. Frames below a threshold are treated as silence and "
        "removed, so the API receives only speech.\n\n"
        "Step three, noise reduction, which is the core. We use spectral subtraction. Each frame is "
        "multiplied by a Hamming window to reduce spectral leakage, and transformed with the FFT. We "
        "estimate the noise spectrum from the silent frames, subtract it from the magnitude, keep "
        "the original phase, and go back to the time domain with the inverse FFT and overlap-add.\n\n"
        "Step four, level normalization. Seniors often speak softly, so we raise the level to a "
        "target in decibels without clipping the 16-bit range.\n\n"
        "All four steps use concepts from Unit 4, and we will implement them ourselves in Python.")
cards = (("Format conversion", "Resample to 16 kHz, 16-bit, mono"),
         ("Voice activity detection", "Frame energy in dB; drop silent frames"),
         ("Noise reduction", "Spectral subtraction using noise from silent frames"),
         ("Level normalization", "Raise soft voices to a target level without clipping"))
for i, (h, d) in enumerate(cards):
    x = 0.6 + i * 3.13
    box(s, x, 1.55, 2.75, 3.1)
    badge(s, x + 0.2, 1.7, str(i + 1), d=0.45, size=14)
    text(s, x + 0.2, 2.25, 2.45, 0.9, h, size=22, bold=True, font=HEAD)
    text(s, x + 0.2, 3.25, 2.45, 1.3, d, size=18, color=GRAY)
    if i < 3:
        arrow(s, x + 2.83, 2.95)
text(s, 0.6, 4.9, 12.1, 0.5, "Step 3 in detail: spectral subtraction", size=20, bold=True, color=RED, font=HEAD)
sub = ("Split into frames", "Hamming window", "FFT", "Subtract noise magnitude", "Inverse FFT", "Overlap-add")
for i, lab in enumerate(sub):
    x = 0.6 + i * 2.076
    box(s, x, 5.55, 1.75, 1.0, fill=RED if i == 3 else LGRAY)
    text(s, x, 5.55, 1.75, 1.0, lab, size=16, bold=True, color=WHITE if i == 3 else DARK,
         align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
    if i < 5:
        arrow(s, x + 1.80, 5.9)

# ---------------------------------------------------------------- 7 Output
s = add("Methods 2: Shaping the reply for older ears", "1:10", "Member C",
        "On the output side, the text-to-speech API gives us a clean voice, but it is designed for "
        "normal hearing.\n\n"
        "Age-related hearing loss mainly affects high frequencies. Those frequencies carry consonants "
        "such as s, t and k, so speech sounds loud enough but unclear. Our first step is a hearing "
        "compensation equalizer. We transform the signal to the frequency domain, apply more gain "
        "roughly between one and four kilohertz, and transform it back. The curve on the right is our "
        "starting target. We will tune it after listening tests with seniors.\n\n"
        "Second, loudness normalization. Every sentence is adjusted to the same level in decibels, so "
        "the guidance is consistently loud outdoors.\n\n"
        "Third, we slow down the speaking rate. This is only a parameter of the API, so it is not our "
        "own processing, but it matters for seniors.")
outs = (("Hearing compensation EQ", "Boost about 1 to 4 kHz in the frequency domain, where consonants live", RED),
        ("Loudness normalization", "Bring every sentence to the same level so guidance stays audible outdoors", RED),
        ("Slower speaking rate", "Set through the text-to-speech API; not our own processing", GRAY))
for i, (h, d, col) in enumerate(outs):
    y = 1.55 + i * 1.65
    box(s, 0.6, y, 6.0, 1.5)
    badge(s, 0.8, y + 0.2, str(i + 1), d=0.45, size=14, fill=col)
    text(s, 1.45, y + 0.08, 5.0, 1.4, [[(h, {"bold": True, "size": 22, "font": HEAD})], [(d, {"color": GRAY})]],
         size=18, space=2)
cd = XyChartData()
ser = cd.add_series("Planned gain (dB)")
for f, g in ((0.25, 0), (0.5, 0), (1, 2), (2, 6), (3, 8), (4, 8), (6, 5), (8, 3)):
    ser.add_data_point(f, g)
gf = s.shapes.add_chart(XL_CHART_TYPE.XY_SCATTER_SMOOTH_NO_MARKERS, Inches(7.0), Inches(1.55), Inches(5.73), Inches(4.3), cd)
ch = gf.chart
ch.has_legend = False
ch.has_title = True
ch.chart_title.text_frame.text = "Planned EQ target: gain (dB) by frequency (kHz)"
tr = ch.chart_title.text_frame.paragraphs[0].runs[0]
tr.font.size, tr.font.bold, tr.font.name = Pt(16), True, BODY
tr.font.color.rgb = DARK
ch.plots[0].series[0].format.line.color.rgb = RED
ch.plots[0].series[0].format.line.width = Pt(3)
va, ca = ch.value_axis, ch.category_axis
va.minimum_scale, va.maximum_scale, va.major_unit = 0, 10, 2
ca.minimum_scale, ca.maximum_scale, ca.major_unit = 0, 8, 1
for ax in (va, ca):
    ax.tick_labels.font.size = Pt(14)
    ax.tick_labels.font.color.rgb = GRAY
    ax.format.line.color.rgb = LGRAY
va.major_gridlines.format.line.color.rgb = LGRAY
ca.has_major_gridlines = False
text(s, 7.0, 5.9, 5.73, 0.8, "Illustrative starting curve, not measured data. To be tuned with listening tests.",
     size=14, color=GRAY, italic=True)

# ---------------------------------------------------------------- 8 Recommendation
s = add("Methods 3: Route recommendation", "0:45", "Member D",
        "After recognition, the app turns the text into a recommendation. We keep this part simple.\n\n"
        "We extract the intent with keyword rules, with a language model as a backup. Temple data "
        "comes from government open data and OpenStreetMap, limited to Minxiong and Xingang in "
        "Chiayi. We will add a few labels by hand, such as whether the entrance has stairs and "
        "whether there are benches.\n\n"
        "Each candidate gets a score: distance and stairs increase the cost, benches reduce it. The "
        "weights change with the user's mobility, for example if they use a cane. A safe-arrival "
        "message to the family is our stretch goal.")
box(s, 0.6, 1.55, 12.13, 1.2, fill=DARK)
text(s, 0.6, 1.55, 12.13, 1.2, "cost = w1·distance + w2·stairs − w3·benches", size=28, bold=True, color=WHITE,
     font=HEAD, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
recs = (("Intent", "Keyword rules, with a language model as backup"),
        ("Data", "Government open data and OpenStreetMap; Minxiong and Xingang only"),
        ("Manual labels", "Stairs at the entrance, benches nearby"),
        ("Weights", "Adjusted to the user's mobility, such as using a cane"))
for i, (h, d) in enumerate(recs):
    x = 0.6 + (i % 2) * 6.215
    y = 3.0 + (i // 2) * 1.45
    box(s, x, y, 5.915, 1.3)
    text(s, x + 0.25, y + 0.08, 5.4, 1.2, [[(h, {"bold": True, "size": 20, "font": HEAD})], [(d, {"color": GRAY})]],
         size=18, space=2)
box(s, 0.6, 5.9, 12.13, 0.7, fill=GOLDT)
text(s, 0.85, 5.9, 11.6, 0.7, [[("Stretch goal: ", {"bold": True}), ("a safe-arrival message to the family", {})]],
     size=18, anchor=MSO_ANCHOR.MIDDLE)

# ---------------------------------------------------------------- 9 Evaluation
s = add("Evaluation: does pre-processing help?", "0:45", "Member C",
        "How do we know our processing really helps? We will measure it.\n\n"
        "We will record twenty to thirty spoken commands in real places, such as a temple courtyard "
        "and a roadside. Each recording is sent to the same speech-to-text API twice: once raw, and "
        "once after our pre-processing. Then we compare the character error rate of the two "
        "results.\n\n"
        "We will also show waveforms and spectrograms before and after, and on the output side we "
        "will ask a few seniors which voice is clearer.")
box(s, 0.6, 1.55, 12.13, 0.9, fill=GOLDT)
text(s, 0.6, 1.55, 12.13, 0.9, "20 to 30 commands recorded on site, with real background noise", size=20, bold=True,
     align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
for j, (a_, b_, col) in enumerate((("Raw audio", "Character error rate (baseline)", LGRAY),
                                   ("Pre-processed audio", "Character error rate (ours)", RED))):
    y = 2.75 + j * 1.15
    fg = WHITE if col == RED else DARK
    for k, (lab, w, x) in enumerate(((a_, 4.2, 0.6), ("Same speech-to-text API", 3.2, 5.1), (b_, 4.13, 8.6))):
        box(s, x, y, w, 0.95, fill=col if k != 1 else LGRAY)
        text(s, x, y, w, 0.95, lab, size=18, bold=True, color=fg if k != 1 else DARK,
             align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
    arrow(s, 4.85, y + 0.325, w=0.2)
    arrow(s, 8.35, y + 0.325, w=0.2)
for i, (h, d) in enumerate((("Before and after", "Waveforms and spectrograms of the same recording"),
                            ("Output side", "A short listening survey with seniors"))):
    x = 0.6 + i * 6.215
    box(s, x, 5.2, 5.915, 1.3)
    text(s, x + 0.25, 5.28, 5.4, 1.2, [[(h, {"bold": True, "size": 20, "font": HEAD})], [(d, {"color": GRAY})]],
         size=18, space=2)

# ---------------------------------------------------------------- 10 Team & timeline
s = add("Team responsibilities and six-week plan", "0:55", "Member A",
        "Here is how the five of us share the work.\n\n"
        "Member A is the project lead and handles the architecture, the backend, and the connection "
        "to the speech APIs. Member B builds the input pre-processing: resampling, voice activity "
        "detection, noise reduction and normalization. Member C builds the output processing and "
        "runs the evaluation experiments. Member D handles the app logic, the temple data and the "
        "scoring. Member E designs the big-button interface, leads the field recording and the "
        "trials with seniors, and prepares the USR documents.\n\n"
        "We have about six weeks. In week one we record test audio and prepare data. In weeks two "
        "and three we finish the two audio modules offline. In week four we build the end-to-end "
        "prototype, in week five we test on site, and in week six we prepare the demo.")
team = (("A", "Lead and integration", "Architecture, backend, speech API integration"),
        ("B", "Audio input", "Resampling, VAD, spectral subtraction, normalization"),
        ("C", "Audio output and evaluation", "Hearing EQ, loudness; test recordings, error rate"),
        ("D", "App logic and data", "Intent extraction, temple data, route scoring"),
        ("E", "Interface and field study", "Big-button UI, field recording, senior trials, USR docs"))
for i, (l, h, d) in enumerate(team):
    y = 1.5 + i * 1.02
    box(s, 0.6, y, 7.0, 0.92)
    badge(s, 0.78, y + 0.21, l, d=0.5)
    text(s, 1.5, y + 0.02, 6.0, 0.9, [[(h, {"bold": True, "size": 19, "font": HEAD})], [(d, {"color": GRAY})]],
         size=16, space=0, anchor=MSO_ANCHOR.MIDDLE)
box(s, 7.9, 1.5, 4.83, 5.0, fill=DARK)
text(s, 8.15, 1.6, 4.3, 0.5, "Six-week plan", size=20, bold=True, color=GOLD, font=HEAD)
plan = (("Week 1", "Field recordings, temple data, API choice"), ("Weeks 2–3", "Input and output modules, offline in Python"),
        ("Week 4", "End-to-end prototype with interface"), ("Week 5", "On-site tests, error-rate comparison"),
        ("Week 6", "Demo video and final presentation"))
for i, (w, d) in enumerate(plan):
    y = 2.2 + i * 0.85
    text(s, 8.15, y, 4.4, 0.8, [[(w, {"bold": True, "color": GOLD, "size": 16})], [(d, {"color": WHITE})]],
         size=16, space=0)

# ---------------------------------------------------------------- 11 USR
s = add("Connection to the USR competition", "0:55", "Member E",
        "Finally, the connection to the USR competition, whose theme is co-creating a happy life "
        "for seniors.\n\n"
        "First, social participation. Going to the temple is something seniors already want to do, "
        "so we lower the barrier of an existing habit instead of teaching a new one.\n\n"
        "Second, digital inclusion. The app is voice-first, so reading and typing are not required, "
        "and the audio is adapted to seniors, not the other way around.\n\n"
        "Third, local co-creation. Our test recordings and trials come from seniors and temples in "
        "Chiayi, so the community helps shape the system.\n\n"
        "Fourth, family connection. A safe-arrival message gives family members peace of mind.\n\n"
        "In short, we use digital audio techniques from this course to help seniors keep doing "
        "something they love. Thank you. We are happy to take questions.", dark=True)
usr = (("Social participation", "Lower the barrier to a habit seniors already love, so they keep going out"),
       ("Digital inclusion", "Voice-first, no reading or typing; audio adapted to seniors, not the reverse"),
       ("Local co-creation", "Recordings and trials with seniors and temples in Chiayi"),
       ("Family connection", "A safe-arrival message gives families peace of mind"))
for i, (h, d) in enumerate(usr):
    x = 0.6 + (i % 2) * 6.215
    y = 1.6 + (i // 2) * 2.05
    box(s, x, y, 5.915, 1.8, fill=DARK2)
    badge(s, x + 0.3, y + 0.3, str(i + 1), fill=GOLD, color=DARK)
    text(s, x + 1.05, y + 0.2, 4.65, 1.55, [[(h, {"bold": True, "size": 24, "font": HEAD, "color": GOLD})],
                                            [(d, {"color": WHITE})]], size=18)
text(s, 0.6, 6.0, 12.1, 0.7, "Thank you. Questions are welcome.", size=24, bold=True, color=WHITE, font=HEAD)

prs.save(OUT_PPTX)

# ---------------------------------------------------------------- script markdown
words = sum(len(n.split()) for *_, n in SCRIPT)
md = ["# BaiBai Go — Midterm Presentation Script", "",
      f"Total: about {words} words, 10 minutes. Speakers are suggestions; replace Member A–E with real names.", ""]
for i, (t, tm, sp, n) in enumerate(SCRIPT, 1):
    md += [f"## Slide {i} — {t}", "", f"**Time:** {tm}  |  **Suggested speaker:** {sp}  |  **Words:** {len(n.split())}", "", n, ""]
open(OUT_MD, "w", encoding="utf-8").write("\n".join(md))
print("slides", len(prs.slides), "words", words)
