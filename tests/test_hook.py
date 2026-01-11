"""Tests for explanatory hook module."""

import pytest

from amplifier_hooks_explanatory.main import (
    EXPLANATORY_CONTEXT,
    explanatory_hook,
)


@pytest.mark.asyncio
async def test_injects_on_session_start():
    """Should inject context on session:start event."""
    result = await explanatory_hook("session:start", {"session_id": "test-123"})

    assert result.action == "inject_context"
    assert "★ Insight" in result.context_injection
    assert result.context_injection_role == "system"
    assert result.ephemeral is False
    assert result.user_message == "Explanatory output style enabled"
    assert result.user_message_level == "info"


@pytest.mark.asyncio
async def test_continues_on_other_events():
    """Should pass through on non-session:start events."""
    events = ["tool:pre", "tool:post", "provider:request", "prompt:submit"]

    for event in events:
        result = await explanatory_hook(event, {})
        assert result.action == "continue"


@pytest.mark.asyncio
async def test_context_content():
    """Context should match expected format."""
    result = await explanatory_hook("session:start", {})

    assert "explanatory" in result.context_injection.lower()
    assert "educational" in result.context_injection.lower()
    assert "★ Insight" in result.context_injection
    assert "<style-guide" in result.context_injection


@pytest.mark.asyncio
async def test_context_is_complete():
    """Ensure context injection equals the full EXPLANATORY_CONTEXT."""
    result = await explanatory_hook("session:start", {})
    assert result.context_injection == EXPLANATORY_CONTEXT
