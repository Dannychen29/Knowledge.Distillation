[CmdletBinding()]
param(
    [string]$SkillsPath
)

$ErrorActionPreference = 'Stop'
if ([string]::IsNullOrWhiteSpace($SkillsPath)) {
    $SkillsPath = (Resolve-Path (Join-Path $PSScriptRoot '..\..')).Path
}

$requiredFiles = @(
    'bu-knowledge-workflow/SKILL.md',
    'bu-knowledge-workflow/scripts/new-run.ps1',
    'bu-knowledge-workflow/references/run-state-contract.md',
    'bu-knowledge-workflow/references/workflow-contract.md',
    'bu-knowledge-workflow/references/intake-contract.md',
    'bu-knowledge-workflow/references/spec-contract.md',
    'bu-knowledge-workflow/references/solution-contract.md',
    'bu-knowledge-workflow/references/feedback-contract.md',
    'bu-knowledge-workflow/references/run-workspace-contract.md'
)
$requiredSkills = @('conduct-bu-interview', 'distill-bu-knowledge', 'build-bu-solution', 'validate-and-improve-solution')
$requiredOptionalSkills = @('record-bu-walkthrough', 'prepare-audio-evidence', 'extract-video-evidence', 'analyze-video-evidence')
$missing = @()

foreach ($relativePath in $requiredFiles) {
    if (-not (Test-Path -LiteralPath (Join-Path $SkillsPath $relativePath) -PathType Leaf)) {
        $missing += $relativePath
    }
}

foreach ($skillName in $requiredSkills) {
    $skillFile = Join-Path $SkillsPath "$skillName/SKILL.md"
    if (-not (Test-Path -LiteralPath $skillFile -PathType Leaf)) {
        $missing += "$skillName/SKILL.md"
    }
}

foreach ($skillName in $requiredOptionalSkills) {
    $skillFile = Join-Path $SkillsPath "$skillName/SKILL.md"
    if (-not (Test-Path -LiteralPath $skillFile -PathType Leaf)) {
        $missing += "$skillName/SKILL.md"
    }
}

if ($missing.Count -gt 0) {
    throw "Skill-set structure is incomplete: $($missing -join ', ')"
}

Write-Output 'VALID: pure BU knowledge workflow skill set'
