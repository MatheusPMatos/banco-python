import json
import csv
import os

# Nome do arquivo JSON (mesmo diretório)
json_file = "todosEstudantes_2025.json"
output_file = "alunos.csv"

# Lê o JSON
with open(json_file, "r", encoding="utf-8") as f:
    data = json.load(f)

# Cria o CSV
with open(output_file, mode="w", newline="", encoding="utf-8") as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=["matricula", "nome", "email", "turma"],delimiter=";")
    writer.writeheader()

    for matricula, values in data.items():
        nome = values[0].strip()
        turma = values[1].strip()
        email = f"{matricula}@estudantes.ifpr.edu.br"

        writer.writerow({
            "matricula": matricula.strip(),
            "nome": nome,
            "email": email,
            "turma": turma
        })

print(f"CSV gerado com sucesso: {os.path.abspath(output_file)}")
