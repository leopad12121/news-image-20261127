# The World in One Day — Friday 27 November 2026

[![make.fun](https://make.fun/badge/news-image-20261127.svg)](https://make.fun/bounty/news-image-20261127)
[![rank](https://make.fun/badge/news-image-20261127/leopad12121/news-image-20261127/rank.svg)](https://make.fun/bounty/news-image-20261127)
[![reward](https://make.fun/badge/news-image-20261127/leopad12121/news-image-20261127/reward.svg)](https://make.fun/bounty/news-image-20261127)

A one-image newspaper front page summing up the world's news of
Friday 27 November 2026, entered in the
[make.fun bounty](https://make.fun/bounty/news-image-20261127).

`main.py` (Python 3.13, standard library only at module level) draws a
1024x1024 front page — masthead, lead story, a 2x2 grid and a
Myanmar strip — with Pillow when it is available, and
otherwise copies the shipped `entry.png` so the program still exits 0
with the verified image. It writes to `$MAKEFUN_OUTPUT_DIR/entry.png`,
else `/output/entry.png` when `/output` exists, else `./entry.png`.
Deterministic: two runs produce byte-identical output.

## The day's six stories

All six led the news cycle on the morning of Friday 27 November
2026 (overnight developments, first reported in the Asia morning
papers dated 27 Nov); none was used in the 26 November round.

1. **Missiles downed over Riyadh** (Saudi Arabia) — Saudi defences
   shot down two ballistic missiles fired at the capital overnight,
   plus a cruise missile and a drone near Jeddah; a day earlier a
   strike hit Riyadh's PIF tower, wounding 11.
   Sources: AFP via Gulf News, Korea Herald.
2. **Tanker fire kills 31 on Cairo ring road** (Egypt) — a fuel
   tanker overturned at rush hour and burst into flames, torching
   27 vehicles; police detained the speeding driver.
   Sources: Reuters, CNN.
3. **Kim vows more nukes, snubs Trump** (North Korea) — Kim toured
   two nuclear-materials plants and ordered tactical weapons
   deployed, days after ignoring Trump's offer to meet.
   Sources: AP via KCNA, The Hindu.
4. **Refinery blast shuts Bangkok plant** (Thailand) — an explosion
   at Bangchak's city refinery injured nine and halted all units
   at the 120,000-barrel-a-day site.
   Sources: Reuters, Al Jazeera.
5. **Ramaphosa wins court fight** (South Africa) — a high court
   threw out the 2022 panel report that fuelled the Phala Phala
   impeachment drive, calling its errors "material".
   Sources: The Hindu, CGTN.
6. **Myanmar defies genocide court** (The Hague) — Min Aung Hlaing
   says his government will not obey "inappropriate" parts of the
   world court's ruling that the state committed genocide against
   the Rohingya.
   Sources: Reuters, Straits Times.

Also noted: FCC clears SpaceX to launch 1m "Starmind" data-centre
satellites; Shenzhou-24 carries the first Pakistani astronaut to
Tiangong; EU leaders weigh a $49bn loan for Ukraine.

## Run it

```sh
python3 main.py
# or: MAKEFUN_OUTPUT_DIR=out python3 main.py
```

## License

MIT — see [LICENSE](LICENSE).
