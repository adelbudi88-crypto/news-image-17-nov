# 17 November 2026 — The World in One Day

[![news-image-20261117](https://make.fun/badge/news-image-20261117.svg)](https://make.fun/bounty/news-image-20261117)
[![rank](https://make.fun/badge/news-image-20261117/adelbudi88-crypto/news-image-17-nov/rank.svg)](https://make.fun/bounty/news-image-20261117)
[![reward](https://make.fun/badge/news-image-20261117/adelbudi88-crypto/news-image-17-nov/reward.svg)](https://make.fun/bounty/news-image-20261117)

A one-image front page summing up the world's news of Tuesday 17 November 2026, built for the [make.fun bounty](https://make.fun/bounty/news-image-20261117).

The image is a newspaper-style poster (1024x1024): a big navy header names the day, **17 November 2026**, and six drawn panels cover the day's most consequential stories across regions:

1. **Kerch Bridge struck again** (Ukraine, hero panel) — Ukraine hits the Crimea bridge a second time in under 24 hours; Russia hits Kyiv bridges over the Dnipro in reply.
2. **Tankers mined near Hormuz** (Middle East) — two tankers mined and burning; a third US carrier, USS Theodore Roosevelt, joins the region.
3. **Xi, Trump, Putin to meet** (Asia) — three-way talks in Shenzhen on Thu 19 Nov, during the APEC summit.
4. **Iran drone at US radar** (Middle East) — drone fired at US radar in Bahrain; intercepted, no casualties.
5. **UK sanctions 8 Israeli firms** (Europe) — over West Bank settlements; allies press Israel to open Gaza crossings.
6. **Japan scrambles jets + Pentagon fails 9th audit** (Asia / USA) — Russian planes near Japan; over $4.8T unverified, ninth year in a row.

## How the image was made

`entry.png` was drawn from scratch with Python + Pillow (`tools/draw.py`): flat geometric illustrations (bridge, tanker, flags, radar, gavel, jet, Pentagon) on an off-white newsprint background, navy ink, brick red and gold. No AI image generation, no downloaded images.

## Run

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
```

`main.ts` (Node 22, standard library only) copies `entry.png` to `/output/entry.png`. Running it twice writes byte-identical output.

## License

MIT — see [LICENSE](LICENSE).
