# Remove unnecessay files from SourceMod to make it GMod Addon
param(
  [string] $directory = (Get-Location)
)

############
# Function #
############
function Write-Message {
  param(
    [string]$Object,
    [string]$Color = 'Green',
    [string]$Header = 'INFO',
    [switch]$NoNewline = $false
  )
  Write-Host -NoNewline -ForegroundColor $Color "$Header "
  if ($NoNewline) {
    Write-Host $Object -NoNewline
  }
  else {
    Write-Host $Object
  }
}

function Rename-Sanitize {
  param([string]$filePath)
  $fileName = [System.IO.Path]::GetFileNameWithoutExtension($filePath)
  $extension = [System.IO.Path]::GetExtension($filePath)
  $directoryPath = [System.IO.Path]::GetDirectoryName($filePath)
  $newFileName = $fileName -replace '-', '_' -replace '_+', '_'
  $newFilePath = Join-Path -Path $directoryPath -ChildPath "$newFileName$extension"
  Rename-Item -Path $filePath -NewName $newFilePath
}
########
# Body #
########

# Check 'maps' directory
$mapsDir = Join-Path -Path $directory -ChildPath 'maps'
if (-Not (Test-Path -Path $mapsDir)) {
  Write-Message 'maps directory not present. Aborting...'
  exit 1
}
$graphsDir = Join-Path -Path $mapsDir -ChildPath 'graphs'

# Remove/Sanitize files under 'maps' and 'graphs'
$dtp = @( @{ Dir = $mapsDir; Ext = '.bsp' }, @{ Dir = $graphsDir; Ext = '.ain' } )
foreach ($d in $dtp) {
  if (Test-Path -Path $d.Dir) {
    Get-ChildItem -Path $d.Dir -File | ForEach-Object {
      if ($_.Extension -eq $d.Ext) {
        Rename-Sanitize $_.FullName
      }
      else {
        Write-Message "Removing $($_.FullName)" -Color Yellow -Header REMOVE
        Remove-Item $_.FullName
      }
    }
  }
}

# Lowercase files via 'lowercase.exe'
$proc = Start-Process -NoNewWindow -Wait -FilePath 'lowercase.exe' -ArgumentList "-y `"$directory`""

# Remove obvious directories
$dirsToRemove = @(
  'bin',
  'cfg',
  'downloadlists',
  'mapsrc',
  'materialsrc',
  'media',
  'save',
  'screenshots',
  'steam-gridview-icons',
  'steam-gridview-images'
)
foreach ($dir in $dirsToRemove) {
  $removePath = Join-Path -Path $directory -ChildPath $dir
  if (Test-Path -Path $removePath) {
    Write-Message "Removing $removePath" -Color Yellow -Header REMOVE
    Remove-Item -Recurse -Force -Path $removePath
  }
}

# Remove nested directories
$soundUiPath = [IO.Path]::Combine($directory, 'sound', 'ui')
if (Test-Path -Path $soundUiPath) {
  Write-Message "Removing $soundUiPath" -Color Yellow -Header REMOVE
  Remove-Item -Recurse -Force -Path $soundUiPath
}

# Remove .bak files
Get-ChildItem -Path $directory -Recurse -Filter '*.bak' | ForEach-Object {
  Write-Message "Removing $($_.FullName)" -Color Yellow -Header REMOVE
  Remove-Item -Force -Path $_.FullName | Out-Null
}
# Remove .cache files
Get-ChildItem -Path $directory -Recurse -Filter '*.cache' | ForEach-Object {
  Write-Message "Removing $($_.FullName)" -Color Yellow -Header REMOVE
  Remove-Item -Force -Path $_.FullName | Out-Null
}
# Remove .db files
Get-ChildItem -Path $directory -Recurse -Filter '*.db' | ForEach-Object {
  Write-Message "Removing $($_.FullName)" -Color Yellow -Header REMOVE
  Remove-Item -Force -Path $_.FullName | Out-Null
}
# Remove .image files
Get-ChildItem -Path $directory -Recurse -Filter '*.image' | ForEach-Object {
  Write-Message "Removing $($_.FullName)" -Color Yellow -Header REMOVE
  Remove-Item -Force -Path $_.FullName | Out-Null
}
# Remove .raw files
Get-ChildItem -Path $directory -Recurse -Filter '*.raw' | ForEach-Object {
  Write-Message "Removing $($_.FullName)" -Color Yellow -Header REMOVE
  Remove-Item -Force -Path $_.FullName | Out-Null
}
# Remove .tga files
Get-ChildItem -Path $directory -Recurse -Filter '*.tga' | ForEach-Object {
  Write-Message "Removing $($_.FullName)" -Color Yellow -Header REMOVE
  Remove-Item -Force -Path $_.FullName | Out-Null
}
# Remove .sw.vtx and .xbox.vtx files
Get-ChildItem -Path $directory -Recurse -Filter '*.sw.vtx' | ForEach-Object {
  Write-Message "Removing $($_.FullName)" -Color Yellow -Header REMOVE
  Remove-Item -Force -Path $_.FullName | Out-Null
}
Get-ChildItem -Path $directory -Recurse -Filter '*.xbox.vtx' | ForEach-Object {
  Write-Message "Removing $($_.FullName)" -Color Yellow -Header REMOVE
  Remove-Item -Force -Path $_.FullName | Out-Null
}

# Remove wrong placed files
$materialsDir = Join-Path -Path $directory -ChildPath "materials"
if (Test-Path -Path $materialsDir) {
  Get-ChildItem -Path $materialsDir -Recurse -Include *.vtx, *.vvd, *.mdl, *.phy, *.jpg, *.png | ForEach-Object {
    Write-Message "Removing $($_.FullName)" -Color Yellow -Header REMOVE
    Remove-Item -Force -Path $_.FullName | Out-Null
  }
}
$modelsDir = Join-Path -Path $directory -ChildPath "models"
if (Test-Path -Path $modelsDir) {
  Get-ChildItem -Path $modelsDir -Recurse -Include *.vtf, *.vmt, *.jpg, *.png | ForEach-Object {
    Write-Message "Removing $($_.FullName)" -Color Yellow -Header REMOVE
    Remove-Item -Force -Path $_.FullName | Out-Null
  }
}

# [MapBase] Replace shader of materials
if (Test-Path -Path $materialsDir) {
  Get-ChildItem -Path $materialsDir -Recurse -Include *.vmt | ForEach-Object {
    $fPath = $_.FullName
    $content = Get-Content -Path $fPath -Raw
    $content = $content -replace '"SDK_LightmappedGeneric"', '"LightmappedGeneric"'
    $content = $content -replace '"SDK_Sprite"', '"Sprite"'
    $content = $content -replace '"SDK_VertexLitGeneric"', '"VertexLitGeneric"'
    if ($content) {
      Set-Content -Path $fPath -Value $content -Force
    }
  }
}

# Create 'data_static' directory
$dataStaticDir = Join-Path -Path $directory -ChildPath 'data_static'
if (-Not (Test-Path -Path $dataStaticDir)) {
  New-Item -ItemType Directory -Path $dataStaticDir | Out-Null
}

# Move readme files to 'data_static'
$readmeItems = Get-ChildItem -Path $directory -Filter 'readme*' -ErrorAction SilentlyContinue
foreach ($item in $readmeItems) {
  if ($item.PSIsContainer) {
    Get-ChildItem -Path $item.FullName | Move-Item -Destination $dataStaticDir -Force
    if (-Not (Get-ChildItem -Path $item.FullName -Recurse)) {
      Write-Message "Removing $($item.FullName)" -Color Yellow -Header REMOVE
      Remove-Item -Path $item.FullName -Force
    }
  }
  elseif ($item.PSIsContainer -eq $false) {
    Move-Item -Path $item.FullName -Destination $dataStaticDir -Force
  }
}

# Remove files directly under $directory
Get-ChildItem -Path $directory -File | ForEach-Object {
  Write-Message "Removing $($_.FullName)" -Color Yellow -Header REMOVE
  Remove-Item $_.FullName -Force
}

# Define $lowercase from the name of $directory
$dir = Split-Path -Leaf -Path $directory
$lowercase = $dir.ToLower() -replace '[^a-z0-9]', '_' -replace '_+', '_' -replace '^_+|_+$', ''

# Define $maps from .bsp files under 'maps' directory
$maps = (Get-ChildItem -Path (Join-Path -Path $directory -ChildPath 'maps') -Filter '*.bsp' | ForEach-Object { $_.Name -replace '\.bsp$', '|' }) -join ''
$maps = $maps.TrimEnd('|')

# Create gamemodes.txt file
$gamemodesDir = [IO.Path]::Combine($directory, "gamemodes", $lowercase)
if (-Not (Test-Path -Path $gamemodesDir)) {
  New-Item -ItemType Directory -Path $gamemodesDir -Force | Out-Null
}
$gamemodesFile = Join-Path -Path $gamemodesDir -ChildPath "$lowercase.txt"
$gamemodesContent = @"
"$lowercase"
{
  "title" "$dir"
  "maps" "$maps"
  "menusystem" "0"
  "source" ""
}
"@
Set-Content -Path $gamemodesFile -Value $gamemodesContent

# Create addon.json in the directory
$addonFile = Join-Path -Path $directory -ChildPath "addon.json"
$addonContent = @"
{
  "title": "$dir",
  "type": "map",
  "tags": [
    "scenic",
    "realism"
  ]
}
"@
Set-Content -Path $addonFile -Value $addonContent

Write-Host '########## DONE ##########' -ForegroundColor Green
