# Project policies

This project uses ASM for development policy checks and run accounting. Its running
application has no dependency on ASM. Shared rules are linked from AGENTS.md.

## Depends on

Development: ai-service-manager owns the local policy hooks and run registry.
Without it, enrolled commits cannot run their checks; the application keeps running.
Install ASM and its agent-hub plugin, then run `asm project init` and
`asm project doctor`. Configure project-specific privacy paths and documentation
mappings before adding personal data or changing code.
