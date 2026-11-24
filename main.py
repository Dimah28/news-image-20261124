#!/usr/bin/env python3
"""news-image-20261124 -- "The World in One Day" newspaper front page.

Draws a 1024x1024 PNG summing up Tuesday 24 November 2026 world news:
35 dated stories across 7 regions, 3 illustrated leads, a numbers band,
a schematic world map, a DATE CHECK strip and a sources footer.

Standard library only (math, os, struct, zlib). No network, no clock,
no randomness, no system fonts, no Pillow. All lettering uses a hand-built
5x7 bitmap font defined below. Output is fully deterministic: run it twice
and the bytes are identical.

Usage:  MAKEFUN_OUTPUT_DIR=out python3 main.py   -> writes out/entry.png
"""
import math
import os
import struct
import zlib

W, H = 1024, 1024

INK = (18, 18, 18)
PAPER = (255, 253, 247)
RED = (178, 30, 30)
DARKRED = (140, 20, 20)
BLUE = (28, 58, 128)
GREEN = (16, 110, 58)
GOLD = (176, 128, 20)
GRAY = (96, 96, 96)
LIGHT = (238, 236, 230)
MID = (210, 208, 200)
SKY = (214, 232, 244)
SEA = (64, 110, 168)

# ---------------------------------------------------------------- font ----
# 5x7 bitmap glyphs, rows top to bottom, '#' = on. Uppercase + digits +
# the punctuation used on the page. Unknown chars render as blank.
FONT = {
    'A': ("01110", "10001", "10001", "11111", "10001", "10001", "10001"),
    'B': ("11110", "10001", "10001", "11110", "10001", "10001", "11110"),
    'C': ("01110", "10001", "10000", "10000", "10000", "10001", "01110"),
    'D': ("11110", "10001", "10001", "10001", "10001", "10001", "11110"),
    'E': ("11111", "10000", "10000", "11110", "10000", "10000", "11111"),
    'F': ("11111", "10000", "10000", "11110", "10000", "10000", "10000"),
    'G': ("01110", "10001", "10000", "10111", "10001", "10001", "01111"),
    'H': ("10001", "10001", "10001", "11111", "10001", "10001", "10001"),
    'I': ("01110", "00100", "00100", "00100", "00100", "00100", "01110"),
    'J': ("00111", "00010", "00010", "00010", "00010", "10010", "01100"),
    'K': ("10001", "10010", "10100", "11000", "10100", "10010", "10001"),
    'L': ("10000", "10000", "10000", "10000", "10000", "10000", "11111"),
    'M': ("10001", "11011", "10101", "10101", "10001", "10001", "10001"),
    'N': ("10001", "11001", "10101", "10011", "10001", "10001", "10001"),
    'O': ("01110", "10001", "10001", "10001", "10001", "10001", "01110"),
    'P': ("11110", "10001", "10001", "11110", "10000", "10000", "10000"),
    'Q': ("01110", "10001", "10001", "10001", "10101", "10010", "01101"),
    'R': ("11110", "10001", "10001", "11110", "10100", "10010", "10001"),
    'S': ("01111", "10000", "10000", "01110", "00001", "00001", "11110"),
    'T': ("11111", "00100", "00100", "00100", "00100", "00100", "00100"),
    'U': ("10001", "10001", "10001", "10001", "10001", "10001", "01110"),
    'V': ("10001", "10001", "10001", "10001", "10001", "01010", "00100"),
    'W': ("10001", "10001", "10001", "10101", "10101", "11011", "10001"),
    'X': ("10001", "10001", "01010", "00100", "01010", "10001", "10001"),
    'Y': ("10001", "10001", "01010", "00100", "00100", "00100", "00100"),
    'Z': ("11111", "00001", "00010", "00100", "01000", "10000", "11111"),
    '0': ("01110", "10001", "10011", "10101", "11001", "10001", "01110"),
    '1': ("00100", "01100", "00100", "00100", "00100", "00100", "01110"),
    '2': ("01110", "10001", "00001", "00110", "01000", "10000", "11111"),
    '3': ("11110", "00001", "00001", "01110", "00001", "00001", "11110"),
    '4': ("00010", "00110", "01010", "10010", "11111", "00010", "00010"),
    '5': ("11111", "10000", "11110", "00001", "00001", "10001", "01110"),
    '6': ("00110", "01000", "10000", "11110", "10001", "10001", "01110"),
    '7': ("11111", "00001", "00010", "00100", "01000", "01000", "01000"),
    '8': ("01110", "10001", "10001", "01110", "10001", "10001", "01110"),
    '9': ("01110", "10001", "10001", "01111", "00001", "00010", "01100"),
    ' ': ("00000", "00000", "00000", "00000", "00000", "00000", "00000"),
    '.': ("00000", "00000", "00000", "00000", "00000", "01100", "01100"),
    ',': ("00000", "00000", "00000", "00000", "01100", "00100", "01000"),
    ':': ("00000", "01100", "01100", "00000", "01100", "01100", "00000"),
    ';': ("00000", "01100", "01100", "00000", "01100", "00100", "01000"),
    "'": ("00100", "00100", "01000", "00000", "00000", "00000", "00000"),
    '!': ("00100", "00100", "00100", "00100", "00100", "00000", "00100"),
    '?': ("01110", "10001", "00001", "00110", "00100", "00000", "00100"),
    '-': ("00000", "00000", "00000", "01110", "00000", "00000", "00000"),
    '+': ("00000", "00100", "00100", "01110", "00100", "00100", "00000"),
    '%': ("11001", "11010", "00010", "00100", "01000", "01011", "10011"),
    '/': ("00001", "00010", "00010", "00100", "01000", "01000", "10000"),
    '(': ("00010", "00100", "01000", "01000", "01000", "00100", "00010"),
    ')': ("01000", "00100", "00010", "00010", "00010", "00100", "01000"),
    '&': ("01100", "10010", "10100", "01000", "10101", "10010", "01101"),
    '$': ("00100", "01111", "10100", "01110", "00101", "11110", "00100"),
    '=': ("00000", "00000", "01110", "00000", "01110", "00000", "00000"),
    '"': ("01010", "01010", "00000", "00000", "00000", "00000", "00000"),
    '*': ("00000", "10101", "01110", "10101", "00000", "00000", "00000"),
}


def text_w(s, scale):
    return len(s) * 6 * scale - scale


def wrap(s, scale, max_w):
    """Greedy word wrap; returns list of lines fitting max_w pixels."""
    cw = 6 * scale
    lines, cur = [], ""
    for word in s.split(" "):
        trial = word if not cur else cur + " " + word
        if len(trial) * cw - scale <= max_w or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


# -------------------------------------------------------------- canvas ----
class Canvas:
    def __init__(self, w, h, bg):
        self.w, self.h = w, h
        self.px = bytearray(bg * (w * h))

    def set(self, x, y, c):
        if 0 <= x < self.w and 0 <= y < self.h:
            i = (y * self.w + x) * 3
            self.px[i:i + 3] = bytes(c)

    def fill(self, x, y, w, h, c):
        x0, y0 = max(0, x), max(0, y)
        x1, y1 = min(self.w, x + w), min(self.h, y + h)
        row = bytes(c) * (x1 - x0)
        for yy in range(y0, y1):
            i = (yy * self.w + x0) * 3
            self.px[i:i + len(row)] = row

    def hline(self, x, y, w, c, t=1):
        self.fill(x, y, w, t, c)

    def vline(self, x, y, h, c, t=1):
        self.fill(x, y, t, h, c)

    def rect(self, x, y, w, h, c, t=1):
        self.hline(x, y, w, c, t)
        self.hline(x, y + h - t, w, c, t)
        self.vline(x, y, h, c, t)
        self.vline(x + w - t, y, h, c, t)

    def line(self, x0, y0, x1, y1, c, t=1):
        dx, dy = abs(x1 - x0), abs(y1 - y0)
        sx = 1 if x0 < x1 else -1
        sy = 1 if y0 < y1 else -1
        err, x, y = dx - dy, x0, y0
        while True:
            self.fill(x - t // 2, y - t // 2, t, t, c)
            if x == x1 and y == y1:
                break
            e2 = 2 * err
            if e2 > -dy:
                err -= dy
                x += sx
            if e2 < dx:
                err += dx
                y += sy

    def poly(self, pts, c, fill_c=None):
        if fill_c is not None:
            miny = min(p[1] for p in pts)
            maxy = max(p[1] for p in pts)
            n = len(pts)
            for yy in range(miny, maxy + 1):
                xs = []
                for i in range(n):
                    x0, y0 = pts[i]
                    x1, y1 = pts[(i + 1) % n]
                    if (y0 <= yy < y1) or (y1 <= yy < y0):
                        xs.append(x0 + (yy - y0) * (x1 - x0) / (y1 - y0))
                xs.sort()
                for k in range(0, len(xs) - 1, 2):
                    self.hline(int(xs[k]), yy, max(1, int(xs[k + 1]) - int(xs[k])), fill_c)
        for i in range(len(pts)):
            x0, y0 = pts[i]
            x1, y1 = pts[(i + 1) % len(pts)]
            self.line(x0, y0, x1, y1, c)

    def circle(self, cx, cy, r, c, fill_c=None):
        if fill_c is not None:
            for yy in range(cy - r, cy + r + 1):
                dx = int(math.sqrt(max(0, r * r - (yy - cy) ** 2)))
                self.hline(cx - dx, yy, 2 * dx + 1, fill_c)
        for a in range(0, 360, 2):
            rad = math.radians(a)
            self.set(int(cx + r * math.cos(rad)), int(cy + r * math.sin(rad)), c)

    def text(self, x, y, s, scale, c):
        s = s.upper()
        cx = x
        for ch in s:
            g = FONT.get(ch, FONT[' '])
            for r in range(7):
                row = g[r]
                for col in range(5):
                    if row[col] == '1':
                        self.fill(cx + col * scale, y + r * scale, scale, scale, c)
            cx += 6 * scale
        return cx

    def text_c(self, cx, y, s, scale, c):
        self.text(cx - text_w(s, scale) // 2, y, s, scale, c)

    def text_r(self, x, y, s, scale, c):
        self.text(x - text_w(s, scale), y, s, scale, c)

    def para(self, x, y, s, scale, max_w, c, lh=None):
        lh = lh or (9 * scale)
        for ln in wrap(s, scale, max_w):
            self.text(x, y, ln, scale, c)
            y += lh
        return y

    def save_png(self, path):
        raw = bytearray()
        stride = self.w * 3
        for yy in range(self.h):
            raw.append(0)
            raw += self.px[yy * stride:(yy + 1) * stride]
        comp = zlib.compress(bytes(raw), 9)

        def chunk(typ, data):
            out = struct.pack(">I", len(data)) + typ + data
            out += struct.pack(">I", zlib.crc32(typ + data) & 0xFFFFFFFF)
            return out

        ihdr = struct.pack(">IIBBBBB", self.w, self.h, 8, 2, 0, 0, 0)
        png = b"\x89PNG\r\n\x1a\n"
        png += chunk(b"IHDR", ihdr)
        png += chunk(b"IDAT", comp)
        png += chunk(b"IEND", b"")
        with open(path, "wb") as f:
            f.write(png)

# ------------------------------------------------------------- content ----
# Every number/name below was verified against reporting published
# 23-24 Nov 2026 (Reuters, AP, BBC, CNN, Investopedia, The Times of
# India, CBS/NBC projections). Events dated before 24 Nov are labelled
# with their date in the DATE CHECK strip, never presented as 24 Nov news.

LEADS = [
    {
        "kicker": "LEAD 1 - MARKETS",
        "head": "HUANG IS BACK: NVIDIA +31% IN A DAY",
        "body": "Board reinstates Jensen Huang as CEO Mon 23 Nov, 11 days after his resignation. Trump backs it. Nasdaq +6.5%, S and P +4.7%, Dow +1,450.",
        "art": "chart",
    },
    {
        "kicker": "LEAD 2 - CLIMATE",
        "head": "COP31 ENDS WITH NO DEAL",
        "body": "Summit in Antalya collapses Sun 22 Nov: EU, Panama and about 130 parties reject a text with no fossil-fuel mention after two days overtime. Fallout dominates Tue 24 Nov.",
        "art": "summit",
    },
    {
        "kicker": "LEAD 3 - WAR AT SEA",
        "head": "UKRAINE SINKS RUSSIAN WARSHIP OFF LIBYA",
        "body": "Zelensky says Mon 23 Nov sea drones sank the corvette Merkury at Benghazi and hit a second vessel. Seven drones used.",
        "art": "ship",
    },
]

FEATURES = [
    ("4", "IRAN V US BLOCKADE", "Tehran vows all means against a US naval blockade; two supertankers hit mines near Hormuz and burn. Bahrain: Iranian strike wounds two."),
    ("5", "DYMER: 14 DEAD IN KYIV REGION", "Russian drone partly collapses a 5-storey block Sun night. Boy pulled alive after 14 hours, elderly woman after 22."),
    ("6", "BANTEN FACTORY FIRE: 24 DEAD", "Candy factory blaze in Indonesia Sat evening. Rescuers still search for 34 missing workers."),
    ("7", "DEMOCRATS TAKE 258 HOUSE SEATS", "Largest House majority since 1992. Hubbard beats Foxx by 330 votes after a recount in North Carolina."),
    ("8", "ICJ: MYANMAR COMMITTED GENOCIDE", "Top UN court rules against Myanmar over the Rohingya. A landmark verdict, years in the making."),
    ("9", "SUDAN: STRIKES HIT UN BUILDING", "Drone strikes hit homes and a UN building around Khartoum Sun. Four killed; fears for aid workers."),
    ("10", "THAI-CAMBODIA TRUCE HOLDS", "Border fighting on hold after a truce. Both sides count the cost of the flare-up."),
    ("11", "POPE LEO XIV IN SOUTH AMERICA", "12-day tour: Uruguay, Argentina, Peru. Economy and social needs top talks with President Milei."),
    ("12", "ALCARAZ WINS ATP FINALS", "Beats Zverev in Turin for his first ATP Finals title. Spain's star ends the season on top."),
    ("13", "LAS VEGAS GRAND PRIX", "F1's weekend under the lights on the Strip. Verstappen among the front-runners again."),
]

ALSO = [
    ("14", "GERMANY: $300M MILITARY AID FOR UKRAINE"),
    ("15", "UKRAINE: PATRIOT INTERCEPTORS EXHAUSTED"),
    ("16", "HOUTHIS FIRE AT SAUDI POWER PLANT, PORT"),
    ("17", "IRGC STRIKES TANKER IN STRAIT OF HORMUZ"),
    ("18", "US FORCES STRIKE OUTSKIRTS OF QESHM ISLAND"),
    ("19", "WAYMO PULLS DRIVERLESS TAXIS OFF US FREEWAYS"),
    ("20", "SENEGAL BOAT CAPSIZES: 4 DEAD, DOZENS MISSING"),
    ("21", "ARMENIA DRAFTS CONSTITUTION FOR PEACE DEAL"),
    ("22", "EU PLANS 3% DIGITAL TAX ON BIG TECH"),
    ("23", "SOFTBANK TO INVEST $2B IN INTEL"),
    ("24", "BANGLADESH MASS TYPHOID VACCINATION DRIVE"),
    ("25", "HIMALAYAN FLOOD: ARMY HUNTS FOR MISSING"),
    ("26", "US VARSITY SHOOTING: TWO DEAD, ONE HURT"),
    ("27", "TRUMP WARNS IRAN OF VERY TRAUMATIC OUTCOME"),
    ("28", "US PLANS NEW CITIZENSHIP TEST, H-1B RULES"),
    ("29", "APEC FRICTION: JAPAN-CHINA STALEMATE"),
    ("30", "EU: RUSSIA STALLING PEACE TALKS, BOMBING ON"),
    ("31", "NATO VOWS SPACE DEFENCE AFTER SATELLITE ROW"),
    ("32", "UK CONFIRMED AS 2035 WOMEN'S WORLD CUP HOST"),
    ("33", "GUKESH DEFENDS CHESS CROWN IN GENEVA"),
    ("34", "MODI OPENS AI CENTRE AT IIT PATNA"),
    ("35", "GAZA CONTAMINATION: OXFAM WARNS OF TOXINS"),
]

NUMBERS = [
    ("+31%", "NVIDIA SHARES"),
    ("+6.5%", "NASDAQ, MON 23 NOV"),
    ("258", "DEMOCRAT HOUSE SEATS"),
    ("14", "DEAD, KYIV REGION"),
    ("24", "DEAD, BANTEN FIRE"),
    ("130", "PARTIES REJECT COP31 TEXT"),
]

REGIONS = ["EUROPE", "MIDDLE EAST", "AFRICA", "ASIA", "SOUTH ASIA", "AMERICAS", "MARKETS + SPORT"]

DATE_CHECK = [
    "NOT 24 NOV NEWS: SHENZHEN SUMMIT 19 NOV - KERCH BRIDGE STRIKE 17 NOV -",
    "NVIDIA CEO RESIGNS 12 NOV - PERU 6.7 QUAKE 20 NOV - GTA VI LAUNCH 19 NOV -",
    "FIONA THE HIPPO DIES 19 NOV - COP31 COLLAPSE ITSELF SUN 22 NOV (FALLOUT IS 24 NOV)",
]

SOURCES = "SOURCES: REUTERS - AP - BBC - CNN - INVESTOPEDIA - THE TIMES OF INDIA - CBS - NBC - UKMTO - AL JAZEERA"


# ------------------------------------------------------------ drawings ----
def draw_chart(c, x, y, w, h):
    """Rising market chart: chip + green arrow line."""
    c.fill(x, y, w, h, SKY)
    # chip
    cx, cy, cw, ch = x + 14, y + 58, 74, 46
    c.fill(cx, cy, cw, ch, INK)
    c.fill(cx + 6, cy + 6, cw - 12, ch - 12, (40, 40, 40))
    c.text(cx + 14, cy + 16, "NVDA", 1, (120, 220, 140))
    for i in range(4):
        c.fill(cx - 6, cy + 10 + i * 10, 6, 3, GOLD)
        c.fill(cx + cw, cy + 10 + i * 10, 6, 3, GOLD)
    # rising line with arrowhead
    pts = [(x + 100, y + 92), (x + 140, y + 78), (x + 170, y + 84),
           (x + 205, y + 52), (x + 240, y + 58), (x + 272, y + 22)]
    for i in range(len(pts) - 1):
        c.line(pts[i][0], pts[i][1], pts[i + 1][0], pts[i + 1][1], GREEN, 4)
    ex, ey = pts[-1]
    c.poly([(ex, ey), (ex - 16, ey - 2), (ex - 4, ey + 12)], GREEN, GREEN)
    c.text(x + 216, y + 8, "+31%", 2, GREEN)
    c.text(x + 14, y + 8, "MON 23 NOV", 1, GRAY)


def draw_summit(c, x, y, w, h):
    """Summit hall: round table, flags, cracked globe, NO DEAL banner."""
    c.fill(x, y, w, h, (232, 226, 208))
    # cracked globe
    gx, gy, gr = x + 66, y + 52, 34
    c.circle(gx, gy, gr, BLUE, (168, 200, 228))
    c.line(gx - 20, gy - 24, gx - 4, gy - 2, BLUE, 2)
    c.line(gx - 4, gy - 2, gx + 8, gy + 14, BLUE, 2)
    c.line(gx + 8, gy + 14, gx + 2, gy + 30, BLUE, 2)
    c.text(gx - 12, gy - 4, "COP31", 1, BLUE)
    # table + flags
    c.fill(x + 130, y + 66, 150, 10, (120, 84, 48))
    for i, col in enumerate([(28, 58, 128), (178, 30, 30), (16, 110, 58),
                             (176, 128, 20), (90, 40, 110)]):
        fx = x + 142 + i * 28
        c.vline(fx, y + 38, 28, INK, 2)
        c.fill(fx, y + 38, 18, 12, col)
    c.fill(x + 130, y + 76, 8, 26, INK)
    c.fill(x + 272, y + 76, 8, 26, INK)
    # empty chair (no deal)
    c.line(x + 196, y + 88, x + 196, y + 104, INK, 3)
    c.line(x + 214, y + 88, x + 214, y + 104, INK, 3)
    c.line(x + 192, y + 88, x + 218, y + 88, INK, 3)
    c.fill(x, y + h - 26, w, 26, RED)
    c.text_c(x + w // 2, y + h - 21, "NO DEAL", 2, PAPER)


def draw_ship(c, x, y, w, h):
    """Sinking corvette at Benghazi: hull, smoke, sea, 7 drones."""
    c.fill(x, y, w, h, SKY)
    # sea
    c.fill(x, y + 78, w, h - 78, SEA)
    for wy in (88, 98, 108):
        for sx in range(x + 8, x + w - 8, 26):
            c.line(sx, y + wy, sx + 14, y + wy - 4, (200, 224, 240), 2)
    # tilted hull
    hull = [(x + 60, y + 66), (x + 250, y + 48), (x + 262, y + 66),
            (x + 240, y + 84), (x + 80, y + 92)]
    c.poly(hull, INK, (70, 74, 80))
    c.fill(x + 150, y + 30, 10, 22, INK)
    c.fill(x + 196, y + 36, 26, 8, INK)
    # smoke + fire
    c.circle(x + 96, y + 40, 12, GRAY, (150, 150, 150))
    c.circle(x + 84, y + 26, 9, GRAY, (170, 170, 170))
    c.poly([(x + 88, y + 66), (x + 100, y + 44), (x + 112, y + 66)], RED, (230, 90, 30))
    # 7 sea drones (small dots with wake)
    for i, (dx, dy) in enumerate([(30, 100), (58, 106), (86, 100), (120, 108),
                                  (150, 102), (196, 108), (238, 102)]):
        c.circle(x + dx, y + dy, 4, INK, PAPER)
        c.text(x + dx - 2, y + dy - 12, str(i + 1), 1, INK)
    c.text(x + 10, y + 8, "BENGHAZI, LIBYA", 1, GRAY)


ART = {"chart": draw_chart, "summit": draw_summit, "ship": draw_ship}


def draw_map(c, x, y, w, h):
    """Schematic world map: rough continent polygons + numbered pins."""
    c.fill(x, y, w, h, (226, 236, 240))
    c.rect(x, y, w, h, INK, 1)
    # North America
    c.poly([(x + 18, y + 26), (x + 78, y + 16), (x + 96, y + 34),
            (x + 82, y + 62), (x + 52, y + 70), (x + 26, y + 56)],
           GRAY, (196, 200, 196))
    # South America
    c.poly([(x + 66, y + 84), (x + 96, y + 80), (x + 100, y + 112),
            (x + 84, y + 148), (x + 70, y + 118)], GRAY, (196, 200, 196))
    # Europe
    c.poly([(x + 138, y + 30), (x + 166, y + 22), (x + 178, y + 40),
            (x + 162, y + 56), (x + 140, y + 50)], GRAY, (196, 200, 196))
    # Africa
    c.poly([(x + 142, y + 66), (x + 178, y + 62), (x + 190, y + 92),
            (x + 172, y + 126), (x + 152, y + 100)], GRAY, (196, 200, 196))
    # Asia
    c.poly([(x + 186, y + 22), (x + 262, y + 14), (x + 288, y + 36),
            (x + 268, y + 66), (x + 224, y + 70), (x + 196, y + 52)],
           GRAY, (196, 200, 196))
    # Australia
    c.poly([(x + 252, y + 118), (x + 284, y + 114), (x + 292, y + 132),
            (x + 262, y + 138)], GRAY, (196, 200, 196))
    pins = [(19, 52, 44), (14, 146, 30), (15, 182, 42), (17, 200, 60),
            (20, 148, 78), (24, 236, 42), (27, 252, 64), (33, 162, 52)]
    for num, px, py in pins:
        c.circle(x + px, y + py, 8, RED, RED)
        c.text(x + px - 3, y + py - 3, str(num), 1, PAPER)
    c.text(x + 8, y + h - 16, "PINS: STORIES 14, 15, 17, 19, 20, 24, 27, 33", 1, GRAY)


# -------------------------------------------------------------- render ----
def render():
    c = Canvas(W, H, PAPER)
    M = 24
    # --- masthead ---
    c.text_c(W // 2, 14, "THE WORLD IN ONE DAY", 5, INK)
    c.hline(M, 62, W - 2 * M, RED, 4)
    c.text(M, 72, "TUESDAY 24 NOVEMBER 2026", 2, INK)
    c.text_r(W - M, 72, "ALL TIMES UTC", 2, RED)
    c.hline(M, 92, W - 2 * M, INK, 2)
    # --- subhead ---
    c.text_c(W // 2, 100, "HUANG RETURNS, NVIDIA SOARS - COP31 COLLAPSES -", 2, INK)
    c.text_c(W // 2, 118, "UKRAINE SINKS A RUSSIAN WARSHIP OFF LIBYA", 2, INK)
    # --- numbers band ---
    y0 = 142
    bw = (W - 2 * M) // 6
    for i, (num, lab) in enumerate(NUMBERS):
        bx = M + i * bw
        c.fill(bx + 2, y0, bw - 4, 52, LIGHT)
        c.rect(bx + 2, y0, bw - 4, 52, MID, 1)
        c.text_c(bx + bw // 2, y0 + 6, num, 3, RED)
        c.text_c(bx + bw // 2, y0 + 34, lab, 1, INK)
    # --- region chips ---
    y0 = 202
    cx = M
    for r in REGIONS:
        wch = text_w(r, 1) + 16
        c.fill(cx, y0, wch, 20, INK)
        c.text(cx + 8, y0 + 6, r, 1, PAPER)
        cx += wch + 8
    # --- leads ---
    y0 = 232
    cw = (W - 2 * M - 16) // 3
    ch = 218
    for i, lead in enumerate(LEADS):
        lx = M + i * (cw + 8)
        c.rect(lx, y0, cw, ch, INK, 2)
        ART[lead["art"]](c, lx + 6, y0 + 6, cw - 12, 118)
        c.text(lx + 8, y0 + 130, lead["kicker"], 1, RED)
        y = c.para(lx + 8, y0 + 146, lead["head"], 2, cw - 16, INK, lh=18)
        c.para(lx + 8, y + 2, lead["body"], 1, cw - 16, INK, lh=9)
    # --- the day in ten ---
    y0 = 462
    c.fill(M, y0, W - 2 * M, 26, INK)
    c.text(M + 8, y0 + 8, "THE DAY IN TEN", 2, PAPER)
    c.text_r(W - M - 8, y0 + 8, "FEATURES 4-13", 1, PAPER)
    y0 += 34
    fw = (W - 2 * M - 8) // 2
    fh = 42
    for i, (num, head, body) in enumerate(FEATURES):
        fx = M + (i % 2) * (fw + 8)
        fy = y0 + (i // 2) * (fh + 3)
        c.fill(fx, fy, fw, fh, LIGHT)
        c.fill(fx, fy, 30, fh, RED)
        c.text(fx + 8, fy + 15, num, 2, PAPER)
        c.text(fx + 38, fy + 5, head, 1, INK)
        c.para(fx + 38, fy + 17, body, 1, fw - 46, GRAY, lh=9)
    # --- also on tuesday ---
    y0 = y0 + 5 * (fh + 3) + 10
    c.fill(M, y0, W - 2 * M, 26, INK)
    c.text(M + 8, y0 + 8, "ALSO ON TUESDAY 24 NOVEMBER - 22 MORE STORIES", 2, PAPER)
    y0 += 34
    mw, mh = 310, 164
    draw_map(c, M, y0, mw, mh)
    ax = M + mw + 12
    aw = W - M - ax
    half = (len(ALSO) + 1) // 2
    for col in range(2):
        tx = ax + col * (aw // 2)
        for j, (num, line) in enumerate(ALSO[col * half:(col + 1) * half]):
            yy = y0 + j * 16
            c.text(tx, yy, num + ".", 1, RED)
            c.text(tx + 22, yy, line, 1, INK)
    # --- date check strip ---
    y0 = y0 + mh + 10
    c.fill(M, y0, W - 2 * M, 46, RED)
    c.text(M + 8, y0 + 5, "DATE CHECK - THESE ARE NOT 24 NOV NEWS:", 1, PAPER)
    c.text(M + 8, y0 + 18, "SHENZHEN SUMMIT 19 NOV - KERCH BRIDGE 17 NOV - NVIDIA CEO RESIGNS 12 NOV -", 1, PAPER)
    c.text(M + 8, y0 + 30, "PERU QUAKE 20 NOV - GTA VI LAUNCH 19 NOV - COP31 COLLAPSE ITSELF SUN 22 NOV", 1, PAPER)
    # --- footer ---
    y0 = y0 + 46 + 8
    c.text_c(W // 2, y0, "35 STORIES - 7 REGIONS - ONE PAGE - ORIGINAL VECTOR DRAWINGS", 1, GRAY)
    c.text_c(W // 2, y0 + 12, SOURCES, 1, GRAY)
    return c


def main():
    outdir = os.environ.get("MAKEFUN_OUTPUT_DIR", "out")
    os.makedirs(outdir, exist_ok=True)
    render().save_png(os.path.join(outdir, "entry.png"))


if __name__ == "__main__":
    main()
