# news-image-20261124

[![make.fun · news-image-20261124](https://make.fun/badge/news-image-20261124.svg)](https://make.fun/bounty/news-image-20261124?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)
[![rank](https://make.fun/badge/news-image-20261124/Dimah28/news-image-20261124/rank.svg)](https://make.fun/bounty/news-image-20261124/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)
[![reward](https://make.fun/badge/news-image-20261124/Dimah28/news-image-20261124/reward.svg)](https://make.fun/bounty/news-image-20261124?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)

Entry for the make.fun bounty **"Sum up 24 November's world news in one image"** ([news-image-20261124](https://make.fun/bounty/news-image-20261124), $100, ends Thu 26 Nov 2026 07:00 WIB).

## The image

`entry.png` — a 1024×1024 newspaper front page drawn entirely procedurally, in the style of a classic broadsheet:

- masthead: **TUESDAY 24 NOVEMBER 2026** (35 stories · 7 regions · one page)
- three lead stories, each with its own illustration: **Jensen Huang reinstated as Nvidia CEO, shares +31% in a day** (Nasdaq +6.5%, S&P +4.7%, Dow +1,450), **COP31 ending with no deal** (EU, Panama and about 130 parties reject a text with no fossil-fuel mention), and **Ukraine sinking the Russian corvette Merkury off Libya** (seven sea drones, second vessel hit)
- ten feature cards: **Iran vowing "all means" against a US naval blockade**, **14 dead in the Kyiv region after a drone collapses a block in Dymer**, **24 dead in the Banten candy factory fire**, **Democrats taking 258 House seats**, **the ICJ ruling Myanmar committed genocide against the Rohingya**, **drone strikes hitting a UN building near Khartoum**, **the Thai-Cambodia truce holding**, **Pope Leo XIV's South America tour**, **Alcaraz winning the ATP Finals**, and **the Las Vegas Grand Prix**
- a **BY THE NUMBERS** band (+31% Nvidia · +6.5% Nasdaq · 258 House seats · 14 Kyiv dead · 24 Banten dead · 130 parties) and region chips (Europe · Middle East · Africa · Asia · South Asia · Americas · Markets + Sport)
- a **world map** with numbered pins, and **ALSO ON TUESDAY 24 NOVEMBER — 22 MORE STORIES** (stories 14–35, one line each)
- a **DATE CHECK** strip naming stories that are deliberately NOT shown as 24 Nov news (Shenzhen summit 19 Nov, Kerch Bridge strike 17 Nov, Nvidia CEO resignation 12 Nov, Peru quake 20 Nov, GTA VI launch 19 Nov, COP31 collapse itself Sun 22 Nov)
- footer: sources Reuters · AP · BBC · CNN · Investopedia · The Times of India · CBS · NBC · UKMTO · Al Jazeera, "Original vector drawings."

Every story here happened, or was first reported, on Tuesday 24 November 2026 in at least one time zone. Claims are attributed, not stated as fact.

## How it is drawn

`main.py` is standard library only (`math`, `os`, `struct`, `zlib`) — no Pillow, no system fonts, no network. All lettering uses a hand-built 5×7 bitmap font, so text stays crisp at any size. The market chart, the summit hall, the sinking warship and the world map are all drawn with the same small canvas primitives (rectangles, polygons, circles, thick lines).

## Run it

```sh
MAKEFUN_OUTPUT_DIR=/tmp/out python3 main.py
# writes /tmp/out/entry.png (1024x1024, deterministic — run twice, same bytes)
```
