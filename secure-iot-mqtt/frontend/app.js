const doorStatus = document.getElementById('door-status');
const lightStatus = document.getElementById('light-status');
const alarmStatus = document.getElementById('alarm-status');
const logContainer = document.getElementById('log-container');

// Fetch initial state
fetch('/api/state')
    .then(res => res.json())
    .then(data => updateDevices(data));

// Fetch initial logs
fetch('/api/logs')
    .then(res => res.json())
    .then(data => {
        data.forEach(log => addLogEntry(log));
    });

// Connect SSE for real-time updates
const evtSource = new EventSource("/stream");
evtSource.onmessage = function(event) {
    const data = JSON.parse(event.data);
    if (data.type === "state_update") {
        updateDevices(data.devices);
    } else if (data.type === "security_log") {
        addLogEntry(data.event);
    }
};

function updateDevices(devices) {
    updateBadge(doorStatus, devices["DOOR-001"] || "UNKNOWN");
    updateBadge(lightStatus, devices["LIGHT-001"] || "UNKNOWN");
    updateBadge(alarmStatus, devices["ALARM-001"] || "UNKNOWN");
}

function updateBadge(element, status) {
    let colorClass = "gray";
    if (status === "UNLOCKED" || status === "OFF" || status === "DISARMED") colorClass = "green";
    if (status === "LOCKED" || status === "ON" || status === "ARMED") colorClass = (status==="ON"?"blue":"red");
    
    element.innerHTML = `Status: <span class="badge ${colorClass}">${status}</span>`;
}

function sendCommand(device, command) {
    fetch('/api/command', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ device, command })
    });
}

function addLogEntry(log) {
    const el = document.createElement('div');
    const isAllowed = log.result === 'ALLOWED' || log.result === 'SUCCESS';
    el.className = `log-entry ${isAllowed ? 'allowed' : 'blocked'}`;
    
    el.innerHTML = `
        <div class="log-time">${log.timestamp} | Client: ${log.client}</div>
        <div class="log-action">${log.action} ➔ ${log.topic}</div>
        <div class="log-result">Result: <span style="font-weight:bold;color:${isAllowed ? '#10b981' : '#ef4444'}">${log.result}</span> (${log.reason})</div>
    `;
    
    logContainer.prepend(el);
}
