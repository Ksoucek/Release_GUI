Import-Module "C:\Program Files\Microsoft Dynamics 365 Business Central\170\Service\NavAdminTool.ps1"
Import-Module "C:\PowershellTools\Modules\Import-ToolsModules.ps1"
Import-Module -Name Microsoft.PowerShell.Management 



$SettingsObject = Get-Content -Path C:\Temp\Settings.JSON | ConvertFrom-Json


#KOPIE SLOŽKY
$Path = "C:\PowershellTools\Release"
$copydfolder = gci $Path | ? { $_.PSIsContainer } | sort CreationTime -desc | select -f 1
$lastFile = gci C:\PowershellTools\SSC | sort LastWriteTime | select -last 1
$name2 = Get-Date -UFormat "%Y%m%d%H%M"
Copy-Item -Path "C:\PowershellTools\Release\$copydfolder" -Destination "C:\PowershellTools\Release\$name2" -recurse -Force  
Get-ChildItem -Path "C:\PowershellTools\Release\$name2" | Where-Object Name -Like '*Středisko společných činností*' | ForEach-Object { Remove-Item -LiteralPath C:\PowershellTools\Release\$name2\$_ }
Move-Item -Path C:\PowershellTools\SSC\$lastFile -Destination C:\PowershellTools\Release\$name2

$Instance = $SettingsObject.'$DeploymentInstance'
$EmailFrom = $SettingsObject.'$EmailFrom'
$EmailTo = $SettingsObject.'$EmailTo'
$SMTPServer = “smtp.office365.com”
$SMTPClient = New-Object Net.Mail.SmtpClient($SmtpServer, 587)
$SMTPClient.EnableSsl = $true 
$SMTPClient.Credentials = New-Object System.Net.NetworkCredential($EmailFrom, “scdcxwrwygwmsvbv”);
$Subject = $SettingsObject.'$Subject' + $SettingsObject.'$SubjectFinish'
$Body = $SettingsObject.'$BodyFinish'

cd..
cd..
cd powershelltools

$NavVerNo = (Convert-DynamicsVersion -Value 170 -OutputType ProductVersion) + "*"
$RunningServerInstances = (Get-NAVServerInstance -ErrorAction SilentlyContinue | Where-Object State -eq Running | Where-Object Version -Like $NavVerNo)
$RunningServerInstances | Set-NAVServerInstance -Stop |Out-Null

C:\powershelltools\Scripts\DeployDynamicsReleases\DeployDynamicsReleases.ps1 -ConfigFileName C:\powershelltools\\Configs\DeployDynamicsReleases.config |Out-Null


$RunningServerInstances | Set-NAVServerInstance -Restart |Out-Null


$SMTPClient.Send($EmailFrom, $EmailTo, $Subject, $Body)