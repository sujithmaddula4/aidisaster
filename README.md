# 🚨 AI Disaster Commander

**Advanced AI-Powered Disaster Detection & Alert System using Agentic AI**

An intelligent emergency response system that uses agentic AI to detect potential disasters and issue real-time audio alerts.

## Features

✨ **Agentic AI Disaster Detection**
- Intelligent pattern matching against 6 disaster types (earthquake, hurricane, flooding, tornado, wildfire, tsunami)
- Multi-step reasoning process for accurate analysis
- Real-time environmental data analysis

🔊 **Audio Alert System**
- Automatic sound alerts when disasters are detected
- Text-to-speech emergency notifications
- System beep fallback for compatibility

📊 **Real-time Dashboard**
- Live monitoring status
- Risk assessment gauge
- Environmental parameter inputs
- Detailed AI reasoning transparency
- Detection history tracking

🎯 **6 Disaster Types Supported**
1. **Earthquake** - Seismic activity detection
2. **Hurricane** - Wind speed & pressure analysis
3. **Flooding** - Rainfall & water level monitoring
4. **Tornado** - Wind shear & rotation detection
5. **Wildfire** - Temperature & humidity analysis
6. **Tsunami** - Seismic & ocean wave monitoring

## Project Structure

```
ai_disaster_commander/
├── app.py                          # Main Flask application
├── requirements.txt                # Python dependencies
├── agents/
│   ├── __init__.py
│   └── disaster_detector.py        # Agentic AI disaster detection engine
├── utils/
│   ├── __init__.py
│   └── sound_alert.py              # Audio alert system
├── templates/
│   └── dashboard.html              # Web interface
└── static/
    ├── css/
    │   └── style.css               # Modern UI styling
    ├── js/
    │   └── app.js                  # Interactive dashboard logic
    └── sounds/                     # Custom alert sounds (optional)
```

## Installation

### Prerequisites
- Python 3.8+
- pip (Python package manager)

### Setup Steps

1. **Navigate to project directory:**
   ```bash
   cd ai_disaster_commander
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

   Or install manually:
   ```bash
   pip install Flask Flask-CORS pydub pyttsx3
   ```

3. **Run the application:**
   ```bash
   python app.py
   ```

4. **Open in browser:**
   - Navigate to `http://127.0.0.1:5000`
   - Or `http://localhost:5000`

## Usage

### Start Real-time Monitoring
1. Click **"Start Monitoring"** button
2. System will continuously scan for disasters every 10 seconds
3. Audio alerts trigger automatically when threats detected
4. View risk levels and alerts in real-time

### Manual Analysis
1. Enter location (or use "auto")
2. Click **"Analyze Now"** button
3. View detailed AI reasoning and results

### Custom Environmental Data Analysis
1. Input environmental parameters:
   - Temperature (°C)
   - Humidity (%)
   - Air Pressure (hPa)
   - Wind Speed (km/h)
   - Precipitation (mm)
   - Seismic Activity (Magnitude)
   - Water Level (m)
   - Air Quality (AQI)
2. Click **"Analyze with Custom Data"**
3. System processes data through AI agents

## API Endpoints

### Start Monitoring
```
POST /api/start-monitoring
```
Begins continuous disaster monitoring.

### Stop Monitoring
```
POST /api/stop-monitoring
```
Stops the monitoring loop.

### Detect Disaster
```
POST /api/detect-disaster
Body: {
  "location": "string",
  "parameters": {
    "temperature": number,
    "humidity": number,
    "pressure": number,
    "wind_speed": number,
    "precipitation": number,
    "seismic_activity": number,
    "water_level": number,
    "air_quality": number
  }
}
```
Analyzes conditions for disaster risks.

### Get Status
```
GET /api/status
```
Returns current system status and detected disasters.

### Clear Alerts
```
POST /api/clear-alerts
```
Clears alert history.

## AI Agentic System

The system uses a multi-step agentic reasoning process:

### Step 1: Data Gathering
- Collects environmental sensor data
- Retrieves location information
- Gathers historical patterns

### Step 2: Pattern Matching
- Analyzes against 6 disaster type patterns
- Calculates match scores (0-100)
- Identifies matched indicators

### Step 3: Risk Assessment
- Evaluates pattern match confidence
- Determines risk level (MINIMAL/LOW/MODERATE/HIGH/CRITICAL)
- Generates recommendations

### Step 4: Alert Response
- Triggers audio warnings for HIGH+ risk
- Updates dashboard in real-time
- Maintains detection history

## Risk Levels

| Level | Confidence | Action |
|-------|-----------|--------|
| MINIMAL | <20% | Continue monitoring |
| LOW | 20-40% | Continue normal activities |
| MODERATE | 40-60% | Stay informed and ready |
| HIGH | 60-80% | Prepare for evacuation |
| CRITICAL | 80%+ | Evacuate immediately |

## Sound Alerts

The system provides multiple alert methods:
- **Text-to-Speech**: Direct voice announcements via pyttsx3
- **System Beep**: Fallback alarm (3 rapid beeps)
- **Custom Sounds**: Optional custom audio files in `/static/sounds/`

## Browser Compatibility

- ✅ Chrome/Chromium (recommended)
- ✅ Firefox
- ✅ Safari
- ✅ Edge
- ✅ Mobile browsers

## Customization

### Add Custom Disaster Pattern
Edit `agents/disaster_detector.py`:
```python
self.disaster_patterns['new_disaster'] = {
    'indicators': ['indicator1', 'indicator2'],
    'thresholds': {'param': value},
    'sound': 'alert.mp3'
}
```

### Modify Alert Thresholds
Edit risk assessment in `agents/disaster_detector.py` `_assess_risk()` method.

### Change UI Colors
Edit `static/css/style.css` gradient and color variables.

## Dependencies

- **Flask** (3.0+) - Web framework
- **Flask-CORS** - Enable cross-origin requests
- **pyttsx3** - Text-to-speech engine
- **pydub** - Audio processing (optional)
- **NumPy** - Numerical operations

## Troubleshooting

### "Address already in use" error
- Change port in `app.py` line 82: `port=5000` → `port=5001`
- Or kill existing Flask process

### Audio not playing
- Ensure system volume is ON
- Install pyttsx3: `pip install pyttsx3`
- For pydub: `pip install pydub`

### ModuleNotFoundError
- Reinstall dependencies: `pip install -r requirements.txt`
- Verify Python version: `python --version`

## Performance Tips

1. **Disable browser auto-refresh** if analyzing large datasets
2. **Use Chrome DevTools** for performance monitoring
3. **Clear history** periodically for better memory usage
4. **Close unused tabs** to reduce CPU load

## Future Enhancements

- 🗺️ Real-time map integration
- 📡 Live weather API integration
- 🤖 Machine learning model integration
- 📱 Mobile app version
- 🌐 Multi-language support
- 🔔 Push notification system
- 📊 Advanced analytics dashboard

## License

MIT License - Feel free to use and modify

## Support

For issues, suggestions, or contributions, please create an issue or pull request.

---

**Stay Safe. Stay Alert. AI Disaster Commander.** 🚨
