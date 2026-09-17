# Power BI Skills

> **Repositório portátil de skills para Power BI Desktop — com preferência por MCP Server.**

Automatize Power BI Desktop via **Model Context Protocol (MCP)**: crie medidas DAX, gere visuals HTML/SVG, valide e publique no modelo sem sair do terminal ou do agente. Quando o MCP não alcança, o repo já traz os fallbacks (`te` CLI, TOM, TMDL, PBIR).

<p>

![Power BI](https://img.shields.io/badge/Power%20BI-Desktop-F2C811?style=flat-square&logo=powerbi&logoColor=000)
![MCP](https://img.shields.io/badge/MCP-powerbi--modeling--mcp-0B4FA3?style=flat-square)
![Python](https://img.shields.io/badge/Python-3.11%2B-3776AB?style=flat-square&logo=python&logoColor=white)
![Windows](https://img.shields.io/badge/Windows-10%2F11-0078D6?style=flat-square&logo=windows&logoColor=white)
![Skills](https://img.shields.io/badge/skills-32-16A34A?style=flat-square)

</p>

---

## Por que este projeto?

Trabalhar com Power BI Desktop hoje exige alternar entre DAX, cliques no Desktop, Tabular Editor e edição manual de JSON. Este repo unifica tudo em **skills acionáveis por IA ou CLI**, com uma regra simples:

> **MCP primeiro. Sempre.**

- **MCP Server (`powerbi-modeling-mcp`)** faz 95% do trabalho (conectar, listar, validar, gravar medidas) via XMLA — sem PowerShell, sem TOM manual.
- **Fallbacks já curados** (`connect-pbid` via TOM, `te` CLI, `tmdl`/`pbip`, `pbir-cli`) só entram quando o MCP não cobre.

Resultado: um agente (Hermes, OpenCode, Claude) ou você no terminal executa o mesmo comando e obtém o mesmo efeito no `.pbix`/`.pbip` aberto.

## Demonstração (30s)

```bash
# 1. Desktop aberto com .pbix → valida DAX sem gravar (via MCP)
python skills/pbi-mcp/scripts/pbi_apply_exe.py "Dashboard HTML" medida.dax validate 64857

# 2. Grava no modelo
python skills/pbi-mcp/scripts/pbi_apply_exe.py "Dashboard HTML" medida.dax update 64857

# 3. Preview no navegador
python skills/pbi-mcp/scripts/pbi_apply_exe.py "Dashboard HTML" medida.dax render 64857
# → preview.html (arraste a medida para o visual htmlContent no Desktop)
```

Via agente com MCP direto:
```
connection_operations ListLocalInstances → Connect localhost:64857 → dax_query_operations Validate → measure_operations Update
```

## Catálogo de skills (32)

### Núcleo — MCP First
| Skill | O que faz | Quando usar |
|-------|-----------|-------------|
| **pbi-mcp** | Tooling portátil: `pbi_apply_exe.py` + `mcp-server.exe` | Criar/editar medidas, validate/render/update |
| **powerbi-modeling** | Workflow oficial Microsoft + `references/` (star schema, RLS, performance) | Modelagem guiada por MCP |
| **mcp-python-generator** | Gera MCPs Python com `mcp[cli]` | Criar seu próprio MCP a partir dos scripts |

### Modelagem semântica
`connect-pbid` (TOM/ADOMD fallback) · `semantic-model` (orquestrador te→TOM→TMDL) · `tmdl` · `pbip` · `dax` · `bpa-rules` · `te-cli` / `te2-cli` / `te-docs` · `c-sharp-scripting` · `power-query` · `standardize-naming-conventions` · `pbi-dax-optimization` · `pbi-model-design-review` · `pbi-performance-troubleshooting`

### Reports & Visuals (PBIR)
`pbir-cli` · `pbir-format` · `create-pbi-report` · `review-report` · `pbi-report-design` · `modifying-theme-json` · **`svg-visuals`** (DAX + ImageUrl, ideal para suas medidas HTML) · `deneb-visuals` · `powerbi-custom-visuals` · `python-visuals` · `r-visuals` · `refresh-semantic-model` · `lineage-analysis` · `paginated-report`

> Curadoria, origens e skills ignoradas: [`docs/CURADORIA.md`](docs/CURADORIA.md)

## Arquitetura

```
Power BI Desktop (msmdsrv.exe :porta XMLA)
        ▲
        │  localhost:<PORTA>  (MCP first)
        │
  ┌─────┴──────┐
  │ MCP Server │  powerbi-modeling-mcp.exe --start
  │  (preferência 1)  │  connection/measure/dax_query/table/relationship ops
  └─────┬──────┘
        │  fallback
  ┌─────┴──────┐
  │  te CLI / TOM / TMDL  │  te-cli, connect-pbid (PowerShell), tmdl/pbip
  └─────┬──────┘
        │  reports
  ┌─────┴──────┐
  │ pbir CLI   │  pbir-cli, pbir-format, svg-visuals, deneb
  └────────────┘

skills/pbi-mcp/scripts/pbi_apply_exe.py  ──→  MCP Server  ──→  Desktop
skills/powerbi-modeling/SKILL.md         ──→  workflow/roteamento
```

## Comece agora

### Pré-requisitos
- Windows 10/11, Power BI Desktop aberto com `.pbix`/`.pbip`
- Python 3.11+ (`pip install mcp`), Node.js opcional (fallback `npx`)
- `mcp-server/powerbi-modeling-mcp.exe` já incluso (~38MB) — ou `npx @microsoft/powerbi-modeling-mcp`

### Instalação

```bash
git clone <este-repo>
cd "Power BI MCP Dirr"
pip install mcp
# opcional: winget install Microsoft.NuGet  (só para fallback TOM)
```

### Uso com agente

O `SKILL.md` na raiz já instrui o agente a preferir MCP. Basta pedir:

> "Conecte ao Power BI Desktop e crie a medida Dashboard HTML a partir de `medida.dax`"

O agente seguirá a hierarquia `MCP → te → TOM → TMDL` automaticamente.

### Uso manual

```bash
# descobrir porta (via MCP)
python -c "import asyncio; ... ListLocalInstances ..."  # ver SKILL.md
# ou: netstat -ano | find "<PID msmdsrv>"

python skills/pbi-mcp/scripts/pbi_apply_exe.py "Minha Medida" medida.dax validate 54321
python skills/pbi-mcp/scripts/pbi_apply_exe.py "Minha Medida" medida.dax update 54321
```

Hermes:
```bash
hermes mcp add --command "<repo>/mcp-server/powerbi-modeling-mcp.exe" --args "--start" --name powerbi-modeling
```

## Estrutura de pastas

```
/
├── SKILL.md                 # skill raiz — MCP First (para o agente)
├── README.md                # este arquivo
├── skills/                  # 32 skills (cada uma com SKILL.md)
│   ├── pbi-mcp/             # canônico: scripts + mcp-server + templates
│   ├── powerbi-modeling/    # oficial MS + references/
│   ├── connect-pbid/        # fallback TOM (só se MCP/te falharem)
│   ├── semantic-model/ tmdl/ pbip/ dax/ bpa-rules/ te-cli/ ...
│   ├── pbir-cli/ pbir-format/ svg-visuals/ deneb-visuals/ ...
│   └── _template/           # copie para criar nova skill
├── templates/dax/           # templates DAX compartilhados
├── scripts/ + mcp-server/   # aliases raiz (compatibilidade)
└── docs/                    # CURADORIA.md, CONTRIBUTING.md
```

## Criar nova skill

```powershell
Copy-Item -Recurse skills/_template skills/minha-skill
# edite SKILL.md, adicione scripts/, atualize README
```

Guia: [`docs/CONTRIBUTING.md`](docs/CONTRIBUTING.md) · Template: [`skills/_template/README.md`](skills/_template/README.md)

## Roadmap

- [ ] Unificar `dax` + `pbi-dax-optimization`
- [ ] Publicar MCP Python próprio a partir de `pbi_apply_exe.py` (`mcp-python-generator`)
- [ ] Templates `svg-visuals` para medidas HTML (sparklines, bullet, gauges)

---

**Repositório oficial do MCP:** https://github.com/microsoft/powerbi-modeling-mcp · **Docs:** https://learn.microsoft.com/power-bi/
