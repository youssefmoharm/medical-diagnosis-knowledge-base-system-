from dataclasses import dataclass, field
from typing import List
from enum import Enum


class Urgency(str, Enum):
    LOW      = "Low"
    MEDIUM   = "Medium"
    HIGH     = "High"
    CRITICAL = "Critical"

    # Allow comparison by severity rank
    def rank(self) -> int:
        return {"Low": 0, "Medium": 1, "High": 2, "Critical": 3}[self.value]

    def __lt__(self, other):  return self.rank() < other.rank()
    def __le__(self, other):  return self.rank() <= other.rank()
    def __gt__(self, other):  return self.rank() > other.rank()
    def __ge__(self, other):  return self.rank() >= other.rank()


@dataclass
class Rule:
    """
    A single IF-THEN production rule.

    Attributes
    ----------
    rule_id    : Unique identifier (e.g. "R01").
    conditions : List of fact keys that must ALL be True for the rule to fire.
    diagnosis  : Human-readable condition name.
    urgency    : Urgency level (Urgency enum).
    action     : Recommended next step.
    confidence : Float in [0.0, 1.0] representing clinical certainty.
    """
    rule_id    : str
    conditions : List[str]
    diagnosis  : str
    urgency    : Urgency
    action     : str
    confidence : float = 1.0
    excluded_conditions: List[str] = field(default_factory=list)

    def matches(self, facts: dict) -> bool:
        """Return True when required facts are true and excluded facts are false."""
        required_ok = all(facts.get(c, False) for c in self.conditions)
        excluded_ok = all(not facts.get(c, False) for c in self.excluded_conditions)
        return required_ok and excluded_ok


RULES: List[Rule] = [
    Rule(
        rule_id    = "R01",
        conditions = ["fever", "cough", "fatigue"],
        diagnosis  = "Flu",
        urgency    = Urgency.MEDIUM,
        action     = "Rest at home, stay hydrated, monitor temperature.",
        confidence = 0.80,
    ),
    Rule(
        rule_id    = "R02",
        conditions = ["fever", "cough", "shortness_of_breath"],
        diagnosis  = "COVID-19",
        urgency    = Urgency.HIGH,
        action     = "Get tested immediately and self-isolate.",
        confidence = 0.90,
    ),
    Rule(
        rule_id    = "R03",
        conditions = ["headache", "nausea"],
        excluded_conditions = ["fever"],
        diagnosis  = "Migraine",
        urgency    = Urgency.LOW,
        action     = "Rest in a quiet, dark room and take over-the-counter pain relief.",
        confidence = 0.70,
    ),
    Rule(
        rule_id    = "R04",
        conditions = ["chest_pain", "high_heart_rate"],
        diagnosis  = "Possible Heart Issue",
        urgency    = Urgency.CRITICAL,
        action     = "Seek emergency care immediately.",
        confidence = 0.95,
    ),
    Rule(
        rule_id    = "R05",
        conditions = ["cough", "sore_throat"],
        excluded_conditions = ["fever"],
        diagnosis  = "Common Cold",
        urgency    = Urgency.LOW,
        action     = "Home care - fluids, rest, throat lozenges.",
        confidence = 0.75,
    ),
    Rule(
        rule_id    = "R06",
        conditions = ["fever", "cough", "shortness_of_breath", "history_of_asthma"],
        diagnosis  = "Asthma Complication",
        urgency    = Urgency.HIGH,
        action     = "Seek urgent medical consultation and monitor breathing closely.",
        confidence = 0.88,
    ),
    Rule(
        rule_id    = "R07",
        conditions = ["chest_pain", "sweating", "dizziness", "history_of_heart_disease"],
        diagnosis  = "Possible Heart Attack",
        urgency    = Urgency.CRITICAL,
        action     = "Call emergency services (911 / 123) immediately.",
        confidence = 0.97,
    ),
    Rule(
        rule_id    = "R08",
        conditions = ["headache", "fever", "light_sensitivity"],
        diagnosis  = "Possible Meningitis",
        urgency    = Urgency.CRITICAL,
        action     = "Go to the emergency department immediately.",
        confidence = 0.92,
    ),
    Rule(
        rule_id    = "R09",
        conditions = ["abdominal_pain", "fever", "nausea"],
        diagnosis  = "Appendicitis / GI Infection",
        urgency    = Urgency.HIGH,
        action     = "Visit an urgent care clinic or emergency room promptly.",
        confidence = 0.80,
    ),
    Rule(
        rule_id    = "R10",
        conditions = ["shortness_of_breath", "low_oxygen_level"],
        diagnosis  = "Respiratory Distress",
        urgency    = Urgency.CRITICAL,
        action     = "Call emergency services and seek immediate care.",
        confidence = 0.95,
    ),
]
