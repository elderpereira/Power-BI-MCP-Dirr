# Power BI MCP Skill

Skill para criar/editar relatórios Power BI via MCP (Model Context Protocol).

## Estrutura

```
skill/
├── SKILL.md                    # Documentação completa
├── scripts/
│   ├── pbi_apply.py            # Cliente MCP (validate/render/update/create)
│   ├── pbi_getmeasure.py       # Restaura medida do modelo para arquivo local
│   ├── medida_html_template.dax # Template para medidas HTML (tabela genérica)
│   └── visao_geral_template.dax # Template para dashboard de KPIs
└── templates/
    (reservado para futuros templates)
```

## Uso rápido

### 1. Conectar ao BI aberto

```bash
python scripts/pbi_apply.py "<Nome Medida>" arquivo.dax validate <PORTA>
```

Para descobrir a porta XMLA:
```bash
# Via MCP
python -c "from pbi_apply import *; discover_port()"
```

### 2. Criar/atualizar medida HTML

```bash
python scripts/pbi_apply.py "<Nome Medida>" arquivo.dax update <PORTA>
```

### 3. Renderizar preview

```bash
python scripts/pbi_apply.py "<Nome Medida>" arquivo.dax render <PORTA>
# Abra preview.html no navegador
```

### 4. Restaurar medida do modelo para arquivo local

```bash
python scripts/pbi_getmeasure.py <PORTA> "<Nome Medida>"
```

## Regras importantes

### Colunas vs. Medidas
- **Colunas calculadas**: não usam `CALCULATE` entre tabelas, nem referenciam outras medidas
- **Medidas**: podem usar `CALCULATE`, `RELATEDTABLE`, `SELECTEDVALUE`

### Nomes de colunas
Usar aspas simples + colchetes: `'Tabela'[Coluna]`

### SVGs e HTML
- Sempre aspas simples nos SVGs
- Remover metadados (xmlns, SVGRepo, Inkscape)
- Para SVGs pequenos, confirmar via DOM/console (não screenshot)

### pbix_editor
- Trava com Desktop aberto (Permission denied)
- Preferir XMLA (modelo ao vivo) via pbi_apply.py

## Exemplo: criar dashboard completo

```python
# 1. Criar arquivo medida_html.dax com HTML+DAX
# 2. Validar
python pbi_apply.py "Dashboard" medida_html.dax validate 54887

# 3. Gravar no modelo
python pbi_apply.py "Dashboard" medida_html.dax update 54887

# 4. No PBI Desktop: visual custom htmlContent → arrastar medida
```

## Perfis do Hermes Agent

A skill foi desenvolvida com perfil `pbi`, que fornece:
- `mcp__powerbi_modeling__*` — operações no modelo
- `mcp__pbix_editor__*` — operações no arquivo .pbix

Sem o perfil, use os scripts Python diretamente via terminal.
