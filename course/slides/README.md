# FDE101 Slides Pipeline

Turn the chapter/bonus `courseware.md` files into presentation slides using [Marp](https://marp.app/).

## How it works

```
courseware.md  →  convert.py  →  build/*.marp.md  →  Marp CLI  →  HTML / PDF / PPTX
                                                      (mlopsguru theme)
```

`convert.py` extracts each `### Slide N — Title` block (and its bullets) from a courseware file and emits clean Marp markdown using the `mlopsguru` theme.

## One-time setup

```bash
cd course/slides
npm install            # installs @marp-team/marp-cli locally
```

## Build all decks

```bash
cd course/slides
./build.sh
```

Outputs land in `course/slides/build/`:
- `*.html` — always generated (no Chrome needed)
- `*.pdf` / `*.pptx` — generated when a Chrome/Chromium is available to Marp

## Build a single deck

```bash
python3 convert.py ../bonus-modules/aws/courseware.md build/aws.marp.md
node_modules/.bin/marp --theme-set theme/mlopsguru.css build/aws.marp.md -o build/aws.html
```

## Branding

Theme: `theme/mlopsguru.css` — title is **mlopsguru**. Edit colors/footer there.

## PDF/PPTX troubleshooting

Marp uses headless Chrome (Puppeteer) for PDF/PPTX. If export hangs:
- Generate HTML first (works offline, no Chrome).
- Set `CHROME_PATH` to a Chrome/Chromium binary, or install one.
- Close other Chrome instances, then re-run `./build.sh`.
- As a fallback, open the HTML in a browser and "Print → Save as PDF".

## Free alternative: Gamma

You can import the generated markdown into [Gamma](https://gamma.app) (free tier) to auto-format slides — paste the contents of a `courseware.md` or a `build/*.marp.md` file.
