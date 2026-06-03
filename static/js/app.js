// Global Variables
let isMonitoring = false;
let analysisHistory = [];

// Initialize on page load
document.addEventListener('DOMContentLoaded', function() {
    console.log('AI Disaster Commander initialized');
    updateStatus();
});

// Start monitoring
async function startMonitoring() {
    try {
        const response = await fetch('/api/start-monitoring', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' }
        });
        
        const data = await response.json();
        console.log('Monitoring started:', data);
        
        isMonitoring = true;
        document.getElementById('startBtn').disabled = true;
        document.getElementById('stopBtn').disabled = false;
        
        // Update UI
        updateStatus();
        
        // Show notification
        showNotification('Monitoring started successfully!', 'success');
        
        // Refresh status every 5 seconds
        setInterval(function() {
            if (isMonitoring) {
                updateStatus();
            }
        }, 5000);
        
    } catch (error) {
        console.error('Error starting monitoring:', error);
        showNotification('Error starting monitoring: ' + error.message, 'error');
    }
}

// Stop monitoring
async function stopMonitoring() {
    try {
        const response = await fetch('/api/stop-monitoring', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' }
        });
        
        const data = await response.json();
        console.log('Monitoring stopped:', data);
        
        isMonitoring = false;
        document.getElementById('startBtn').disabled = false;
        document.getElementById('stopBtn').disabled = true;
        
        updateStatus();
        showNotification('Monitoring stopped', 'info');
        
    } catch (error) {
        console.error('Error stopping monitoring:', error);
        showNotification('Error stopping monitoring: ' + error.message, 'error');
    }
}

// Detect disaster with manual input
async function detectDisaster() {
    const location = document.getElementById('location').value || 'auto';
    
    try {
        const response = await fetch('/api/detect-disaster', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                location: location,
                parameters: {}
            })
        });
        
        const result = await response.json();
        console.log('Detection result:', result);
        
        processDetectionResult(result);
        updateStatus();
        
    } catch (error) {
        console.error('Error during detection:', error);
        showNotification('Detection error: ' + error.message, 'error');
    }
}

// Detect disaster with custom environmental data
async function detectDisasterWithData() {
    const parameters = {
        temperature: parseFloat(document.getElementById('temp').value),
        humidity: parseFloat(document.getElementById('humidity').value),
        pressure: parseFloat(document.getElementById('pressure').value),
        wind_speed: parseFloat(document.getElementById('windSpeed').value),
        precipitation: parseFloat(document.getElementById('precipitation').value),
        seismic_activity: parseFloat(document.getElementById('seismic').value),
        water_level: parseFloat(document.getElementById('waterLevel').value),
        air_quality: parseFloat(document.getElementById('airQuality').value)
    };
    
    const location = document.getElementById('location').value || 'manual_input';
    
    try {
        const response = await fetch('/api/detect-disaster', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                location: location,
                parameters: parameters
            })
        });
        
        const result = await response.json();
        console.log('Detection result with custom data:', result);
        
        processDetectionResult(result);
        updateStatus();
        
    } catch (error) {
        console.error('Error during detection:', error);
        showNotification('Detection error: ' + error.message, 'error');
    }
}

// Process detection results
function processDetectionResult(result) {
    // Add to history
    analysisHistory.unshift(result);
    if (analysisHistory.length > 20) {
        analysisHistory.pop();
    }
    
    // Update risk level
    const riskLevel = result.risk_level;
    const riskElement = document.getElementById('riskLevel');
    const riskGauge = document.getElementById('riskGauge');
    const riskText = document.getElementById('riskText');
    
    riskElement.textContent = riskLevel;
    riskElement.className = 'value risk-' + riskLevel.toLowerCase();
    
    // Update gauge
    const riskPercentage = calculateRiskPercentage(riskLevel);
    riskGauge.style.width = riskPercentage + '%';
    
    riskText.textContent = result.description;
    
    // Update alerts
    if (riskLevel !== 'LOW' && riskLevel !== 'MINIMAL') {
        addAlert(result.disaster_type, result.risk_level, result.description);
        playAlertSound(result.disaster_type);
    }
    
    // Display reasoning
    displayReasoning(result.reasoning);
    
    // Update history
    updateHistory();
    
    // Show notification
    if (riskLevel === 'CRITICAL') {
        showNotification('🚨 CRITICAL DISASTER ALERT! ' + result.disaster_type.toUpperCase(), 'critical');
    } else if (riskLevel === 'HIGH') {
        showNotification('⚠️ HIGH RISK: ' + result.disaster_type, 'warning');
    } else {
        showNotification('Analysis complete: ' + result.disaster_type, 'info');
    }
}

// Calculate risk percentage for gauge
function calculateRiskPercentage(riskLevel) {
    const percentages = {
        'MINIMAL': 0,
        'LOW': 20,
        'MODERATE': 50,
        'HIGH': 75,
        'CRITICAL': 100
    };
    return percentages[riskLevel] || 0;
}

// Add alert to list
function addAlert(disasterType, riskLevel, description) {
    const alertsList = document.getElementById('alertsList');
    
    // Remove placeholder if exists
    const placeholder = alertsList.querySelector('.no-alerts');
    if (placeholder) {
        placeholder.remove();
    }
    
    const alertItem = document.createElement('div');
    alertItem.className = 'alert-item ' + riskLevel.toLowerCase();
    
    const timestamp = new Date().toLocaleTimeString();
    
    alertItem.innerHTML = `
        <h4>${disasterType.toUpperCase()} - ${riskLevel}</h4>
        <p>${description}</p>
        <small>${timestamp}</small>
    `;
    
    alertsList.insertBefore(alertItem, alertsList.firstChild);
    
    // Update badge
    const alertCount = alertsList.querySelectorAll('.alert-item').length;
    document.getElementById('alertCount').textContent = alertCount;
}

// Clear alerts
async function clearAlerts() {
    try {
        const response = await fetch('/api/clear-alerts', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' }
        });
        
        document.getElementById('alertsList').innerHTML = '<p class="no-alerts">No active alerts</p>';
        document.getElementById('alertCount').textContent = '0';
        showNotification('Alerts cleared', 'success');
        
    } catch (error) {
        console.error('Error clearing alerts:', error);
    }
}

// Play alert sound
function playAlertSound(disasterType) {
    // Create audio context and play sound
    const audioContext = new (window.AudioContext || window.webkitAudioContext)();
    
    const oscillator = audioContext.createOscillator();
    const gainNode = audioContext.createGain();
    
    oscillator.connect(gainNode);
    gainNode.connect(audioContext.destination);
    
    // Different frequencies for different disasters
    const frequencies = {
        'earthquake': 600,
        'hurricane': 700,
        'flooding': 500,
        'tornado': 800,
        'wildfire': 900,
        'tsunami': 550
    };
    
    const frequency = frequencies[disasterType] || 1000;
    
    oscillator.frequency.value = frequency;
    gainNode.gain.setValueAtTime(0.3, audioContext.currentTime);
    gainNode.gain.exponentialRampToValueAtTime(0.01, audioContext.currentTime + 1);
    
    oscillator.start(audioContext.currentTime);
    oscillator.stop(audioContext.currentTime + 1);
}

// Display AI reasoning
function displayReasoning(reasoning) {
    const reasoningPanel = document.getElementById('reasoningPanel');
    
    let html = '<div>';
    
    // Display steps
    if (reasoning.steps) {
        html += '<h4>Analysis Steps:</h4>';
        reasoning.steps.forEach((step, index) => {
            html += `<p><strong>Step ${index + 1}:</strong> ${step}</p>`;
        });
    }
    
    // Display gathered data
    if (reasoning.gathered_data) {
        html += '<h4>Environmental Data Gathered:</h4>';
        html += '<ul>';
        Object.keys(reasoning.gathered_data).forEach(key => {
            const value = reasoning.gathered_data[key];
            if (typeof value === 'number') {
                html += `<li><strong>${key}:</strong> ${value.toFixed(2)}</li>`;
            } else {
                html += `<li><strong>${key}:</strong> ${value}</li>`;
            }
        });
        html += '</ul>';
    }
    
    // Display analysis
    if (reasoning.analysis && reasoning.analysis.length > 0) {
        html += '<h4>Pattern Matches:</h4>';
        reasoning.analysis.forEach(match => {
            html += `<div class="reasoning-step">`;
            html += `<strong>Disaster Type:</strong> ${match.disaster_type}<br>`;
            html += `<strong>Score:</strong> ${match.score}/100<br>`;
            html += `<strong>Indicators:</strong> ${match.matched_indicators.join(', ')}<br>`;
            html += `</div>`;
        });
    }
    
    // Display conclusion
    if (reasoning.conclusion) {
        html += `<h4>Conclusion:</h4><p>${reasoning.conclusion}</p>`;
    }
    
    html += '</div>';
    reasoningPanel.innerHTML = html;
}

// Update history display
function updateHistory() {
    const historyList = document.getElementById('historyList');
    
    historyList.innerHTML = '';
    
    if (analysisHistory.length === 0) {
        historyList.innerHTML = '<p class="placeholder">No detection history yet</p>';
        return;
    }
    
    analysisHistory.forEach((item, index) => {
        const historyItem = document.createElement('div');
        historyItem.className = 'history-item';
        
        const timestamp = new Date(item.timestamp).toLocaleString();
        
        historyItem.innerHTML = `
            <h4>${item.disaster_type.toUpperCase()} - ${item.risk_level}</h4>
            <p><strong>Location:</strong> ${item.location}</p>
            <p><strong>Confidence:</strong> ${item.confidence.toFixed(1)}%</p>
            <p><strong>Time:</strong> ${timestamp}</p>
            <p><strong>Action:</strong> ${item.recommended_action}</p>
        `;
        
        historyList.appendChild(historyItem);
    });
}

// Update status from server
async function updateStatus() {
    try {
        const response = await fetch('/api/status', {
            method: 'GET',
            headers: { 'Content-Type': 'application/json' }
        });
        
        const status = await response.json();
        
        // Update monitoring status
        const monitoringStatus = document.getElementById('monitoringStatus');
        if (status.monitoring) {
            monitoringStatus.textContent = 'ON';
            monitoringStatus.className = 'value status-active';
        } else {
            monitoringStatus.textContent = 'OFF';
            monitoringStatus.className = 'value status-inactive';
        }
        
        // Update risk level
        document.getElementById('riskLevel').textContent = status.risk_level;
        document.getElementById('riskLevel').className = 'value risk-' + status.risk_level.toLowerCase();
        
        // Update last check time
        if (status.last_check) {
            const lastCheck = new Date(status.last_check).toLocaleTimeString();
            document.getElementById('lastCheck').textContent = lastCheck;
        }
        
    } catch (error) {
        console.error('Error updating status:', error);
    }
}

// Show notification
function showNotification(message, type = 'info') {
    // Create notification element
    const notification = document.createElement('div');
    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        padding: 15px 20px;
        background: ${type === 'critical' ? '#8b0000' : type === 'error' ? '#f44336' : type === 'warning' ? '#ff9800' : type === 'success' ? '#4caf50' : '#2196F3'};
        color: white;
        border-radius: 6px;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
        z-index: 1000;
        animation: slideIn 0.3s ease;
        max-width: 400px;
    `;
    
    notification.textContent = message;
    document.body.appendChild(notification);
    
    // Remove after 5 seconds
    setTimeout(() => {
        notification.style.animation = 'slideOut 0.3s ease';
        setTimeout(() => notification.remove(), 300);
    }, 5000);
}

// Add animation styles
const style = document.createElement('style');
style.textContent = `
    @keyframes slideIn {
        from {
            transform: translateX(400px);
            opacity: 0;
        }
        to {
            transform: translateX(0);
            opacity: 1;
        }
    }
    
    @keyframes slideOut {
        from {
            transform: translateX(0);
            opacity: 1;
        }
        to {
            transform: translateX(400px);
            opacity: 0;
        }
    }
`;
document.head.appendChild(style);

// Auto-update status every 10 seconds
setInterval(updateStatus, 10000);
