import os
import logging
from pathlib import Path

logger = logging.getLogger(__name__)

class SoundAlert:
    """Handle sound alerts for disaster warnings"""
    
    def __init__(self):
        self.sound_dir = os.path.join(os.path.dirname(__file__), '..', 'static', 'sounds')
        self.use_fallback = True  # Use system sounds if custom unavailable
    
    def play_warning(self, disaster_type='general'):
        """Play warning sound based on disaster type"""
        try:
            # Try using pyttsx3 for text-to-speech alert
            import pyttsx3
            engine = pyttsx3.init()
            engine.setProperty('rate', 150)
            engine.setProperty('volume', 1.0)
            
            alert_text = self._get_alert_text(disaster_type)
            engine.say(alert_text)
            engine.runAndWait()
            logger.info(f"Audio alert played for {disaster_type}")
            
        except ImportError:
            logger.warning("pyttsx3 not available, using system beep")
            self._system_beep()
        except Exception as e:
            logger.error(f"Error playing sound: {str(e)}")
            self._system_beep()
    
    def _get_alert_text(self, disaster_type):
        """Get alert text based on disaster type"""
        alerts = {
            'earthquake': 'WARNING! Earthquake detected! Drop, cover and hold on!',
            'hurricane': 'ALERT! Hurricane warning! Seek shelter immediately!',
            'flooding': 'DANGER! Flooding detected! Move to higher ground!',
            'tornado': 'TORNADO WARNING! Take shelter in a sturdy building!',
            'wildfire': 'WILDFIRE ALERT! Evacuate the area immediately!',
            'tsunami': 'TSUNAMI WARNING! Evacuate to higher ground now!',
            'general': 'DISASTER ALERT! Emergency conditions detected!'
        }
        return alerts.get(disaster_type, alerts['general'])
    
    def _system_beep(self):
        """Produce system beep sound"""
        try:
            import winsound
            # Play beep 3 times
            for _ in range(3):
                winsound.Beep(1000, 500)  # Frequency and duration
        except ImportError:
            # For non-Windows systems
            print('\a')  # System bell
    
    def play_custom_sound(self, filename):
        """Play custom sound file if available"""
        try:
            from pydub import AudioSegment
            from pydub.playback import play
            
            sound_path = os.path.join(self.sound_dir, filename)
            if os.path.exists(sound_path):
                sound = AudioSegment.from_file(sound_path)
                play(sound)
            else:
                logger.warning(f"Sound file not found: {filename}")
                self.play_warning()
        except ImportError:
            logger.warning("pydub not available, using fallback alert")
            self.play_warning()
        except Exception as e:
            logger.error(f"Error playing custom sound: {str(e)}")
            self.play_warning()
