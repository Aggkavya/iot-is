param(
    [string]$Mode = ""
)

if ($Mode -eq "") {
    Write-Host "========================================="
    Write-Host "  SECURE IOT MQTT PROJECT CONTROL PANEL  "
    Write-Host "========================================="
    Write-Host "1. Start VULNERABLE Environment"
    Write-Host "2. Start PROTECTED Environment"
    Write-Host "3. Run Attacker Script"
    Write-Host "4. Stop All Processes (Clean up)"
    Write-Host "5. Exit"
    $choice = Read-Host "`nEnter choice (1-5)"
} else {
    $choice = $Mode
}

if ($choice -eq '4') {
    Write-Host "Stopping Mosquitto and Python scripts..."
    Stop-Process -Name "mosquitto" -Force -ErrorAction SilentlyContinue
    # Ask for confirmation before killing all python processes just in case
    $confirm = Read-Host "This will forcefully stop all 'python.exe' processes. Proceed? (y/n)"
    if ($confirm -eq 'y') {
        Stop-Process -Name "python" -Force -ErrorAction SilentlyContinue
        Write-Host "Done!"
    }
    exit
}

if ($choice -eq '3') {
    Write-Host "Launching Attacker in new window..."
    Start-Process -FilePath "powershell" -ArgumentList "-NoExit -Command `"& { title ATTACKER; .\venv\Scripts\activate; python attacker\attacker.py }`"" -WorkingDirectory $PWD
    exit
}

if ($choice -eq '1' -or $choice -eq '2') {
    Write-Host "Stopping any running Mosquitto instances first..."
    Stop-Process -Name "mosquitto" -Force -ErrorAction SilentlyContinue
    
    if ($choice -eq '1') {
        $conf = "mosquitto_vulnerable.conf"
        Write-Host "`n>>> STARTING VULNERABLE MODE <<<"
    } else {
        $conf = "mosquitto_protected.conf"
        Write-Host "`n>>> STARTING PROTECTED MODE <<<"
    }

    Write-Host "1. Starting MQTT Broker..."
    Start-Process -FilePath "C:\Program Files\mosquitto\mosquitto.exe" -ArgumentList "-v -c $conf" -WorkingDirectory "$PWD\broker"

    Start-Sleep -Seconds 2

    Write-Host "2. Starting Backend..."
    Start-Process -FilePath "powershell" -ArgumentList "-Command `"& { title BACKEND; .\venv\Scripts\activate; python backend\app.py }`"" -WorkingDirectory $PWD

    Write-Host "3. Starting IoT Devices..."
    Start-Process -FilePath "powershell" -ArgumentList "-Command `"& { title DOOR_DEVICE; .\venv\Scripts\activate; python devices\door_device.py }`"" -WorkingDirectory $PWD
    Start-Process -FilePath "powershell" -ArgumentList "-Command `"& { title LIGHT_DEVICE; .\venv\Scripts\activate; python devices\light_device.py }`"" -WorkingDirectory $PWD
    Start-Process -FilePath "powershell" -ArgumentList "-Command `"& { title ALARM_DEVICE; .\venv\Scripts\activate; python devices\alarm_device.py }`"" -WorkingDirectory $PWD

    Write-Host "`nAll systems are running!"
    Write-Host "Dashboard: http://localhost:5000"
    Write-Host "Run this script again and select Option 3 to launch the Attacker.`n"
    Write-Host "NOTE: To completely stop the environment, close the popup windows or use Option 4."
}
