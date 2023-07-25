
$SettingsObject = Get-Content -Path C:\NTC\Settings.JSON | ConvertFrom-Json

$TaskName = $SettingsObject.'$TaskName'
Unregister-ScheduledTask -TaskName $TaskName -Confirm:$False

Get-ScheduledTask -TaskName "*34*"
