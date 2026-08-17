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

Then verify with `gh workflow run "Nightly scan" -f smoke=true` — two cycles, one
story, about 55 minutes, and it works at any time of day. A non-smoke dispatch
only does useful work inside the 22:00–01:20 UTC window: outside it the loop
captures the feeds, writes its report, says so in the log and exits **green**
within a few minutes. It used to exit red and this runbook called that correct;
it was not. A red badge for doing exactly what was asked is how a red badge
stops meaning anything. A *scheduled* run that finds no runway is different —
the cron was delivered too late to be usable, the night is lost, and that one
does go red with an issue.

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
2. **Open issues.** Exactly one per night. The loop titles it "Night review
   needed" when the job succeeded but something wants a look — a zero-publish
   night, an unclean cycle, a content-gate trip, a blocked out-of-scope write,
   an early usage stop — and "Nightly run failed" when the job failed. Both go
   through `flag_issue.sh`, so a condition that repeats comments on the open
   thread instead of opening a new issue every time. The workflow's own handler
   files only when the loop never got far enough to file for itself.
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
docker compose run --rm pipeline python -m noiseless.run source-status
docker compose run --rm pipeline python -m noiseless.run publish --out site/dist
```

Workflow files are checked by CI with actionlint, which knows rules a YAML
parser does not. Locally:

```sh
docker run --rm -v "$PWD":/repo -w /repo rhysd/actionlint:latest .github/workflows/*.yml
```

Worth running before pushing a workflow change: GitHub does not report a file
it cannot parse as a broken workflow, it reports a zero-second run named after
the file path and then behaves as though that workflow does not exist.

`validate-sources --live` reports three things, not one: `[FAIL]` cannot be
fetched, `[STALE]` fetches fine but nobody has published in a while, `[BLOCKED]`
a known refusal of CI address ranges recorded in the registry.
`source-status` applies source-lifecycle.md §4 to our own ingest record.

`data/` belongs to CI. `git pull` before any local run that writes it, and use
`ingest --data-dir /tmp/nn-data` for experiments so local state never diverges.

### Bumping the agent CLI

`nightly.yml` pins `@anthropic-ai/claude-code` to an exact version, the same way
`pipeline/requirements.txt` pins everything else. Bump it in a commit of its own
so a bad night can be traced to the change; verify with
`gh workflow run "Nightly scan" -f smoke=true` before leaving it to run
unattended.

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
