# Curadoria — skills/.agents/skills → Power BI MCP

## Histórico
- **2026-09-17 (1ª varredura):** 435 skills genéricas → 6 importadas (powerbi-modeling + 4 pbi-* + mcp-python-generator)
- **2026-09-17 (2ª varredura):** `.agents/skills` atualizado para **32 skills Power BI especializadas** → 25 novas importadas

Critério: **relevante para Power BI Desktop via MCP Server/Microsoft (XMLA/TOM/te CLI/TMDL) ou criação de MCP Python** (como seus `pbi_apply.py`).

## ✅ Importadas (31 + pbi-mcp = 32 no total)

### Núcleo Desktop + MCP (seus scripts)
| Skill | Origem | Motivo |
|-------|--------|--------|
| `pbi-mcp` | própria | Tooling portátil `pbi_apply_exe.py` + `mcp-server.exe` — validate/render/update via XMLA |
| `powerbi-modeling` | `powerbi-modeling` | Oficial MS — workflow MCP (connection/table/measure/relationship/dax_query) + references STAR-SCHEMA/RLS |
| `mcp-python-generator` | `python-mcp-server-generator` | Gerar MCPs Python `mcp[cli]` — padrão para evoluir scripts para MCP próprio |

### Modelagem semântica (alternativas/complementos ao MCP)
| Skill | Linhas | Motivo |
|-------|--------|--------|
| `connect-pbid` | 491 | **Alternativa direta ao MCP** — TOM/ADOMD.NET via PowerShell no Desktop local, Desktop Bridge (reload/screenshot), daxlib. Usar quando MCP/te não disponíveis |
| `semantic-model` | 82 | Orquestrador — cascata `te` CLI → TOM/MCP → TMDL (`fab`). Lifecycle design/build/refresh/review |
| `tmdl` | 355 | Autoria TMDL direta + BIM→TMDL |
| `pbip` | 168 | Estrutura PBIP (thick/thin, .pbip/.pbism, renames/forks) |
| `dax` | 21 | Tuning DAX isolado |
| `pbi-dax-optimization` | 142 | Otimização DAX legada (mantida por compatibilidade, `dax` é mais recente) |
| `bpa-rules` | 278 | Criar/validar regras BPA (Best Practice Analyzer) |
| `te-cli` | 163 | Tabular Editor CLI cross-platform (`te`) |
| `te2-cli` | 179 | Tabular Editor 2 CLI (`TabularEditor.exe`) |
| `te-docs` | 132 | Docs/config TE3 (.tmuo, Preferences.json) |
| `c-sharp-scripting` | 310 | Scripts C# TOM em TE2/3 (macros, bulk update, calculation groups) |
| `power-query` | 165 | Author/validação M em partitions |
| `standardize-naming-conventions` | 108 | Padronização nomes TMDL |
| `pbi-model-design-review` | 335 | Review arquitetura (legado, complementa `semantic-model`) |
| `pbi-performance-troubleshooting` | 323 | Diagnóstico performance (legado) |

### Reports / PBIR (Desktop canvas)
| Skill | Linhas | Motivo |
|-------|--------|--------|
| `pbir-cli` | 366 | CLI `pbir` — criar/explorar/formatar/validar reports + `pbir desktop` (reload/screenshot) |
| `pbir-format` | 165 | Referência JSON PBIR (visual.json, objects, themes) |
| `create-pbi-report` | 186 | Workflow criar report do zero via pbir CLI |
| `review-report` | 195 | Auditoria qualidade/uso de reports |
| `pbi-report-design` | 296 | Canon design (3-30-300, hierarquia, cor, acessibilidade) |
| `modifying-theme-json` | 99 | Themes via pbir CLI (criar/audit/validar) |
| `svg-visuals` | 241 | SVGs via DAX + ImageUrl (sparklines, bullet, gauges) — **diretamente útil para suas medidas HTML** |
| `deneb-visuals` | 155 | Deneb/Vega-Lite em PBIR |
| `powerbi-custom-visuals` | 79 | Dev .pbiviz (pbiviz toolchain + MCP) |
| `python-visuals` | 145 | Python/matplotlib em PBIR |
| `r-visuals` | 157 | R/ggplot2 em PBIR |

### Outros relevantes
| Skill | Motivo |
|-------|--------|
| `refresh-semantic-model` | Refresh dataset/model (útil pós-`pbi_apply`) |
| `lineage-analysis` | Linhagem model→reports cross-workspace (impact analysis) |
| `paginated-report` | RDL/paginated (se precisar print-perfect) |

## ❌ Ignoradas (7 de 32)

| Skill | Motivo |
|-------|--------|
| `fabric-cli` | Fabric workspace/service — fora escopo Desktop MCP |
| `executing-spark` | Spark/Livy Fabric — não Desktop |
| `using-duckdb` | DuckDB para lakehouse — não Desktop MCP |
| `audit-tenant-settings` | Admin tenant Fabric — governance |
| `help-me-get-started` | Onboarding genérico agentes |
| `improve-my-agent-setup` | Auditoria setup agente (Goblin Mode) |
| _(antigas 1ª varredura)_ `power-platform-mcp-connector-suite`, `fabric-lakehouse`, `dotnet-mcp-builder` etc. | Já documentadas acima |

Ative-as se expandir para Fabric/Service.

## 🔗 Mapa de uso

```
Desktop aberto
  ├─ MCP (recomendado): pbi-mcp (seus scripts) + powerbi-modeling (workflow)
  ├─ te CLI: te-cli → semantic-model → tmdl
  ├─ TOM fallback: connect-pbid (PowerShell) — quando te/MCP indisponíveis
  └─ Reports: pbir-cli + pbir-format (+ create-pbi-report/review-report/theme/svg-visuals)
```

## Próximos passos
- Unificar `dax` + `pbi-dax-optimization` (duplicidade)
- Avaliar `mcp-python-generator` para transformar `pbi_apply_exe.py` em MCP Python stdio publicável
