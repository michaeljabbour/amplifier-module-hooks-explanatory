"""
Explanatory Output Style Hook for Amplifier.

This module injects educational style instructions at prompt submit,
encouraging the model to provide Insight blocks with implementation
explanations.

Ported from: Claude Code explanatory-output-style plugin
Original author: Dickson Tsai (Anthropic)
"""

from typing import Any, Callable

from amplifier_core.models import HookResult

# The prompt content - educational style instructions
EXPLANATORY_CONTEXT = """<style-guide source="hooks-explanatory">
## Output Style: Explanatory Mode

You are in 'explanatory' output style mode, where you should provide educational insights about the codebase as you help with the user's task.

You should be clear and educational, providing helpful explanations while remaining focused on the task. Balance educational content with task completion.

### Insight Blocks

Before and after writing code or explaining concepts, provide brief educational insights using a blockquote with the ★ Insight header. Format exactly like this:

> **★ Insight**
>
> - First key educational point about WHY something works
> - Second point connecting to broader concepts or patterns
> - Third point with practical implications or best practices

Guidelines for insights:
- Use blockquote format (> prefix) so they render with a background/border
- Include them in the conversation, not in the codebase
- Focus on insights specific to the codebase or code you just wrote
- Share relevant patterns, best practices, or mental models
- Do not wait until the end - provide them as you write code
- Keep insights concise (2-4 bullet points) and directly relevant
</style-guide>"""

# Track if we've already injected this session
_injected_sessions: set[str] = set()


async def explanatory_hook(event: str, data: dict[str, Any]) -> HookResult:
    """
    Inject explanatory style context on first prompt of a session.

    Args:
        event: The event name (we use "prompt:submit")
        data: Event data (prompt, session_id, etc.)

    Returns:
        HookResult with context injection for first prompt,
        otherwise continue normally.
    """
    # Only inject on prompt:submit
    if event != "prompt:submit":
        return HookResult(action="continue")

    # Only inject once per session
    session_id = data.get("session_id", "default")
    if session_id in _injected_sessions:
        return HookResult(action="continue")
    
    _injected_sessions.add(session_id)

    return HookResult(
        action="inject_context",
        context_injection=EXPLANATORY_CONTEXT,
        context_injection_role="system",
        ephemeral=False,  # Persist in context across turns
        user_message="Explanatory output style enabled",
        user_message_level="info",
    )


async def mount(coordinator: Any, config: dict[str, Any]) -> Callable[[], None] | None:
    """
    Mount the explanatory hook module.

    Called by Amplifier kernel during session initialization.
    Registers our hook handler for prompt:submit events.

    Args:
        coordinator: The ModuleCoordinator for registration
        config: Module configuration from bundle

    Returns:
        Cleanup function to unregister hook on shutdown
    """
    handlers = []

    # Register our handler for prompt:submit
    handlers.append(
        coordinator.hooks.register(
            event="prompt:submit",
            handler=explanatory_hook,
            priority=100,  # Low priority (runs after security hooks)
            name="explanatory-style-injection",
        )
    )

    # Return cleanup function
    def cleanup() -> None:
        for unregister in handlers:
            unregister()

    return cleanup
