# This script creates a Mosquitto password file containing all the identities required for the project.

# Check if mosquitto_passwd is in PATH, or try the default installation location
$mosquitto_passwd = "mosquitto_passwd"
if (-not (Get-Command mosquitto_passwd -ErrorAction SilentlyContinue)) {
    if (Test-Path "C:\Program Files\mosquitto\mosquitto_passwd.exe") {
        $mosquitto_passwd = "C:\Program Files\mosquitto\mosquitto_passwd.exe"
    } else {
        Write-Error "Could not find mosquitto_passwd. Please ensure Mosquitto is installed and in your PATH."
        exit 1
    }
}

Write-Host "Creating password file for MQTT broker..."

# -c creates a new file, -b runs in batch mode (no prompt)
& $mosquitto_passwd -c -b password.txt dashboard_user dash123
& $mosquitto_passwd -b password.txt door_device door123
& $mosquitto_passwd -b password.txt light_device light123
& $mosquitto_passwd -b password.txt alarm_device alarm123
& $mosquitto_passwd -b password.txt attacker_test hacker123

Write-Host "Done! 'password.txt' has been created in the broker directory."
