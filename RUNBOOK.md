# Runbook

Everything here is a thing you will want at a bad moment and will not want to
work out from first principles. Keep it short enough to stay true.

## The system in one paragraph

A GitHub Actions cron starts `night_loop.sh` at 21:40 UTC. It holds until 22:00,
then runs up to six cycles: ingest feeds → fresh `claude -p` session → verify and
publish → commit → dispatch a site deploy. It ends by 01:20 UTC. Two daytime
ingest crons capture feeds without any model calls. Every push to `main` rebuilds
and deploys the site. Nothing needs a human to run.

## Pause publishing

Create a `.paused` file at the repo root and push it:

```sh
touch .paused && git add .paused && git commit -m "Pause nightly publishing" && git push
```

The night loop checks for it before doing anything and exits cleanly. Daytime
ingest and the deploy workflow keep running — they cost nothing and publish
nothing new. Delete the file to resume.

Do this rather than disabling the workflow in GitHub's UI: the pause is then
visible in the repository, and it comes back on its own if you forget why.

## Take an article down

Do not delete the file. Follow `policy/verification.md §11`: replace the body at
the same slug with a retraction notice in **both** languages, add a
`correction:` entry to `updated:`, and push. The correction appears on
`/corrections.html` automatically and the deploy publishes within a couple of
minutes.

If something must come off the live site immediately and the retraction text can
wait, set `title:` and `tldr:` to a holding line and push — then write the proper
retraction. Removing the file entirely leaves a 404 where a reader had a link,
which is worse.

## The token stopped working

The nightly run authenticates with `CLAUDE_CODE_OAUTH_TOKEN`, a Claude Code
OAuth token tied to a Pro/Max subscription, stored as a repository secret.

```sh
claude setup-token                  # generates a new token locally
gh secret set CLAUDE_CODE_OAUTH_TOKEN --repo y-nihat/noiseless-news
```

Then re-run the workflow: `gh workflow run "Nightly scan"`. Note this runs a full
night immediately; use `-f smoke=true` for a two-cycle, one-story test instead.

Symptoms of an expired token: the night fails with zero successful cycles, an
issue is opened automatically, and the agent stream shows an authentication
error rather than a usage-limit error. A usage-limit error is different — the
loop detects it, ends the night deliberately, and reports
`Usage-limit stop: yes` in the run report footer.

## A night went wrong

Read in this order:

1. The **run report** for that night: `data/ledger/run-report-<date>-<HHMM>Z.md`.
   Its footer carries cycles run, articles new/updated, cost, push status and
   blocked write attempts.
2. **Open issues.** The loop opens "Night review needed" for a zero-publish
   night, an unclean cycle, a blocked out-of-scope write or an early usage stop.
   A hard failure opens "Nightly run failed" with the tail of the agent stream.
3. `data/ledger/night-stats.jsonl` — one record per cycle: gate, turns, duration,
   cost, tokens.
4. The Actions log, if the above is not enough. Agent stream files live only on
   the runner and are gone once the job ends.

**Push failed** is the one to take seriously: the night's work was committed
locally on a runner that no longer exists. The job now exits non-zero for this,
so it is visible; the work itself is lost and the stories will be re-found on a
later night.

## Roll back a bad deploy

```sh
git revert <commit> && git push
```

The push triggers a rebuild. There is no separate deploy state to unwind. If the
site build itself is broken, the last successful deployment stays live —
`build_site` renders into a staging directory and only swaps on success.

## Local development

Everything runs in Docker; no local installs.

```sh
docker compose run --rm pipeline pytest
docker compose run --rm pipeline python -m noiseless.run validate-sources --live
docker compose run --rm pipeline python -m noiseless.run validate-content
docker compose run --rm pipeline python -m noiseless.run publish --out site/dist
```

`data/` belongs to CI. `git pull` before any local run that writes it, and use
`ingest --data-dir /tmp/nn-data` for experiments so local state never diverges.

## If you are away

The system runs unattended and will keep publishing. What it cannot do without
you: answer the tuning questions in each night's report, promote or retire
sources, resolve a correction request, or notice that it has been publishing
nothing for a week.

Before a long absence, either pause it (above) or accept that the archive will
grow without review. The night-review issues will be waiting when you get back.

## Contacts

- Repository and issues: https://github.com/y-nihat/noiseless-news
- Corrections and complaints arrive as GitHub issues; the site footer points
  readers there.
