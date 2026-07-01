"""
Hybrid Lead Extraction

Uses:
- GPT-4.1 Mini for semantic extraction
- Regex for phone number extraction
"""

import re
from typing import Optional

from pydantic import BaseModel, Field
from langchain_core.prompts import ChatPromptTemplate

from backend.app.rag import get_llm


# =====================================================
# Phone Extraction
# =====================================================

PHONE_REGEX = re.compile(
    r"(?:\+91[- ]?)?[6-9]\d{9}"
)


def extract_phone(message: str) -> Optional[str]:

    match = PHONE_REGEX.search(message)

    if not match:
        return None

    phone = re.sub(r"\D", "", match.group())

    if len(phone) > 10:
        phone = phone[-10:]

    return phone


# =====================================================
# Structured Output
# =====================================================

class LeadExtraction(BaseModel):

    is_lead: bool = Field(
        description=(
            "True if the user is genuinely interested in "
            "buying, investing, pricing, site visit, booking, "
            "or talking to sales."
        )
    )

    name: Optional[str] = Field(
        default=None,
        description=(
            "User's personal name ONLY IF explicitly introduced."
        )
    )

    requirement: Optional[str] = Field(
        default=None,
        description=(
            "Property/project/location/budget requirement."
        )
    )


# =====================================================
# Prompt
# =====================================================

PROMPT = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
You are an information extraction assistant.

Extract ONLY structured information.

Rules:

1. Detect buying intent.

2. Extract a name ONLY if the user explicitly says:

- My name is ...
- I am ...
- I'm ...
- This is ...

Never guess names.

Never treat greetings like

hi
hello
hey
thanks
okay
yes
no
sure
fine
i already did

as names.

Never infer a standalone word is a person's name.

3. Extract project names, locations,
property types or budgets mentioned by the user.

Examples:

"Paradise Dream City"

"Nirvana Homes"

"Greater Noida"

"Haridwar"

"Industrial Plot"

"30 lakh budget"

Return only structured information.
""",
        ),
        (
            "human",
            "{message}",
        ),
    ]
)


# =====================================================
# Chain
# =====================================================

_llm = get_llm().with_structured_output(
    LeadExtraction
)

_chain = PROMPT | _llm


# =====================================================
# Main Extraction
# =====================================================

def extract_lead(message: str) -> dict:

    phone = extract_phone(message)

    try:

        result = _chain.invoke(
            {
                "message": message,
            }
        )

        return {

            "is_lead": result.is_lead,

            "name": result.name,

            "phone": phone,

            "requirement": result.requirement,

        }

    except Exception:

        return {

            "is_lead": False,

            "name": None,

            "phone": phone,

            "requirement": None,

        }