# -*- coding: utf-8 -*-
"""Render BaiBaiGo_mockup.html state by state with headless Edge and assemble an animated GIF.

Usage (from the repo root, on Windows with Microsoft Edge installed):
    python tools/make_gif.py [MOCKUP_HTML] [OUT_GIF]

Defaults read BaiBaiGo_mockup.html and write build/baibaigo_demo.gif.
Copy the result to assets/ when you want the deck to use it.

Run it from PowerShell or cmd. Launched from Git Bash, headless Edge may exit
without writing the screenshot.
"""
import json
import os
import subprocess
import sys
import urllib.parse
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = sys.argv[1] if len(sys.argv) > 1 else os.path.join(ROOT, "BaiBaiGo_mockup.html")
OUT = sys.argv[2] if len(sys.argv) > 2 else os.path.join(ROOT, "build", "baibaigo_demo.gif")
WORK = os.path.join(ROOT, "build", "frames")
os.makedirs(WORK, exist_ok=True)
os.makedirs(os.path.dirname(os.path.abspath(OUT)), exist_ok=True)
EDGE = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
W, H, SCALE = 380, 760, 1.5

html = open(SRC, encoding="utf-8").read()
# Freeze animations, hide the side panel, and set the screen state from the URL hash.
inject = r"""
<style>
  *, *::before, *::after { transition: none !important; animation: none !important; }
  body { padding: 0 !important; background: #fff !important; display: block !important; min-height: 0 !important; }
  .side { display: none !important; }
  .phone { box-shadow: none !important; }
  .bars i:nth-child(odd) { height: 30px !important; } .bars i:nth-child(even) { height: 16px !important; }
  .bars i:nth-child(3n) { height: 40px !important; }
  .speaking .bars i:nth-child(odd) { height: 22px !important; } .speaking .bars i:nth-child(even) { height: 12px !important; }
</style>
<script>
(function () {
  var o = JSON.parse(decodeURIComponent(location.hash.slice(1)));
  var $ = function (id) { return document.getElementById(id); };
  document.querySelectorAll(".screen").forEach(function (s) { s.classList.toggle("on", s.id === o.screen); });
  if (o.heard !== undefined) $("heard").textContent = o.heard;
  if (o.done !== undefined) Array.prototype.forEach.call($("todo").children, function (li, i) { li.classList.toggle("done", i < o.done); });
  if (o.rec) {
    $("tName").textContent = o.rec.name; $("tMeta").textContent = o.rec.meta; $("recSay").textContent = o.rec.say;
    o.rec.tags.forEach(function (t) { var s = document.createElement("span"); s.textContent = t; $("tTags").appendChild(s); });
    document.querySelector(".route").open = !!o.open;
  }
  if (o.g) {
    $("gNo").textContent = o.g.no; $("gTurn").textContent = o.g.turn; $("gDist").textContent = o.g.dist; $("gSay").textContent = o.g.say;
    $("gArrow").style.transform = "rotate(" + o.g.rot + "deg)";
    $("me").style.transform = "translate(" + o.g.x + "px," + o.g.y + "px) rotate(" + o.g.head + "deg)";
    $("nextBtn").textContent = o.g.btn;
  }
  if (o.dname) $("dName").textContent = o.dname;
})();
</script>
"""
stage = os.path.join(WORK, "stage.html")
open(stage, "w", encoding="utf-8").write(html.replace("</body>", inject + "</body>"))

REC = {"name": "新港奉天宮", "meta": "走路約 8 分鐘 · 550 公尺", "tags": ["樓梯少", "途中有 2 處座椅", "有遮蔭"],
       "say": "推薦您去新港奉天宮，走路大約八分鐘，路上樓梯很少，還有兩個地方可以坐下來休息。"}
STEPS = [
    ("直直往前走", "大約 150 公尺", 0, "請直直往前走，大約一百五十公尺。"),
    ("前面路口右轉", "轉彎後有座椅可以休息", 90, "前面路口請右轉，轉過去有椅子可以休息。"),
    ("再往前走", "大約 200 公尺", 0, "再往前走，大約兩百公尺。"),
    ("廟在您的左手邊", "從側門進去沒有樓梯", -90, "廟就在您的左手邊，從側門進去沒有樓梯。"),
]


def g(i, x, y, head):
    t, d, rot, say = STEPS[i]
    return {"screen": "s-guide", "g": {"no": "第 %d 步，共 4 步" % (i + 1), "turn": t, "dist": d, "rot": rot, "say": say,
                                       "x": x, "y": y, "head": head, "btn": "我到了" if i == 3 else "下一步"}}


def lerp(a, b, n):
    return [(a[0] + (b[0] - a[0]) * k / n, a[1] + (b[1] - a[1]) * k / n) for k in range(1, n)]


# (state, duration in ms)
frames = [({"screen": "s-home"}, 1800),
          ({"screen": "s-listen", "heard": ""}, 900),
          ({"screen": "s-listen", "heard": "「我想去拜拜」"}, 1200)]
frames += [({"screen": "s-work", "done": k}, 450 if k < 4 else 700) for k in range(5)]
frames += [({"screen": "s-rec", "rec": REC, "open": False}, 2600), ({"screen": "s-rec", "rec": REC, "open": True}, 2000)]
frames.append((g(0, 90, 470, 0), 1500))
frames += [(g(1, x, y, 0), 140) for x, y in lerp((90, 470), (90, 326), 5)]
frames.append((g(1, 90, 326, 0), 1500))
frames.append((g(2, 90, 300, 0), 140))
frames.append((g(2, 90, 300, 90), 140))
frames += [(g(2, x, y, 90), 140) for x, y in lerp((90, 300), (150, 300), 3)]
frames.append((g(2, 150, 300, 90), 1500))
frames += [(g(3, x, y, 90), 140) for x, y in lerp((150, 300), (268, 300), 5)]
frames.append((g(3, 268, 300, 90), 1700))
frames.append(({"screen": "s-done", "dname": "新港奉天宮"}, 2800))

imgs, durs = [], []
base = "file:///" + stage.replace("\\", "/")
for i, (state, ms) in enumerate(frames):
    png = os.path.join(WORK, "f%02d.png" % i)
    if os.path.exists(png):
        os.remove(png)
    url = base + "#" + urllib.parse.quote(json.dumps(state, ensure_ascii=False))
    subprocess.run([EDGE, "--headless=new", "--disable-gpu", "--hide-scrollbars", "--no-first-run",
                    "--user-data-dir=" + os.path.join(WORK, "profile"),
                    "--force-device-scale-factor=%s" % SCALE, "--window-size=%d,%d" % (W, H),
                    "--virtual-time-budget=1500", "--screenshot=" + png, url],
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=60)
    im = Image.open(png).convert("RGB")
    imgs.append(im)
    durs.append(ms)
    print(i, state["screen"], im.size, flush=True)

pal = [im.quantize(colors=128, method=Image.Quantize.MEDIANCUT, dither=Image.Dither.NONE) for im in imgs]
pal[0].save(OUT, save_all=True, append_images=pal[1:], duration=durs, loop=0, optimize=False, disposal=1)
print("gif", OUT, os.path.getsize(OUT) // 1024, "KB", len(pal), "frames", sum(durs) / 1000, "s")
