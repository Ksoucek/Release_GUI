$SettingsObject = Get-Content -Path C:\NTC\Settings.JSON | ConvertFrom-Json

$TaskName = $SettingsObject.'$TaskName'
$TaskTime = $SettingsObject.'$TaskTime'
$ReleasedFeatures = $SettingsObject.'$ReleasedFeatures'

$STPrin = New-ScheduledTaskPrincipal -UserId $SettingsObject.'$UserID' -LogonType ServiceAccount -RunLevel Highest -ProcessTokenSidType Default
$Action = New-ScheduledTaskAction -Execute "PowerShell.exe" -Argument "C:\Temp\ReleaseAndNotification.ps1"
$Trigger = New-ScheduledTaskTrigger -Once  -At $TaskTime 
$ScheduledTask = New-ScheduledTask -Action $action -Principal $STPrin -Trigger $trigger 
 
Register-ScheduledTask -TaskName $TaskName -InputObject $ScheduledTask

if ($SettingsObject.'$SentEmailBefore') 
{
$EmailFrom = $SettingsObject.'$EmailFrom'
$EmailTo = $SettingsObject.'$EmailTo'
$Subject = $SettingsObject.'$Subject'
$TaskTime=$SettingsObject.'$TaskTime'
$ReleasedFeatures=$SettingsObject.'$ReleasedFeatures'
$Body=$SettingsObject.'$Body'
$Body=$Body.replace('$TaskTime',$TaskTime)
$Body=$Body.replace('$ReleasedFeatures',$ReleasedFeatures)
$SMTPServer = “smtp.office365.com”
$SMTPClient = New-Object Net.Mail.SmtpClient($SmtpServer, 587)
$SMTPClient.EnableSsl = $true 
$SMTPClient.Credentials = New-Object System.Net.NetworkCredential($EmailFrom, “scdcxwrwygwmsvbv”);
$SMTPClient.Send($EmailFrom, $EmailTo, $Subject, $Body)
}
