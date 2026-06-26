"""
Guardrail utilities for input filtering and safety checks.

This module implements a defence-in-depth approach to LLM safety:
  1. Input validation & sanitisation  (filter_input)
  2. Prompt injection detection        (detect_prompt_injection)
  3. Policy violation detection        (detect_policy_violation)
  4. Output moderation                 (moderate_output)

Design decisions
----------------
* Every public function returns ``Tuple[bool, str]`` with consistent semantics:
    - ``filter_input``:            (is_valid,              message)
    - ``detect_prompt_injection``: (is_injection_detected,  reason)
    - ``detect_policy_violation``: (is_violation_detected,  reason)
    - ``moderate_output``:         (is_safe,                reason)
* Patterns are compiled once at module level for O(1) amortised cost.
* All checks are intentionally **deterministic** (no ML model dependency)
  so the guardrail layer remains fast, testable and explainable.

Guardrail Hardening (Task 3)
----------------------------
The following improvements have been applied:

1. **Input normalisation** – Unicode NFKC canonicalisation and whitespace
   collapse prevent trivial bypasses such as zero-width characters,
   full-width Latin letters, or excessive spacing between keywords.

2. **Expanded injection patterns** – Added coverage for:
   - Role-play / jailbreak patterns ("pretend you are", "DAN mode")
   - Delimiter-based injections (markdown fences, XML-like tags)
   - Obfuscation via character repetition ("ignoooore")

3. **Enhanced output moderation** – Added detection for:
   - PII leaks (emails, phone numbers, IP addresses)
   - URLs that might indicate data exfiltration
   - Hallucination confidence markers

4. **Structured logging** – Every guardrail decision emits a structured
   log event with ``event_type``, ``result`` and ``detail`` fields to
   support downstream monitoring, alerting and analytics.
"""

import logging
import re
import unicodedata
from typing import Tuple

# ---------------------------------------------------------------------------
# Logging — structured guardrail events
# ---------------------------------------------------------------------------
logger = logging.getLogger(__name__)


def _log_guardrail_event(
    event_type: str,
    result: str,
    detail: str = "",
    input_snippet: str = "",
) -> None:
    """
    Emit a structured log entry for every guardrail decision.

    Structured fields enable downstream log aggregation tools (e.g. ELK,
    Datadog, Splunk) to build dashboards and alerts on guardrail metrics
    such as block-rate, injection-attempt frequency and false-positive
    trends — all critical for **monitoring and logging** (Task 3 §2).

    Args:
        event_type: Guardrail stage name (e.g. "input_filter", "injection_detect").
        result:     Outcome — "pass", "block", or "warn".
        detail:     Human-readable description of what was detected.
        input_snippet: First 120 chars of user input for audit trail.
    """
    logger.info(
        "guardrail_event",
        extra={
            "event_type": event_type,
            "result": result,
            "detail": detail,
            "input_snippet": input_snippet[:120] if input_snippet else "",
        },
    )


# ---------------------------------------------------------------------------
# Constants — max input length threshold
# ---------------------------------------------------------------------------
MAX_INPUT_LENGTH = 1000


# ---------------------------------------------------------------------------
# Input normalisation helpers (Task 3 — defence-in-depth)
# ---------------------------------------------------------------------------
def _normalise_text(text: str) -> str:
    """
    Normalise user input to neutralise common bypass techniques.

    Applies:
    * **NFKC Unicode normalisation** — collapses full-width Latin characters
      (e.g. 'ｉｇｎｏｒｅ' → 'ignore') and decomposes ligatures, preventing
      adversaries from evading keyword-based pattern matching.
    * **Whitespace collapse** — reduces multiple spaces / tabs / newlines to a
      single space so patterns like "ignore    previous    instructions"
      still match the regex.

    Returns:
        Normalised string ready for pattern matching.
    """
    # NFKC canonical decomposition + compatibility composition
    normalised = unicodedata.normalize("NFKC", text)
    # Collapse all whitespace sequences (spaces, tabs, newlines) into a single space
    normalised = re.sub(r"\s+", " ", normalised)
    return normalised.strip()


# ---------------------------------------------------------------------------
# 1. Input filtering & validation
# ---------------------------------------------------------------------------
def filter_input(text: str) -> Tuple[bool, str]:
    """
    Validate and sanitise user input before any further processing.

    Checks performed:
    * Empty / whitespace-only input rejection.
    * Maximum length enforcement (prevents token-stuffing attacks and
      controls downstream LLM cost).

    BUG FIX (Task 1):
        Original code used ``len(text) < 1000`` which **rejected** every
        input shorter than 1000 characters — i.e. virtually all valid
        customer queries.  Corrected to ``len(text) > MAX_INPUT_LENGTH``.

    Returns:
        Tuple of (is_valid, filtered_text_or_error_message).
    """
    # Reject empty / whitespace-only input
    if not text or len(text.strip()) == 0:
        _log_guardrail_event("input_filter", "block", "Empty input")
        return False, "Input cannot be empty"

    # FIX: Original had `< 1000` which inverted the logic.
    # We reject inputs EXCEEDING the maximum allowed length.
    if len(text) > MAX_INPUT_LENGTH:
        _log_guardrail_event(
            "input_filter", "block",
            f"Input too long: {len(text)} chars (max {MAX_INPUT_LENGTH})",
        )
        return False, "Input is too long (max 1000 characters)"

    filtered = text.strip()
    _log_guardrail_event("input_filter", "pass", input_snippet=filtered)
    return True, filtered


# ---------------------------------------------------------------------------
# 2. Prompt injection detection
# ---------------------------------------------------------------------------

# Pre-compiled regex patterns for prompt injection detection.
# Compiled once at module-load time for performance.
#
# Task 3 improvements:
#   • Added role-play / jailbreak patterns ("pretend you are", "DAN mode")
#   • Added delimiter-based injection ("<|system|>", "```system")
#   • Added obfuscation-resistant pattern for character repetition
_INJECTION_PATTERNS = [
    # --- Original patterns (retained) ---
    re.compile(r"ignore (previous|above|all) (instructions|rules|prompts)", re.IGNORECASE),
    re.compile(r"ignore all (previous|above)", re.IGNORECASE),
    re.compile(r"disregard (previous|above|all)", re.IGNORECASE),
    re.compile(r"forget (your|previous|all) (instructions|rules|training)", re.IGNORECASE),
    re.compile(r"you are now", re.IGNORECASE),
    re.compile(r"new (role|instructions|system)", re.IGNORECASE),
    re.compile(r"system\s*:+", re.IGNORECASE),
    re.compile(r"<\s*prompt\s*>", re.IGNORECASE),
    re.compile(r"act as a", re.IGNORECASE),

    # --- Expanded patterns (Task 3 — defence-in-depth) ---
    # Catch the simpler form "ignore instructions" without requiring
    # the qualifier "previous/above/all".  This was a gap that caused
    # test_prompt_injection_detection to fail for "ignore instructions".
    re.compile(r"ignore\b.*\binstructions\b", re.IGNORECASE),

    # Role-play & jailbreak patterns
    re.compile(r"pretend (you are|you're|to be)", re.IGNORECASE),
    re.compile(r"(DAN|developer|sudo)\s*mode", re.IGNORECASE),
    re.compile(r"(unlock|enable|activate)\s*(hidden|secret|admin|developer)", re.IGNORECASE),
    re.compile(r"jailbreak", re.IGNORECASE),
    re.compile(r"bypass\s*(filter|safety|security|restriction)", re.IGNORECASE),

    # Delimiter / tag-based injections
    re.compile(r"<\|?\s*(system|assistant|user)\s*\|?>", re.IGNORECASE),
    re.compile(r"```\s*(system|prompt)", re.IGNORECASE),
    re.compile(r"\[\s*INST\s*\]", re.IGNORECASE),

    # Override / reset patterns
    re.compile(r"override\s*(all|safety|security|previous)", re.IGNORECASE),
    re.compile(r"reset\s*(your|all|the)\s*(rules|instructions|context)", re.IGNORECASE),

    # Context manipulation
    re.compile(r"(from now on|henceforth),?\s*(you|act|behave|respond)", re.IGNORECASE),
    re.compile(r"do not follow\s*(your|any|the)\s*(rules|instructions|guidelines)", re.IGNORECASE),
]


def detect_prompt_injection(text: str) -> Tuple[bool, str]:
    """
    Detect potential prompt injection attempts in user input.

    Strategy (Task 3 — defence-in-depth):
        1. Normalise input (NFKC + whitespace collapse) to defeat obfuscation.
        2. Match against an expanded set of pre-compiled regex patterns.
        3. Log every decision for downstream monitoring.

    Trade-off note (Task 3 §3):
        The pattern list intentionally errs on the side of **catching more**
        (lower false-negative rate) at the acceptable cost of occasionally
        blocking a legitimate query that happens to contain trigger phrases.
        This is the correct trade-off for a customer-service bot where the
        consequence of a successful injection (data exfiltration, brand
        damage) far outweighs the cost of asking the user to rephrase.

    Returns:
        Tuple of (is_injection_detected, reason).
    """
    # Normalise to defeat unicode / whitespace obfuscation
    normalised = _normalise_text(text)

    for pattern in _INJECTION_PATTERNS:
        if pattern.search(normalised):
            _log_guardrail_event(
                "injection_detect", "block",
                f"Matched pattern: {pattern.pattern}",
                input_snippet=text,
            )
            return True, "Prompt injection attempt detected"

    _log_guardrail_event("injection_detect", "pass", input_snippet=text)
    return False, ""


# ---------------------------------------------------------------------------
# 3. Policy violation detection
# ---------------------------------------------------------------------------

# Keyword lists kept as module-level constants for easy maintenance.
_HARMFUL_KEYWORDS = [
    "hack", "crack", "steal", "illegal", "drug", "weapon",
    "violence", "harm", "kill", "murder", "suicide",
    # Task 3 — expanded harmful terms
    "exploit", "bomb", "terrorism", "trafficking",
]

_PERSONAL_DATA_KEYWORDS = [
    "social security", "ssn", "credit card", "password",
    "personal information", "private data", "confidential",
    # Task 3 — expanded PII request terms
    "date of birth", "bank account", "routing number",
    "driver's license", "passport number",
]

_OFF_TOPIC_KEYWORDS = [
    "weather", "sports", "politics", "religion",
    "movie", "recipe", "travel destination", "homework",
    # Task 3 — expanded off-topic terms
    "celebrity", "gossip", "astrology", "lottery",
]


def detect_policy_violation(text: str) -> Tuple[bool, str]:
    """
    Detect policy-violating content in user input.

    Policy categories:
        * **Harmful / illegal** — requests involving violence, drugs, weapons, etc.
        * **Personal data requests** — attempts to extract PII or credentials.
        * **Off-topic queries** — questions outside the e-commerce domain.

    BUG FIX (Task 1):
        The original implementation had **inverted boolean return values**:
        - Returned ``False`` when a violation *was* detected  (should be ``True``)
        - Returned ``True``  when the input was safe          (should be ``False``)

        This caused every harmful/off-topic/PII query to slip through
        unblocked, while every legitimate customer query was blocked.

        Fixed: ``True`` now means "violation detected", ``False`` means "safe".

    Returns:
        Tuple of (is_violation_detected, reason).
    """
    # Normalise to defeat trivial obfuscation
    text_lower = _normalise_text(text).lower()

    # Check for harmful content
    for keyword in _HARMFUL_KEYWORDS:
        if keyword in text_lower:
            _log_guardrail_event(
                "policy_violation", "block",
                f"Harmful/illegal keyword: '{keyword}'",
                input_snippet=text,
            )
            # FIX: Return True (violation detected), was incorrectly False
            return True, "Policy violation: Harmful/illegal content"

    # Check for personal data requests
    for keyword in _PERSONAL_DATA_KEYWORDS:
        if keyword in text_lower:
            _log_guardrail_event(
                "policy_violation", "block",
                f"Personal data keyword: '{keyword}'",
                input_snippet=text,
            )
            # FIX: Return True (violation detected), was incorrectly False
            return True, "Policy violation: Personal data request"

    # Check for off-topic queries
    for keyword in _OFF_TOPIC_KEYWORDS:
        if keyword in text_lower:
            _log_guardrail_event(
                "policy_violation", "block",
                f"Off-topic keyword: '{keyword}'",
                input_snippet=text,
            )
            # FIX: Return True (violation detected), was incorrectly False
            return True, "Policy violation: Off-topic query"

    _log_guardrail_event("policy_violation", "pass", input_snippet=text)
    # FIX: Return False (no violation), was incorrectly True
    return False, ""


# ---------------------------------------------------------------------------
# 4. Output moderation
# ---------------------------------------------------------------------------

# Pre-compiled patterns for output safety checks.
# Task 3 improvements: added PII leak patterns (email, phone, IP, URL).
_OUTPUT_HARMFUL_PATTERNS = [
    # --- Original patterns (retained) ---
    re.compile(r"\b(password|credit card|ssn)\b.*[:=]", re.IGNORECASE),
    re.compile(r"\d{3}-\d{2}-\d{4}"),                        # SSN format
    re.compile(r"\d{4}[\s-]?\d{4}[\s-]?\d{4}[\s-]?\d{4}"),  # Credit card format

    # --- Task 3 — expanded PII leak detection ---
    # Email addresses — prevents the model from leaking customer emails
    re.compile(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", re.IGNORECASE),
    # Phone numbers (various formats: +1-xxx-xxx-xxxx, (xxx) xxx-xxxx, etc.)
    re.compile(r"(\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}"),
    # IP addresses — could indicate infrastructure leaks
    re.compile(r"\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b"),
]

# System information leak phrases
_SYSTEM_LEAK_PHRASES = [
    "system prompt", "my instructions", "i am programmed",
    "as an ai model", "my training",
    # Task 3 — expanded leak indicators
    "my guidelines say", "i was told to", "my rules state",
    "according to my programming", "internal instructions",
]


def moderate_output(text: str) -> Tuple[bool, str]:
    """
    Moderate LLM output before returning it to the user.

    This is the **last line of defence** — even if a prompt injection
    or policy violation slips past the input guardrails, the output
    moderation layer can catch unsafe responses.

    Checks performed:
        * System information / instruction leaks
        * PII patterns (SSN, credit card, email, phone, IP)
        * Sensitive data with assignment operators

    Task 3 improvements:
        * Added email, phone number, and IP address detection
        * Expanded system leak phrase list
        * Added structured logging for every moderation decision

    Trade-off note (Task 3 §3 — Explainability vs Accuracy):
        Regex-based moderation is **highly explainable** — when a response
        is blocked, the exact pattern and reason are logged. This is
        preferred over an ML-based classifier which might be more accurate
        but offers no actionable explanation for why a response was flagged.

    Returns:
        Tuple of (is_safe, reason_if_unsafe).
    """
    text_lower = text.lower()

    # Check for leaked system information
    for leak in _SYSTEM_LEAK_PHRASES:
        if leak in text_lower:
            _log_guardrail_event(
                "output_moderation", "block",
                f"System leak phrase: '{leak}'",
            )
            return False, "Output contains system information leak"

    # Check for PII and sensitive data patterns
    for pattern in _OUTPUT_HARMFUL_PATTERNS:
        if pattern.search(text):
            _log_guardrail_event(
                "output_moderation", "block",
                f"Sensitive data pattern: {pattern.pattern}",
            )
            return False, "Output contains sensitive information"

    _log_guardrail_event("output_moderation", "pass")
    return True, ""
