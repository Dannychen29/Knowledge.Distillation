[CmdletBinding()]
param(
    [string]$RunsRoot,
    [string]$RunId
)

$ErrorActionPreference = 'Stop'
if ([string]::IsNullOrWhiteSpace($RunsRoot)) {
    $repositoryRoot = (Resolve-Path (Join-Path $PSScriptRoot '..\..\..\..')).Path
    $RunsRoot = Join-Path $repositoryRoot 'runs'
}

if ([string]::IsNullOrWhiteSpace($RunId)) {
    $RunId = 'RUN-{0:yyyyMMdd-HHmmss}' -f (Get-Date)
}

$runPath = Join-Path $RunsRoot $RunId
if (Test-Path -LiteralPath $runPath) {
    throw "Run already exists: $runPath"
}

$directories = @(
    'input/prd',
    'input/process-diagrams',
    'input/documents',
    'input/supporting',
    'input/media',
    'input/observations',
    'output',
    'solution',
    'feedback',
    'evaluation'
)

foreach ($directory in $directories) {
    New-Item -ItemType Directory -Force -Path (Join-Path $runPath $directory) | Out-Null
}

$statePath = Join-Path $runPath 'run-state.yaml'
@"
run_id: $RunId
status: active
intake_mode: null
current_stage: interview
next_skill: conduct-bu-interview
next_action: collect_intake
iteration: 0
artifacts:
  intake_package: null
  normalized_prd: null
  implementation_spec: null
  solution_brief: null
  solution: null
  validation_record: null
open_item:
  kind: none
  id: null
  prompt: null
invalidated_artifacts: []
"@ | Set-Content -LiteralPath $statePath -Encoding utf8

Write-Output $runPath
