#!/usr/bin/env python3
"""Render the entry video for "The agent builds a game from one prompt".

Scenes (1920x1080, 30 fps), all drawn frame by frame with PIL:
  1. The prompt      — a chat bubble types out the one prompt.
  2. The agent works — the game's code types into an editor while
                       a checklist ticks off: canvas, ghost, coins,
                       blocks, score.
  3. The game        — Ghost Grab actually playing: the ghost hunts
                       star coins, red blocks rain, the score climbs.
  4. The call        — one line over the frozen game.
The official make.fun referral end card is NOT drawn here: the
assembly step appends the press pack's own card video untouched,
with the referral code typed into its field.

Run:  python3 make_video.py   (writes frames/ and scene clips)
"""

import math
import os
import random
import subprocess

from PIL import Image, ImageDraw, ImageFont

W, H, FPS = 1920, 1080, 30
HERE = os.path.dirname(os.path.abspath(__file__))
FRAMES = os.path.join(HERE, "frames")
os.makedirs(FRAMES, exist_ok=True)

FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
MONO = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"
MONO_B = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf"


def f(path, size):
    return ImageFont.truetype(path, size)


BG = (20, 16, 28)
PANEL = (29, 20, 48)
MAGENTA = (194, 24, 139)
WHITE = (245, 240, 250)
DIM = (185, 168, 217)
GOLD = (255, 207, 63)
RED = (229, 72, 77)

PROMPT = ("build me a tiny browser game: a ghost that grabs star coins "
          "and dodges red blocks — arrow keys, 60 seconds, high score wins")

CODE_LINES = [
    "const ghost = { x: 400, y: 250, r: 22 };",
    "function drawGhost(x, y, r) { /* white, round, brave */ }",
    "coins.forEach(drawCoin);          // +10 each",
    "blocks.forEach(b => b.y += b.vy); // dodge these",
    "if (hit) { score += 10; spawnCoin(); }",
    "hud.textContent = `Score: ${score}`;",
    "requestAnimationFrame(step);      // 60 fps, one file",
]
CHECKS = ["canvas 800x500", "the ghost", "star coins", "red blocks",
          "score + timer"]


def wrap(draw, text, font, maxw):
    words, lines, cur = text.split(), [], ""
    for w_ in words:
        t = (cur + " " + w_).strip()
        if draw.textlength(t, font=font) <= maxw:
            cur = t
        else:
            lines.append(cur)
            cur = w_
    if cur:
        lines.append(cur)
    return lines


def ghost(draw, x, y, r):
    pts = []
    for i in range(25):
        a = math.pi + i * math.pi / 24
        pts.append((x + r * math.cos(a), y - r * 0.2 + r * math.sin(a)))
    pts += [(x + r, y + r), (x + r * 0.66, y + r * 0.7), (x + r * 0.33, y + r),
            (x, y + r * 0.7), (x - r * 0.33, y + r), (x - r * 0.66, y + r * 0.7),
            (x - r, y + r)]
    draw.polygon(pts, fill=WHITE)
    for dx in (-0.35, 0.35):
        draw.ellipse([x + dx * r - r * 0.13, y - r * 0.38,
                      x + dx * r + r * 0.13, y - r * 0.12], fill=BG)


def star(draw, x, y, r, color=GOLD):
    pts = []
    for i in range(10):
        a = -math.pi / 2 + i * math.pi / 5
        rad = r * 0.45 if i % 2 else r
        pts.append((x + rad * math.cos(a), y + rad * math.sin(a)))
    draw.polygon(pts, fill=color)


def save(img, idx):
    img.save(os.path.join(FRAMES, f"f{idx:05d}.png"))


def scene_prompt(start):
    idx = start
    total = 5 * FPS
    font_t = f(BOLD, 92)
    font_p = f(FONT, 44)
    for n in range(total):
        img = Image.new("RGB", (W, H), BG)
        d = ImageDraw.Draw(img)
        t = n / FPS
        if t > 0.4:
            txt = "ONE PROMPT."
            d.text((140, 120), txt, font=font_t, fill=WHITE)
            d.text((140, 240), "that's all it took:", font=f(FONT, 48), fill=DIM)
        # chat bubble
        bx, by, bw = 140, 420, 1500
        chars = int(max(0, (t - 1.0)) * 55)
        shown = PROMPT[:chars]
        lines = wrap(d, shown, font_p, bw - 80) or [""]
        bh = 70 + 58 * len(lines)
        d.rounded_rectangle([bx, by, bx + bw, by + bh], 28, fill=PANEL,
                            outline=MAGENTA, width=4)
        for i, ln in enumerate(lines):
            d.text((bx + 40, by + 32 + i * 58), ln, font=font_p, fill=WHITE)
        if chars < len(PROMPT) and t > 1.0:
            cx = bx + 40 + d.textlength(lines[-1], font=font_p)
            d.rectangle([cx + 6, by + 36 + (len(lines) - 1) * 58,
                         cx + 30, by + 82 + (len(lines) - 1) * 58], fill=GOLD)
        save(img, idx)
        idx += 1
    return idx


def scene_code(start):
    idx = start
    total = 8 * FPS
    font_c = f(MONO, 40)
    font_h = f(BOLD, 54)
    font_k = f(FONT, 46)
    for n in range(total):
        img = Image.new("RGB", (W, H), BG)
        d = ImageDraw.Draw(img)
        t = n / FPS
        d.text((140, 90), "…and the agent just builds it", font=font_h, fill=WHITE)
        # editor window
        ex, ey, ew, eh = 140, 220, 1180, 700
        d.rounded_rectangle([ex, ey, ex + ew, ey + eh], 20, fill=(24, 18, 38),
                            outline=(70, 55, 110), width=3)
        d.rounded_rectangle([ex, ey, ex + ew, ey + 64], 20, fill=(38, 28, 62))
        d.rectangle([ex, ey + 40, ex + ew, ey + 64], fill=(38, 28, 62))
        d.text((ex + 30, ey + 12), "ghost-grab.html", font=f(MONO, 34), fill=DIM)
        typed = (t / 7.0) * sum(len(l) + 1 for l in CODE_LINES)
        used = 0
        for i, ln in enumerate(CODE_LINES):
            y = ey + 110 + i * 76
            take = max(0, min(len(ln), int(typed - used)))
            used += len(ln) + 1
            if take > 0:
                d.text((ex + 40, y), ln[:take], font=font_c,
                       fill=(168, 230, 170) if i % 2 else (240, 220, 160))
        # checklist
        kx = 1400
        d.text((kx, 240), "building:", font=f(BOLD, 44), fill=WHITE)
        for i, item in enumerate(CHECKS):
            y = 330 + i * 92
            done = t > 1.2 + i * 1.25
            box = [kx, y, kx + 46, y + 46]
            d.rounded_rectangle(box, 8, outline=MAGENTA, width=4)
            if done:
                d.line([kx + 9, y + 24, kx + 19, y + 35], fill=GOLD, width=6)
                d.line([kx + 19, y + 35, kx + 38, y + 10], fill=GOLD, width=6)
            d.text((kx + 66, y - 4), item, font=font_k,
                   fill=WHITE if done else DIM)
        save(img, idx)
        idx += 1
    return idx


def scene_game(start):
    idx = start
    total = 16 * FPS
    rnd = random.Random(7)
    # playfield matching game.html, scaled x2.16 and centred
    fw, fh = 1600, 1000
    ox, oy = (W - fw) // 2, 50
    gx, gy = ox + fw / 2, oy + fh / 2
    coins = [(ox + rnd.uniform(80, fw - 80), oy + rnd.uniform(80, fh - 80))
             for _ in range(5)]
    blocks = []
    score = 0
    font_hud = f(BOLD, 44)
    for n in range(total):
        t = n / FPS
        img = Image.new("RGB", (W, H), BG)
        d = ImageDraw.Draw(img)
        d.rounded_rectangle([ox, oy, ox + fw, oy + fh], 24, fill=PANEL,
                            outline=MAGENTA, width=6)
        # chase nearest coin
        tx, ty = min(coins, key=lambda c: (c[0] - gx) ** 2 + (c[1] - gy) ** 2)
        dx, dy = tx - gx, ty - gy
        dist = math.hypot(dx, dy) or 1
        sp = 7.5
        gx += dx / dist * min(sp, dist)
        gy += dy / dist * min(sp, dist)
        if dist < 46:
            coins.remove((tx, ty))
            coins.append((ox + rnd.uniform(80, fw - 80),
                          oy + rnd.uniform(80, fh - 80)))
            score += 10
        if rnd.random() < 0.03:
            blocks.append([ox + rnd.uniform(30, fw - 60), oy - 40,
                           rnd.uniform(4, 8)])
        for b in blocks:
            b[1] += b[2]
        blocks = [b for b in blocks if b[1] < oy + fh + 50]
        for cx, cy in coins:
            star(d, cx, cy, 26)
        for bx, by, _ in blocks:
            d.rectangle([bx, by, bx + 62, by + 62], fill=RED)
        ghost(d, gx, gy, 44)
        time_left = max(0, 60 - int(t * 3.2))
        d.text((ox + 30, oy + fh - 70),
               f"Score: {score}   Hearts: ♥♥♥   Time: {time_left}",
               font=font_hud, fill=WHITE)
        save(img, idx)
        idx += 1
    return idx, score


def scene_cta(start, score):
    idx = start
    total = 3 * FPS
    font_a = f(BOLD, 96)
    font_b = f(FONT, 54)
    last = Image.open(os.path.join(FRAMES, f"f{start - 1:05d}.png")).convert("RGB")
    dark = Image.new("RGB", (W, H), (8, 6, 14))
    base = Image.blend(last, dark, 0.55)
    for n in range(total):
        img = base.copy()
        d = ImageDraw.Draw(img)
        d.text((W / 2, 400), "One prompt. One game.", font=font_a,
               fill=WHITE, anchor="ma")
        d.text((W / 2, 540), f"final score {score} — playable in your browser",
               font=font_b, fill=GOLD, anchor="ma")
        d.text((W / 2, 650), "Come build yours on make.fun",
               font=font_b, fill=WHITE, anchor="ma")
        save(img, idx)
        idx += 1
    return idx


def main():
    idx = 0
    idx = scene_prompt(idx)
    idx = scene_code(idx)
    idx, score = scene_game(idx)
    idx = scene_cta(idx, score)
    print(f"frames: {idx} ({idx / FPS:.1f}s)")
    out = os.path.join(HERE, "main-scenes.mp4")
    subprocess.run(
        ["ffmpeg", "-y", "-v", "error", "-framerate", str(FPS),
         "-i", os.path.join(FRAMES, "f%05d.png"),
         "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "20", out],
        check=True)
    print("wrote", out)


if __name__ == "__main__":
    main()
