# UML Diagrams - Health Research Agentic System

This directory contains PlantUML diagrams for the updated system architecture.

## Files

### 1. `component_diagram.puml`
**Component-level architecture diagram** showing:
- System layers (Presentation, Application, Orchestration, Worker Agents, Data)
- NEW: System Controller layer between UI and Orchestrator
- Agent components and their relationships
- Data flow and dependencies

**Key Updates:**
- UI no longer connects directly to Orchestrator
- Controller mediates all UI-backend communication
- Feedback loop explicitly shown

### 2. `sequence_diagram.puml`
**UML Interaction Sequence Diagram** showing:
- Initial query processing workflow
- Agent interactions and message passing
- NEW: User feedback loop with re-summarization
- Feedback storage in ChromaDB

**Key Updates:**
- Controller validates and routes all requests
- User feedback flow explicitly modeled
- Reflective Agent can trigger revision
- Two-phase workflow: initial query + feedback iteration

### 3. `class_diagram.puml`
**Comprehensive class diagram** showing:
- Base agent abstractions
- All concrete agent classes with attributes and methods
- Controller and service classes
- Data models (Query, Summary, Feedback, etc.)
- Knowledge base components
- Class relationships (inheritance, composition, association)

**Key Updates:**
- SystemController class with validation and session management
- UserFeedback and ReflectionReport models
- SessionState for tracking user interactions
- Feedback processing methods in ReflectiveAgent

## How to View These Diagrams

### Option 1: VS Code Extension
1. Install "PlantUML" extension by jebbs
2. Open any `.puml` file
3. Press `Alt+D` to preview

### Option 2: Online Viewer
1. Go to http://www.plantuml.com/plantuml/uml/
2. Copy and paste the content of any `.puml` file
3. View the rendered diagram

### Option 3: Local PlantUML Installation
```powershell
# Install Java (required for PlantUML)
choco install openjdk11

# Install Graphviz (for diagram rendering)
choco install graphviz

# Download PlantUML JAR
# From: https://plantuml.com/download

# Generate PNG from PUML
java -jar plantuml.jar component_diagram.puml
```

### Option 4: Export to Images
Using the VS Code extension:
1. Open `.puml` file
2. Right-click in editor
3. Select "Export Current Diagram" → Choose format (PNG, SVG, PDF)

## Design Changes Summary

### Change 1: Controller Layer
**Before:** UI → Orchestrator (direct)  
**After:** UI → Controller → Orchestrator

**Rationale:** 
- Separation of concerns
- Input validation centralized
- Session management
- Easier to test and maintain

### Change 2: User Feedback Integration
**Before:** No mechanism for user feedback  
**After:** User → UI → Controller → Orchestrator → Reflective Agent

**Rationale:**
- Human-in-the-loop validation
- Quality improvement through user input
- Responsible AI with human oversight
- Learning from user preferences

### Change 3: Class Structure
**Before:** Informal agent structure  
**After:** Well-defined class hierarchy with BaseAgent abstraction

**Rationale:**
- Code reusability
- Consistent interface across agents
- Easier to add new agents
- Better type safety

## Diagram Conventions

### Component Diagram
- **Blue:** UI/Presentation layer
- **Green:** Controller/Application layer
- **Yellow:** Agent/Business logic layer
- **Gray:** Storage/Data layer
- **Solid arrows:** Direct dependencies
- **Dashed arrows:** Indirect or feedback relationships

### Sequence Diagram
- **Solid arrows:** Synchronous calls
- **Dashed arrows:** Return values
- **Notes:** Important design decisions or explanations
- **Alt blocks:** Conditional flows

### Class Diagram
- **Solid lines with filled diamonds:** Composition (strong ownership)
- **Solid lines with empty diamonds:** Aggregation (weak ownership)
- **Dashed lines with arrows:** Dependencies
- **Solid lines with empty triangles:** Inheritance

## Next Steps

After reviewing these diagrams:

1. **Implementation Phase**
   - Create SystemController class
   - Add feedback models
   - Update UI for feedback collection
   - Modify Reflective Agent to process feedback

2. **Testing**
   - Unit tests for each class
   - Integration tests for workflows
   - User acceptance testing with feedback loop

3. **Documentation**
   - API documentation
   - User guide for feedback feature
   - Development guide for adding new agents

## Questions for Professor

1. ✅ UI no longer communicates directly with Orchestrator - is this the intended separation?
2. ✅ User feedback loop integrated - should feedback be stored persistently or just in-session?
3. ✅ Class diagram shows inheritance hierarchy - is this level of detail appropriate?
4. Should we add a workflow diagram showing the state machine for query processing?
5. Do you want sequence diagrams for other scenarios (e.g., error handling, multi-query sessions)?

## References

- PlantUML Documentation: https://plantuml.com/
- UML Best Practices: https://www.visual-paradigm.com/guide/uml-unified-modeling-language/
- Multi-Agent Systems Design: Wooldridge, M. (2009). An Introduction to MultiAgent Systems
