param(
    [Alias('WorkspaceRoot')]
    [string]$StorageRoot,
    [switch]$StorageConfirmed,
    [string]$TemplatePath,
    [string]$EngagementId
)

$ErrorActionPreference = 'Stop'
if (-not $StorageConfirmed) { throw 'Storage location is not confirmed. Confirm it once with the participant before creating a new engagement.' }
if (-not $StorageRoot) {
    $documents = [Environment]::GetFolderPath('MyDocuments')
    if ([string]::IsNullOrWhiteSpace($documents)) { throw 'Unable to resolve the current user Documents folder. Pass -StorageRoot explicitly.' }
    $StorageRoot = Join-Path $documents 'BU Knowledge Engagements'
}
$engagementRoot = [System.IO.Path]::GetFullPath($StorageRoot)

# Refuse to place business outputs inside the delivery workspace or plugin source.
$cursor = [System.IO.DirectoryInfo]::new([System.IO.Path]::GetFullPath((Join-Path $PSScriptRoot '..')))
$deliveryRoot = $null
while ($cursor) {
    if ((Test-Path -LiteralPath (Join-Path $cursor.FullName '.agents\skills') -PathType Container) -or
        (Test-Path -LiteralPath (Join-Path $cursor.FullName '.codex-plugin\plugin.json') -PathType Leaf)) {
        $deliveryRoot = $cursor.FullName
        break
    }
    $cursor = $cursor.Parent
}
if ($deliveryRoot) {
    $deliveryPrefix = $deliveryRoot.TrimEnd('\', '/') + [System.IO.Path]::DirectorySeparatorChar
    if ($engagementRoot.Equals($deliveryRoot, [System.StringComparison]::OrdinalIgnoreCase) -or
        $engagementRoot.StartsWith($deliveryPrefix, [System.StringComparison]::OrdinalIgnoreCase)) {
        throw "Storage root must be outside the Skill, Plugin, or delivery workspace: $engagementRoot"
    }
}

if (-not (Test-Path -LiteralPath $engagementRoot)) { New-Item -ItemType Directory -Path $engagementRoot -Force | Out-Null }
if (-not (Test-Path -LiteralPath $engagementRoot -PathType Container)) { throw "Storage root is not a directory: $engagementRoot" }
$bundledTemplate = [System.IO.Path]::GetFullPath((Join-Path $PSScriptRoot '..\assets\engagement-template'))
$template = if ($TemplatePath) {
    [System.IO.Path]::GetFullPath($TemplatePath)
} else {
    $bundledTemplate
}
if (-not (Test-Path -LiteralPath $template)) { throw "Engagement template not found: $template" }

if (-not $EngagementId) {
    # The business need is intentionally unknown at case creation time. Keep the
    # identifier neutral and never derive it from the workspace or folder name.
    $EngagementId = 'ENG-{0}' -f (Get-Date -Format 'yyyyMMdd-HHmmss')
}

$target = [System.IO.Path]::GetFullPath((Join-Path $engagementRoot $EngagementId))
$engagementPrefix = $engagementRoot.TrimEnd('\', '/') + [System.IO.Path]::DirectorySeparatorChar
if (-not $target.StartsWith($engagementPrefix, [System.StringComparison]::OrdinalIgnoreCase)) {
    throw "Unsafe engagement path: $target"
}
if (Test-Path -LiteralPath $target) { throw "Engagement already exists: $target" }

Copy-Item -LiteralPath $template -Destination $target -Recurse
$now = (Get-Date).ToString('o')
$yamlPath = Join-Path $target 'engagement.yaml'
$yaml = Get-Content -Raw -LiteralPath $yamlPath
$yaml = $yaml -replace 'engagement_id: ""', ('engagement_id: "{0}"' -f $EngagementId)
$yaml = $yaml -replace 'created_at: ""', ('created_at: "{0}"' -f $now)
$yaml = $yaml -replace 'updated_at: ""', ('updated_at: "{0}"' -f $now)
$yamlRoot = $engagementRoot.Replace('\', '/')
$yamlTarget = $target.Replace('\', '/')
$yaml = $yaml -replace "root: ''", ("root: '{0}'" -f $yamlRoot.Replace("'", "''"))
$yaml = $yaml -replace "engagement_path: ''", ("engagement_path: '{0}'" -f $yamlTarget.Replace("'", "''"))
$yaml = $yaml -replace "confirmed_at: ''", ("confirmed_at: '{0}'" -f $now)
Set-Content -LiteralPath $yamlPath -Value $yaml -Encoding UTF8

$manifestPath = Join-Path $target '10_evidence\evidence-manifest.json'
$manifest = Get-Content -Raw -LiteralPath $manifestPath | ConvertFrom-Json
$manifest.engagement_id = $EngagementId
$manifest | ConvertTo-Json -Depth 8 | Set-Content -LiteralPath $manifestPath -Encoding UTF8

[PSCustomObject]@{
    engagement_id = $EngagementId
    path = $target
    storage_root = $engagementRoot
    storage_confirmed = $true
    created_at = $now
} | ConvertTo-Json
