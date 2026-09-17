"""
Template de script para skill.
Uso: python skills/minha-skill/scripts/example.py --help
"""
import argparse

def main():
    parser = argparse.ArgumentParser(description="Descrição da skill")
    parser.add_argument("input", help="Arquivo de entrada")
    parser.add_argument("--port", default="55000", help="Porta XMLA do PBI Desktop")
    args = parser.parse_args()
    print(f"Input: {args.input} | Port: {args.port}")
    # TODO: implementar lógica

if __name__ == "__main__":
    main()
