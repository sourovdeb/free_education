param([ValidateSet('menu','audit')][string]$Action='menu')
$ErrorActionPreference='Stop'
$Root='E:\Studio'
if (-not (Test-Path 'E:\')) { throw 'E drive is unavailable.' }
if ((Split-Path -Qualifier $PSScriptRoot) -ne 'E:') { throw 'Extract this pack onto E:.' }
$Folders=@('tools','envs','cache\tmp','cache\uv','cache\pip','cache\pycache','cache\hf','cache\matplotlib','reports','secrets','state','inbox','projects')
foreach($Folder in $Folders){New-Item -ItemType Directory -Path (Join-Path $Root $Folder) -Force | Out-Null}
$env:TEMP="$Root\cache\tmp"; $env:TMP=$env:TEMP; $env:TMPDIR=$env:TEMP
$env:UV_CACHE_DIR="$Root\cache\uv"; $env:PIP_CACHE_DIR="$Root\cache\pip"
$env:UV_PYTHON_INSTALL_DIR="$Root\tools\python"; $env:UV_PYTHON_BIN_DIR="$Root\tools\python-bin"
$env:UV_PYTHON_INSTALL_BIN='0'; $env:UV_PYTHON_NO_REGISTRY='1'
$env:UV_TOOL_DIR="$Root\tools\uv-tools"; $env:UV_TOOL_BIN_DIR="$Root\tools\bin"
$env:UV_UNMANAGED_INSTALL="$Root\tools\uv"; $env:UV_NO_MODIFY_PATH='1'
$env:PYTHONPYCACHEPREFIX="$Root\cache\pycache"; $env:HF_HOME="$Root\cache\hf"
$env:MPLCONFIGDIR="$Root\cache\matplotlib"; $env:XDG_CACHE_HOME="$Root\cache\xdg"
$env:OMP_NUM_THREADS='2'; $env:OPENBLAS_NUM_THREADS='2'; $env:MKL_NUM_THREADS='2'
$Python="$Root\envs\visual-director\Scripts\python.exe"
$Runner=Join-Path $PSScriptRoot 'director.py'
$State="$Root\state\visual-director.json"
$KeyFile="$Root\secrets\visual-director.key.dpapi"
$KnownSkills=@('.agents\skills\typesafe-ai','.vibe\skills\typesafe-ai','.claude\skills\typesafe-ai','.grok\skills\typesafe-ai','.pi\agent\skills\typesafe-ai','.codeium\windsurf\skills\typesafe-ai')

function Write-Json($Path,$Value){$Value | ConvertTo-Json -Depth 12 | Set-Content -Encoding UTF8 -Path $Path}
function Invoke-Runner([string[]]$Arguments){
 if(-not (Test-Path $Python)){throw 'Run setup before this step.'}
 & $Python $Runner @Arguments
 if($LASTEXITCODE -ne 0){throw 'The workflow stopped. Read above.'}
}
function Get-Project{
 if(Test-Path $State){$s=Get-Content $State -Raw | ConvertFrom-Json; if(Test-Path $s.project){return $s.project}}
 throw 'Start a transcript project first.'
}
function Find-Tool([string]$Name,[string[]]$Candidates){
 $paths=@()
 $command=Get-Command $Name -ErrorAction SilentlyContinue | Select-Object -First 1
 if($command -and $command.Source){$paths+= $command.Source}
 foreach($candidate in $Candidates){if(Test-Path $candidate){$paths+=(Resolve-Path $candidate).Path}}
 return ,@($paths | Select-Object -Unique)
}
function Audit{
 $tools=[ordered]@{}
 $tools.Python=Find-Tool 'python.exe' @($Python)
 $tools.Uv=Find-Tool 'uv.exe' @("$Root\tools\uv\uv.exe")
 $tools.OBS=Find-Tool 'obs64.exe' @("$env:ProgramFiles\obs-studio\bin\64bit\obs64.exe",'E:\obs-studio\bin\64bit\obs64.exe')
 $tools.Resolve=Find-Tool 'Resolve.exe' @("$env:ProgramFiles\Blackmagic Design\DaVinci Resolve\Resolve.exe",'E:\Programs\DaVinci Resolve\Resolve.exe')
 $tools.FFmpeg=Find-Tool 'ffmpeg.exe' @('E:\ffmpeg\bin\ffmpeg.exe',"$Root\tools\ffmpeg\bin\ffmpeg.exe")
 $tools.Blender=Find-Tool 'blender.exe' @()
 $tools.Hermes=Find-Tool 'hermes.exe' @()
 $tools.Vibe=Find-Tool 'vibe.exe' @()
 $tools.Codex=Find-Tool 'codex.exe' @()
 $skills=@()
 foreach($p in $KnownSkills){$s=Join-Path $HOME $p;if(Test-Path "$s\SKILL.md"){$skills+=@{path=$s;sha256=(Get-FileHash "$s\SKILL.md" -Algorithm SHA256).Hash}}}
 $scope=@("$Root\tools",'E:\tools','E:\Programs')
 $discovered=@();$queue=New-Object System.Collections.Queue
 foreach($p in $scope){if(Test-Path $p){$queue.Enqueue(@{path=$p;depth=0})}}
 $count=0
 while($queue.Count -gt 0 -and $count -lt 1500){
  $item=$queue.Dequeue();$count++
  $children=@(Get-ChildItem -LiteralPath $item.path -ErrorAction SilentlyContinue)
  foreach($child in $children){
   if($child.Attributes -band [IO.FileAttributes]::ReparsePoint){continue}
   if($child.PSIsContainer){if($item.depth -lt 4 -and $child.Name -notin @('cache','node_modules','.git','site-packages')){$queue.Enqueue(@{path=$child.FullName;depth=$item.depth+1})}}
   elseif($child.Name -in @('python.exe','manim.exe','obs64.exe','Resolve.exe','ffmpeg.exe','blender.exe','SKILL.md')){$discovered+= $child.FullName}
  }
 }
 $versions=[ordered]@{}
 foreach($pair in @(@('OBS',$tools.OBS),@('Resolve',$tools.Resolve),@('Blender',$tools.Blender))){
  if($pair[1].Count -gt 0){$versions[$pair[0]]=(Get-Item $pair[1][0]).VersionInfo.FileVersion}
 }
 if(Test-Path $Python){
  $versions.Python=(& $Python --version 2>&1 | Out-String).Trim()
  $packages=& $Python -c "import importlib.metadata,json; print(json.dumps({d.metadata['Name']:d.version for d in importlib.metadata.distributions()}))" 2>$null
  if($LASTEXITCODE -eq 0){$versions.Packages=$packages | ConvertFrom-Json}
 }
 $os=Get-CimInstance Win32_OperatingSystem
 $report=[ordered]@{date=(Get-Date).ToString('o');tools=$tools;versions=$versions;typesafe_skill=$skills;
  bounded_search=$scope;additional_paths=$discovered;search_truncated=($queue.Count -gt 0);
  api_key_present=([bool]$env:TYPESAFE_API_KEY -or (Test-Path $KeyFile));
  ram_total_gb=[math]::Round($os.TotalVisibleMemorySize/1MB,2);ram_available_gb=[math]::Round($os.FreePhysicalMemory/1MB,2);
  e_free_gb=[math]::Round((Get-PSDrive E).Free/1GB,2);
  gpu=@(Get-CimInstance Win32_VideoController | Select-Object Name,DriverVersion);
  resolve_api_readme="$env:ProgramData\Blackmagic Design\DaVinci Resolve\Support\Developer\Scripting\README.txt";
  meaning='Unlisted tools were not found within the search scope. API connectivity was not tested.'}
 $path="$Root\reports\visual-director-preflight-$(Get-Date -Format yyyyMMdd-HHmmss).json"
 Write-Json $path $report
 Write-Host "Report: $path"
 foreach($k in $tools.Keys){Write-Host "$k : $($tools[$k] -join '; ')"}
 Write-Host 'Blank paths need further investigation.'
 return $path
}
function Setup{
 if((Read-Host 'Install dependencies? Type SETUP') -cne 'SETUP'){return}
 if((Get-PSDrive E).Free -lt 10GB){throw 'E drive needs space first.'}
 $uv="$Root\tools\uv\uv.exe"
 if(-not(Test-Path $uv)){
  $installer="$Root\tools\uv-install.ps1"
  Invoke-WebRequest 'https://astral.sh/uv/install.ps1' -OutFile $installer -UseBasicParsing
  Get-FileHash $installer -Algorithm SHA256 | Format-List
  Write-Host 'Source: https://astral.sh/uv/install.ps1'
  if((Read-Host 'Run this installer? Type INSTALL') -cne 'INSTALL'){return}
  & powershell.exe -NoProfile -ExecutionPolicy Bypass -File $installer
  if($LASTEXITCODE -ne 0 -or -not(Test-Path $uv)){throw 'uv installation did not complete.'}
 }
 & $uv python install 3.12
 if($LASTEXITCODE -ne 0){throw 'Python installation did not complete.'}
 if(-not(Test-Path $Python)){
  & $uv venv --managed-python --python 3.12 "$Root\envs\visual-director"
  if($LASTEXITCODE -ne 0){throw 'Environment creation failed.'}
 }
 & $uv pip install --python $Python -r (Join-Path $PSScriptRoot 'requirements.txt')
 if($LASTEXITCODE -ne 0){throw 'Dependency installation failed.'}
 & $uv pip freeze --python $Python | Set-Content -Encoding UTF8 "$Root\reports\visual-director-resolved-requirements.txt"
 if($LASTEXITCODE -ne 0){throw 'Dependency recording failed.'}
 $vendor=Join-Path $PSScriptRoot 'vendor\typesafe-ai'
 if(-not(Test-Path "$vendor\SKILL.md")){
  $found=$null
  foreach($p in $KnownSkills){$candidate=Join-Path $HOME $p;if(Test-Path "$candidate\SKILL.md"){$found=$candidate;break}}
  New-Item -ItemType Directory (Split-Path $vendor) -Force | Out-Null
  if($found){Copy-Item -LiteralPath $found -Destination $vendor -Recurse}
  else{
   $zip="$Root\cache\tmp\typesafe-skills.zip"
   $extract="$Root\cache\tmp\typesafe-skills-$(Get-Date -Format yyyyMMddHHmmss)"
   Invoke-WebRequest 'https://github.com/typesafe-ai/skills/archive/refs/heads/main.zip' -OutFile $zip -UseBasicParsing
   Expand-Archive $zip $extract
   Copy-Item "$extract\skills-main\skills\typesafe-ai" $vendor -Recurse
  }
 }
 if(-not(Test-Path "$vendor\SKILL.md")){throw 'TypeSafe skill installation needs review.'}
 Get-FileHash "$vendor\SKILL.md" -Algorithm SHA256 | Format-List
 if(-not $env:TYPESAFE_API_KEY -and -not(Test-Path $KeyFile)){
  Write-Host 'The key is never printed.'
  $secret=Read-Host 'Paste TypeSafe key, or press Enter' -AsSecureString
  if($secret.Length -gt 0){$secret | ConvertFrom-SecureString | Set-Content -Path $KeyFile -Encoding ASCII}
 }
 & $Python -m unittest discover -s (Join-Path $PSScriptRoot 'tests') -v
 if($LASTEXITCODE -ne 0){throw 'Tests failed. Stop here.'}
 Write-Host 'Setup finished. Run the audit.'
}
function Load-Key{
 if(-not $env:TYPESAFE_API_KEY -and (Test-Path $KeyFile)){
  $secure=Get-Content $KeyFile -Raw | ConvertTo-SecureString
  $ptr=[Runtime.InteropServices.Marshal]::SecureStringToBSTR($secure)
  try{$env:TYPESAFE_API_KEY=[Runtime.InteropServices.Marshal]::PtrToStringBSTR($ptr)}
  finally{[Runtime.InteropServices.Marshal]::ZeroFreeBSTR($ptr)}
 }
}
function New-Project{
 Add-Type -AssemblyName System.Windows.Forms
 $dialog=New-Object System.Windows.Forms.OpenFileDialog
 $dialog.InitialDirectory="$Root\inbox";$dialog.Filter='Transcript|*.srt;*.vtt;*.json'
 if($dialog.ShowDialog() -ne 'OK'){return}
 if((Split-Path -Qualifier $dialog.FileName) -ne 'E:'){throw 'Place the transcript on E:.'}
 Write-Host 'Use transcript timing after editing.'
 if((Read-Host 'Timeline edits finished? Type LOCKED') -cne 'LOCKED'){return}
 $name=Read-Host 'Project name, using lowercase letters'
 $timeline=Read-Host 'Exact Resolve timeline name'
 $fps=Read-Host 'Timeline fps, such as 25'
 $offset=Read-Host 'Transcript time offset, usually 0'
 if(-not $offset){$offset='0'}
 Invoke-Runner @('ingest','--source',$dialog.FileName,'--root',$Root,'--name',$name,'--fps',$fps,'--timeline',$timeline,'--offset-seconds',$offset)
 $p="$Root\projects\$name";Write-Json $State @{project=$p}
 Start-Process notepad.exe -ArgumentList "`"$p\HANDOFF.md`""
 Write-Host 'Give HANDOFF.md to your agent.'
}
function Evaluate-Project{
 $p=Get-Project
 Write-Host 'TypeSafe receives proposal evidence excerpts.'
 Write-Host 'Recordings and keys remain unpublished.'
 Write-Host 'Requests may consume account credit.'
 if((Read-Host 'Send excerpts? Type SEND') -ceq 'SEND'){
  Load-Key
  Invoke-Runner @('evaluate','--project',$p,'--allow-typesafe')
 }else{Invoke-Runner @('evaluate','--project',$p)}
 Start-Process "$p\01_work\review.html"
}
function Review-Render{
 $p=Get-Project
 Start-Process "$p\01_work\review.html"
 Write-Host 'Check claims, labels, and timing.'
 if((Read-Host 'Finished reviewing? Type APPROVE') -cne 'APPROVE'){return}
 Invoke-Runner @('approve','--project',$p,'--reviewed')
 Write-Host 'Save and close Resolve/OBS first.'
 if((Read-Host 'Render assets? Type RENDER') -ceq 'RENDER'){
  Invoke-Runner @('render','--project',$p)
  Start-Process explorer.exe -ArgumentList "`"$p\02_resolve\imports`""
 }
}
function Import-Resolve{
 $p=Get-Project
 Write-Host 'Open the intended Resolve project.'
 Write-Host 'This imports files, not edits.'
 if((Read-Host 'Import assets? Type IMPORT') -cne 'IMPORT'){return}
 & $Python (Join-Path $PSScriptRoot 'resolve_import.py') --manifest "$p\02_resolve\manifest.json" --apply
 if($LASTEXITCODE -ne 0){Write-Host 'Use the imports folder instead.';Start-Process explorer.exe -ArgumentList "`"$p\02_resolve`""}
}
Set-Location $PSScriptRoot
if($Action -eq 'audit'){Audit | Out-Null;exit}
$OriginalKey=$env:TYPESAFE_API_KEY
try{
 while($true){
  Write-Host "`n1 Check this PC`n2 Set up E-drive tools`n3 Start from transcript`n4 Evaluate the agent proposal`n5 Review and render`n6 Import into Resolve`n0 Exit"
  try{
   switch(Read-Host 'Choose the next step'){
    '1'{Audit | Out-Null}
    '2'{Setup}
    '3'{New-Project}
    '4'{Evaluate-Project}
    '5'{Review-Render}
    '6'{Import-Resolve}
    '0'{return}
    default{Write-Host 'Choose a displayed number.'}
   }
  }catch{Write-Host "STOP: $($_.Exception.Message)"}
 }
}finally{$env:TYPESAFE_API_KEY=$OriginalKey}
