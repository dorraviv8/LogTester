import re
from typing import List, Tuple, Literal

ErrorType = Literal["python", "java", "jenkins", "unknown"]


PY_PATTERNS = [
    re.compile(r"Traceback \(most recent call last\):", re.IGNORECASE),
    re.compile(r"\b(ModuleNotFoundError|ImportError|ValueError|TypeError|KeyError|AttributeError)\b"),
]

JAVA_PATTERNS = [
    re.compile(r"\bException in thread\b"),
    re.compile(r"\b(Caused by:)\b"),
    re.compile(r"\b(NullPointerException|ClassNotFoundException|NoSuchMethodError|OutOfMemoryError)\b"),
]

JENKINS_PATTERNS = [
    re.compile(r"\bFinished: FAILURE\b"),
    re.compile(r"\bscript returned exit code\b", re.IGNORECASE),
    re.compile(r"\bERROR:?\b"),
]


def _extract_error_lines(log_text: str, max_lines: int = 25) -> List[str]:
    lines = [ln.rstrip() for ln in log_text.splitlines()]
    candidates = []

    keywords = ("error", "exception", "traceback", "failed", "failure", "caused by", "exit code")
    for ln in lines:
        low = ln.lower()
        if any(k in low for k in keywords):
            candidates.append(ln)

    # keep order, unique
    seen = set()
    uniq = []
    for ln in candidates:
        if ln not in seen:
            uniq.append(ln)
            seen.add(ln)

    return uniq[:max_lines]


def _detect_type(log_text: str) -> ErrorType:
    if any(p.search(log_text) for p in PY_PATTERNS):
        return "python"
    if any(p.search(log_text) for p in JAVA_PATTERNS):
        return "java"
    if any(p.search(log_text) for p in JENKINS_PATTERNS):
        return "jenkins"
    return "unknown"


def analyze_log(log_text: str, source_hint: str = "unknown") -> Tuple[ErrorType, str, str, List[str], float, List[str]]:
    extracted = _extract_error_lines(log_text)

    detected = _detect_type(log_text)
    if source_hint in ("python", "java", "jenkins") and detected == "unknown":
        detected = source_hint  # weak hint usage

    if detected == "python":
        summary = "Detected a Python error/exception pattern in the log."
        cause = "Likely an exception raised during runtime (check traceback and the final exception line)."
        fixes = [
            "Locate the last exception line in the traceback and identify the failing module/function.",
            "If it's an import/module error, verify dependencies are installed and the correct venv/image is used.",
            "If it's a type/value error, validate inputs and add guards + logging around the failing line.",
        ]
        conf = 0.78

    elif detected == "java":
        summary = "Detected a Java exception pattern in the log."
        cause = "Likely a runtime exception (inspect 'Caused by' chain to find the root cause)."
        fixes = [
            "Search for 'Caused by:' and take the deepest cause as the likely root cause.",
            "Check classpath/dependencies if it’s ClassNotFoundException/NoSuchMethodError.",
            "If NullPointerException, identify the null object and add validations or initialize properly.",
        ]
        conf = 0.78

    elif detected == "jenkins":
        summary = "Detected a Jenkins pipeline/build failure pattern in the log."
        cause = "A pipeline stage likely returned a non-zero exit code or a step failed."
        fixes = [
            "Find the failing stage and the command that returned a non-zero exit code.",
            "Re-run locally with the same env vars/tools to reproduce (or run with 'set -x' for shell steps).",
            "Check credentials/secrets, workspace paths, and Docker/K8s connectivity if relevant.",
        ]
        conf = 0.75

    else:
        summary = "Could not confidently classify the log source."
        cause = "The log may not contain a clear exception/failure signature."
        fixes = [
            "Paste a larger section including the failure moment (a few lines before/after the error).",
            "Include the stacktrace/exit code line if available.",
            "Provide a hint for source (python/java/jenkins) to improve classification.",
        ]
        conf = 0.35

    return detected, summary, cause, fixes, conf, extracted

