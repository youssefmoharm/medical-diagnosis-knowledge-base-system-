from dataclasses import dataclass
from typing import List
from knowledge_base import Rule, Urgency, RULES
from working_memory import WorkingMemory


@dataclass
class FiredRule:
    """Represents a rule that matched the current facts."""
    rule     : Rule
    is_primary: bool = False   # set to True for the top-ranked result

    # Convenience pass-throughs
    @property
    def rule_id(self)   -> str:     return self.rule.rule_id
    @property
    def diagnosis(self) -> str:     return self.rule.diagnosis
    @property
    def urgency(self)   -> Urgency: return self.rule.urgency
    @property
    def action(self)    -> str:     return self.rule.action
    @property
    def confidence(self)-> float:   return self.rule.confidence
    @property
    def conditions(self)-> list:    return self.rule.conditions


def infer(rules: List[Rule], memory: WorkingMemory) -> List[FiredRule]:
    """
    Evaluate all rules against *memory* and return ranked FiredRule list.

    Parameters
    ----------
    rules  : Full rule set (typically ``RULES`` from knowledge_base).
    memory : Populated WorkingMemory for the current session.

    Returns
    -------
    List[FiredRule] ranked by (urgency DESC, confidence DESC).
    The first element is the primary result; all others are alternatives.
    Returns an empty list when no rule fires.
    """
    #Step 1: Forward chaining – collect conflict set 
    conflict_set: List[FiredRule] = [
        FiredRule(rule=rule)
        for rule in rules
        if rule.matches(memory.facts)
    ]

    if not conflict_set:
        return []

    #Step 2: Conflict resolution
    # Primary key  : urgency rank (descending)
    # Secondary key: confidence (descending)
    conflict_set.sort(
        key=lambda fr: (fr.urgency.rank(), fr.confidence),
        reverse=True,
    )

    # Mark the winner
    conflict_set[0].is_primary = True

    return conflict_set


def run_triage(
    symptoms     : dict,
    heart_rate   : int  = None,
    oxygen_level : int  = None,
    background   : dict = None,
) -> List[FiredRule]:
    """
    Convenience wrapper: builds WorkingMemory, runs inference, returns results.

    Parameters
    ----------
    symptoms     : {UI label: bool} — e.g. {"Fever": True, "Cough": True}
    heart_rate   : int beats/min (optional)
    oxygen_level : int SpO₂ % (optional)
    background   : {UI label: bool} — chronic conditions / history flags

    Returns
    -------
    Ranked list of FiredRule objects (may be empty).

    Raises
    ------
    ValueError if numeric inputs are out of plausible range.
    """
    memory = WorkingMemory()
    memory.load(
        symptoms     = symptoms or {},
        heart_rate   = heart_rate,
        oxygen_level = oxygen_level,
        background   = background or {},
    )
    return infer(RULES, memory)
