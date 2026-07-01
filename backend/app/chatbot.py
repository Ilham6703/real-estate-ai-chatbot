"""
Main chatbot orchestration logic.
"""

import logging
import re

from backend.app.guardrails import validate_message
from backend.app.lead_capture import extract_lead
from backend.app.memory import (
    get_history,
    add_message,
    get_lead,
    update_lead,
    mark_saved,
)
from backend.app.rag import (
    retrieve_context,
    generate_response,
)
from backend.app.sheets import save_lead

logger = logging.getLogger(__name__)


PHONE_REGEX = re.compile(r"(?:\+91[- ]?)?[6-9]\d{9}")


def process_chat(
    session_id: str,
    message: str,
) -> str:

    message = message.strip()

    # =====================================================
    # Guardrails
    # =====================================================

    is_valid, response = validate_message(message)

    if not is_valid:
        return response

    try:

        history = get_history(session_id)

        lead = get_lead(session_id)

        # =====================================================
        # Waiting for Name
        # =====================================================

        if lead["awaiting_name"]:

            if (
                len(message.split()) <= 3
                and message.replace(" ", "").isalpha()
            ):

                update_lead(
                    session_id=session_id,
                    name=message.title(),
                )

                add_message(
                    session_id,
                    "user",
                    message,
                )

                response = (
                    f"Thank you, {message.title()}."
                    "\n\nCould you please share your mobile number?"
                )

                add_message(
                    session_id,
                    "assistant",
                    response,
                )

                return response

        # =====================================================
        # Waiting for Phone
        # =====================================================

        if lead["awaiting_phone"]:

            match = PHONE_REGEX.search(message)

            if match:

                phone = re.sub(
                    r"\D",
                    "",
                    match.group(),
                )[-10:]

                update_lead(
                    session_id=session_id,
                    phone=phone,
                )

                lead = get_lead(session_id)

                saved = save_lead(
                    name=lead["name"],
                    phone=lead["phone"],
                    requirement=lead["requirement"] or "General Inquiry",
                )

                if saved:

                    mark_saved(session_id)

                    add_message(
                        session_id,
                        "user",
                        message,
                    )

                    response = (
                        "✅ Thank you!"
                        "\n\nYour details have been shared with our sales team."
                        "\nOur property expert will contact you shortly."
                    )

                    add_message(
                        session_id,
                        "assistant",
                        response,
                    )

                    return response

                return (
                    "Unable to save your details at the moment."
                )

        # =====================================================
        # Lead Extraction
        # =====================================================

        extracted = extract_lead(message)

        update_lead(
            session_id=session_id,
            name=extracted["name"],
            phone=extracted["phone"],
            requirement=extracted["requirement"],
            interested=extracted["is_lead"],
        )

        lead = get_lead(session_id)

        # =====================================================
        # RAG
        # =====================================================

        documents = retrieve_context(message)

        response = generate_response(
            question=message,
            documents=documents,
            history=history,
        )

        # =====================================================
        # Lead Collection
        # =====================================================

        if lead["interested"]:

            if not lead["name"]:

                lead["awaiting_name"] = True

                response += (
                    "\n\nGreat! I'd be happy to help you."
                    "\n\nTo connect you with one of our property experts,"
                    "\ncould you please share your name?"
                )

            elif not lead["phone"]:

                lead["awaiting_phone"] = True

                response += (
                    "\n\nCould you also share your mobile number?"
                )

        # =====================================================
        # Save Chat
        # =====================================================

        add_message(
            session_id,
            "user",
            message,
        )

        add_message(
            session_id,
            "assistant",
            response,
        )

        return response

    except Exception:

        logger.exception(
            "Chatbot processing failed."
        )

        return (
            "I'm sorry, something went wrong."
            "\nPlease try again."
        )