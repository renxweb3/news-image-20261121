// news-image-20261121 — entry program (Node 22, standard library only).
//
// The picture itself is drawn by draw.py (Pillow, using the system DejaVu
// fonts) and stored as entry.png beside this file. This program copies that
// image to the output directory the grader provides, so every run writes
// exactly the same bytes. No network, no randomness.
//
// Run it locally like this:
//   mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { copyFileSync } from "node:fs";
import { join } from "node:path";

const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";

copyFileSync(
  new URL("./entry.png", import.meta.url),
  join(outDir, "entry.png"),
);
