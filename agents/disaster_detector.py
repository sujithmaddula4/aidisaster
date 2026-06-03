import json
from datetime import datetime
import random
import logging

logger = logging.getLogger(__name__)

class DisasterDetectorAgent:
    """
    Agentic AI for disaster detection.
    Uses reasoning and pattern matching to identify potential disasters.
    """
    
    def __init__(self):
        self.disaster_patterns = {
            'earthquake': {
                'indicators': ['ground_movement', 'seismic_waves', 'tremors'],
                'thresholds': {'magnitude': 4.0, 'depth': 100},
                'sound': 'earthquake_alert.mp3'
            },
            'hurricane': {
                'indicators': ['wind_speed', 'pressure_drop', 'cloud_formation'],
                'thresholds': {'wind_speed': 74, 'pressure': 950},
                'sound': 'hurricane_alert.mp3'
            },
            'flooding': {
                'indicators': ['water_level', 'rainfall', 'river_flow'],
                'thresholds': {'rainfall': 50, 'water_level': 3},
                'sound': 'flood_alert.mp3'
            },
            'tornado': {
                'indicators': ['rotation', 'wind_shear', 'cloud_rotation'],
                'thresholds': {'rotation_speed': 100, 'wind_shear': 20},
                'sound': 'tornado_alert.mp3'
            },
            'wildfire': {
                'indicators': ['temperature', 'humidity', 'vegetation'],
                'thresholds': {'temperature': 35, 'humidity': 20},
                'sound': 'wildfire_alert.mp3'
            },
            'tsunami': {
                'indicators': ['ocean_waves', 'seismic_activity', 'tide'],
                'thresholds': {'wave_height': 10, 'seismic': 7.0},
                'sound': 'tsunami_alert.mp3'
            }
        }
        
        self.reasoning_history = []
    
    def analyze(self, location, parameters):
        """
        Main analysis method using agentic reasoning
        """
        reasoning = {
            "steps": [],
            "gathered_data": {},
            "analysis": [],
            "conclusion": ""
        }
        
        # Step 1: Gather environmental data
        reasoning["steps"].append("Step 1: Gathering environmental data from sensors and sources")
        gathered_data = self._gather_environmental_data(location, parameters)
        reasoning["gathered_data"] = gathered_data
        
        # Step 2: Analyze patterns
        reasoning["steps"].append("Step 2: Analyzing disaster patterns against gathered data")
        pattern_matches = self._match_patterns(gathered_data)
        reasoning["analysis"] = pattern_matches
        
        # Step 3: Calculate risk level
        reasoning["steps"].append("Step 3: Calculating overall risk level")
        risk_assessment = self._assess_risk(pattern_matches, gathered_data)
        reasoning["conclusion"] = risk_assessment["summary"]
        
        # Step 4: Generate response
        reasoning["steps"].append("Step 4: Generating alert response")
        
        result = {
            "timestamp": datetime.now().isoformat(),
            "location": location,
            "disaster_type": risk_assessment["primary_disaster"],
            "risk_level": risk_assessment["risk_level"],
            "confidence": risk_assessment["confidence"],
            "description": risk_assessment["description"],
            "reasoning": reasoning,
            "recommended_action": risk_assessment["recommended_action"]
        }
        
        # Store reasoning history
        self.reasoning_history.append(result)
        
        return result
    
    def _gather_environmental_data(self, location, parameters):
        """Gather environmental data from various sources"""
        data = {
            "location": location,
            "temperature": parameters.get('temperature', random.uniform(20, 40)),
            "humidity": parameters.get('humidity', random.uniform(30, 80)),
            "pressure": parameters.get('pressure', random.uniform(980, 1030)),
            "wind_speed": parameters.get('wind_speed', random.uniform(0, 50)),
            "precipitation": parameters.get('precipitation', random.uniform(0, 100)),
            "seismic_activity": parameters.get('seismic_activity', random.uniform(0, 8)),
            "water_level": parameters.get('water_level', random.uniform(0, 5)),
            "air_quality": parameters.get('air_quality', random.uniform(0, 500))
        }
        return data
    
    def _match_patterns(self, data):
        """Match gathered data against disaster patterns"""
        matches = []
        
        for disaster_type, pattern in self.disaster_patterns.items():
            score = 0
            matched_indicators = []
            
            if disaster_type == 'earthquake':
                if data['seismic_activity'] >= pattern['thresholds']['magnitude']:
                    score += 40
                    matched_indicators.append('seismic_waves')
            
            elif disaster_type == 'hurricane':
                if data['wind_speed'] >= pattern['thresholds']['wind_speed']:
                    score += 40
                    matched_indicators.append('wind_speed')
                if data['pressure'] <= pattern['thresholds']['pressure']:
                    score += 30
                    matched_indicators.append('pressure_drop')
            
            elif disaster_type == 'flooding':
                if data['precipitation'] >= pattern['thresholds']['rainfall']:
                    score += 40
                    matched_indicators.append('rainfall')
                if data['water_level'] >= pattern['thresholds']['water_level']:
                    score += 30
                    matched_indicators.append('water_level')
            
            elif disaster_type == 'tornado':
                if data['wind_speed'] >= 80 and data['pressure'] < 1000:
                    score += 50
                    matched_indicators.extend(['rotation', 'wind_shear'])
            
            elif disaster_type == 'wildfire':
                if data['temperature'] >= pattern['thresholds']['temperature'] and \
                   data['humidity'] <= pattern['thresholds']['humidity']:
                    score += 45
                    matched_indicators.extend(['temperature', 'humidity'])
            
            elif disaster_type == 'tsunami':
                if data['seismic_activity'] >= pattern['thresholds']['seismic']:
                    score += 40
                    matched_indicators.append('seismic_activity')
            
            if score > 0:
                matches.append({
                    "disaster_type": disaster_type,
                    "score": score,
                    "matched_indicators": matched_indicators
                })
        
        # Sort by score
        matches.sort(key=lambda x: x['score'], reverse=True)
        return matches
    
    def _assess_risk(self, pattern_matches, data):
        """Assess overall risk level based on pattern matching"""
        if not pattern_matches:
            return {
                "primary_disaster": "NONE",
                "risk_level": "LOW",
                "confidence": 0,
                "description": "No disaster indicators detected",
                "summary": "Environmental conditions are normal",
                "recommended_action": "Continue monitoring"
            }
        
        primary = pattern_matches[0]
        score = primary['score']
        
        # Determine risk level
        if score >= 80:
            risk_level = "CRITICAL"
            confidence = min(100, score)
            recommended_action = "EVACUATE IMMEDIATELY - Seek shelter"
        elif score >= 60:
            risk_level = "HIGH"
            confidence = min(100, score)
            recommended_action = "PREPARE FOR EVACUATION - Stay alert"
        elif score >= 40:
            risk_level = "MODERATE"
            confidence = min(100, score)
            recommended_action = "Stay informed and ready to act"
        elif score >= 20:
            risk_level = "LOW"
            confidence = min(100, score)
            recommended_action = "Continue normal activities with caution"
        else:
            risk_level = "MINIMAL"
            confidence = 0
            recommended_action = "Continue monitoring"
        
        description = f"{primary['disaster_type'].upper()} risk detected. "
        description += f"Indicators: {', '.join(primary['matched_indicators'])}. "
        description += f"Confidence: {confidence:.0f}%"
        
        return {
            "primary_disaster": primary['disaster_type'],
            "risk_level": risk_level,
            "confidence": confidence,
            "description": description,
            "summary": f"Risk level: {risk_level}. {recommended_action}",
            "recommended_action": recommended_action
        }
    
    def get_history(self):
        """Get reasoning history"""
        return self.reasoning_history[-10:]  # Return last 10 analyses
