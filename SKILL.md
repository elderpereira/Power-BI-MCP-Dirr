---
name: powerbi-skills
description: Repositório de skills para Power BI Desktop com preferência por MCP Server (powerbi-modeling-mcp). Use quando o usuário mencionar Power BI, PBIX/PBIP, DAX, medidas, modelo semântico, TMDL, Tabular Editor, PBIR, SVG/HTML visuals ou automação via XMLA/TOM.
---

# Power BI Skills — MCP First

> **Regra de ouro:** prefira sempre o **MCP Server** (`powerbi-modeling-mcp`) para qualquer operação no modelo. Só caia para `te` CLI, TOM (`connect-pbid`) ou TMDL quando o MCP não estiver disponível ou não cobrir a operação.

## Hierarquia de ferramentas (obrigatória)

| Prioridade | Ferramenta | Quando usar |
|------------|------------|-------------|
| **1 — MCP** | `mcp-server/powerbi-modeling-mcp.exe --start` ou `npx @microsoft/powerbi-modeling-mcp` → `connection_operations`, `measure_operations`, `dax_query_operations` etc. | **Sempre primeiro.** Cobre 95% dos casos: conectar, listar/criar/atualizar medidas, validar DAX, executar queries. É o que `skills/pbi-mcp/scripts/pbi_apply_exe.py` faz por baixo. |
| 2 — te CLI | `te` (cross-platform) / `TabularEditor.exe` | Quando precisa de `bpa`, `vertipaq`, deploy, ou propriedades que o MCP não expõe. Ver `skills/te-cli/`, `skills/semantic-model/` |
| 3 — TOM fallback | `skills/connect-pbid/` (PowerShell + TOM/ADOMD) | **Só se MCP e te indisponíveis.** Requer PowerShell + NuGet TOM. Útil para traces `EVALUATEANDLOG`, Desktop Bridge |
| 4 — TMDL direto | `skills/tmdl/` + `skills/pbip/` | Edição de arquivos `.tmdl` em PBIP quando Desktop fechado |

**Nunca edite `report.json`/`visual.json` manualmente** se `pbir-cli` estiver disponível — use `skills/pbir-cli/`.

## Roteamento por intenção

| Usuário quer... | Skill canônica | Ferramenta |
|-----------------|----------------|------------|
| Conectar ao Desktop, validar/gravar medida, render HTML | `skills/pbi-mcp/` | MCP (pbi_apply_exe.py) |
| Modelagem completa (star schema, relações, RLS, calc groups) | `skills/powerbi-modeling/` + `skills/semantic-model/` | MCP → te → TMDL |
| DAX performance | `skills/dax/` (preferir) / `skills/pbi-dax-optimization/` | MCP `dax_query_operations` Validate/Execute |
| BPA / review / naming | `skills/bpa-rules/`, `skills/standardize-naming-conventions/` | `te bpa` |
| Reports/PBIR, themes, SVGs | `skills/pbir-cli/`, `skills/svg-visuals/`, `skills/deneb-visuals/` | `pbir` CLI |
| Criar novo MCP Python | `skills/mcp-python-generator/` | `mcp[cli]` |

## Fluxo padrão (agente)

```
1. Descobrir porta: connection_operations ListLocalInstances (via MCP)
   └─ fallback: netstat -ano | find "<PID msmdsrv>" ou Get-Content msmdsrv.port.txt
2. Conectar: connection_operations Connect localhost:<PORTA>
3. Inspecionar: model_operations Get + table_operations List + measure_operations List
4. Agir: measure_operations Create/Update, dax_query_operations Validate/Execute
5. Validar: dax_query_operations Validate com EVALUATE ROW("h", <expr>)
6. (se report) pbir desktop refresh + screenshot para confirmar
```

## Comandos de referência (MCP first)

```bash
# Validar sem gravar (MCP)
python skills/pbi-mcp/scripts/pbi_apply_exe.py "Minha Medida" medida.dax validate <PORTA>

# Gravar no modelo (MCP)
python skills/pbi-mcp/scripts/pbi_apply_exe.py "Minha Medida" medida.dax update <PORTA>

# Preview HTML
python skills/pbi-mcp/scripts/pbi_apply_exe.py "Minha Medida" medida.dax render <PORTA>

# Restaurar medida
python skills/pbi-mcp/scripts/pbi_getmeasure.py <PORTA> "Minha Medida"
```

Via MCP direto (sem scripts Python):
```
connection_operations { operation: "ListLocalInstances" }
connection_operations { operation: "Connect", dataSource: "localhost:<PORTA>" }
dax_query_operations { operation: "Validate", query: "EVALUATE ROW(\"h\", <DAX>)" }
measure_operations { operation: "Update", definitions: [{ name, tableName: "#Medidas", expression }] }
```

## Estrutura do repo

```
skills/
├── pbi-mcp/              # tooling executável MCP (canônico) + mcp-server.exe
├── powerbi-modeling/     # workflow oficial MS + references/
├── connect-pbid/         # fallback TOM (só se MCP/te falharem)
├── semantic-model/       # orquestrador te→TOM→TMDL
├── tmdl/ pbip/ pbir-cli/ pbir-format/  # PBIP/PBIR
├── dax/ bpa-rules/ te-cli/ ...         # tuning e TE
└── svg-visuals/ deneb-visuals/ ...     # visuals
mcp-server/ + scripts/    # aliases raiz para compatibilidade (apontam para skills/pbi-mcp/)
```

## Regras DAX/HTML (resumo)

- Medidas podem usar `CALCULATE`; colunas calculadas não.
- SVGs com aspas simples, sem `xmlns`/`Inkscape`.
- Nomes com espaço: `'Tabela'[Coluna com Espaço]`
- Ver detalhes em `skills/pbi-mcp/SKILL.md` e `skills/powerbi-modeling/references/MEASURES-DAX.md`

## Fallback explícito

Só use `skills/connect-pbid/` se:
- `mcp-server.exe` não está disponível E `npx` falha E `te` CLI não está instalado.
Documente o motivo no log da sessão.
