# Skill: NOME_DA_SKILL

> Descrição de 1-2 linhas do que a skill faz.

## Quando usar

Descreva gatilhos: quando o agente deve ativar esta skill automaticamente.

- Ex: usuário pede para "criar medida DAX"
- Ex: usuário menciona "Power BI", "PBIX", etc.

## Estrutura

```
skills/nome-da-skill/
├── SKILL.md              # Este arquivo (instruções para o agente)
├── README.md             # Guia para humanos
├── scripts/              # Scripts Python/Node/etc
├── templates/            # Templates .dax, .json, etc
├── mcp-server/           # (opcional) binários MCP
└── docs/                 # (opcional) docs extras
```

## Instruções para o agente

1. Passo 1: o que fazer primeiro
2. Passo 2: como validar
3. Passo 3: como finalizar

### Comandos

```bash
python skills/nome-da-skill/scripts/seu_script.py <args>
```

## Regras / Boas práticas

- Regra 1
- Regra 2

## Troubleshooting

| Erro | Causa | Solução |
|------|-------|---------|
| ... | ... | ... |

## Referências

- Link oficial 1
- Link oficial 2
