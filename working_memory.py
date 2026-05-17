"""
Holds all patient facts for a single triage session.
Facts are Boolean flags derived from symptoms, indicators, and background info.
"""
from dataclasses import dataclass, field
from typing import Dict, Any

# Mapping from UI-friendly labels to internal fact keys
FACT_KEYS = {
    # ── Symptoms ──────────────────────────────────────────────────────────
    "Fever"                : "fever",
    "Cough"                : "cough",
    "Fatigue"              : "fatigue",
    "Shortness of Breath"  : "shortness_of_breath",
    "Headache"             : "headache",
    "Nausea"               : "nausea",
    "Chest Pain"           : "chest_pain",
    "Sore Throat"          : "sore_throat",
    "Sweating"             : "sweating",
    "Dizziness"            : "dizziness",
    "Light Sensitivity"    : "light_sensitivity",
    "Abdominal Pain"       : "abdominal_pain",

    # ── Health indicators (derived from numeric thresholds) ────────────
    "High Heart Rate"      : "high_heart_rate",   # HR > 100 bpm
    "Low Oxygen Level"     : "low_oxygen_level",  # SpO₂ < 94 %

    # ── Background / history ──────────────────────────────────────────
    "History of Asthma"         : "history_of_asthma",
    "History of Heart Disease"  : "history_of_heart_disease",
}

# Numeric thresholds used to derive Boolean health-indicator facts
HEART_RATE_HIGH_THRESHOLD = 100   # bpm
OXYGEN_LOW_THRESHOLD      = 94    # %


@dataclass
class WorkingMemory:
    """
    Dynamic fact store for one triage session.

    Parameters accepted in `load()`:
    - symptoms    : dict[str, bool]   – checked symptom checkboxes
    - heart_rate  : int | None        – beats per minute (optional)
    - oxygen_level: int | None        – SpO₂ percentage (optional)
    - background  : dict[str, bool]   – chronic-disease / history flags
    """
    facts: Dict[str, bool] = field(default_factory=dict)

    def load(
        self,
        symptoms     : Dict[str, bool],
        heart_rate   : Any = None,
        oxygen_level : Any = None,
        background   : Dict[str, bool] = None,
    ) -> None:
        """Validate inputs and populate the fact store."""
        self.facts.clear()

        # --- symptoms ---
        for label, value in symptoms.items():
            key = FACT_KEYS.get(label)
            if key:
                self.facts[key] = bool(value)

        # --- health indicators ---
        if heart_rate is not None:
            try:
                hr = int(heart_rate)
                if hr < 20 or hr > 300:
                    raise ValueError(f"Heart rate {hr} is outside a plausible range (20–300 bpm).")
                self.facts["high_heart_rate"] = hr > HEART_RATE_HIGH_THRESHOLD
            except (TypeError, ValueError) as exc:
                raise ValueError(f"Invalid heart rate: {exc}") from exc

        if oxygen_level is not None:
            try:
                spo2 = int(oxygen_level)
                if spo2 < 50 or spo2 > 100:
                    raise ValueError(f"Oxygen level {spo2} % is outside a plausible range (50–100 %).")
                self.facts["low_oxygen_level"] = spo2 < OXYGEN_LOW_THRESHOLD
            except (TypeError, ValueError) as exc:
                raise ValueError(f"Invalid oxygen level: {exc}") from exc

        # --- background / history ---
        if background:
            for label, value in background.items():
                key = FACT_KEYS.get(label)
                if key:
                    self.facts[key] = bool(value)

    def get(self, key: str, default: bool = False) -> bool:
        return self.facts.get(key, default)

    def active_facts(self) -> list:
        """Return the list of fact keys that are currently True."""
        return [k for k, v in self.facts.items() if v]

    def __repr__(self) -> str:
        return f"WorkingMemory(active={self.active_facts()})"
