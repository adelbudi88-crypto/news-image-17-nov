// News-image entry (Node 22, standard library only): the image is the
// entry.png beside this file, drawn with Python + Pillow in tools/draw.py,
// and this program copies it to /output/entry.png. Deterministic: the same
// bytes are written on every run, with no network access and no randomness.
// The output directory is created when it does not exist yet, so the copy
// works both in the grader's container and in a local checkout.
//
// Outside the grader's container, MAKEFUN_OUTPUT_DIR stands in for /output:
//   mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { copyFileSync, mkdirSync } from 'node:fs';
import { join } from 'node:path';

const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';
mkdirSync(outDir, { recursive: true });
copyFileSync(
  new URL('./entry.png', import.meta.url),
  join(outDir, 'entry.png'),
);
