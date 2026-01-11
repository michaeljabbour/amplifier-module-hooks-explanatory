# amplifier-module-hooks-explanatory

Amplifier hook module that injects explanatory/educational output style instructions at session start.

## Origin

This module is a port of the [Claude Code explanatory-output-style plugin](https://github.com/anthropics/claude-code-plugins) by Dickson Tsai (Anthropic).

## What it Does

At session start, this hook injects instructions that encourage the model to:

1. Provide educational insights as it works
2. Use `★ Insight` blocks to explain WHY something works
3. Share patterns, best practices, and mental models
4. Connect tasks to broader concepts

## Installation

```bash
# From source
pip install git+https://github.com/microsoft/amplifier-module-hooks-explanatory@main

# Local development
pip install -e ~/dev/amplifier-module-hooks-explanatory
```

## Bundle Configuration

Add to your bundle YAML:

```yaml
hooks:
  - module: hooks-explanatory
    source: git+https://github.com/microsoft/amplifier-module-hooks-explanatory@main
```

Or for local development:

```yaml
hooks:
  - module: hooks-explanatory
    source: file:///Users/you/dev/amplifier-module-hooks-explanatory
```

## Example Output

When enabled, the model will include blocks like:

```
★ Insight ─────────────────────────────────────
This pattern uses dependency injection to decouple the
service from its concrete implementation, making testing
easier and allowing runtime configuration.
─────────────────────────────────────────────────
```

## Development

```bash
cd ~/dev/amplifier-module-hooks-explanatory

# Install in development mode
pip install -e .

# Run tests
pytest tests/
```

## License

MIT
