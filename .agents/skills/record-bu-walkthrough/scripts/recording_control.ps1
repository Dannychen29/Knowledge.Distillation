param(
    [Parameter(Mandatory = $true)]
    [ValidateSet('check', 'start', 'stop', 'status')]
    [string]$Action,
    [Parameter(Mandatory = $true)]
    [string]$EngagementPath,
    [string]$Label = 'screen-walkthrough',
    [switch]$Confirmed,
    [int]$DiscoveryTimeoutSeconds = 30,
    [string]$PythonPath,
    [string]$TranscriptionModel = 'small',
    [int]$TranscriptionBeamSize = 1,
    [string]$Language = 'auto',
    [string]$InitialPrompt = '',
    [switch]$AllowModelDownload
)

$ErrorActionPreference = 'Stop'

function Get-SafeEngagementPath([string]$Path) {
    $resolved = [System.IO.Path]::GetFullPath($Path)
    if (-not (Test-Path -LiteralPath $resolved -PathType Container)) { throw "Engagement path not found: $resolved" }
    if (-not (Test-Path -LiteralPath (Join-Path $resolved 'engagement.yaml'))) { throw "Not an engagement folder: $resolved" }
    return $resolved
}

function Get-RecordingStatePath([string]$Engagement) {
    $runtime = Join-Path $Engagement '.runtime'
    if (-not (Test-Path -LiteralPath $runtime)) { New-Item -ItemType Directory -Path $runtime | Out-Null }
    return Join-Path $runtime 'recording-session.json'
}

function Get-GameBarCheck {
    $package = Get-AppxPackage Microsoft.XboxGamingOverlay -ErrorAction SilentlyContinue
    $gameDvr = Get-ItemProperty 'HKCU:\System\GameConfigStore' -ErrorAction SilentlyContinue
    $capture = Get-ItemProperty 'HKCU:\Software\Microsoft\Windows\CurrentVersion\GameDVR' -ErrorAction SilentlyContinue
    $privacy = Get-ItemProperty 'HKCU:\Software\Microsoft\Windows\CurrentVersion\CapabilityAccessManager\ConsentStore\microphone' -ErrorAction SilentlyContinue
    $videos = [Environment]::GetFolderPath('MyVideos')
    $captureFolder = Join-Path $videos 'Captures'
    $checks = [ordered]@{
        xbox_game_bar_installed = [bool]$package
        game_dvr_enabled = ($gameDvr.GameDVR_Enabled -eq 1)
        app_capture_enabled = ($capture.AppCaptureEnabled -eq 1)
        system_audio_enabled = ($capture.AudioCaptureEnabled -eq 1)
        microphone_capture_enabled = ($capture.MicrophoneCaptureEnabled -eq 1)
        microphone_privacy_allowed = ($null -eq $privacy -or $privacy.Value -ne 'Deny')
        capture_folder = $captureFolder
    }
    $ready = $checks.xbox_game_bar_installed -and $checks.game_dvr_enabled -and $checks.app_capture_enabled -and $checks.system_audio_enabled -and $checks.microphone_capture_enabled -and $checks.microphone_privacy_allowed
    return [PSCustomObject]@{ ready = $ready; provider = 'xbox-game-bar'; checks = $checks }
}

function Send-GameBarChord([char]$Key) {
    if (-not ('GameBarKeys' -as [type])) {
        Add-Type @'
using System;
using System.Runtime.InteropServices;
public static class GameBarKeys {
  [DllImport("user32.dll", SetLastError = true)]
  private static extern void keybd_event(byte bVk, byte bScan, uint dwFlags, UIntPtr dwExtraInfo);
  private const uint KEYUP = 0x0002;
  public static void Chord(byte key) {
    keybd_event(0x5B, 0, 0, UIntPtr.Zero);
    keybd_event(0x12, 0, 0, UIntPtr.Zero);
    keybd_event(key, 0, 0, UIntPtr.Zero);
    keybd_event(key, 0, KEYUP, UIntPtr.Zero);
    keybd_event(0x12, 0, KEYUP, UIntPtr.Zero);
    keybd_event(0x5B, 0, KEYUP, UIntPtr.Zero);
  }
}
'@
    }
    [GameBarKeys]::Chord([byte][char]$Key)
}

function Test-Mp4Track([string]$Path, [string]$Marker) {
    $needle = [Text.Encoding]::ASCII.GetBytes($Marker)
    $stream = [IO.File]::OpenRead($Path)
    try {
        $buffer = New-Object byte[] 1048576
        $tail = New-Object byte[] ($needle.Length - 1)
        $tailLength = 0
        while (($read = $stream.Read($buffer, 0, $buffer.Length)) -gt 0) {
            $combined = New-Object byte[] ($tailLength + $read)
            if ($tailLength -gt 0) { [Array]::Copy($tail, 0, $combined, 0, $tailLength) }
            [Array]::Copy($buffer, 0, $combined, $tailLength, $read)
            for ($i = 0; $i -le $combined.Length - $needle.Length; $i++) {
                $match = $true
                for ($j = 0; $j -lt $needle.Length; $j++) { if ($combined[$i + $j] -ne $needle[$j]) { $match = $false; break } }
                if ($match) { return $true }
            }
            $tailLength = [Math]::Min($tail.Length, $combined.Length)
            [Array]::Copy($combined, $combined.Length - $tailLength, $tail, 0, $tailLength)
        }
        return $false
    } finally { $stream.Dispose() }
}

function Update-EvidenceManifest([string]$Engagement, $Item) {
    $manifestPath = Join-Path $Engagement '10_evidence\evidence-manifest.json'
    $manifest = if (Test-Path -LiteralPath $manifestPath) { Get-Content -Raw -LiteralPath $manifestPath | ConvertFrom-Json } else { [PSCustomObject]@{ engagement_id = ''; items = @() } }
    $items = @($manifest.items | Where-Object { $_.evidence_id -ne $Item.evidence_id }) + @($Item)
    $manifest.items = $items
    $manifest | ConvertTo-Json -Depth 10 | Set-Content -LiteralPath $manifestPath -Encoding UTF8
}

$engagement = Get-SafeEngagementPath $EngagementPath
$statePath = Get-RecordingStatePath $engagement
$preflight = Get-GameBarCheck

if ($Action -eq 'check') { $preflight | ConvertTo-Json -Depth 6; exit $(if ($preflight.ready) { 0 } else { 2 }) }

if ($Action -eq 'status') {
    if (Test-Path -LiteralPath $statePath) { Get-Content -Raw -LiteralPath $statePath } else { @{ status = 'idle'; provider = 'xbox-game-bar' } | ConvertTo-Json }
    exit 0
}

if ($Action -eq 'start') {
    if (-not $Confirmed) { throw 'Explicit screen and microphone consent is required. Pass -Confirmed only after the participant agrees in the conversation.' }
    if (-not $preflight.ready) { $preflight | ConvertTo-Json -Depth 6; throw 'Recording preflight failed.' }
    if (Test-Path -LiteralPath $statePath) {
        $oldState = Get-Content -Raw -LiteralPath $statePath | ConvertFrom-Json
        if ($oldState.status -eq 'recording_requested') { throw 'A recording session is already active for this engagement.' }
    }
    $start = (Get-Date).ToUniversalTime()
    $state = [ordered]@{
        status = 'recording_requested'
        provider = 'xbox-game-bar'
        started_at = $start.ToString('o')
        label = $Label
        microphone_required = $true
        capture_folder = $preflight.checks.capture_folder
    }
    $state | ConvertTo-Json -Depth 5 | Set-Content -LiteralPath $statePath -Encoding UTF8
    Send-GameBarChord 'R'
    Start-Sleep -Milliseconds 1200
    $state | ConvertTo-Json -Depth 5
    exit 0
}

if (-not (Test-Path -LiteralPath $statePath)) { throw 'No recording session state exists for this engagement.' }
$session = Get-Content -Raw -LiteralPath $statePath | ConvertFrom-Json
if ($session.status -ne 'recording_requested') { throw "Recording session is not active; current status: $($session.status)" }

Send-GameBarChord 'R'
$startedAt = [DateTime]::Parse($session.started_at).ToUniversalTime()
$deadline = (Get-Date).AddSeconds($DiscoveryTimeoutSeconds)
$candidate = $null
do {
    Start-Sleep -Milliseconds 750
    if (Test-Path -LiteralPath $session.capture_folder) {
        $candidate = Get-ChildItem -LiteralPath $session.capture_folder -Filter '*.mp4' -File -ErrorAction SilentlyContinue |
            Where-Object { $_.LastWriteTimeUtc -ge $startedAt.AddSeconds(-3) } |
            Sort-Object LastWriteTimeUtc -Descending |
            Select-Object -First 1
    }
} until ($candidate -or (Get-Date) -ge $deadline)

if (-not $candidate) {
    $session.status = 'failed_no_output'
    $session | ConvertTo-Json -Depth 6 | Set-Content -LiteralPath $statePath -Encoding UTF8
    throw 'Game Bar did not produce a new MP4. The target app may not support capture.'
}

$videoDir = Join-Path $engagement '10_evidence\video'
if (-not (Test-Path -LiteralPath $videoDir)) { New-Item -ItemType Directory -Path $videoDir | Out-Null }
$safeLabel = ($session.label -replace '[^a-zA-Z0-9\p{L}-]+', '-').Trim('-')
if (-not $safeLabel) { $safeLabel = 'screen-walkthrough' }
$targetName = '{0}_{1}.mp4' -f (Get-Date -Format 'yyyyMMdd-HHmmss'), $safeLabel
$targetPath = Join-Path $videoDir $targetName
Copy-Item -LiteralPath $candidate.FullName -Destination $targetPath

$hash = (Get-FileHash -LiteralPath $targetPath -Algorithm SHA256).Hash.ToLowerInvariant()
$hasAudio = Test-Mp4Track $targetPath 'soun'
$hasVideo = Test-Mp4Track $targetPath 'vide'
$evidenceId = 'EVD-VID-{0}' -f (Get-Date -Format 'yyyyMMddHHmmss')
$item = [PSCustomObject]@{
    evidence_id = $evidenceId
    type = 'screen_recording'
    original_capture = $candidate.FullName
    stored_path = $targetPath
    captured_at = (Get-Date).ToString('o')
    sha256 = $hash
    microphone_required = $true
    audio_track_detected = $hasAudio
    video_track_detected = $hasVideo
    authorization = 'confirmed_in_conversation'
    status = $(if ($hasAudio -and $hasVideo) { 'captured' } else { 'incomplete' })
    processing_status = $(if ($PythonPath -and $hasAudio -and $hasVideo) { 'preparing_interview_transcript' } else { 'pending_transcription' })
    next_action = 'return_to_interview_for_gap_review'
}
Update-EvidenceManifest $engagement $item

if ($PythonPath -and $hasAudio -and $hasVideo) {
    if (-not (Test-Path -LiteralPath $PythonPath -PathType Leaf)) { throw "Python runtime not found: $PythonPath" }
    $transcriptWorker = [System.IO.Path]::GetFullPath((Join-Path $PSScriptRoot 'prepare_walkthrough_transcript.py'))
    $arguments = @($transcriptWorker, '--engagement', $engagement, '--source', $targetPath, '--evidence-id', $evidenceId, '--model', $TranscriptionModel, '--language', $Language, '--beam-size', $TranscriptionBeamSize)
    if ($InitialPrompt) { $arguments += @('--initial-prompt', $InitialPrompt) }
    if ($AllowModelDownload) { $arguments += '--allow-model-download' }
    & $PythonPath @arguments
    if ($LASTEXITCODE -eq 0) {
        $transcriptPackage = Join-Path $engagement "10_evidence\transcripts\$evidenceId"
        $item.processing_status = 'transcript_ready_for_interview_review'
        $item | Add-Member -NotePropertyName transcript_package -NotePropertyValue $transcriptPackage -Force
        $item | Add-Member -NotePropertyName transcript_path -NotePropertyValue (Join-Path $transcriptPackage 'transcript.json') -Force
    } else {
        $item.processing_status = 'transcription_failed'
    }
    Update-EvidenceManifest $engagement $item
}

$session.status = $item.status
$session | Add-Member -NotePropertyName stopped_at -NotePropertyValue ((Get-Date).ToUniversalTime().ToString('o')) -Force
$session | Add-Member -NotePropertyName evidence_id -NotePropertyValue $evidenceId -Force
$session | Add-Member -NotePropertyName stored_path -NotePropertyValue $targetPath -Force
$session | Add-Member -NotePropertyName audio_track_detected -NotePropertyValue $hasAudio -Force
$session | Add-Member -NotePropertyName video_track_detected -NotePropertyValue $hasVideo -Force
$session | ConvertTo-Json -Depth 6 | Set-Content -LiteralPath $statePath -Encoding UTF8
$item | ConvertTo-Json -Depth 6
if (-not ($hasAudio -and $hasVideo)) { exit 3 }
