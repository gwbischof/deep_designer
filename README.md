# Deep Designer

Transform ideas into implementation-ready design documents with human collaboration.

## Overview

Note that this project is very new and needs some work to sculpt it into a useful tool. Leave an Issue or PR if you have any ideas or suggestions for this project!

Deep Designer converts a human's product idea into a detailed design for use by coding agents. The system focuses on deep product design analysis and human-in-the-loop iterative refinement.

Deep Designer uses [Agno](https://docs.agno.com/introduction) for multi-agent orchestration, and [dotprompt](https://google.github.io/dotprompt/) for prompt templating. Deep Designer is also model agnostic.

## Agents

- **Manager**: Coordinates overall design process
- **Marketing**: Defines user personas and requirements
- **Architect**: Designs technical architecture
- **Designer**: Creates interface specifications

## Workflow

1. Read idea from IDEA.md
2. Agents analyze requirements through targeted questions
3. Human provides feedback at each iteration
4. Final document includes implementation tasks for coding agents

## Usage

```bash
# Run with default IDEA.md
pixi run dd

# Custom idea file
pixi run dd -i /path/to/IDEA.md
```

## Requirements

- Python 3.9+
- Agno
- OpenAI API key
