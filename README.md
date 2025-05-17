# Deep Designer

Transform ideas into implementation-ready design documents with human collaboration.

## Overview

Deep Designer converts a product idea (described in IDEA.md) into a comprehensive design document for use by coding agents. The system focuses on in-depth product design analysis and human-in-the-loop iterative refinement.

Deep Designer uses [Agno](https://docs.agno.com/introduction) for AI agent orchestration and is optimized to work with Anthropic's Claude models.

## Features

- **Structured Output**: Uses Pydantic models to generate well-structured design documents
- **Interactive Feedback**: Asks clarifying questions to improve the design
- **Comprehensive Design**: Covers product idea, marketing, technical architecture, and UI/UX design

## TODO
- Support for Image input, see: https://docs.agno.com/agents/multimodal
- Improve the prompt and output models.
- Use [Memory](https://docs.agno.com/agents/memory) to allow pausing and resuming of the design process.
- Figure out if it would be helpful to add or [Knowledge](https://docs.agno.com/agents/knowledge) 
- Generate tasks for coding agents from the design document, similar to [claude-task-master](https://github.com/eyaltoledano/claude-task-master).
- Better docs.
- Try with deepseek reasoning models to reduce cost.
- I'm not sure if an MCP makes sense for this project, because there is a lot of human-in-the-loop to get from the Idea document to the Design document. If we add the feature to generate tasks, then you can just tell your coding agent to work through the tasks file.
- Load information with Context7 or Perplexity about the technologies used to help inform design.
- Collaborative editing with Agent.
- Improve the UI. Agno `cli_app` doesn't work with the `ask_customer` tool, and it doesn't really do HITL.

## Structure

The design document covers four main sections:

1. **Idea**: Problem definition, solution overview, audience, core and optional features
2. **Marketing**: User personas, market analysis, and user requirements
3. **Architecture**: Technical requirements, system design, technology stack
4. **Design**: UI components, screens, user flows, and visual specifications

## Usage

```bash
# Install dependencies
pixi install

# Run with default IDEA.md in the project root
pixi run dd

# Validate DESIGN.json structure
pixi run validate
```

## Requirements

- Python 3.13+
- Agno 1.4.3+
- Anthropic API key

## Getting Started

1. Create an IDEA.md file in the project root with your product idea
2. Run `pixi run dd` to generate a design document
3. Answer the agent's questions to refine the design
4. The final design will be saved in DESIGN.json

## Idea Document Schema
```
# Idea document

## Problem

- A description of the problem.
- An example of the problem.

## Solution

- A high level summary of the solution to the problem.
- A list of challenges to making this a successful product.
- A high level description about what this product must do to overcome the challenges.

## Audience

- A high level description about who the target audience is.

## Features

- **Core features**
    - A list of descriptions of core features.
- **Optional features**
    - A list of descriptions of optional features.

## Business Model

- A high level description of what the business model is.

## Marketing

- A list of marketing strategies.
```
