# Organização Automática de Contra-Cheques (PDF)

## Objetivo
Este projeto automatiza a organização de contra-cheques em PDF, renomeando
os arquivos e organizando-os em pastas por ano.

## Padrão de Nome
```
ANO-MÊS - CC - TIPO.pdf
```

### Exemplos
- 2025-09 - CC - Normal.pdf
- 2025-12 - CC - 13Salario.pdf

## Funcionalidades
- Leitura de PDFs com pdfplumber
- Extração do campo "Tipo da Folha"
- Mês sempre com dois dígitos
- Organização automática por ano
- Evita sobrescrita de arquivos

## Dependências
```bash
pip install pdfplumber tqdm
```

## Execução
1. Ajuste o caminho da pasta no script
2. Execute:
```bash
python contracheques-pdf-organizer.py
```

## Estrutura Final
```
PDFs/
 ├─ 2024/
 └─ 2025/
```

## Licença
Uso pessoal / interno.
