#!/bin/python3
import os
import json
import argparse
import subprocess

CONFIG_FILE_PATH = os.getenv('GIT_CONFIG_FILE_PATH', os.path.join(os.getenv("HOME"), '.config/git_config.json'))

# Cria o parser de argumentos
parser = argparse.ArgumentParser(description='Comando create')
subparsers = parser.add_subparsers(dest='command')

# Parser para o comando create
create_parser = subparsers.add_parser('create', help='Cria um usuário')
create_parser.add_argument('--config-file', help='Arquivo de configuração JSON')

subparser_use = subparsers.add_parser('use', help='Ativa uma configuração')
subparser_use.add_argument('config', help='Nome da configuração')

subparser_list = subparsers.add_parser('list', help="Exibe todas as configurações")
subparser_list.add_argument('--config',required=False, help='Nome da configuração')

subparser_edit = subparsers.add_parser('edit', help='Cria um usuário')
subparser_edit.add_argument('--config-file', help='Arquivo de configuração JSON')

def verificar_e_criar_caminho(caminho_arquivo):
  nome_arquivo = os.path.basename(caminho_arquivo)
  pasta = os.path.dirname(caminho_arquivo)

  if pasta != '' and not os.path.exists(pasta):
    try:
      os.makedirs(pasta)
      print(f'Diretório "{pasta}" criado com sucesso.')
    except OSError as error:
      print(f'Erro ao criar o diretório "{pasta}": {error}')
  if not os.path.exists(caminho_arquivo):
    try:
      # Tenta criar o arquivo vazio
      with open(caminho_arquivo, 'w') as arquivo:
        json.dump({}, arquivo, indent=4)
        print(f'Arquivo "{nome_arquivo}" criado com sucesso.')
    except OSError as error:
      print(f'Erro ao criar o arquivo "{nome_arquivo}": {error}')

def salvar_configuracao(config):
  with open(CONFIG_FILE_PATH, 'r') as file:
    actual = json.load(file)
    for conf in config:
      actual[conf] = config[conf]
  with open(CONFIG_FILE_PATH, 'w') as arquivo:
    json.dump(actual, arquivo, indent=4)

def create_config(config_file=""):
  if config_file:
    with open(args.config_file) as file:
      config = json.load(file)
  else:
    config = {
      input('Nome da configuração: '):{
        'name': input('Nome de usuário: '),
        'email': input('Endereço de e-mail: '),
        'username': input('Nome completo: ')
      }
    }
  salvar_configuracao(config)

def listar_configs(config_name):
  with open(CONFIG_FILE_PATH, 'r') as file:
    config = json.load(file)
    if not config:
      print("Nenhuma configuração encontrada.")
      exit(0)
    for conf in config:
      if config_name and conf != config_name:
        continue
      print(f'[{conf}]')
      for key in config[conf]:
        print(f'  {key}: {config[conf][key]}')
      print("")

def executar_comando(key,value):
  command = ['git','config','--global']
  if key:
    command.append(key)
  if value:
    command.append(value)
  subprocess.call(command)

def usar_config(config_name):
  with open(CONFIG_FILE_PATH, 'r') as file:
    configs = json.load(file)
    config = configs.get(config_name)
    if not config:
      print(f'Configuração "{config_name}" não encontrada.')
      exit(1)
    for conf in config:
      executar_comando(f'user.{conf}', config[conf])
  print(f'Configuração "{config_name}" ativada com sucesso.')
  executar_comando('-l','')
if __name__ == '__main__':
  verificar_e_criar_caminho(CONFIG_FILE_PATH)
  args = parser.parse_args()
  if args.command == 'create':
    create_config(args.config_file)
  elif args.command == 'list':
    listar_configs(args.config)
  elif args.command == 'use':
    usar_config(args.config)
