"""
Explanatory Output Style Hook for Amplifier.

This module injects educational style instructions at session start,
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

You should be clear and educational, providing helpful explanations while remaining focused on the task. Balance educational content with task completion. When providing insights, you may exceed typical length constraints, but remain focused and relevant.

### Insight Blocks

In order to encourage learning, before and after writing code, always provide brief educational explanations about implementation choices using this format:

```
★ Insight ─────────────────────────────────────
[2-3 key educational points about WHY something works, not just WHAT to do]
─────────────────────────────────────────────────
```

Guidelines for insights:
- Include them in the conversation, not in the codebase
- Focus on insights specific to the codebase or code you just wrote
- Share relevant patterns, best practices, or mental models
- Connect the current task to broader concepts
- Do not wait until the end - provide them as you write code
- Keep insights concise and directly relevant to current context
</style-guide>"""


async def explanatory_hook(event: str, data: dict[str, Any]) -> HookResult:
    """
    Inject explanatory style context at session start.

    Args:
        event: The event name (we only care about "session:start")
        data: Event data (session_id, config, etc.)

    Returns:
        HookResult with context injection for session:start,
        otherwise continue normally.
    """
    # Only inject on session start
    if event != "session:start":
        return HookResult(action="continue")

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
    Registers our hook handler for session:start events.

    Args:
        coordinator: The ModuleCoordinator for registration
        config: Module configuration from bundle

    Returns:
        Cleanup function to unregister hook on shutdown
    """
    handlers = []

    # Register our handler with the hook registry
    handlers.append(
        coordinator.hooks.register(
            event="session:start",
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
