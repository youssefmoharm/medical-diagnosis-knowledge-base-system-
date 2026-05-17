from typing import List, Dict
from inference_engine import FiredRule


def full_explanation(fired_rules: List[FiredRule], active_facts: List[str]) -> Dict[str, str]:
    """
    Generate WHY and HOW explanations for the inference results.
    
    Parameters
    ----------
    fired_rules : List of rules that matched and fired
    active_facts : List of active facts from working memory
    
    Returns
    -------
    Dictionary with "why" and "how" explanation strings
    """
    
    # WHY Explanation - explains which facts triggered which rules
    why_lines = ["[STEP] WHY Explanation - Facts that triggered rules:\n"]
    
    if not active_facts:
        why_lines.append("[STEP] No active facts provided.")
    else:
        why_lines.append(f"[STEP] Active facts detected: {', '.join(active_facts)}\n")
    
    if not fired_rules:
        why_lines.append("[RESULT] No rules matched the given facts.")
    else:
        for rule in fired_rules:
            why_lines.append(f"[MATCH] Rule {rule.rule_id} ({rule.diagnosis}) matched because:")
            why_lines.append(f"  - Required conditions: {', '.join(rule.conditions)}")
            why_lines.append(f"  - Urgency: {rule.urgency.value}")
            why_lines.append(f"  - Confidence: {rule.confidence * 100:.1f}%\n")
    
    # HOW Explanation - explains the reasoning process
    how_lines = ["[STEP] HOW Explanation - Reasoning process:\n"]
    
    how_lines.append("[STEP] 1. Pattern Matching Phase:")
    how_lines.append(f"  - Evaluated all rules against {len(active_facts)} active facts")
    how_lines.append(f"  - Found {len(fired_rules)} matching rule(s)\n")
    
    if fired_rules:
        how_lines.append("[STEP] 2. Conflict Resolution Phase:")
        how_lines.append("  - Strategy: Urgency-first, then confidence")
        
        # Group by urgency
        urgency_groups = {}
        for rule in fired_rules:
            urgency = rule.urgency.value
            if urgency not in urgency_groups:
                urgency_groups[urgency] = []
            urgency_groups[urgency].append(rule)
        
        for urgency, rules in urgency_groups.items():
            how_lines.append(f"  - {urgency.upper()}: {len(rules)} rule(s)")
        
        how_lines.append("")
        how_lines.append("[STEP] 3. Primary Selection:")
        primary = fired_rules[0]
        how_lines.append(f"  - Selected: {primary.diagnosis}")
        how_lines.append(f"  - Urgency: {primary.urgency.value}")
        how_lines.append(f"  - Confidence: {primary.confidence * 100:.1f}%")
        how_lines.append(f"  - Action: {primary.action}\n")
        
        if len(fired_rules) > 1:
            how_lines.append("[STEP] 4. Alternative Diagnoses:")
            for alt in fired_rules[1:]:
                how_lines.append(f"  - {alt.diagnosis} ({alt.urgency.value}, {alt.confidence * 100:.1f}%)")
    else:
        how_lines.append("[RESULT] No diagnosis could be determined from the given facts.")
    
    return {
        "why": "\n".join(why_lines),
        "how": "\n".join(how_lines)
    }
