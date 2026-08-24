import assert from "node:assert/strict";
import {
  chmodSync,
  mkdtempSync,
  mkdirSync,
  readFileSync,
  readdirSync,
  realpathSync,
  rmSync,
  writeFileSync,
} from "node:fs";
import { tmpdir } from "node:os";
import { join, resolve } from "node:path";
import { spawnSync } from "node:child_process";
import test from "node:test";

const WRAPPER = resolve("plugins/kestrel/bin/kestrel-assign");

test("kestrel-assign submits a full-auto managed-worktree job and preserves its output", () => {
  const fixture = createFixture("COMPLETED");
  try {
    const result = runWrapper(fixture);
    assert.equal(result.status, 0, result.stderr);

    const assignmentDir = onlyAssignment(fixture.stateDir);
    const input = JSON.parse(readFileSync(join(assignmentDir, "input.json"), "utf8"));
    const output = JSON.parse(readFileSync(join(assignmentDir, "output.json"), "utf8"));

    assert.equal(input.version, "job_input_v2");
    assert.equal(input.environmentPresetId, "cli_dev_local");
    assert.equal(input.profileId, "kestrel:cli_dev_local:fixture");
    assert.equal(input.approvalPolicyPackId, "dev");
    assert.equal(input.turn.message, "Implement sample behavior.\nValidate it.");
    assert.equal(input.turn.interactionMode, "build");
    assert.equal(input.turn.actSubmode, "full_auto");
    assert.equal(input.turn.noninteractive, true);
    assert.equal(input.turn.workspace.workspaceRoot, realpathSync(fixture.workspace));
    assert.equal(input.turn.workspace.managedWorktreeRequired, true);
    assert.equal(input.turn.workspace.managedWorktreeIsolation, "session");
    assert.match(input.turn.systemInstructions.join("\n"), /host exec_command/u);
    assert.equal(output.job.status, "COMPLETED");
    assert.match(result.stdout, /status=COMPLETED/u);
    assert.match(result.stdout, /run=run-test/u);
    assert.match(result.stdout, /replay=kestrel runtime replay --run-id run-test/u);
    assert.match(result.stdout, /Implemented and validated\./u);
  } finally {
    rmSync(fixture.root, { recursive: true, force: true });
  }
});

test("kestrel-assign fails before assignment when job preflight is unsatisfied", () => {
  const fixture = createFixture("COMPLETED");
  try {
    const result = spawnSync(process.execPath, [WRAPPER, "--workspace", fixture.workspace, "--task-file", fixture.taskFile, "--state-dir", fixture.stateDir, "--kestrel-bin", fixture.fakeKestrel, "--json"], { cwd:resolve("."), encoding:"utf8", env:{...process.env,FAKE_KESTREL_PREFLIGHT:"missing-tool"} });
    assert.equal(result.status, 3, result.stderr);
    assert.equal(JSON.parse(result.stdout).status, "SETUP_REQUIRED");
    assert.deepEqual(readdirSync(join(fixture.stateDir, "runs")), []);
  } finally { rmSync(fixture.root, { recursive:true, force:true }); }
});

test("kestrel-assign returns a distinct status when Kestrel is waiting", () => {
  const fixture = createFixture("WAITING");
  try {
    const result = runWrapper(fixture);
    assert.equal(result.status, 2, result.stderr);
    assert.match(result.stdout, /status=WAITING/u);
    assert.match(result.stdout, /output=.*output\.json/u);
  } finally {
    rmSync(fixture.root, { recursive: true, force: true });
  }
});

function createFixture(status) {
  const root = mkdtempSync(join(tmpdir(), "kestrel-assign-test-"));
  const workspace = join(root, "workspace");
  const stateDir = join(root, "state");
  const taskFile = join(root, "task.md");
  const fakeKestrel = join(root, "fake-kestrel.mjs");
  mkdirSync(workspace);
  mkdirSync(stateDir);
  writeFileSync(taskFile, "Implement sample behavior.\nValidate it.\n", "utf8");
  writeFileSync(join(workspace, "README.md"), "fixture\n", "utf8");
  run("git", ["init", "-q"], workspace);
  run("git", ["config", "user.email", "test@example.com"], workspace);
  run("git", ["config", "user.name", "Test User"], workspace);
  run("git", ["add", "README.md"], workspace);
  run("git", ["commit", "-qm", "fixture"], workspace);
  writeFileSync(fakeKestrel, fakeKestrelSource(), "utf8");
  chmodSync(fakeKestrel, 0o755);
  return { root, workspace, stateDir, taskFile, fakeKestrel, status };
}

function runWrapper(fixture) {
  return spawnSync(
    process.execPath,
    [
      WRAPPER,
      "--workspace",
      fixture.workspace,
      "--task-file",
      fixture.taskFile,
      "--state-dir",
      fixture.stateDir,
      "--kestrel-bin",
      fixture.fakeKestrel,
    ],
    {
      cwd: resolve("."),
      encoding: "utf8",
      env: { ...process.env, FAKE_KESTREL_STATUS: fixture.status },
    },
  );
}

function onlyAssignment(stateDir) {
  const runsDir = join(stateDir, "runs");
  const entries = readdirSync(runsDir);
  assert.equal(entries.length, 1);
  return join(runsDir, entries[0]);
}

function run(command, args, cwd) {
  const result = spawnSync(command, args, { cwd, encoding: "utf8" });
  assert.equal(result.status, 0, result.stderr);
}

function fakeKestrelSource() {
  return `#!/usr/bin/env node
import { readFileSync, writeFileSync } from "node:fs";
const args = process.argv.slice(2);
const inputPath = args[args.indexOf("--json-in") + 1];
const outputPath = args[args.indexOf("--json-out") + 1];
const input = JSON.parse(readFileSync(inputPath, "utf8"));
if (args[0] === "job" && args[1] === "preflight") {
  const missing = process.env.FAKE_KESTREL_PREFLIGHT === "missing-tool";
  writeFileSync(outputPath, JSON.stringify({version:"job_preflight_v1",status:missing?"setup_required":"ready",requestedPresetId:"cli_dev_local",resolvedPresetId:"cli_dev_local",profileId:"kestrel:cli_dev_local:fixture",profileFingerprint:"fixture",approvalPolicyPackId:"dev",policyRevision:"cli_dev_local:v1",effectiveTools:missing?[]:["exec_command"],requiredTools:["exec_command"],missingTools:missing?["exec_command"]:[],...(missing?{code:"SETUP_REQUIRED",remediation:"Enable exec_command"}:{})}));
  process.exit(missing ? 1 : 0);
}
const status = process.env.FAKE_KESTREL_STATUS ?? "COMPLETED";
const output = {
  version: "job_output_v1",
  terminalEventType: "job.completed",
  job: {
    version: "job_run_result_v1",
    sessionId: input.turn.sessionId,
    threadId: "thread-test",
    runId: "run-test",
    status,
    replay: {
      version: "job_replay_pointer_v1",
      sessionId: input.turn.sessionId,
      threadId: "thread-test",
      runId: "run-test",
      replayQuery: { runId: "run-test", sessionId: input.turn.sessionId, threadId: "thread-test" },
      commands: {
        replay: "kestrel runtime replay --run-id run-test",
        doctor: "kestrel runtime doctor --run-id run-test",
        bundle: "kestrel runtime bundle --run-id run-test --out bundle.json"
      }
    },
    result: {
      assistantText: status === "COMPLETED" ? "Implemented and validated." : "Need operator input.",
      output: { status, sessionId: input.turn.sessionId, runId: "run-test", errors: [] }
    }
  }
};
writeFileSync(outputPath, JSON.stringify(output, null, 2));
process.stdout.write("job completed session=" + input.turn.sessionId + " thread=thread-test run=run-test\\n");
`;
}
