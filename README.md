# AI Agent - Autonomous Coding Assistant

This project implements a command-line interface (CLI) agent capable of autonomously analyzing, debugging, and executing code. It leverages Google's Gemini 2.5 Flash model as a reasoning engine to bridge natural language prompts with local file system operations.
The goal of this development is to deconstruct and replicate the architecture behind agentic AI tools (like OpenCode or Claude Code) to understand how Large Language Models interact with deterministic environments.

## Technical Highlights

- **LLM Integration:** Using the Google GenAI SDK and Google Gemini 2.5
- **Security Guardrails:** Implementation of strict path validation to sandbox the agent within specific working directories.
- **CLI Architecture:** Argument parsing using `argparse` to handle prompts and verbose logging flags.
- **Functional Design:** Application of functional programming principles to ensure stateless tool execution and clean data transformations.

## Target Environment

The agent is currently tested against a sample Calculator application (`/calculator`) to validate its ability to navigate file structures, identify syntax errors, and apply code fixes autonomously.
