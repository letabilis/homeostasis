#!/bin/bash

#
########################################################################################################
#                                                                                                      #
# instalador.sh - Instalação das dependencias do projeto Homeostasis                                   #
#                                                                                                      #
# Autor: sDowlani                                                                                      #
#                                                                                                      #
# Repositório: github.com/letabilis/homeostasis                                                        #
                                                                                                     #                                                                                                      #
# Usabilidade: ./instalador.sh                                                                         #
#                                                                                                      #                
# Licença: GPL                                                                                         #
#                                                                                                      #
########################################################################################################
#

#
# Versionamento:                                                                                       #
#   0.1                                                                                                #
#       sDowlani (31/12/2024):                                                                         #
#            Primeiro Commit :)                                                                        #
#            Foi adicionado:                                                                           #
#               - Cabeçalho                                                                            #
#               - Suporte a sistemas baseado em Debian que utilizam APT                                #
#                                                                                                      #
#      

echo "TASK 0: Atualizar Pacotes + NALA: um frontend para APT"

sleep 2

sudo apt update

sudo apt upgrade --yes

sudo apt install nala

clear


echo "TASK 1: Instalar Python e PIP"

sleep 2

sudo nala install python3-full

sudo nala install python3-pip

sleep 2

clear



echo "TASK 2: Instalar SWI-PROLOG"

sudo apt-add-repository --yes ppa:swi-prolog/stable

sudo apt update

sudo nala install swi-prolog

sleep 2

clear


sleep 2

echo "Instalar Dependencias do Projeto: wxPython e swiplserver"
pip install -r requirements.txt --break-system-packages

sleep 4

clear

echo "Finalizando..."
sleep 2


exit
