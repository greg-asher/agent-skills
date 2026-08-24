import assert from "node:assert/strict";
import { chmodSync, existsSync, mkdtempSync, mkdirSync, readFileSync, readdirSync, realpathSync, renameSync, rmSync, writeFileSync } from "node:fs";
import { tmpdir } from "node:os";
import { delimiter, join, resolve } from "node:path";
import { spawnSync } from "node:child_process";
import test from "node:test";

const RUNTIME = resolve("plugins/kestrel/bin/kestrel-plugin");

test("setup treats an explicit missing executable as authoritative", () => {
  const fixture = temp("setup");
  try {
    const npm = executable(fixture, "fake-npm", `process.exit(99);`);
    const result = runtime(["setup", "--state-dir", fixture, "--kestrel-bin", join(fixture, "missing-kestrel"), "--npm-bin", npm, "--install-version", "1.2.3", "--allow-test-node", "--allow-test-platform", "--json"]);
    assert.equal(result.status, 4, result.stderr);
    const output = JSON.parse(result.stdout);
    assert.equal(output.status, "COMPATIBILITY_ERROR");
    assert.equal(output.minimumVersion, "0.8.8");
    assert.match(output.message, /authoritative/u);
  } finally { rmSync(fixture, { recursive: true, force: true }); }
});

test("setup does not replace an explicit incompatible executable", () => {
  const fixture = temp("explicit-incompatible");
  try {
    const marker = join(fixture, "npm-ran");
    const npm = executable(fixture, "fake-npm", `import {writeFileSync} from 'node:fs';writeFileSync(${JSON.stringify(marker)},'ran');`);
    const kestrel = executable(fixture, "old-kestrel", `if(process.argv.includes('--help'))process.stdout.write('status workspace job setup runtime');else if(process.argv.includes('--version'))process.stdout.write('kestrel 0.8.7');`);
    const result = runtime(["setup", "--state-dir", fixture, "--kestrel-bin", kestrel, "--npm-bin", npm, "--approve-install", "--allow-test-node", "--allow-test-platform", "--json"]);
    assert.equal(result.status, 4, result.stderr);
    assert.equal(JSON.parse(result.stdout).detectedVersion, "0.8.7");
    assert.equal(existsSync(marker), false);
  } finally { rmSync(fixture, { recursive: true, force: true }); }
});

test("approved npm install retains its realpath despite an older PATH shadow and persists it", () => {
  const fixture = temp("npm-realpath"), prefix = join(fixture, "npm-prefix"), binDir = join(prefix, "bin"), shadowDir = join(fixture, "shadow"), state = join(fixture, "state"), capture = join(fixture, "capture.json");
  mkdirSync(binDir, { recursive:true }); mkdirSync(shadowDir);
  const oldSource = executable(shadowDir, "kestrel", `if(process.argv.includes('--help'))process.stdout.write('status workspace job setup runtime');else if(process.argv.includes('--version'))process.stdout.write('kestrel 0.8.7');`), old=join(shadowDir,"kestrel"); renameSync(oldSource,old);
  const installedSource = executable(binDir, "kestrel", `
import {writeFileSync,readFileSync} from 'node:fs';
const args=process.argv.slice(2);
if(args.includes('--help')){process.stdout.write('status workspace job setup runtime --event-type');process.exit(0)}
if(args.includes('--version')){process.stdout.write('kestrel 0.8.8');process.exit(0)}
if(args[0]==='status'){process.stdout.write('Kestrel Local Core: healthy');process.exit(0)}
if(args[0]==='job'&&args[1]==='preflight'){writeFileSync(process.env.CAPTURE,JSON.stringify({args,env:Object.fromEntries(Object.entries(process.env).filter(([key])=>key.startsWith('KESTREL_')))}));const input=JSON.parse(readFileSync(args[args.indexOf('--json-in')+1],'utf8'));writeFileSync(args[args.indexOf('--json-out')+1],JSON.stringify({version:'job_preflight_v1',capability:'local-core.execution-profile-resolution.v2',status:'ready',requestedPresetId:'cli_dev_local',resolvedPresetId:'cli_dev_local',profileId:'kestrel:cli_dev_local:fixture',profileFingerprint:'a'.repeat(64),approvalPolicyPackId:'dev',policyRevision:'kestrel:v1/cli_dev_local:v1',effectiveTools:['exec_command'],requiredTools:['exec_command'],missingTools:[],executionProfileBinding:{version:'job_execution_profile_binding_v1',authoringProfileId:input.profileId,environmentPresetId:'cli_dev_local',resolvedProfileId:'kestrel:cli_dev_local:fixture',profileFingerprint:'a'.repeat(64),policy:{id:'kestrel',version:1},approvalPolicyPack:{id:'dev',version:1,digest:'b'.repeat(64)}}}));process.exit(0)}
`), installed=join(binDir,"kestrel"); renameSync(installedSource,installed);
  const npm = executable(fixture, "npm", `const args=process.argv.slice(2);if(args[0]==='prefix'){process.stdout.write(${JSON.stringify(prefix)});process.exit(0)}if(args[0]==='install')process.exit(0);process.exit(9);`);
  try {
    const env={...process.env,PATH:`${shadowDir}${delimiter}${process.env.PATH}`,CAPTURE:capture,KESTREL_CORE_HOME:"/wrong/core",KESTREL_STATE_DIR:"/wrong/state",KESTREL_RUNTIME_DIR:"/wrong/runtime"};
    const result=spawnSync(process.execPath,[RUNTIME,"setup","--state-dir",state,"--npm-bin",npm,"--install-version","0.8.8","--approve-install","--skip-configure","--allow-test-node","--allow-test-platform","--json"],{encoding:"utf8",env});
    assert.equal(result.status,0,result.stderr);
    const saved=JSON.parse(readFileSync(join(state,"setup.json"),"utf8"));
    assert.equal(saved.executable,realpathSync(installed)); assert.notEqual(saved.executable,realpathSync(old));
    assert.equal(saved.detectedVersion,"0.8.8"); assert.equal(saved.minimumVersion,"0.8.8"); assert.equal(saved.v2Capability,"local-core.execution-profile-resolution.v2");
    const child=JSON.parse(readFileSync(capture,"utf8"));
    assert.equal(child.args.includes("--state-dir"),false); assert.deepEqual(child.env,{KESTREL_HOME:resolve(state)});
    const doctor=spawnSync(process.execPath,[RUNTIME,"doctor","--state-dir",state,"--allow-test-node","--allow-test-platform","--json"],{encoding:"utf8",env});
    assert.equal(doctor.status,0,doctor.stderr);
    assert.equal(JSON.parse(doctor.stdout).checks.kestrel.version,"0.8.8");
  } finally { rmSync(fixture,{recursive:true,force:true}); }
});

test("assignment rejects Kestrel without filtered replay support before job preflight", () => {
  const fixture = temp("replay-capability"), workspace = repository(fixture), task = join(fixture, "task.md"), marker = join(fixture, "job-ran.txt");
  writeFileSync(task, "Deliver the fixture.\n", "utf8");
  const kestrel = executable(fixture, "fake-old-kestrel", `
import { writeFileSync } from 'node:fs';
const args = process.argv.slice(2);
if (args.includes('--help')) { process.stdout.write('status workspace job setup runtime'); process.exit(0); }
if (args.includes('--version')) { process.stdout.write('kestrel 0.8.6'); process.exit(0); }
writeFileSync(${JSON.stringify(marker)}, 'ran\\n', 'utf8');
process.exit(99);
`);
  try {
    const result = runtime(["assign", "--workspace", workspace, "--task-file", task, "--state-dir", join(fixture, "state"), "--kestrel-bin", kestrel, "--json"]);
    assert.equal(result.status, 4, result.stderr);
    assert.equal(JSON.parse(result.stdout).status, "COMPATIBILITY_ERROR");
    assert.equal(existsSync(marker), false);
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

test("run recovers the managed result from replay, validates it before integration, and preserves unrelated files", () => {
  const fixture = temp("run"), workspace = repository(fixture), worktree = join(fixture, "managed"), state = join(fixture, "state"), task = join(fixture, "task.md"), validation = join(fixture, "validation.json");
  run("git", ["-C", workspace, "worktree", "add", "-q", "--detach", worktree]);
  mkdirSync(join(workspace, "unrelated")); writeFileSync(join(workspace, "unrelated", "keep.txt"), "keep\n", "utf8");
  mkdirSync(join(worktree, "delivered")); writeFileSync(join(worktree, "delivered", "one.txt"), "one\n", "utf8"); writeFileSync(join(worktree, "delivered", "two.txt"), "two\n", "utf8");
  const sourceRevision = run("git", ["-C", workspace, "rev-parse", "HEAD"]).stdout.trim();
  writeFileSync(task, "Deliver the fixture.\n", "utf8");
  writeJson(validation, [[process.execPath, "-e", `const fs=require('fs');fs.accessSync('delivered/one.txt');fs.accessSync('delivered/two.txt');if(fs.existsSync(${JSON.stringify(join(workspace, "delivered"))}))process.exit(9)`]]);
  const kestrel = executable(fixture, "fake-run-kestrel", `
import { readFileSync, writeFileSync } from 'node:fs';
const args = process.argv.slice(2);
if (args.includes('--help')) { process.stdout.write('status workspace job setup runtime --event-type'); process.exit(0); }
if (args.includes('--version')) { process.stdout.write('kestrel 1.2.3'); process.exit(0); }
if (args[0] === 'status') { process.stdout.write('Kestrel Local Core: healthy'); process.exit(0); }
if (args[0] === 'job' && args[1] === 'preflight') { const input=JSON.parse(readFileSync(args[args.indexOf('--json-in')+1],'utf8')); writeFileSync(args[args.indexOf('--json-out')+1],JSON.stringify({version:'job_preflight_v1',capability:'local-core.execution-profile-resolution.v2',status:'ready',requestedPresetId:'cli_dev_local',resolvedPresetId:'cli_dev_local',profileId:'kestrel:cli_dev_local:fixture',profileFingerprint:'a'.repeat(64),approvalPolicyPackId:'dev',policyRevision:'kestrel:v1/cli_dev_local:v1',effectiveTools:['exec_command'],requiredTools:['exec_command'],missingTools:[],executionProfileBinding:{version:'job_execution_profile_binding_v1',authoringProfileId:'kestrel',environmentPresetId:'cli_dev_local',resolvedProfileId:'kestrel:cli_dev_local:fixture',profileFingerprint:'a'.repeat(64),policy:{id:'kestrel',version:1},approvalPolicyPack:{id:'dev',version:1,digest:'b'.repeat(64)}}})); process.exit(0); }
if (args[0] === 'workspace') process.exit(1);
if (args[0] === 'runtime' && args[1] === 'replay') {
  const candidate={runId:'run-one',sessionId:'session-one',type:'managed_worktree.promotion_candidate',metadata:{worktreeRoot:${JSON.stringify(worktree)},sourceWorkspaceRoot:${JSON.stringify(workspace)},baseHead:${JSON.stringify(sourceRevision)},scope:{kind:'sessionId',value:'session-one'},changedFiles:['delivered/one.txt','delivered/two.txt'],candidateFingerprint:'candidate-one',promotionId:'promotion-one'}};
  const eventTypes=args.flatMap((value,index)=>value==='--event-type'?[args[index+1]]:[]);
  const events=eventTypes.length>0?[candidate]:[{runId:'run-one',sessionId:'session-one',type:'run.progress',metadata:{payload:'x'.repeat(17*1024*1024)}},candidate];
  writeFileSync(1, JSON.stringify({events}));
}
if (args[0] === 'job') {
  const input = JSON.parse(readFileSync(args[args.indexOf('--json-in') + 1], 'utf8'));
  const output = {job:{status:'COMPLETED',sessionId:input.turn.sessionId,threadId:'thread-one',runId:'run-one',replay:{runId:'run-one'},result:{assistantText:'done',output:{status:'COMPLETED',sessionId:input.turn.sessionId,runId:'run-one'}}}};
  writeFileSync(args[args.indexOf('--json-out') + 1], JSON.stringify(output));
}
`);
  try {
    const oversizedReplay = spawnSync(kestrel, ["runtime", "replay", "--run-id", "run-one", "--json"], { encoding: "utf8", maxBuffer: 24 * 1024 * 1024 });
    assert.equal(oversizedReplay.status, 0, oversizedReplay.stderr);
    assert.equal(Buffer.byteLength(oversizedReplay.stdout) > 16 * 1024 * 1024, true);
    assert.match(oversizedReplay.stdout, /managed_worktree\.promotion_candidate/u);
    const result = runtime(["run", "--workspace", workspace, "--task-file", task, "--validation-file", validation, "--state-dir", state, "--session", "session-one", "--kestrel-bin", kestrel, "--json"]);
    const actualRun = join(state, "runs", readdirSync(join(state, "runs"))[0]);
    assert.equal(result.status, 0, `${result.stderr}\n${readFileSync(join(actualRun, "manifest.json"), "utf8")}`); assert.equal(readFileSync(join(workspace, "delivered", "one.txt"), "utf8"), "one\n"); assert.equal(readFileSync(join(workspace, "delivered", "two.txt"), "utf8"), "two\n");
    assert.equal(readFileSync(join(workspace, "unrelated", "keep.txt"), "utf8"), "keep\n");
    const saved = JSON.parse(readFileSync(join(actualRun, "manifest.json"), "utf8"));
    const assignedInput = JSON.parse(readFileSync(join(actualRun, "input.json"), "utf8"));
    const expectedCommands = JSON.parse(readFileSync(validation, "utf8"));
    assert.deepEqual(saved.validationCommands, expectedCommands);
    assert.deepEqual(saved.validation.map((entry) => entry.command), expectedCommands);
    assert.equal(assignedInput.turn.systemInstructions.join("\n").includes(JSON.stringify(expectedCommands)), true);
    assert.equal(saved.lifecycle, "CLEANED"); assert.equal(saved.integration.validationStatus, "PASSED"); assert.equal(saved.resultHandle.source, "managed_worktree_replay"); assert.deepEqual(saved.resultHandle.changedFiles, ["delivered/one.txt", "delivered/two.txt"]);
    assert.equal(run("git", ["-C", workspace, "status", "--porcelain"]).stdout.includes("?? unrelated/"), true);
  } finally { rmSync(fixture, { recursive: true, force: true }); }
});

test("run uses the completed job result handle without replay fallback", () => {
  const fixture = temp("direct-result"), workspace = repository(fixture), worktree = join(fixture, "managed"), state = join(fixture, "state"), task = join(fixture, "task.md");
  run("git", ["-C", workspace, "worktree", "add", "-q", "--detach", worktree]);
  writeFileSync(join(worktree, "delivered.txt"), "direct result\n", "utf8");
  const sourceRevision = run("git", ["-C", workspace, "rev-parse", "HEAD"]).stdout.trim();
  writeFileSync(task, "Deliver the direct result.\n", "utf8");
  const kestrel = executable(fixture, "fake-direct-result-kestrel", `
import { readFileSync, writeFileSync } from 'node:fs';
const args = process.argv.slice(2);
if (args.includes('--help')) { process.stdout.write('status workspace job setup runtime --event-type'); process.exit(0); }
if (args.includes('--version')) { process.stdout.write('kestrel 1.2.3'); process.exit(0); }
if (args[0] === 'status') { process.stdout.write('Kestrel Local Core: healthy'); process.exit(0); }
if (args[0] === 'job' && args[1] === 'preflight') { writeFileSync(args[args.indexOf('--json-out')+1],JSON.stringify({version:'job_preflight_v1',capability:'local-core.execution-profile-resolution.v2',status:'ready',requestedPresetId:'cli_dev_local',resolvedPresetId:'cli_dev_local',profileId:'kestrel:cli_dev_local:fixture',profileFingerprint:'a'.repeat(64),approvalPolicyPackId:'dev',policyRevision:'kestrel:v1/cli_dev_local:v1',effectiveTools:['exec_command'],requiredTools:['exec_command'],missingTools:[],executionProfileBinding:{version:'job_execution_profile_binding_v1',authoringProfileId:'kestrel',environmentPresetId:'cli_dev_local',resolvedProfileId:'kestrel:cli_dev_local:fixture',profileFingerprint:'a'.repeat(64),policy:{id:'kestrel',version:1},approvalPolicyPack:{id:'dev',version:1,digest:'b'.repeat(64)}}})); process.exit(0); }
if (args[0] === 'runtime' && args[1] === 'replay') process.exit(91);
if (args[0] === 'job') {
  const input = JSON.parse(readFileSync(args[args.indexOf('--json-in') + 1], 'utf8'));
  const resultHandle={version:'job_managed_result_handle_v1',kind:'managed_worktree',worktreePath:${JSON.stringify(worktree)},sourceWorkspaceRoot:${JSON.stringify(workspace)},baseRevision:${JSON.stringify(sourceRevision)},candidateRevision:'candidate-direct',changedFiles:['delivered.txt'],promotionId:'promotion-direct'};
  writeFileSync(args[args.indexOf('--json-out') + 1], JSON.stringify({job:{status:'COMPLETED',sessionId:input.turn.sessionId,threadId:'thread-direct',runId:'run-direct',resultHandle,result:{assistantText:'done',output:{status:'COMPLETED',sessionId:input.turn.sessionId,runId:'run-direct'}}}}));
}
`);
  try {
    const result = runtime(["run", "--workspace", workspace, "--task-file", task, "--state-dir", state, "--session", "session-direct", "--kestrel-bin", kestrel, "--json"]);
    assert.equal(result.status, 0, result.stderr);
    assert.equal(readFileSync(join(workspace, "delivered.txt"), "utf8"), "direct result\n");
    const saved = JSON.parse(readFileSync(join(state, "runs", "session-direct", "manifest.json"), "utf8"));
    assert.equal(saved.lifecycle, "CLEANED");
    assert.equal(saved.resultHandle.source, "job_output");
    assert.equal(saved.resultHandle.candidateFingerprint, "candidate-direct");
  } finally { rmSync(fixture, { recursive: true, force: true }); }
});

test("run rejects a direct result handle from another job session", () => {
  const fixture = temp("direct-result-identity"), workspace = repository(fixture), worktree = join(fixture, "managed"), state = join(fixture, "state"), task = join(fixture, "task.md");
  run("git", ["-C", workspace, "worktree", "add", "-q", "--detach", worktree]);
  writeFileSync(join(worktree, "wrong-result.txt"), "wrong session\n", "utf8");
  const sourceRevision = run("git", ["-C", workspace, "rev-parse", "HEAD"]).stdout.trim();
  writeFileSync(task, "Deliver the requested result.\n", "utf8");
  const kestrel = executable(fixture, "fake-mismatched-result-kestrel", `
import { writeFileSync } from 'node:fs';
const args = process.argv.slice(2);
if (args.includes('--help')) { process.stdout.write('status workspace job setup runtime --event-type'); process.exit(0); }
if (args.includes('--version')) { process.stdout.write('kestrel 1.2.3'); process.exit(0); }
if (args[0] === 'status') { process.stdout.write('Kestrel Local Core: healthy'); process.exit(0); }
if (args[0] === 'job' && args[1] === 'preflight') { writeFileSync(args[args.indexOf('--json-out')+1],JSON.stringify({version:'job_preflight_v1',capability:'local-core.execution-profile-resolution.v2',status:'ready',requestedPresetId:'cli_dev_local',resolvedPresetId:'cli_dev_local',profileId:'kestrel:cli_dev_local:fixture',profileFingerprint:'a'.repeat(64),approvalPolicyPackId:'dev',policyRevision:'kestrel:v1/cli_dev_local:v1',effectiveTools:['exec_command'],requiredTools:['exec_command'],missingTools:[],executionProfileBinding:{version:'job_execution_profile_binding_v1',authoringProfileId:'kestrel',environmentPresetId:'cli_dev_local',resolvedProfileId:'kestrel:cli_dev_local:fixture',profileFingerprint:'a'.repeat(64),policy:{id:'kestrel',version:1},approvalPolicyPack:{id:'dev',version:1,digest:'b'.repeat(64)}}})); process.exit(0); }
if (args[0] === 'runtime' && args[1] === 'replay') { process.stderr.write('no fallback candidate\\n'); process.exit(91); }
if (args[0] === 'job') {
  const resultHandle={version:'job_managed_result_handle_v1',kind:'managed_worktree',worktreePath:${JSON.stringify(worktree)},sourceWorkspaceRoot:${JSON.stringify(workspace)},baseRevision:${JSON.stringify(sourceRevision)},candidateRevision:'candidate-wrong-session',changedFiles:['wrong-result.txt']};
  writeFileSync(args[args.indexOf('--json-out')+1],JSON.stringify({job:{status:'COMPLETED',sessionId:'another-session',threadId:'thread-wrong-session',runId:'run-wrong-session',resultHandle,result:{assistantText:'done',output:{status:'COMPLETED',sessionId:'another-session',runId:'run-wrong-session'}}}}));
}
`);
  try {
    const result = runtime(["run", "--workspace", workspace, "--task-file", task, "--state-dir", state, "--session", "expected-session", "--kestrel-bin", kestrel]);
    assert.equal(result.status, 1);
    assert.equal(existsSync(join(workspace, "wrong-result.txt")), false);
    assert.equal(existsSync(worktree), true);
    const saved = JSON.parse(readFileSync(join(state, "runs", "expected-session", "manifest.json"), "utf8"));
    assert.equal(saved.lifecycle, "COMPLETED_ISOLATED");
    assert.equal(saved.worktreePath, null);
    assert.equal(saved.resultHandle.reason, "replay_failed");
  } finally { rmSync(fixture, { recursive: true, force: true }); }
});

test("run retains isolated evidence when replay has no managed result candidate", () => {
  const fixture = temp("missing-result"), workspace = repository(fixture), state = join(fixture, "state"), task = join(fixture, "task.md");
  writeFileSync(task, "Deliver the fixture.\n", "utf8");
  const kestrel = executable(fixture, "fake-missing-result-kestrel", `
import { readFileSync, writeFileSync } from 'node:fs';
const args = process.argv.slice(2);
if (args.includes('--help')) { process.stdout.write('status workspace job setup runtime --event-type'); process.exit(0); }
if (args.includes('--version')) { process.stdout.write('kestrel 1.2.3'); process.exit(0); }
if (args[0] === 'status') { process.stdout.write('Kestrel Local Core: healthy'); process.exit(0); }
if (args[0] === 'job' && args[1] === 'preflight') { writeFileSync(args[args.indexOf('--json-out')+1],JSON.stringify({version:'job_preflight_v1',capability:'local-core.execution-profile-resolution.v2',status:'ready',requestedPresetId:'cli_dev_local',resolvedPresetId:'cli_dev_local',profileId:'kestrel:cli_dev_local:fixture',profileFingerprint:'a'.repeat(64),approvalPolicyPackId:'dev',policyRevision:'kestrel:v1/cli_dev_local:v1',effectiveTools:['exec_command'],requiredTools:['exec_command'],missingTools:[],executionProfileBinding:{version:'job_execution_profile_binding_v1',authoringProfileId:'kestrel',environmentPresetId:'cli_dev_local',resolvedProfileId:'kestrel:cli_dev_local:fixture',profileFingerprint:'a'.repeat(64),policy:{id:'kestrel',version:1},approvalPolicyPack:{id:'dev',version:1,digest:'b'.repeat(64)}}})); process.exit(0); }
if (args[0] === 'runtime' && args[1] === 'replay') { process.stdout.write('{"events":[]}'); process.exit(0); }
if (args[0] === 'job') {
  const input = JSON.parse(readFileSync(args[args.indexOf('--json-in') + 1], 'utf8'));
  writeFileSync(args[args.indexOf('--json-out') + 1], JSON.stringify({job:{status:'COMPLETED',sessionId:input.turn.sessionId,threadId:'thread-one',runId:'run-one',replay:{commands:{replay:"kestrel runtime replay --run-id 'run-one'"}},result:{assistantText:'done',output:{status:'COMPLETED',sessionId:input.turn.sessionId,runId:'run-one'}}}}));
}
`);
  try {
    const result = runtime(["run", "--workspace", workspace, "--task-file", task, "--state-dir", state, "--session", "session-one", "--kestrel-bin", kestrel]);
    assert.equal(result.status, 1);
    assert.match(result.stderr, /not recoverable from its durable replay evidence/u);
    const runDir = join(state, "runs", "session-one"), saved = JSON.parse(readFileSync(join(runDir, "manifest.json"), "utf8"));
    assert.equal(saved.lifecycle, "COMPLETED_ISOLATED");
    assert.equal(saved.resultHandle.reason, "candidate_missing");
    assert.equal(run("git", ["-C", workspace, "status", "--porcelain"]).stdout, "");
  } finally { rmSync(fixture, { recursive: true, force: true }); }
});

test("run preserves the child-process error when filtered replay still exceeds the buffer", () => {
  const fixture = temp("replay-buffer-error"), workspace = repository(fixture), state = join(fixture, "state"), task = join(fixture, "task.md");
  writeFileSync(task, "Deliver the fixture.\n", "utf8");
  const kestrel = executable(fixture, "fake-replay-buffer-error-kestrel", `
import { readFileSync, writeFileSync } from 'node:fs';
const args = process.argv.slice(2);
if (args.includes('--help')) { process.stdout.write('status workspace job setup runtime --event-type'); process.exit(0); }
if (args.includes('--version')) { process.stdout.write('kestrel 1.2.3'); process.exit(0); }
if (args[0] === 'status') { process.stdout.write('Kestrel Local Core: healthy'); process.exit(0); }
if (args[0] === 'job' && args[1] === 'preflight') { writeFileSync(args[args.indexOf('--json-out')+1],JSON.stringify({version:'job_preflight_v1',capability:'local-core.execution-profile-resolution.v2',status:'ready',requestedPresetId:'cli_dev_local',resolvedPresetId:'cli_dev_local',profileId:'kestrel:cli_dev_local:fixture',profileFingerprint:'a'.repeat(64),approvalPolicyPackId:'dev',policyRevision:'kestrel:v1/cli_dev_local:v1',effectiveTools:['exec_command'],requiredTools:['exec_command'],missingTools:[],executionProfileBinding:{version:'job_execution_profile_binding_v1',authoringProfileId:'kestrel',environmentPresetId:'cli_dev_local',resolvedProfileId:'kestrel:cli_dev_local:fixture',profileFingerprint:'a'.repeat(64),policy:{id:'kestrel',version:1},approvalPolicyPack:{id:'dev',version:1,digest:'b'.repeat(64)}}})); process.exit(0); }
if (args[0] === 'runtime' && args[1] === 'replay') { process.stderr.write('replay warning\\n'); writeFileSync(1, 'x'.repeat(17*1024*1024)); }
if (args[0] === 'job') {
  const input = JSON.parse(readFileSync(args[args.indexOf('--json-in') + 1], 'utf8'));
  writeFileSync(args[args.indexOf('--json-out') + 1], JSON.stringify({job:{status:'COMPLETED',sessionId:input.turn.sessionId,threadId:'thread-one',runId:'run-one',result:{assistantText:'done',output:{status:'COMPLETED',sessionId:input.turn.sessionId,runId:'run-one'}}}}));
}
`);
  try {
    const result = runtime(["run", "--workspace", workspace, "--task-file", task, "--state-dir", state, "--session", "session-one", "--kestrel-bin", kestrel]);
    assert.equal(result.status, 1);
    const saved = JSON.parse(readFileSync(join(state, "runs", "session-one", "manifest.json"), "utf8"));
    assert.equal(saved.lifecycle, "COMPLETED_ISOLATED");
    assert.equal(saved.resultHandle.reason, "replay_failed");
    assert.match(saved.resultHandle.message, /replay warning/u);
    assert.match(saved.resultHandle.message, /ENOBUFS|maxBuffer|buffer/u);
  } finally { rmSync(fixture, { recursive: true, force: true }); }
});

test("run does not validate or mutate the source workspace for a nonterminal job", () => {
  const fixture = temp("running"), workspace = repository(fixture), state = join(fixture, "state"), task = join(fixture, "task.md"), validation = join(fixture, "validation.json"), marker = join(workspace, "should-not-exist.txt");
  writeFileSync(task, "Keep the result isolated.\n", "utf8");
  writeJson(validation, [[process.execPath, "-e", `require('fs').writeFileSync(${JSON.stringify(marker)}, 'mutated\\n')`]]);
  const kestrel = executable(fixture, "fake-running-kestrel", `
import { readFileSync, writeFileSync } from 'node:fs';
const args = process.argv.slice(2);
if (args.includes('--help')) { process.stdout.write('status workspace job setup runtime --event-type'); process.exit(0); }
if (args.includes('--version')) { process.stdout.write('kestrel 1.2.3'); process.exit(0); }
if (args[0] === 'status') { process.stdout.write('Kestrel Local Core: healthy'); process.exit(0); }
if (args[0] === 'job' && args[1] === 'preflight') { writeFileSync(args[args.indexOf('--json-out')+1],JSON.stringify({version:'job_preflight_v1',capability:'local-core.execution-profile-resolution.v2',status:'ready',requestedPresetId:'cli_dev_local',resolvedPresetId:'cli_dev_local',profileId:'kestrel:cli_dev_local:fixture',profileFingerprint:'a'.repeat(64),approvalPolicyPackId:'dev',policyRevision:'kestrel:v1/cli_dev_local:v1',effectiveTools:['exec_command'],requiredTools:['exec_command'],missingTools:[],executionProfileBinding:{version:'job_execution_profile_binding_v1',authoringProfileId:'kestrel',environmentPresetId:'cli_dev_local',resolvedProfileId:'kestrel:cli_dev_local:fixture',profileFingerprint:'a'.repeat(64),policy:{id:'kestrel',version:1},approvalPolicyPack:{id:'dev',version:1,digest:'b'.repeat(64)}}})); process.exit(0); }
if (args[0] === 'job') { const input=JSON.parse(readFileSync(args[args.indexOf('--json-in')+1],'utf8')); writeFileSync(args[args.indexOf('--json-out')+1],JSON.stringify({job:{status:'RUNNING',sessionId:input.turn.sessionId,threadId:'thread-running',runId:'run-running',result:{assistantText:'still running',output:{status:'RUNNING',sessionId:input.turn.sessionId,runId:'run-running'}}}})); }
`);
  try {
    const result = runtime(["run", "--workspace", workspace, "--task-file", task, "--validation-file", validation, "--state-dir", state, "--session", "session-running", "--kestrel-bin", kestrel, "--json"]);
    assert.equal(result.status, 1, result.stderr);
    assert.equal(existsSync(marker), false);
    const saved = JSON.parse(readFileSync(join(state, "runs", "session-running", "manifest.json"), "utf8"));
    assert.equal(saved.lifecycle, "RUNNING");
    assert.equal(saved.integration.validationStatus, undefined);
  } finally { rmSync(fixture, { recursive:true, force:true }); }
});

test("run stops outer validation at the first failure and retains the isolated candidate", () => {
  const fixture = temp("validation-failure"), workspace = repository(fixture), worktree = join(fixture, "managed"), state = join(fixture, "state"), task = join(fixture, "task.md"), validation = join(fixture, "validation.json"), secondMarker = join(worktree, "second-command-ran.txt");
  run("git", ["-C", workspace, "worktree", "add", "-q", "--detach", worktree]);
  writeFileSync(join(worktree, "result.txt"), "candidate\n", "utf8");
  const sourceRevision = run("git", ["-C", workspace, "rev-parse", "HEAD"]).stdout.trim();
  writeFileSync(task, "Deliver the candidate.\n", "utf8");
  writeJson(validation, [[process.execPath, "-e", "process.exit(7)"], [process.execPath, "-e", `require('fs').writeFileSync(${JSON.stringify(secondMarker)}, 'should-not-run\\n')`]]);
  const kestrel = executable(fixture, "fake-validation-failure-kestrel", `
import { readFileSync, writeFileSync } from 'node:fs';
const args = process.argv.slice(2);
if (args.includes('--help')) { process.stdout.write('status workspace job setup runtime --event-type'); process.exit(0); }
if (args.includes('--version')) { process.stdout.write('kestrel 1.2.3'); process.exit(0); }
if (args[0] === 'status') { process.stdout.write('Kestrel Local Core: healthy'); process.exit(0); }
if (args[0] === 'job' && args[1] === 'preflight') { writeFileSync(args[args.indexOf('--json-out')+1],JSON.stringify({version:'job_preflight_v1',capability:'local-core.execution-profile-resolution.v2',status:'ready',requestedPresetId:'cli_dev_local',resolvedPresetId:'cli_dev_local',profileId:'kestrel:cli_dev_local:fixture',profileFingerprint:'a'.repeat(64),approvalPolicyPackId:'dev',policyRevision:'kestrel:v1/cli_dev_local:v1',effectiveTools:['exec_command'],requiredTools:['exec_command'],missingTools:[],executionProfileBinding:{version:'job_execution_profile_binding_v1',authoringProfileId:'kestrel',environmentPresetId:'cli_dev_local',resolvedProfileId:'kestrel:cli_dev_local:fixture',profileFingerprint:'a'.repeat(64),policy:{id:'kestrel',version:1},approvalPolicyPack:{id:'dev',version:1,digest:'b'.repeat(64)}}})); process.exit(0); }
if (args[0] === 'runtime' && args[1] === 'replay') { process.stdout.write(JSON.stringify({events:[{runId:'run-failure',sessionId:'session-failure',type:'managed_worktree.promotion_candidate',metadata:{worktreeRoot:${JSON.stringify(worktree)},sourceWorkspaceRoot:${JSON.stringify(workspace)},baseHead:${JSON.stringify(sourceRevision)},scope:{kind:'sessionId',value:'session-failure'},changedFiles:['result.txt'],candidateFingerprint:'candidate-failure',promotionId:'promotion-failure'}}]})); process.exit(0); }
if (args[0] === 'job') { const input=JSON.parse(readFileSync(args[args.indexOf('--json-in')+1],'utf8')); writeFileSync(args[args.indexOf('--json-out')+1],JSON.stringify({job:{status:'COMPLETED',sessionId:input.turn.sessionId,threadId:'thread-failure',runId:'run-failure',replay:{runId:'run-failure'},result:{assistantText:'done',output:{status:'COMPLETED',sessionId:input.turn.sessionId,runId:'run-failure'}}}})); }
`);
  try {
    const result = runtime(["run", "--workspace", workspace, "--task-file", task, "--validation-file", validation, "--state-dir", state, "--session", "session-failure", "--kestrel-bin", kestrel, "--json"]);
    assert.equal(result.status, 1, result.stderr);
    const runDir = join(state, "runs", "session-failure"), saved = JSON.parse(readFileSync(join(runDir, "manifest.json"), "utf8"));
    assert.equal(saved.lifecycle, "COMPLETED_ISOLATED");
    assert.equal(saved.validation.length, 1);
    assert.equal(saved.validation[0].status, 7);
    assert.equal(saved.integration.status, "NOT_STARTED");
    assert.equal(existsSync(secondMarker), false);
    assert.equal(existsSync(join(workspace, "result.txt")), false);
    assert.equal(existsSync(worktree), true);
  } finally { rmSync(fixture, { recursive:true, force:true }); }
});

test("assign does not reuse a run when the validation contract changes", () => {
  const fixture = temp("reuse-contract"), workspace = repository(fixture), state = join(fixture, "state"), task = join(fixture, "task.md"), validationOne = join(fixture, "validation-one.json"), validationTwo = join(fixture, "validation-two.json");
  writeFileSync(task, "Implement the same task.\n", "utf8");
  writeJson(validationOne, [[process.execPath, "-e", "process.exit(0)"]]);
  writeJson(validationTwo, [[process.execPath, "-e", "process.exit(0)"], [process.execPath, "-e", "process.exit(0)"]]);
  const kestrel = executable(fixture, "fake-reuse-kestrel", `
import { readFileSync, writeFileSync } from 'node:fs';
const args = process.argv.slice(2);
if (args.includes('--help')) { process.stdout.write('status workspace job setup runtime --event-type'); process.exit(0); }
if (args.includes('--version')) { process.stdout.write('kestrel 1.2.3'); process.exit(0); }
if (args[0] === 'status') { process.stdout.write('Kestrel Local Core: healthy'); process.exit(0); }
if (args[0] === 'job' && args[1] === 'preflight') { writeFileSync(args[args.indexOf('--json-out')+1],JSON.stringify({version:'job_preflight_v1',capability:'local-core.execution-profile-resolution.v2',status:'ready',requestedPresetId:'cli_dev_local',resolvedPresetId:'cli_dev_local',profileId:'kestrel:cli_dev_local:fixture',profileFingerprint:'a'.repeat(64),approvalPolicyPackId:'dev',policyRevision:'kestrel:v1/cli_dev_local:v1',effectiveTools:['exec_command'],requiredTools:['exec_command'],missingTools:[],executionProfileBinding:{version:'job_execution_profile_binding_v1',authoringProfileId:'kestrel',environmentPresetId:'cli_dev_local',resolvedProfileId:'kestrel:cli_dev_local:fixture',profileFingerprint:'a'.repeat(64),policy:{id:'kestrel',version:1},approvalPolicyPack:{id:'dev',version:1,digest:'b'.repeat(64)}}})); process.exit(0); }
if (args[0] === 'job') { const input=JSON.parse(readFileSync(args[args.indexOf('--json-in')+1],'utf8')); writeFileSync(args[args.indexOf('--json-out')+1],JSON.stringify({job:{status:'COMPLETED',sessionId:input.turn.sessionId,threadId:'thread-reuse',runId:input.turn.sessionId,replay:{runId:input.turn.sessionId},result:{assistantText:'done',output:{status:'COMPLETED',sessionId:input.turn.sessionId,runId:input.turn.sessionId}}}})); }
`);
  try {
    const first = runtime(["assign", "--workspace", workspace, "--task", "Implement the same task.", "--validation-file", validationOne, "--state-dir", state, "--session", "session-one", "--kestrel-bin", kestrel, "--json"]);
    const second = runtime(["assign", "--workspace", workspace, "--task", "Implement the same task.", "--validation-file", validationTwo, "--state-dir", state, "--session", "session-two", "--kestrel-bin", kestrel, "--json"]);
    assert.equal(first.status, 0, first.stderr);
    assert.equal(second.status, 0, second.stderr);
    assert.deepEqual(readdirSync(join(state, "runs")).sort(), ["session-one", "session-two"]);
    assert.deepEqual(JSON.parse(readFileSync(join(state, "runs", "session-two", "manifest.json"), "utf8")).validationCommands, JSON.parse(readFileSync(validationTwo, "utf8")));
  } finally { rmSync(fixture, { recursive:true, force:true }); }
});

test("doctor and assignment propagate one authoritative state directory", () => {
  const fixture = temp("state-contract"), workspace = repository(fixture), state = join(fixture, "state"), task = join(fixture, "task.md");
  writeFileSync(task, "Use the configured runtime.\n", "utf8");
  const kestrel = executable(fixture, "state-contract-kestrel", `
import { readFileSync, writeFileSync } from 'node:fs';
const args = process.argv.slice(2);
if (args.includes('--help')) { process.stdout.write('status workspace job setup runtime --event-type'); process.exit(0); }
if (args.includes('--version')) { process.stdout.write('kestrel 9.9.9'); process.exit(0); }
if (args[0] === 'status') { process.stdout.write('Kestrel Local Core: healthy'); process.exit(0); }
if (args[0] === 'core') process.exit(0);
if (args[0] === 'job' && args[1] === 'preflight') { writeFileSync(args[args.indexOf('--json-out')+1],JSON.stringify({version:'job_preflight_v1',capability:'local-core.execution-profile-resolution.v2',status:'ready',requestedPresetId:'cli_dev_local',resolvedPresetId:'cli_dev_local',profileId:'kestrel:cli_dev_local:fixture',profileFingerprint:'a'.repeat(64),approvalPolicyPackId:'dev',policyRevision:'kestrel:v1/cli_dev_local:v1',effectiveTools:['exec_command'],requiredTools:['exec_command'],missingTools:[],executionProfileBinding:{version:'job_execution_profile_binding_v1',authoringProfileId:'kestrel',environmentPresetId:'cli_dev_local',resolvedProfileId:'kestrel:cli_dev_local:fixture',profileFingerprint:'a'.repeat(64),policy:{id:'kestrel',version:1},approvalPolicyPack:{id:'dev',version:1,digest:'b'.repeat(64)}}})); process.exit(0); }
if (args[0] === 'job') {
  writeFileSync(process.env.RUNTIME_CAPTURE, JSON.stringify({ args, env: Object.fromEntries(Object.entries(process.env).filter(([key]) => key.startsWith('KESTREL_'))) }));
  const input = JSON.parse(readFileSync(args[args.indexOf('--json-in') + 1], 'utf8'));
  writeFileSync(args[args.indexOf('--json-out') + 1], JSON.stringify({ job: { status: 'WAITING', sessionId: input.turn.sessionId, runId: 'run-state' } }));
}
`);
  const capture = join(fixture, "capture.json");
  try {
    const env = { ...process.env, RUNTIME_CAPTURE: capture };
    const doctor = spawnSync(process.execPath, [RUNTIME, "doctor", "--workspace", workspace, "--state-dir", state, "--kestrel-bin", kestrel, "--allow-test-node", "--allow-test-platform", "--json"], { encoding: "utf8", env });
    assert.equal(doctor.status, 0, doctor.stderr); const report = JSON.parse(doctor.stdout);
    assert.equal(report.status, "READY"); assert.deepEqual(report.runtimeConfig, { stateDir:resolve(state), kestrelHome:resolve(state) });
    const assigned = spawnSync(process.execPath, [RUNTIME, "assign", "--workspace", workspace, "--task-file", task, "--state-dir", state, "--kestrel-bin", kestrel, "--allow-test-node", "--allow-test-platform"], { encoding: "utf8", env });
    assert.equal(assigned.status, 2, assigned.stderr); const saved = JSON.parse(readFileSync(capture, "utf8"));
    assert.deepEqual(saved.env, { KESTREL_HOME:resolve(state) });
    assert.equal(saved.args.includes("--state-dir"), false);
  } finally { rmSync(fixture, { recursive: true, force: true }); }
});

test("older Kestrel fails compatibility without assignment mutation", () => {
  const fixture = temp("old-kestrel"), workspace = repository(fixture), state = join(fixture, "state"), task = join(fixture, "task.md");
  writeFileSync(task, "This must not run.\n", "utf8");
  const kestrel = executable(fixture, "must-not-run-kestrel", `if (process.argv.includes('job')) process.exit(99); if (process.argv.includes('--help')) process.stdout.write('status workspace job setup runtime'); if (process.argv.includes('--version')) process.stdout.write('kestrel 0.8.7');`);
  try {
    const result = runtime(["assign", "--workspace", workspace, "--task-file", task, "--state-dir", state, "--session", "session-one", "--kestrel-bin", kestrel, "--json"]);
    assert.equal(result.status, 4, result.stderr); const output = JSON.parse(result.stdout);
    assert.equal(output.status, "COMPATIBILITY_ERROR"); assert.equal(output.noMutation.assignment, true);
    assert.equal(existsSync(state), false);
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
