param(
    [ValidateSet('Book','Tutorial','Static','Orbit','Side')][string]$Mode = 'Book',
    [switch]$Headless
)
$ErrorActionPreference = 'Stop'
$packageRoot = $PSScriptRoot
try {
    $settingsPath = Join-Path $packageRoot 'local-settings.json'
    if (-not (Test-Path -LiteralPath $settingsPath)) {
        throw 'First copy local-settings.example.json to local-settings.json and set your Blender, source, and output paths. See the PDF manual.'
    }
    $settings = Get-Content -LiteralPath $settingsPath -Raw | ConvertFrom-Json
    if (-not (Test-Path -LiteralPath $settings.blender)) { throw 'Configured Blender executable was not found.' }
    $runName = (Get-Date -Format 'yyyyMMdd-HHmmss-fff') + '-' + $Mode.ToLower()
    $runDir = Join-Path $settings.output_root $runName
    New-Item -ItemType Directory -Path $runDir -ErrorAction Stop | Out-Null
    $blendArgs = @('--background','--factory-startup','--threads','2','--python-exit-code','1')
    if ($Mode -in @('Book','Tutorial')) {
        $job = if ($Mode -eq 'Book') { $settings.book } else { $settings.tutorial }
        if (-not (Test-Path -LiteralPath $job.video)) { throw 'Configured source video was not found.' }
        $scriptName = if ($Mode -eq 'Book') { 'book_reading_blender.py' } else { 'tutorial_blender.py' }
        $blendArgs += @('--python',(Join-Path $packageRoot "basic\$scriptName"),'--','--video',$job.video,'--output',(Join-Path $runDir 'rough_edit.blend'))
        if ($job.plan_json -and $job.review_csv) { $blendArgs += @('--plan-json',$job.plan_json,'--review-csv',$job.review_csv) }
        elseif ($job.plan_json -or $job.review_csv) { throw 'Provide both plan_json and review_csv, or neither.' }
        if ($job.captions) { $blendArgs += @('--captions',$job.captions) }
        if ($Mode -eq 'Tutorial' -and $job.resolve_run) { $blendArgs += @('--resolve-run',$job.resolve_run) }
        if ($Mode -eq 'Book') {
            if (-not (Test-Path -LiteralPath $settings.book_storyboard_glb)) { throw 'Configured open-book GLB was not found.' }
            $blendArgs += @('--storyboard-glb',$settings.book_storyboard_glb)
        }
    } else {
        $preset = Join-Path $packageRoot ('configs\' + $Mode.ToLower() + '.json')
        $blendArgs += @('--python',(Join-Path $packageRoot 'scripts\stage_overlay.py'),'--','--config',$preset,'--output',$runDir,'--preview')
    }
    # Fresh directory and native argument array; no command-string interpolation.
    $logPath = Join-Path $settings.output_root ($runName + '.log')
    & $settings.blender @blendArgs *> $logPath
    if ($LASTEXITCODE -ne 0) { throw "Blender failed. Read: $logPath" }
    if ($Mode -in @('Book','Tutorial')) {
        # Keep the historical draft and make a corrected, readable review copy.
        $result = Join-Path $runDir 'review_edit.blend'
        $styleArgs = @('--background','--factory-startup','--threads','2','--python-exit-code','1',
            '--python',(Join-Path $packageRoot 'scripts\restyle_captions.py'),'--',
            '--project',(Join-Path $runDir 'rough_edit.blend'),'--output',$result,'--preview')
        & $settings.blender @styleArgs *>> $logPath
        if ($LASTEXITCODE -ne 0) { throw "Caption review-copy failed. Read: $logPath" }
    }
    else { $result = Join-Path $runDir 'overlay.blend' }
    if (-not (Test-Path -LiteralPath $result)) { throw 'Blender exited without the expected project.' }
    Write-Output "Saved: $result"
    if (-not $Headless) {
        Add-Type -AssemblyName System.Windows.Forms
        [System.Windows.Forms.MessageBox]::Show("Ready to review:`n$result`n`nA final movie has not been rendered.",'Storyboard Education') | Out-Null
        Start-Process explorer.exe -ArgumentList @('/select,',('"'+$result+'"'))
    }
} catch {
    Write-Error $_ -ErrorAction Continue
    if (-not $Headless) {
        Add-Type -AssemblyName System.Windows.Forms
        [System.Windows.Forms.MessageBox]::Show($_.Exception.Message,'Storyboard build stopped') | Out-Null
    }
    exit 1
}
