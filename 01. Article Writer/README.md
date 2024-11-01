# AI Agent Article Writer

To Execute the code, read the main README.md file of the GitHub repository.

## Agents Workflow

```mermaid
flowchart LR
    A([📚 Researcher Agent]) --> B([📝 Content Writer Agent])
    B -->C([✂️ Content Editor])
    C -->D([Final Article])
    
    classDef default fill:##333300,stroke:#333,stroke-width:2.5px;
    classDef highlight fill:#333300,stroke:#4a90e2,stroke-width:3px;
    
    class A,B,C,D default;
    class D highlight;
```

## Preview of Agentic System
![AI Agent Article Writer](Preview.gif)
