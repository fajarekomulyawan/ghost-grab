// The agent builds a game from one prompt — entry hand-in.
//
// The entry itself is a post on X: a short video of an AI coding
// agent building the tiny browser game in this repository
// (game.html) from a single prompt, ending with make.fun's
// referral end card. This program hands in the post's address:
// it reads POST.json from the repository root, checks that the
// URL is a canonical X status link, and copies POST.json into
// the output directory (/output, or $MAKEFUN_OUTPUT_DIR when the
// grader sets it).
//
//   MAKEFUN_OUTPUT_DIR=out node main.ts
//
// Node 22, standard library only, no network.

import { copyFileSync, mkdirSync, readFileSync } from 'node:fs';
import { join } from 'node:path';
import { fileURLToPath } from 'node:url';

const repoRoot = fileURLToPath(new URL('.', import.meta.url));
const postFile = join(repoRoot, 'POST.json');
const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';

// A canonical status link: https://x.com/<handle>/status/<digits>.
// twitter.com and the www./mobile. subdomains say the same thing,
// and the handle-less /i/web/status/<digits> form is the same
// post again, so both shapes pass.
const STATUS =
  /^https:\/\/(www\.|mobile\.)?(x\.com|twitter\.com)\/[^/]+\/status\/\d+$/;
const WEB_STATUS =
  /^https:\/\/(www\.|mobile\.)?(x\.com|twitter\.com)\/i\/web\/status\/\d+$/;

const parsed = JSON.parse(readFileSync(postFile, 'utf8')) as {
  url?: unknown;
};
const url = parsed.url;

if (typeof url !== 'string' || url.length === 0) {
  throw new Error(`POST.json: "url" must be a non-empty string`);
}
// Query strings and fragments would make the handed-in address
// differ from the post's canonical one, so refuse them outright.
if (url.includes('?') || url.includes('#')) {
  throw new Error(`POST.json: url must not carry ? or #: ${url}`);
}
if (!STATUS.test(url) && !WEB_STATUS.test(url)) {
  throw new Error(`POST.json: not an X status link: ${url}`);
}

mkdirSync(outDir, { recursive: true });
const target = join(outDir, 'POST.json');
copyFileSync(postFile, target);
console.log(`handed in ${url} -> ${target}`);
