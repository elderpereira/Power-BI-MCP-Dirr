# Power BI Skills — Repositório

Coleção de **skills portáteis para Power BI** (MCP, DAX, HTML, automação). Cada skill é independente e pode ser usada via agente (Hermes/OpenCode) ou direto no terminal.

## 📦 Skills disponíveis (32)

### Núcleo — Desktop + MCP (seus scripts)
| Skill | Descrição | Pasta |
|-------|-----------|-------|
| **pbi-mcp** | **Tooling portátil** — `pbi_apply_exe.py` + `mcp-server.exe` — validate/render/update via XMLA | `skills/pbi-mcp/` |
| **powerbi-modeling** | Oficial MS — workflow MCP (connection/table/measure/relationship/dax_query) + references | `skills/powerbi-modeling/` |
| **mcp-python-generator** | Gerar MCPs Python com `mcp[cli]` — base para evoluir seus scripts para MCP próprio | `skills/mcp-python-generator/` |

### Modelagem semântica
| Skill | Descrição | Pasta |
|-------|-----------|-------|
| **connect-pbid** | **Alternativa ao MCP** — TOM/ADOMD.NET via PowerShell + Desktop Bridge (reload/screenshot) — usar quando te/MCP indisponíveis | `skills/connect-pbid/` |
| **semantic-model** | Orquestrador — cascata `te` → TOM/MCP → TMDL | `skills/semantic-model/` |
| **tmdl** | Autoria TMDL + BIM→TMDL | `skills/tmdl/` |
| **pbip** | Estrutura PBIP (thick/thin, .pbip/.pbism) | `skills/pbip/` |
| **dax** | Tuning DAX isolado | `skills/dax/` |
| **bpa-rules** | Criar/validar regras BPA | `skills/bpa-rules/` |
| **te-cli** / **te2-cli** / **te-docs** | Tabular Editor CLI (cross-platform / TE2 / docs) | `skills/te-cli/` etc |
| **c-sharp-scripting** | Scripts C# TOM em TE2/3 (bulk, calc groups) | `skills/c-sharp-scripting/` |
| **power-query** | Author M em partitions | `skills/power-query/` |
| **standardize-naming-conventions** | Padronização nomes TMDL | `skills/standardize-naming-conventions/` |
| *pbi-dax-optimization* | Otimização DAX (legado, preferir `dax`) | `skills/pbi-dax-optimization/` |
| *pbi-model-design-review* / *pbi-performance-troubleshooting* | Reviews legados (complementam `semantic-model`) | `skills/pbi-*` |

### Reports / PBIR
| Skill | Descrição | Pasta |
|-------|-----------|-------|
| **pbir-cli** | CLI `pbir` — criar/validar reports + `pbir desktop` | `skills/pbir-cli/` |
| **pbir-format** | Referência JSON PBIR | `skills/pbir-format/` |
| **create-pbi-report** | Workflow criar report do zero | `skills/create-pbi-report/` |
| **review-report** | Auditoria qualidade/uso de reports | `skills/review-report/` |
| **pbi-report-design** | Canon design (3-30-300, cor, a11y) | `skills/pbi-report-design/` |
| **modifying-theme-json** | Themes via pbir CLI | `skills/modifying-theme-json/` |
| **svg-visuals** | SVGs via DAX + ImageUrl — **útil para suas medidas HTML** | `skills/svg-visuals/` |
| **deneb-visuals** | Deneb/Vega-Lite em PBIR | `skills/deneb-visuals/` |
| **powerbi-custom-visuals** | Dev .pbiviz | `skills/powerbi-custom-visuals/` |
| **python-visuals** / **r-visuals** | Python/matplotlib, R/ggplot2 em PBIR | `skills/python-visuals/` |
| **refresh-semantic-model** | Refresh dataset/model | `skills/refresh-semantic-model/` |
| **lineage-analysis** | Linhagem model→reports cross-workspace | `skills/lineage-analysis/` |
| **paginated-report** | RDL/paginated | `skills/paginated-report/` |
| _template | Template para nova skill | `skills/_template/` |

> Curadoria completa e ignoradas (fabric-cli, using-duckdb etc): [docs/CURADORIA.md](docs/CURADORIA.md)

## 🗂️ Estrutura

```
/
├── skills/                  # 32 skills (cada pasta = 1 skill com SKILL.md)
│   ├── pbi-mcp/             # tooling portátil (scripts + mcp-server)
│   ├── connect-pbid/        # TOM/ADOMD PowerShell (alternativa MCP)
│   ├── semantic-model/ + tmdl/ + pbip/ + dax/ + bpa-rules/
│   ├── te-cli/ te2-cli/ te-docs/ c-sharp-scripting/
│   ├── pbir-cli/ pbir-format/ create-pbi-report/ review-report/
│   ├── svg-visuals/ deneb-visuals/ powerbi-custom-visuals/
│   └── _template/
├── templates/dax/            # templates DAX compartilhados
├── scripts/ + mcp-server/   # compatibilidade (alias para skills/pbi-mcp/)
├── docs/CURADORIA.md + CONTRIBUTING.md
├── SKILL.md                 # índice → skills/pbi-mcp/SKILL.md
└── README.md
```

## 🚀 Uso rápido — pbi-mcp

```bash
python skills/pbi-mcp/scripts/pbi_apply_exe.py "Minha Medida" meu_arquivo.dax validate <PORTA>
python skills/pbi-mcp/scripts/pbi_apply_exe.py "Minha Medida" meu_arquivo.dax update <PORTA>
python skills/pbi-mcp/scripts/pbi_apply_exe.py "Minha Medida" meu_arquivo.dax render <PORTA>
python skills/pbi-mcp/scripts/pbi_getmeasure.py <PORTA> "Minha Medida"
# alias legado: python scripts/pbi_apply_exe.py ...
```

Porta: `netstat -ano | find "<PID msmdsrv>"` ou `ListLocalInstances` via MCP. Docs: [skills/pbi-mcp/SKILL.md](skills/pbi-mcp/SKILL.md)

## 🔀 Quando usar qual skill?

- **MCP disponível:** `pbi-mcp` + `powerbi-modeling` (recomendado)
- **MCP/te indisponíveis:** `connect-pbid` (TOM PowerShell)
- **Modelo via arquivos:** `tmdl` + `pbip` + `te-cli`
- **Reports:** `pbir-cli` + `svg-visuals` (para suas medidas HTML)
- **Criar novo MCP Python:** `mcp-python-generator`

## ➕ Criar nova skill

```powershell
Copy-Item -Recurse skills/_template skills/minha-nova-skill
```

Veja [docs/CONTRIBUTING.md](docs/CONTRIBUTING.md) e [skills/_template/README.md](skills/_template/README.md).

## Requisitos

Windows 10/11, Python 3.11+ (`pip install mcp`), Power BI Desktop
