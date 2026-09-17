# Power BI MCP Skill — Portátil

Skill para criar/editar relatórios Power BI via MCP (Model Context Protocol).
Tudo em uma pasta: scripts, templates e executável MCP.

## Estrutura da pasta

```
skill/
├── SKILL.md                          # Este arquivo
├── README.md                         # Guia rápido
├── scripts/
│   ├── pbi_apply_exe.py              # Cliente MCP (usa .exe local)
│   ├── pbi_apply.py                  # Cliente MCP (usa npx — alternativa)
│   ├── pbi_getmeasure.py             # Restaura medida do modelo
│   ├── medida_html_template.dax      # Template HTML genérico
│   ├── visao_geral_template.dax      # Template de cards KPI
│   └── mcp-server/
│       └── powerbi-modeling-mcp.exe  # Servidor MCP oficial (~38MB)
└── templates/                        # (reservado para futuros templates)
```

## Requisitos

- Windows 10/11
- Python 3.11+ com pacote `mcp` instalado:
  ```bash
  pip install mcp
  ```
- Power BI Desktop (abrir o .pbix que deseja editar)
- Node.js (opcional — apenas se quiser usar o método npx alternativo)

## Como usar

### 1. Conectar ao BI

Descubra a porta XMLA do PBI Desktop:
```bash
python scripts/pbi_apply_exe.py "Teste" teste.dax validate <PORTA>
```

Se der erro de "porta não encontrada", descubra assim:
```bash
# Método 1: Task Manager
# 1. Abrir PBI Desktop com o .pbix
# 2. Task Manager → Detalhes → PID do msmdsrv.exe
# 3. CMD: netstat -ano | find "<PID>"
#    → ouve em 127.0.0.1:5xxxx

# Método 2: via MCP
python -c "
import asyncio
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

async def main():
    p = StdioServerParameters(command='npx.cmd', args=['-y', '@microsoft/powerbi-modeling-mcp@latest', '--start'])
    async with stdio_client(p) as (r, w):
        async with ClientSession(r, w) as s:
            await s.initialize()
            res = await s.call_tool('connection_operations', {'request': {'operation': 'ListLocalInstances'}})
            print(res.content[0].text)

asyncio.run(main())
"
```

### 2. Criar/atualizar medida HTML

```bash
# Validar (sem gravar no modelo)
python scripts/pbi_apply_exe.py "<Nome Medida>" arquivo.dax validate <PORTA>

# Gravar no modelo
python scripts/pbi_apply_exe.py "<Nome Medida>" arquivo.dax update <PORTA>

# Renderizar preview (salva preview.html)
python scripts/pbi_apply_exe.py "<Nome Medida>" arquivo.dax render <PORTA>
```

### 3. Restaurar medida do modelo para arquivo .dax

```bash
python scripts/pbi_getmeasure.py <PORTA> "<Nome Medida>"
```

## Exemplo completo: criar dashboard

```bash
# 1. Criar arquivo medida_html.dax com HTML+DAX
# 2. Validar
python scripts/pbi_apply_exe.py "Dashboard" medida_html.dax validate 64857

# 3. Gravar
python scripts/pbi_apply_exe.py "Dashboard" medida_html.dax update 64857

# 4. No PBI Desktop: inserir visual custom htmlContent → arrastar medida
```

## Regras DAX importantes

### Colunas vs. Medidas
| Colunas calculadas | Medidas |
|---|---|
| Não usam `CALCULATE` entre tabelas | Podem usar `CALCULATE` |
| Não referenciam outras medidas | Referenciam outras medidas livremente |
| Usam referência direta: `[Coluna]` | Usam `SELECTEDVALUE()`, `SUM()`, etc. |

### SVGs e HTML
- Sempre aspas simples nos SVGs (`'...'`)
- Remover metadados (`xmlns`, `SVGRepo`, `Inkscape`)
- Para SVGs pequenos, confirmar via DOM/console (não screenshot)

### Nomes com acentos/espaços
```dax
'Tabela Nome'[Coluna com Espaço]
```

## Troubleshooting

| Erro | Causa | Solução |
|---|---|---|
| "server is not running" | PBI Desktop fechado | Abrir o .pbix no PBI Desktop |
| "Table #Medidas not found" | Tabela não existe | Usar tabela existente ou criar manualmente |
| "Cannot be made. Ensure that the server is running" | Porta errada | Descobrir porta via `netstat -ano \| find "<PID>"` |
| "No connectionName provided" | Parâmetro faltando | Especificar porta no comando |
| Medida retorna vazio | Coluna vs. medida | Converter coluna para medida (ou vice-versa) |

## Alternativa: npx (sem .exe)

Se o `.exe` não estiver disponível, use o `pbi_apply.py` (requer Node.js):

```bash
python scripts/pbi_apply.py "<Nome Medida>" arquivo.dax update <PORTA>
```

**Desvantagem**: trava às vezes em loop de falhas.

## Como obter o .exe

Se o `.exe` não está na pasta `mcp-server/`, obtenha assim:

1. Instalar a extensão no VSCode:
   - `https://aka.ms/powerbi-modeling-mcp-vscode`
2. Copiar o executável:
   ```
   C:\Users\<user>\.vscode\extensions\analysis-services.powerbi-modeling-mcp-0.4.0-win32-x64\server\powerbi-modeling-mcp.exe
   ```
3. Colar em: `skill/scripts/mcp-server/powerbi-modeling-mcp.exe`

## Perfis do Hermes Agent

Se você usa o Hermes Agent, adicione o MCP ao perfil:

```bash
hermes mcp add --command "<CAMINHO>/skill/scripts/mcp-server/powerbi-modeling-mcp.exe" --args "--start" --name powerbi-modeling
```

Ou use as ferramentas MCP diretamente via perfil `pbi`.

## Mais informações

- Repositório oficial: https://github.com/microsoft/powerbi-modeling-mcp
- Documentação: https://learn.microsoft.com/en-us/power-bi/