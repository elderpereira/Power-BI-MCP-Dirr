# Template de Skill

Este é o template base para criar uma nova skill no repositório.

## Como criar uma nova skill

1. Copie esta pasta:
   ```bash
   Copy-Item -Recurse skills/_template skills/minha-nova-skill
   ```

2. Renomeie e edite `SKILL.md` com as instruções da sua skill.

3. Adicione scripts em `scripts/` e templates em `templates/`.

4. Atualize o `README.md` raiz na tabela de skills.

5. Teste localmente antes de commitar.

## Checklist

- [ ] `SKILL.md` com instruções claras para o agente
- [ ] `README.md` com guia humano
- [ ] Scripts com `argparse` / comentários de uso
- [ ] Templates documentados
- [ ] Troubleshooting
