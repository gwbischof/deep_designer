# Deep Designer Models
# Models for structured output generation with Agno

from typing import Dict, List, Any
from pydantic import BaseModel, Field


# Idea Models
class Problem(BaseModel):
    description: str = Field(
        ..., description="A description of the problem being addressed."
    )
    example: str = Field(
        ..., description="A concrete example illustrating the problem."
    )


class Solution(BaseModel):
    summary: str = Field(
        ..., description="A high-level summary of the solution to the problem."
    )
    challenges: List[str] = Field(
        ..., description="List of challenges to making this a successful product."
    )
    requirements: str = Field(
        ...,
        description="High-level description about what this product must do to overcome the challenges.",
    )


class Features(BaseModel):
    core_features: List[str] = Field(
        ..., description="Essential features needed for the minimum viable product."
    )
    optional_features: List[str] = Field(
        ..., description="Additional features that could be added in future versions."
    )


class IdeaDocument(BaseModel):
    problem: Problem = Field(..., description="Problem definition section.")
    solution: Solution = Field(..., description="Solution overview section.")
    audience: str = Field(
        ..., description="Description of the target audience for this product."
    )
    features: Features = Field(
        ..., description="Core and optional features of the product."
    )
    business_model: str = Field(
        ..., description="High-level description of the business model."
    )
    marketing: List[str] = Field(
        ..., description="List of potential marketing strategies."
    )


# Marketing Models
class UserPersona(BaseModel):
    name: str = Field(..., description="Name or identifier for this persona.")
    role: str = Field(..., description="Professional role or position.")
    age: int = Field(..., description="Age of the typical user in this persona.")
    technical_level: str = Field(
        ..., description="Technical proficiency level (e.g., 'High', 'Medium', 'Low')."
    )
    background: str = Field(
        ..., description="Professional and personal background details."
    )
    goals: List[str] = Field(
        ..., description="Primary goals and motivations of this user persona."
    )
    pain_points: List[str] = Field(
        ..., description="Challenges and difficulties faced by this user persona."
    )
    usage_scenario: str = Field(
        ...,
        description="Detailed scenario describing how this persona would use the product.",
    )


class MarketAnalysis(BaseModel):
    target_audience_overview: str = Field(
        ...,
        description="Overview of the target audience demographics and characteristics.",
    )
    market_size_potential: str = Field(
        ..., description="Estimation of market size and growth potential."
    )
    key_competitors: List[str] = Field(
        ..., description="Main competitors and product differentiators."
    )


class UserRequirement(BaseModel):
    description: str = Field(..., description="Description of the requirement.")
    type: str = Field(
        ..., description="Type of requirement (functional or non-functional)."
    )
    priority: str = Field(
        ..., description="Priority level (e.g., 'High', 'Medium', 'Low')."
    )


class MarketingDocument(BaseModel):
    market_analysis: MarketAnalysis = Field(
        ..., description="Analysis of the target market and competitive landscape."
    )
    user_personas: List[UserPersona] = Field(
        ..., description="Detailed representations of target users."
    )
    user_requirements: List[UserRequirement] = Field(
        ..., description="User requirements derived from personas."
    )


# Architecture Models
class TechnicalRequirement(BaseModel):
    name: str = Field(..., description="Name of the technical requirement.")
    description: str = Field(
        ..., description="Detailed description of the requirement."
    )


class TechnologyImplementation(BaseModel):
    technologies: List[str] = Field(
        ..., description="Specific technologies with version requirements."
    )
    component_interactions: str = Field(
        ..., description="How components interact with each other."
    )
    data_requirements: str = Field(
        ..., description="Data requirements for this feature."
    )


class CoreFeatureImplementation(BaseModel):
    name: str = Field(..., description="Name of the core feature.")
    description: str = Field(..., description="Brief description of the feature.")
    detailed_requirements: List[str] = Field(
        ..., description="Detailed technical requirements."
    )
    implementation_approach: str = Field(
        ..., description="Approach to implementing this feature."
    )
    technical_considerations: str = Field(
        ..., description="Technical considerations for implementation."
    )
    technology_implementation: TechnologyImplementation = Field(
        ..., description="Specific technology implementation details."
    )


class OptionalFeatureImplementation(BaseModel):
    name: str = Field(..., description="Name of the optional feature.")
    technical_approach: str = Field(
        ..., description="Technical approach to implementing this feature."
    )
    integration_with_mvp: str = Field(
        ..., description="How this integrates with MVP components."
    )
    additional_requirements: List[str] = Field(
        ..., description="Additional technology requirements."
    )


class SystemOverview(BaseModel):
    purpose: str = Field(..., description="System purpose and high-level design.")
    key_constraints: List[str] = Field(
        ..., description="Key constraints and considerations."
    )
    architecture_pattern: str = Field(
        ..., description="Overall architecture pattern (microservices, monolith, etc.)."
    )


class TechnologyStack(BaseModel):
    frontend: List[str] = Field(
        ..., description="Frontend technologies (frameworks, libraries)."
    )
    backend: List[str] = Field(
        ..., description="Backend technologies (languages, frameworks)."
    )
    database: str = Field(
        ..., description="Database recommendations (type, schema overview)."
    )
    infrastructure: List[str] = Field(
        ..., description="Infrastructure (cloud services, deployment)."
    )
    third_party: List[str] = Field(..., description="Third-party services and APIs.")


class SystemArchitecture(BaseModel):
    components: str = Field(
        ..., description="Component descriptions showing relationships."
    )
    data_flow: str = Field(..., description="Data flow between components.")
    api_specifications: str = Field(
        ..., description="API specifications and integration points."
    )
    auth_approach: str = Field(
        ..., description="Authentication and authorization approach."
    )


class SecurityPerformance(BaseModel):
    security_details: str = Field(..., description="Security implementation details.")
    performance_strategies: List[str] = Field(
        ..., description="Performance optimization strategies."
    )
    scalability: str = Field(..., description="Scalability considerations.")
    monitoring: str = Field(..., description="Monitoring and observability approach.")


class TechnicalConsiderations(BaseModel):
    risks: List[str] = Field(..., description="Implementation risks and mitigations.")
    scalability_concerns: str = Field(..., description="Scalability concerns.")
    development_workflow: str = Field(
        ..., description="Development and deployment workflow."
    )
    testing_strategy: str = Field(..., description="Testing strategy.")


class ArchitectureDocument(BaseModel):
    technical_requirements: List[TechnicalRequirement] = Field(
        ..., description="Core technologies and infrastructure needed."
    )
    core_features: List[CoreFeatureImplementation] = Field(
        ..., description="Technical implementation of core features."
    )
    optional_features: List[OptionalFeatureImplementation] = Field(
        ..., description="Technical implementation of optional features."
    )
    system_overview: SystemOverview = Field(
        ..., description="System purpose and high-level design."
    )
    technology_stack: TechnologyStack = Field(
        ..., description="Technology stack specifications."
    )
    system_architecture: SystemArchitecture = Field(
        ..., description="Detailed system architecture."
    )
    security_performance: SecurityPerformance = Field(
        ..., description="Security and performance details."
    )
    technical_considerations: TechnicalConsiderations = Field(
        ..., description="Additional technical considerations."
    )


# Design Models
class UIComponent(BaseModel):
    name: str = Field(..., description="Name of the UI component.")
    variants: List[str] = Field(
        ..., description="Different variants or types of this component."
    )


class ScreenDefinition(BaseModel):
    name: str = Field(..., description="Name of the screen or page.")
    path: str = Field(..., description="URL path to the screen.")
    purpose: str = Field(..., description="Primary purpose or function of this screen.")
    components: List[str] = Field(..., description="UI components used in this screen.")
    user_interactions: List[str] = Field(
        ..., description="User interactions supported on this screen."
    )
    mockup_description: str = Field(
        ..., description="Detailed description of the screen's visual design."
    )


class UserFlow(BaseModel):
    name: str = Field(..., description="Name of the user flow.")
    steps: List[str] = Field(..., description="Steps involved in this user flow.")


class Typography(BaseModel):
    primary_font: str = Field(
        ..., description="Primary font family for the application."
    )
    code_font: str = Field(..., description="Font used for code displays.")
    heading_sizes: Dict[str, str] = Field(
        ..., description="Font sizes for different heading levels."
    )
    body_text: str = Field(..., description="Font size for body text.")


class DesignDocument(BaseModel):
    design_principles: List[str] = Field(
        ..., description="Core design principles guiding the UI/UX."
    )
    color_palette: Dict[str, str] = Field(
        ..., description="Color scheme with hex values."
    )
    typography: Typography = Field(..., description="Typography specifications.")
    components: List[UIComponent] = Field(..., description="UI component definitions.")
    screens: List[ScreenDefinition] = Field(
        ..., description="Screen/page definitions with details."
    )
    user_flows: List[UserFlow] = Field(..., description="User flow definitions.")
    accessibility_considerations: List[str] = Field(
        ..., description="Accessibility requirements and implementations."
    )
    responsive_breakpoints: Dict[str, str] = Field(
        ..., description="Responsive design breakpoints."
    )
    animations_and_transitions: List[str] = Field(
        ..., description="Animation and transition specifications."
    )


# Complete Design Document
class CompleteDesignDocument(BaseModel):
    idea: IdeaDocument = Field(..., description="Product idea and concept.")
    marketing: MarketingDocument = Field(
        ..., description="Marketing strategy and user personas."
    )
    architecture: ArchitectureDocument = Field(
        ..., description="Technical architecture and system design."
    )
    design: DesignDocument = Field(..., description="UI/UX design specifications.")
    tasks: Dict[str, Any] = Field(
        default={}, description="Implementation tasks and status."
    )
