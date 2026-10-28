#!/usr/bin/env python3
"""Собирает «Liquid Glass Autumn» из базовой темы liquid-glass.theme.css.

  python3 make-autumn.py          writes liquid-glass-autumn.theme.css next to this file

Осенняя тема - не отдельная копия, а база + подмены цветов + свой блок в конце
(иконки-листья/тыквы, тёплые переменные Discord). Правка базы -> запустить снова.
"""
import math
import re
from pathlib import Path
from urllib.parse import quote

HERE = Path(__file__).parent
BASE = HERE / "liquid-glass.theme.css"
OUT = HERE / "liquid-glass-autumn.theme.css"

# 24x24, проверены отрисовкой
LEAF = ("M20.6 3.4C12.6 3.1 5.4 6.8 4.9 14.2c-.1 1.5.2 2.8.8 3.9L3.1 20.7l1.3 1.3 2.6-2.6c1.1.6 2.4.9 3.8.8"
        " 7.6-.5 10.4-8.2 9.8-16.8zM18 6.3c-5.4 2.3-9.3 6.2-11.1 11.4l.9.9c2.1-4.8 5.6-8.4 10.9-11.2z")
PUMPKIN = ("M2.4 14a9.6 7.6 0 1 0 19.2 0a9.6 7.6 0 1 0-19.2 0zM7.4 10L10.9 14.8H3.9zM16.6 10L20.1 14.8H13.1z"
           "M6 16.4H18L16.6 19.8 15 18.2 13.5 20.4 12 18.4 10.5 20.4 9 18.2 7.4 19.8zM10.6 3.2h2.8l.5 3.4h-3.8z")   # jack-o'-lantern

BACKDROP = """    --lg-backdrop:
        radial-gradient(55vmax 45vmax at 8% 4%, rgba(255, 140, 40, 0.20), transparent 62%),
        radial-gradient(50vmax 40vmax at 94% 12%, rgba(200, 70, 35, 0.17), transparent 62%),
        radial-gradient(55vmax 45vmax at 85% 98%, rgba(255, 196, 90, 0.14), transparent 62%),
        radial-gradient(45vmax 35vmax at 10% 95%, rgba(150, 60, 30, 0.18), transparent 62%),
        linear-gradient(135deg, rgba(122, 43, 43, 0.28), transparent 42%, rgba(140, 100, 30, 0.18)),
        #0b0705;"""

SUBS = [
    (" * @name Liquid Glass\n", " * @name Liquid Glass Autumn\n"),
    ("Near-black Discord with iOS-26-style liquid glass:", "Autumn take on the liquid-glass theme: warm amber glass over an ember-dark backdrop, leaf and pumpkin channel icons."),
    ("--lg-tint: rgba(255, 255, 255, 0.035);", "--lg-tint: rgba(255, 226, 190, 0.022);"),
    ("--lg-rim: rgba(255, 255, 255, 0.13);", "--lg-rim: rgba(255, 214, 160, 0.12);"),
    ("--lg-accent: #5865f2;       /* Discord blurple */", "--lg-accent: #ff9a3c;       /* amber */"),
    ("--lg-menu: rgba(10, 10, 12, 0.72);", "--lg-menu: rgba(22, 12, 8, 0.76);"),
    ("rgba(88, 101, 242, 0.18)", "rgba(255, 150, 60, 0.20)"),
    ("rgba(120, 140, 255, 0.75)", "rgba(255, 150, 60, 0.75)"),
    ("#9bb4ff", "#ffd089"),
    ("rgba(61, 220, 132,", "rgba(255, 184, 64,"),
]

AUTUMN = """
/* ======================= autumn ======================= */
:root {
    --lg-speak: #a8d03c;                                   /* leaf green: the one colour that stays "green" because it means "speaking" */
    --lg-speak-glow: color-mix(in srgb, #a8d03c 70%, #f2ff9a);
}
.theme-dark:not(.custom-user-profile-theme),
.theme-light:not(.custom-user-profile-theme) {
    --brand-500: #ff9a3c;
    --brand-530: #f08a2c;
    --brand-560: #d97a22;
    --brand-360: #ffb15c;
    --background-brand: var(--lg-accent);
    --text-link: #ffc27a;
    --text-default: #f1e4d4;
    --text-strong: #fff4e6;
    --text-muted: #b9a28c;
    --status-danger: #e2552b;                              /* mention badges: pumpkin red-orange */
    --red-400: #e2552b;
}
::selection {
    background: rgba(255, 154, 60, 0.40);
}

/* channel icons: text -> leaf, voice -> pumpkin. The SVG path itself is swapped (CSS `d`), so the
   icon keeps Discord's own colour logic. Private/locked channels and live voice channels keep their
   original icons (a lock or a live marker must stay readable). */
a[class*="link_"][aria-label*="текстовый канал"]:not([aria-label*="Приватный"]) svg[class*="icon__"]:not([class*="iconLive_"]) path,
a[class*="link_"][aria-label*="text channel"]:not([aria-label*="Private"]) svg[class*="icon__"]:not([class*="iconLive_"]) path {
    d: path("__LEAF__");
    fill-rule: evenodd;
    clip-rule: evenodd;
}
a[class*="link_"][aria-label*="голосовой канал"]:not([aria-label*="Приватный"]) svg[class*="icon__"]:not([class*="iconLive_"]) path:first-of-type,
a[class*="link_"][aria-label*="voice channel"]:not([aria-label*="Private"]) svg[class*="icon__"]:not([class*="iconLive_"]) path:first-of-type {
    d: path("__PUMPKIN__");
    fill-rule: evenodd;
    clip-rule: evenodd;
}
a[class*="link_"][aria-label*="голосовой канал"]:not([aria-label*="Приватный"]) svg[class*="icon__"]:not([class*="iconLive_"]) path:nth-of-type(n+2),
a[class*="link_"][aria-label*="voice channel"]:not([aria-label*="Private"]) svg[class*="icon__"]:not([class*="iconLive_"]) path:nth-of-type(n+2) {
    d: none;
}
""".replace("__LEAF__", LEAF).replace("__PUMPKIN__", PUMPKIN)


def leaf_uri(color, rot):
    svg = (f"<svg xmlns='http://www.w3.org/2000/svg' viewBox='-3 -3 30 30'><g transform='rotate({rot} 12 12)'>"
           f"<path fill='{color}' fill-rule='evenodd' d='{LEAF}'/></g></svg>")
    return 'url("data:image/svg+xml,' + quote(svg, safe="/:=' ") .replace("'", "%27").replace(" ", "%20") + '")'


def leaf_fall(name, sizes, colors, rots, duration, steps=24):
    """Листопад одним псевдоэлементом: N слоёв-фонов, у каждого своё окно падения и покачивание.
    Слои движутся через background-position (по списку значений в каждом ключевом кадре)."""
    n = len(sizes)
    layers = []
    for i in range(n):
        t0 = 0.02 + 0.34 * ((i * 5) % n) / n            # когда слой начинает падать
        span = 0.58 + 0.06 * (i % 3)                    # какую долю времени падает
        x0 = 6 + 88 * ((i * 37) % 100) / 100            # где по горизонтали
        amp = 3.5 + (i % 4)                             # размах покачивания, %
        ph = i * 1.7
        layers.append((t0, span, x0, amp, ph))
    frames = []
    for k in range(steps + 1):
        t = k / steps
        pos = []
        for t0, span, x0, amp, ph in layers:
            p = min(max((t - t0) / span, 0.0), 1.0)
            y = -14 + 128 * p
            x = x0 + amp * math.sin(2 * math.pi * 1.4 * p + ph)
            pos.append(f"{x:.1f}% {y:.1f}%")
        frames.append(f"    {t * 100:.0f}% {{ background-position: {', '.join(pos)}; }}")
    imgs = ", ".join(leaf_uri(colors[i % len(colors)], rots[i % len(rots)]) for i in range(n))
    sz = ", ".join(f"{z}px" for z in sizes)
    off = ", ".join("50% -30%" for _ in range(n))
    kf = f"@keyframes {name} {{\n" + "\n".join(frames) + "\n}\n"
    return kf, imgs, sz, off, duration


RAIN_SVG = ("<svg xmlns='http://www.w3.org/2000/svg' width='140' height='200' viewBox='0 0 140 200'>"
            + "".join(f"<line x1='{x}' y1='{y}' x2='{x - 7}' y2='{y + l}' stroke='rgb(205,222,245)' "
                      f"stroke-opacity='{o}' stroke-width='1.2' stroke-linecap='round'/>"
                      for x, y, l, o in [(20, 12, 30, .55), (58, 70, 22, .4), (96, 20, 34, .6), (128, 96, 26, .45),
                                         (36, 120, 28, .5), (78, 150, 20, .35), (110, 160, 32, .55), (12, 170, 18, .4),
                                         (66, 30, 16, .3)])
            + "</svg>")


DARKEN = 0.6            # how much of the colour wash stays (1 = original autumn, lower = darker)


def soften(css, k=DARKEN):
    """Scales the alpha of translucent colour washes (alpha < 0.5); solid-ish dark layers stay as they are."""
    def f(m):
        r, g, b, a = m.group(1), m.group(2), m.group(3), float(m.group(4))
        if a < 0.5:
            a = round(a * k, 3)
        return f"rgba({r}, {g}, {b}, {a})"
    return re.sub(r"rgba\((\d+),\s*(\d+),\s*(\d+),\s*([0-9.]+)\)", f, css)


def autumn_motion():
    colors = ["#ff9a3c", "#e2552b", "#ffc15a", "#c9722a", "#f08a2c", "#b5452a"]
    rots = [0, 40, -30, 80, -60, 120, 200, -110]
    kf1, im1, sz1, off1, d1 = leaf_fall("lg-leaves-call", [30, 24, 36, 26, 32, 22, 34, 28, 24], colors, rots, "8s")
    kf2, im2, sz2, off2, d2 = leaf_fall("lg-leaves-card", [18, 14, 20, 15, 17, 13], colors, rots, "5s")
    rain = "url(\"data:image/svg+xml," + quote(RAIN_SVG, safe="/:=' ").replace("'", "%27").replace(" ", "%20") + "\")"
    return f"""
/* ---- autumn motion --------------------------------------------------------------- */
/* Leaves drift down once when a call view / the voice card is created, i.e. right after you join a
   voice channel. One pseudo-element, many background layers, each with its own fall window and sway
   (generated by make-autumn.py). */
{kf1}{kf2}
.callContainer_cb9592 {{
    position: relative;
}}
.callContainer_cb9592::after {{
    content: "";
    position: absolute;
    inset: 0;
    z-index: 3;
    pointer-events: none;
    background-image: {im1};
    background-size: {sz1};
    background-repeat: no-repeat;
    background-position: {off1};
    animation: lg-leaves-call {d1} linear backwards;
}}
.wrapper_e131a9 {{
    position: relative;
}}
.wrapper_e131a9::after {{
    content: "";
    position: absolute;
    inset: 0;
    z-index: 3;
    pointer-events: none;
    background-image: {im2};
    background-size: {sz2};
    background-repeat: no-repeat;
    background-position: {off2};
    animation: lg-leaves-card {d2} linear backwards;
}}

/* Rain: a thin shower across the top of the chat card, fading out downward. Lives inside the card
   (clipped to its rounded corners) and sits above the glass, so nothing behind it is re-blurred.
   Set --lg-rain-opacity to 0 to switch it off. */
:root {{
    --lg-rain-opacity: 0.15;
}}
@keyframes lg-rain {{                       /* each layer moves exactly one of its own tile heights per cycle, so the loop never jumps */
    from {{ background-position: 0 0,    30px 50px; }}
    to   {{ background-position: 0 200px, 30px 180px; }}
}}
.chatContent_f75fb0::after {{
    content: "";
    position: absolute;
    left: 0;
    right: 0;
    top: 0;
    height: 42%;
    z-index: 2;
    pointer-events: none;
    background: {rain} 0 0 / 140px 200px repeat, {rain} 30px 50px / 90px 130px repeat;   /* two layers, two sizes and speeds: depth */
    opacity: var(--lg-rain-opacity);
    -webkit-mask-image: linear-gradient(to bottom, #000 0%, transparent 100%);
            mask-image: linear-gradient(to bottom, #000 0%, transparent 100%);
    animation: lg-rain 0.75s linear infinite;
}}
"""


AUTUMN_COLOUR = """
/* ---- autumn colour: gradients almost everywhere ------------------------------------- */
:root {
    --au-amber: #ff9a3c;
    --au-gold: #f4c15a;
    --au-rust: #d9532a;
    --au-burgundy: #7a2b2b;
    --au-olive: #8c8a3a;
    --au-sheen: radial-gradient(130% 70% at 0% 0%, rgba(255, 235, 205, 0.10), transparent 55%);   /* the glass highlight every card keeps */
}
.theme-dark:not(.custom-user-profile-theme),
.theme-light:not(.custom-user-profile-theme) {
    --border-subtle: rgba(255, 190, 120, 0.10);
    --border-normal: rgba(255, 190, 120, 0.16);
}

/* each card gets its own leaf-coloured gradient (same family, different mix) */
.guilds__5e434 {                                        /* gold -> amber -> rust, top to bottom */
    background: var(--au-sheen), linear-gradient(180deg, rgba(244, 193, 90, 0.20), rgba(255, 154, 60, 0.10) 45%, rgba(217, 83, 42, 0.18)), var(--lg-tint);
}
.sidebarList__5e434 {                                   /* amber ember fading to burgundy */
    background: var(--au-sheen), linear-gradient(165deg, rgba(255, 140, 50, 0.15), rgba(217, 83, 42, 0.05) 45%, rgba(122, 43, 43, 0.17)), var(--lg-tint);
}
.chatContent_f75fb0 {                                   /* the big reading area stays calm: faint warm vignette */
    background: var(--au-sheen), radial-gradient(90% 60% at 100% 0%, rgba(255, 154, 60, 0.07), transparent 60%), linear-gradient(180deg, rgba(122, 43, 43, 0.00), rgba(122, 43, 43, 0.06)), var(--lg-tint);
}
.container_c8ffbb,
.content_f75fb0 > .membersWrap_c8ffbb {                 /* olive -> rust */
    background: var(--au-sheen), linear-gradient(170deg, rgba(140, 138, 58, 0.12), rgba(217, 83, 42, 0.12)), var(--lg-tint);
}
.chat_f75fb0 > .subtitleContainer_f75fb0 {              /* title strip: a warm stripe */
    background: var(--au-sheen), linear-gradient(90deg, rgba(255, 154, 60, 0.15), rgba(217, 83, 42, 0.05) 60%, rgba(122, 43, 43, 0.10)), var(--lg-tint);
}
.activityPanel__5e434,
.wrapper_e131a9 {
    background: var(--au-sheen), linear-gradient(180deg, rgba(255, 140, 50, 0.16), rgba(190, 70, 40, 0.12)), var(--lg-tint);
}
.container__37e49 {                                     /* the account pill: amber -> rust sunset */
    background: var(--au-sheen), linear-gradient(90deg, rgba(255, 150, 60, 0.20), rgba(217, 83, 42, 0.10) 55%, rgba(122, 43, 43, 0.16)), var(--lg-tint);
}

/* menus, popouts, dialogs, tooltips: dark amber glass instead of flat dark */
[class*="menu_"],
[class*="popout_"],
[role="dialog"] {
    background: linear-gradient(160deg, rgba(70, 32, 14, 0.82), rgba(26, 13, 8, 0.80));
}
[class*="tooltip_"] {
    background: linear-gradient(135deg, rgba(90, 42, 16, 0.92), rgba(40, 18, 10, 0.92)) !important;
}

/* selected channel: a warm glowing bar with a gradient fill */
[class*="modeSelected_"] [class*="link_"] {
    background: linear-gradient(90deg, rgba(255, 154, 60, 0.30), rgba(217, 83, 42, 0.10) 70%, transparent) !important;
    box-shadow: inset 3px 0 0 var(--au-amber), 0 0 18px rgba(255, 140, 50, 0.16);
}
/* hovered channel plate: gradient too */
:is([class*="containerDefault_"] [class*="link_"], [class*="wrapperCommon_"][class*="clickable_"]):hover {
    background:
        radial-gradient(120% 160% at 0% 0%, rgba(255, 220, 170, 0.14), transparent 60%),
        linear-gradient(90deg, rgba(255, 154, 60, 0.16), rgba(217, 83, 42, 0.05)) !important;
}

/* filled brand buttons (not the voice-card glass ones): amber-to-rust gradient */
button[class*="lookFilled_"][class*="colorBrand_"]:not([class*="buttonColor_"]) {
    background: linear-gradient(135deg, #ffb15c, #e2552b) !important;
    color: #fff8ee !important;
    box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.35), 0 4px 14px rgba(226, 85, 43, 0.28);
}
/* mention counters */
[class*="numberBadge_"] {
    background: linear-gradient(135deg, #ff8a3c, #d63f24) !important;
    color: #fff6ea !important;
}
/* scrollbars */
::-webkit-scrollbar-thumb {
    background: linear-gradient(180deg, #ffb15c, #c4552a) !important;
    background-clip: padding-box !important;
    opacity: 0.8;
}
/* input: warm focus glow */
[class*="channelTextArea_"]:focus-within {
    border-color: rgba(255, 170, 80, 0.55);
    box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.30), 0 0 0 1px rgba(255, 154, 60, 0.35), 0 8px 30px rgba(255, 120, 40, 0.20);
}
/* server icons: a golden ring lights up on hover */
[data-list-item-id^="guildsnav___"] {
    border-radius: 50%;
}
[data-list-item-id^="guildsnav___"]:hover {
    box-shadow: 0 0 0 2px rgba(255, 190, 100, 0.75), 0 0 20px rgba(255, 140, 50, 0.55);
}
/* messages: a faint warm wash under the cursor */
[id^="chat-messages-"]:hover {
    background: linear-gradient(90deg, rgba(255, 154, 60, 0.05), transparent 70%);
}
/* your name: gold-to-amber text */
.nameTag__37e49 .panelTitleContainer__37e49 [class*="title_"] {
    background: linear-gradient(90deg, #fff2d8, #ffc27a 70%, #ff9a3c);
    -webkit-background-clip: text;
            background-clip: text;
    -webkit-text-fill-color: transparent;
}
"""


AUTUMN_DIM = """
/* ---- darker: the base theme brightens the frosted backdrop by 15%; autumn dims it a little instead ---- */
.guilds__5e434,
.sidebarList__5e434,
.chatContent_f75fb0,
.container_c8ffbb,
.content_f75fb0 > .membersWrap_c8ffbb,
.chat_f75fb0 > .subtitleContainer_f75fb0,
.activityPanel__5e434,
.wrapper_e131a9,
.container__37e49 {
    backdrop-filter: blur(var(--lg-blur)) saturate(140%) brightness(0.9);
}
"""


def main():
    s = BASE.read_text()
    for old, new in SUBS:
        if old not in s:
            raise SystemExit(f"в базе нет фрагмента: {old[:60]!r}")
        s = s.replace(old, new)
    s, n = re.subn(r"    --lg-backdrop:\n.*?#050506;", lambda m: soften(BACKDROP), s, count=1, flags=re.DOTALL)
    if n != 1:
        raise SystemExit("не нашёл --lg-backdrop")
    s += AUTUMN + autumn_motion() + soften(AUTUMN_COLOUR) + AUTUMN_DIM
    OUT.write_text(s)
    print("готово:", OUT)


main()
