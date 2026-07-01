"""
Conversation memory and lead state management.
"""

from collections import defaultdict

# =====================================================
# Chat History
# =====================================================

MAX_HISTORY = 10

_chat_memory = defaultdict(list)

# =====================================================
# Lead Memory
# =====================================================

_lead_memory = defaultdict(
    lambda: {
        "interested": False,
        "name": None,
        "phone": None,
        "requirement": None,
        "saved": False,

        # Conversation State
        "awaiting_name": False,
        "awaiting_phone": False,
    }
)


# =====================================================
# Chat History
# =====================================================

def get_history(session_id: str):
    return _chat_memory[session_id]


def add_message(
    session_id: str,
    role: str,
    content: str,
):

    history = _chat_memory[session_id]

    history.append(
        {
            "role": role,
            "content": content,
        }
    )

    if len(history) > MAX_HISTORY:
        _chat_memory[session_id] = history[-MAX_HISTORY:]


def clear_history(session_id: str):

    _chat_memory.pop(session_id, None)


# =====================================================
# Lead State
# =====================================================

def get_lead(session_id: str):

    return _lead_memory[session_id]


def update_lead(
    session_id: str,
    name=None,
    phone=None,
    requirement=None,
    interested=None,
):

    lead = _lead_memory[session_id]

    # -----------------------------------------
    # Once interested always interested
    # -----------------------------------------

    if interested:
        lead["interested"] = True

    # -----------------------------------------
    # Update fields only if empty
    # -----------------------------------------

    if name and not lead["name"]:
        lead["name"] = name

    if phone and not lead["phone"]:
        lead["phone"] = phone

    if requirement and not lead["requirement"]:
        lead["requirement"] = requirement

    # -----------------------------------------
    # Conversation State
    # -----------------------------------------

    if lead["interested"]:

        lead["awaiting_name"] = lead["name"] is None
        lead["awaiting_phone"] = lead["phone"] is None

    return lead


# =====================================================
# Mark Lead Saved
# =====================================================

def mark_saved(session_id: str):

    lead = _lead_memory[session_id]

    lead["saved"] = True

    lead["awaiting_name"] = False
    lead["awaiting_phone"] = False


# =====================================================
# Clear Lead
# =====================================================

def clear_lead(session_id: str):

    _lead_memory.pop(session_id, None)