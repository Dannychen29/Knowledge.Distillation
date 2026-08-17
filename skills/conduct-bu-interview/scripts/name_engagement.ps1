param(
    [Parameter(Mandatory = $true)]
    [string]$EngagementPath,
    [Parameter(Mandatory = $true)]
    [string]$Title
)

$ErrorActionPreference = 'Stop'
$source = [System.IO.Path]::GetFullPath($EngagementPath)
if (-not (Test-Path -LiteralPath $source -PathType Container)) { throw "Engagement folder not found: $source" }
if ([string]::IsNullOrWhiteSpace($Title)) { throw 'Confirmed title must not be blank.' }

$yamlPath = Join-Path $source 'engagement.yaml'
if (-not (Test-Path -LiteralPath $yamlPath -PathType Leaf)) { throw "engagement.yaml not found: $yamlPath" }
$yaml = Get-Content -Raw -Encoding UTF8 -LiteralPath $yamlPath
$idMatch = [regex]::Match($yaml, '(?m)^engagement_id:\s*"([^"]+)"\s*$')
if (-not $idMatch.Success) { throw 'engagement.yaml has no valid engagement_id.' }
$engagementId = $idMatch.Groups[1].Value
if ($engagementId -notmatch '^ENG-[A-Za-z0-9-]+$') { throw "Unsafe engagement ID: $engagementId" }

$slug = ($Title.Trim().ToLowerInvariant() -replace '[^a-z0-9\p{L}]+', '-' -replace '^-|-$', '')
if ([string]::IsNullOrWhiteSpace($slug)) { throw 'Confirmed title cannot be converted to a safe folder name.' }
if ($slug.Length -gt 32) { $slug = $slug.Substring(0, 32).TrimEnd('-') }

$parent = Split-Path -Parent $source
$target = [System.IO.Path]::GetFullPath((Join-Path $parent ("{0}-{1}" -f $engagementId, $slug)))
$parentPrefix = [System.IO.Path]::GetFullPath($parent).TrimEnd('\', '/') + [System.IO.Path]::DirectorySeparatorChar
if (-not $target.StartsWith($parentPrefix, [System.StringComparison]::OrdinalIgnoreCase)) { throw "Unsafe renamed path: $target" }
if (-not $source.Equals($target, [System.StringComparison]::OrdinalIgnoreCase)) {
    if (Test-Path -LiteralPath $target) { throw "Renamed engagement already exists: $target" }
    Move-Item -LiteralPath $source -Destination $target
}

$now = (Get-Date).ToString('o')
$yamlPath = Join-Path $target 'engagement.yaml'
$yaml = Get-Content -Raw -Encoding UTF8 -LiteralPath $yamlPath
$safeTitle = $Title.Trim().Replace('"', '\"')
$yaml = [regex]::Replace($yaml, '(?m)^title:\s*.*$', ('title: "{0}"' -f $safeTitle), 1)
$yaml = [regex]::Replace($yaml, '(?m)^updated_at:\s*.*$', ('updated_at: "{0}"' -f $now), 1)
$yamlTarget = $target.Replace('\', '/').Replace("'", "''")
$yaml = [regex]::Replace($yaml, "(?m)^\s+engagement_path:\s*'.*'$", ("  engagement_path: '{0}'" -f $yamlTarget), 1)
Set-Content -LiteralPath $yamlPath -Value $yaml -Encoding UTF8

[PSCustomObject]@{
    engagement_id = $engagementId
    title = $Title.Trim()
    path = $target
    renamed_at = $now
} | ConvertTo-Json
