#!/usr/bin/python

import os, sys, time
import datetime

Tentando_Quebrar_Senha = 1

def conferir_Energia():
	aux = os.popen("hdparm -C /dev/sdc")
	aux = [x for x in aux if x != '']

	if ' drive state is:  active/idle\n' in aux:
		return 1
	else: 
		return 0

def conferir_Estado_HD():
	aux = os.popen("hdparm -I /dev/sdc")
	aux = [x for x in aux if x != '']

	

	if '\t\tenabled\n' in aux and '\tnot\texpired: security count\n' in aux:
		return 11
	elif '\t\tenabled\n' in aux and '\t\texpired: security count\n' in aux:
		return 10 
	elif '\tnot\tenabled\n' in aux and '\tnot\texpired: security count\n' in aux:
		return '01'
	elif '\tnot\tenabled\n' in aux and '\t\texpired: security count\n' in aux:
		return '01' 

def testa_Senha():
	print ('senha:')
	senha = raw_input()
	os.system('hdparm --security-disable ' + senha +' /dev/sdc')

def desliga_HDD():
	os.system('echo -n "d                                           " > /dev/ttyUSB0')

def liga_HDD():
	os.system('echo -n "l                                            " > /dev/ttyUSB0')

def Brutforce():
	global Tentando_Quebrar_Senha
	senha = 0
		
	while Tentando_Quebrar_Senha == 1:
		##### os.popen('hdparm -C /dev/sd_____')
		ligado = conferir_Energia()

		liga_HDD()
		time.sleep(20)

		while ligado == 1:
			auxEstado = conferir_Estado_HD()

			# NOT ENABLE / NOT EXPIRED
			if auxEstado == 11: 
				testa_Senha()
				print('testando A SENHA: ')
			# NOT ENABLE / EXPIRED
			elif auxEstado == 10: 
				print('EXPIROU: ######################')
				ligado = 0	
				desliga_HDD()
				time.sleep(5)
				
			# ACHAMOS A SENHA
			elif auxEstado == '01':
				print('ACHAMOS A SENHA: ', senha)
				Tentando_Quebrar_Senha = 0
				ligado = 0



# Start of main()
Brutforce()