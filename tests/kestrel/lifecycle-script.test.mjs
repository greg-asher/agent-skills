import assert from "node:assert/strict";
import { chmodSync, mkdtempSync, mkdirSync, readFileSync, readdirSync, rmSync, writeFileSync } from "node:fs";
import { tmpdir } from "node:os";
import { join, resolve } from "node:path";
import { spawnSync } from "node:child_process";
import test from "node:test";

const RUNTIME = resolve("plugins/kestrel/bin/kestrel-plugin");

test("setup requires approval before invoking npm", () => {
  const fixture = temp("setup");
  try {
    const npm = executable(fixture, "fake-npm", `process.exit(99);`);
    const result = runtime(["setup", "--state-dir", fixture, "--kestrel-bin", join(fixture, "missing-kestrel"), "--npm-bin", npm, "--install-version", "1.2.3", "--allow-test-node", "--allow-test-platform", "--json"]);
    assert.equal(result.status, 2, result.stderr);
    const output = JSON.parse(result.stdout);
    assert.equal(output.status, "INSTALL_APPROVAL_REQUIRED");
    assert.equal(output.version, "1.2.3");
    assert.match(output.command, /@kestrel-agents\/kestrel@1\.2\.3/u);
  } finally { rmSync(fixture, { recursive: true, force: true }); }
});

test("setup rejects a prerelease resolved from npm stable", () => {
  const fixture = temp("prerelease");
  try {
    const npm = executable(fixture, "fake-npm", `process.stdout.write('"1.2.3-beta.1"');`);
    const result = runtime(["setup", "--state-dir", fixture, "--kestrel-bin", join(fixture, "missing-kestrel"), "--npm-bin", npm, "--allow-test-node", "--allow-test-platform"]);
    assert.equal(result.status, 1);
    assert.match(result.stderr, /resolved a prerelease/u);
  } finally { rmSync(fixture, { recursive: true, force: true }); }
});

test("recover records doctor evidence and permits only one replay", () => {
  const fixture = temp("recover"), workspace = repository(fixture), state = join(fixture, "state"), runDir = join(state, "runs", "session-one");
  mkdirSync(runDir, { recursive: true });
  writeJson(join(runDir, "manifest.json"), manifest({ workspace, lifecycle: "INTERRUPTED" }));
  writeJson(join(runDir, "output.json"), { job: { runId: "run-one", replay: { runId: "run-one" } } });
  const kestrel = executable(fixture, "fake-kestrel", `
if (process.argv.includes('doctor')) process.stdout.write('{"healthy":true}');
if (process.argv.includes('replay')) process.stdout.write('{"status":"COMPLETED"}');
`);
  try {
    const inspected = runtime(["recover", "--state-dir", state, "--session", "session-one", "--kestrel-bin", kestrel, "--json"]);
    assert.equal(inspected.status, 2, inspected.stderr);
    assert.equal(JSON.parse(inspected.stdout).status, "REPLAY_AVAILABLE");
    const replayed = runtime(["recover", "--state-dir", state, "--session", "session-one", "--kestrel-bin", kestrel, "--replay", "--json"]);
    assert.equal(replayed.status, 0, replayed.stderr);
    const saved = JSON.parse(readFileSync(join(runDir, "manifest.json"), "utf8"));
    assert.equal(saved.lifecycle, "COMPLETED_ISOLATED");
    assert.equal(saved.recoveryAttempts, 1);
  } finally { rmSync(fixture, { recursive: true, force: true }); }
});

test("integrate cherry-picks an exact result and cleanup retains evidence", () => {
  const fixture = temp("integrate"), workspace = repository(fixture), worktree = join(fixture, "managed"), state = join(fixture, "state"), runDir = join(state, "runs", "session-one");
  run("git", ["-C", workspace, "worktree", "add", "-q", "-b", "kestrel-result", worktree]);
  writeFileSync(join(worktree, "result.txt"), "completed\n", "utf8");
  run("git", ["-C", worktree, "add", "result.txt"]); run("git", ["-C", worktree, "commit", "-qm", "result"]);
  const source = run("git", ["-C", workspace, "rev-parse", "HEAD"]).stdout.trim(), resultRevision = run("git", ["-C", worktree, "rev-parse", "HEAD"]).stdout.trim();
  mkdirSync(runDir, { recursive: true }); writeJson(join(runDir, "manifest.json"), manifest({ workspace, worktree, source, resultRevision, lifecycle: "COMPLETED_ISOLATED" }));
  try {
    const integrated = runtime(["integrate", "--workspace", workspace, "--state-dir", state, "--session", "session-one", "--json"]);
    assert.equal(integrated.status, 0, integrated.stderr); assert.equal(JSON.parse(integrated.stdout).status, "INTEGRATED");
    assert.equal(readFileSync(join(workspace, "result.txt"), "utf8"), "completed\n");
    const cleaned = runtime(["cleanup", "--state-dir", state, "--session", "session-one", "--json"]);
    assert.equal(cleaned.status, 0, cleaned.stderr); assert.equal(JSON.parse(cleaned.stdout).status, "CLEANED");
    assert.equal(readFileSync(join(runDir, "manifest.json"), "utf8").includes('"lifecycle": "CLEANED"'), true);
  } finally { rmSync(fixture, { recursive: true, force: true }); }
});

test("run validates the integrated result before cleaning the worktree", () => {
  const fixture = temp("run"), workspace = repository(fixture), worktree = join(fixture, "managed"), state = join(fixture, "state"), task = join(fixture, "task.md"), validation = join(fixture, "validation.json");
  run("git", ["-C", workspace, "worktree", "add", "-q", "-b", "kestrel-run-result", worktree]);
  writeFileSync(join(worktree, "delivered.txt"), "yes\n", "utf8"); run("git", ["-C", worktree, "add", "delivered.txt"]); run("git", ["-C", worktree, "commit", "-qm", "delivered"]);
  const resultRevision = run("git", ["-C", worktree, "rev-parse", "HEAD"]).stdout.trim();
  writeFileSync(task, "Deliver the fixture.\n", "utf8"); writeJson(validation, [[process.execPath, "-e", "require('fs').accessSync('delivered.txt')"]]);
  const kestrel = executable(fixture, "fake-run-kestrel", `
import { readFileSync, writeFileSync } from 'node:fs';
const args = process.argv.slice(2);
if (args.includes('--help')) { process.stdout.write('status workspace job setup runtime'); process.exit(0); }
if (args.includes('--version')) { process.stdout.write('kestrel 1.2.3'); process.exit(0); }
if (args[0] === 'workspace') process.exit(1);
if (args[0] === 'job') {
  const input = JSON.parse(readFileSync(args[args.indexOf('--json-in') + 1], 'utf8'));
  writeFileSync(args[args.indexOf('--json-out') + 1], JSON.stringify({job:{status:'COMPLETED',sessionId:input.turn.sessionId,threadId:'thread-one',runId:'run-one',result:{assistantText:'done',output:{worktreePath:${JSON.stringify(worktree)},resultRevision:${JSON.stringify(resultRevision)},validation:[{status:'passed'}]}}}}));
}
`);
  try {
    const result = runtime(["run", "--workspace", workspace, "--task-file", task, "--validation-file", validation, "--state-dir", state, "--kestrel-bin", kestrel, "--json"]);
    assert.equal(result.status, 0, result.stderr); assert.equal(readFileSync(join(workspace, "delivered.txt"), "utf8"), "yes\n");
    const actualRun = join(state, "runs", readdirSync(join(state, "runs"))[0]);
    const saved = JSON.parse(readFileSync(join(actualRun, "manifest.json"), "utf8"));
    assert.equal(saved.lifecycle, "CLEANED"); assert.equal(saved.integration.validationStatus, "PASSED");
  } finally { rmSync(fixture, { recursive: true, force: true }); }
});

function manifest({ workspace, worktree = null, source, resultRevision = null, lifecycle }) {
  return { version: "kestrel_plugin_run_v1", sessionId: "session-one", workspaceRoot: workspace, sourceRevision: source ?? run("git", ["-C", workspace, "rev-parse", "HEAD"]).stdout.trim(), lifecycle, worktreePath: worktree, resultRevision, recoveryAttempts: 0, validation: [], integration: { status: "NOT_STARTED" }, cleanup: { status: "NOT_STARTED" }, createdAt: new Date().toISOString(), updatedAt: new Date().toISOString() };
}
function repository(root) { const path = join(root, "repo"); mkdirSync(path); run("git", ["init", "-q", path]); run("git", ["-C", path, "config", "user.email", "test@example.com"]); run("git", ["-C", path, "config", "user.name", "Test User"]); writeFileSync(join(path, "README.md"), "fixture\n", "utf8"); run("git", ["-C", path, "add", "README.md"]); run("git", ["-C", path, "commit", "-qm", "fixture"]); return path; }
function executable(root, name, body) { const path = join(root, `${name}.mjs`); writeFileSync(path, `#!/usr/bin/env node\n${body}\n`, "utf8"); chmodSync(path, 0o755); return path; }
function runtime(args) { return spawnSync(process.execPath, [RUNTIME, ...args], { encoding: "utf8" }); }
function run(bin, args) { const result = spawnSync(bin, args, { encoding: "utf8" }); assert.equal(result.status, 0, result.stderr); return result; }
function writeJson(path, value) { writeFileSync(path, `${JSON.stringify(value, null, 2)}\n`, "utf8"); }
function temp(label) { return mkdtempSync(join(tmpdir(), `kestrel-${label}-test-`)); }
