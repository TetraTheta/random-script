$decoded = ""
if ($args.Count -gt 0) {
  Write-Host $args[0]
  $decoded = [System.Text.Encoding]::UTF8.GetString([System.Convert]::FromBase64String($args[0]))
}
else {
  $clip = Get-Clipboard
  $decoded = [System.Text.Encoding]::UTF8.GetString([System.Convert]::FromBase64String($clip))
}
Set-Clipboard -Value $decoded
Write-Host $decoded
