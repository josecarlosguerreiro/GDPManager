import baseDados.baseDados as db
import os
import re

import mysql.connector
from flask import Flask, flash, redirect, render_template, request, session
from mysql.connector import errorcode

app = Flask(__name__)


class cPlayer:
    def __init__(self, nome, dta_nasc, alcunha, posicao, ptos_fortes, ptos_fracos, tlm, numCC, nif, morada, codPostal,
                 localidade, numCamisola):
        self.nome = nome
        self.dta_nasc = dta_nasc
        self.alcunha = alcunha
        self.posicao = posicao
        self.ptos_fortes = ptos_fortes
        self.ptos_fracos = ptos_fracos
        self.tlm = tlm
        self.numCC = numCC
        self.nif = nif
        self.morada = morada
        self.codPostal = codPostal
        self.localidade = localidade
        self.numCamisola = numCamisola

    # Gets and Sets
    def getName(self):
        return self.nome

    def setName(self, name):
        self.name = name

    def getDtaNasc(self):
        return self.dta_nasc

    def setDtaNasc(self, dta_nasc):
        self.dta_nasc = dta_nasc

    def getAlcunha(self, alcunha):
        self.alcunha = alcunha

    def setAlcunha(self, alcunha):
        self.alcunha = alcunha

    def getPosicao(self):
        return self.posicao

    def setPosicao(self, posicao):
        self.posicao = posicao

    def getPtoFortes(self):
        return self.ptos_fortes

    def getPtoFortes(self, ptos_fortes):
        self.ptos_fortes = ptos_fortes

    def getPtoFracos(self):
        return self.ptos_fracos

    def setPtoFracos(self, pts_fracos):
        self.ptos_fortes = pts_fracos

    def getTlm(self):
        return self.tlm

    def setTlm(self, tlm):
        self.tlm = tlm

    def getNumCC(self):
        return self.numCC

    def setNumCC(self, numCC):
        self.numCC = numCC

    def getNIF(self):
        return self.nif

    def setNIF(self, nif):
        self.nif = nif

    def getMorada(self):
        return self.morada

    def setMorada(self, morada):
        self.morada = morada

    def getCodPostal(self):
        return self.codPostal

    def setCodPostal(self, codPostal):
        self.codPostal = codPostal

    def getLocalidade(self):
        return self.localidade

    def setLocalidade(self, localidade):
        self.localidade = localidade

    def getNumCamisola(self):
        return self.numCamisola

    def setNumCamisola(self, numCamisola):
        self.numCamisola = numCamisola


def getPlayers():
    res = db.getPlayers()
    for i in res:
        print(i)


def login(username, password):
    user_exists = db.checkUsername(username)
    if user_exists is None:
        return -1
    else:
        res = db.login(username, password)
        if res is not None:
            return res
        else:
            return None


def proxJogo():
    res = db.proxJogo()
    if res == None:
        return None
    else:
        print(res)
        print(res[3])
        if res[3] == 1:  # Penela joga em casa
            infoEqCasa = db.getEquipaInfo(res[3])
            img_pen = "static/images/PenelaEmblema.jpg"
            infoEqFora = db.getEquipaInfo(res[4])
            img_fora = "static/images/clubs/" + infoEqFora[2] + ".jpg"
            # print(info)
            data = [res[0], infoEqCasa[2], infoEqFora[2], infoEqCasa[3], img_pen, img_fora]
        else:  # Penela joga fora
            infoEqCasa = db.getEquipaInfo(res[4])
            img_casa = "static/images/clubs/" + infoEqCasa[2] + ".jpg"
            infoEqFora = db.getEquipaInfo(res[3])
            img_pen = "static/images/PenelaEmblema.jpg"
            # print(info)
            data = [res[0], infoEqCasa[2], infoEqFora[2], infoEqCasa[3], img_casa, img_pen]
        return data
