# Contribuindo com Skills

## Padrão de skill

Toda skill em `skills/<nome>/` deve conter:

- `SKILL.md` — instruções para o agente (formato obrigatório)
- `README.md` — guia humano (opcional mas recomendado)
- `scripts/` — código executável
- `templates/` — (opcional) arquivos modelo

## Nomenclatura

- Pasta: `kebab-case` (ex: `pbi-mcp`, `dax-formatter`, `pbix-export`)
- Scripts: `pbi_<acao>.py` para Power BI

## Criando nova skill

```powershell
Copy-Item -Recurse skills/_template skills/minha-skill
# edite SKILL.md e scripts
```

## Testando

1. Valide sintaxe: `python -m py_compile skills/minha-skill/scripts/*.py`
2. Teste com PBI Desktop aberto se for skill MCP
3. Atualize README raiz

## Versionamento

- Cada skill é independente — versione via git tags se necessário
- Mantenha `SKILL.md` em português (padrão do repo)
