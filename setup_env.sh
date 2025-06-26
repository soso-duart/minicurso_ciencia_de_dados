#!/bin/bash
echo "Removendo ambiente virtual antigo (se existir)..."
rm -rf .venv

echo "Criando novo ambiente virtual..."
python3 -m venv .venv

echo "Ativando ambiente..."
source .venv/bin/activate

echo "Atualizando pip..."
pip install --upgrade pip

echo "Instalando dependências..."
pip install -r requirements.txt

echo ""
echo "Ambiente criado e dependências instaladas!"
echo "Para ativar o ambiente, use:"
echo "   source .venv/bin/activate"
