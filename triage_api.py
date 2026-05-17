from typing import Any, Dict, List, Optional
from inference_engine import run_triage, FiredRule
from explanation import full_explanation
from working_memory import WorkingMemory

def _fired_to_dict(fr: FiredRule) -> Dict[str, Any]:
    return {
        "rule_id"   : fr.rule_id,
        "diagnosis" : fr.diagnosis,
        "urgency"   : fr.urgency.value,
        "action"    : fr.action,
        "confidence": round(fr.confidence, 2),
        "conditions": fr.conditions,
        "is_primary": fr.is_primary,
    }


def triage(
    symptoms     : Dict[str, bool],
    heart_rate   : Optional[int] = None,
    oxygen_level : Optional[int] = None,
    background   : Optional[Dict[str, bool]] = None,
) -> Dict[str, Any]:
    """
    Run a full triage cycle and return a structured result dict.

    Parameters
    ----------
    symptoms     : Mapping of symptom label → bool.
                   Labels must match keys in ``FACT_KEYS`` (working_memory.py).
    heart_rate   : Beats per minute (20–300). Pass None to skip.
    oxygen_level : SpO₂ percentage (50–100). Pass None to skip.
    background   : Mapping of background/history label → bool.

    Returns
    -------
    {
        "status"      : "match" | "no_match",
        "primary"     : dict | None,
        "alternatives": list[dict],
        "active_facts": list[str],
        "explanation" : {"why": str, "how": str},
    }

    Raises
    ------
    ValueError   : If numeric inputs are outside plausible ranges.
    """
    # Run inference
    fired: List[FiredRule] = run_triage(
        symptoms     = symptoms or {},
        heart_rate   = heart_rate,
        oxygen_level = oxygen_level,
        background   = background or {},
    )

    # Collect active facts for explanation
    mem = WorkingMemory()
    mem.load(
        symptoms     = symptoms or {},
        heart_rate   = heart_rate,
        oxygen_level = oxygen_level,
        background   = background or {},
    )
    active = mem.active_facts()

    # Build response
    if not fired:
        return {
            "status"      : "no_match",
            "primary"     : None,
            "alternatives": [],
            "active_facts": active,
            "explanation" : full_explanation([], active),
        }

    return {
        "status"      : "match",
        "primary"     : _fired_to_dict(fired[0]),
        "alternatives": [_fired_to_dict(fr) for fr in fired[1:]],
        "active_facts": active,
        "explanation" : full_explanation(fired, active),
    }



if __name__ == "__main__":
    import json

    SEPARATOR = "-" * 60

    scenarios = [
        {
            "label"      : "Scenario 1 - Common Cold (low urgency)",
            "symptoms"   : {"Cough": True, "Sore Throat": True},
            "heart_rate" : None,
            "oxygen"     : None,
            "background" : {},
        },
        {
            "label"      : "Scenario 2 - COVID-19 vs Flu overlap (conflict resolution)",
            "symptoms"   : {"Fever": True, "Cough": True, "Fatigue": True,
                            "Shortness of Breath": True},
            "heart_rate" : 95,
            "oxygen"     : 96,
            "background" : {},
        },
        {
            "label"      : "Scenario 3 - Critical: Possible Heart Attack",
            "symptoms"   : {"Chest Pain": True, "Sweating": True, "Dizziness": True},
            "heart_rate" : 130,
            "oxygen"     : None,
            "background" : {"History of Heart Disease": True},
        },
        {
            "label"      : "Scenario 4 - Respiratory Distress (critical, low SpO2)",
            "symptoms"   : {"Shortness of Breath": True},
            "heart_rate" : None,
            "oxygen"     : 88,
            "background" : {},
        },
        {
            "label"      : "Scenario 5 - No match (vague input)",
            "symptoms"   : {"Fatigue": True},
            "heart_rate" : None,
            "oxygen"     : None,
            "background" : {},
        },
    ]

    for sc in scenarios:
        print(SEPARATOR)
        print(sc["label"])
        result = triage(
            symptoms     = sc["symptoms"],
            heart_rate   = sc["heart_rate"],
            oxygen_level = sc["oxygen"],
            background   = sc["background"],
        )
        print(f"Status      : {result['status']}")
        if result["primary"]:
            p = result["primary"]
            print(f"Primary     : {p['diagnosis']} | {p['urgency']} | conf={p['confidence']}")
        if result["alternatives"]:
            for alt in result["alternatives"]:
                print(f"Alternative : {alt['diagnosis']} | {alt['urgency']} | conf={alt['confidence']}")
        print("\n--- WHY ---")
        print(result["explanation"]["why"])
        print("\n--- HOW ---")
        print(result["explanation"]["how"])

    print(SEPARATOR)
    print("All scenarios completed.")
