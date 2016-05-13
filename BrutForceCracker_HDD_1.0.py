#!/usr/bin/python

import os, sys, time
import datetime

Tentando_Quebrar_Senha = 1
sd = 'sda'

def conferir_Energia():
	aux = os.popen("hdparm -C "+sd)
	aux = [x for x in aux if x != '']

	if ' drive state is:  active/idle\n' in aux:
		return 1
	else: 
		return 0

def conferir_Estado_HD():
	aux = os.popen("hdparm -I "+sd)
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
	os.system('hdparm --security-disable ' + senha +' '+sd)

def desliga_HDD():
	os.system('echo -n "d                                           " > /dev/ttyUSB0')

def liga_HDD():
	os.system('echo -n "l                                                                                                                                          " > /dev/ttyUSB0')

def espera_hd():
	while not(os.path.exists(sd)):
		time.sleep(0.01)

def Brutforce():
	os.popen("stty -F /dev/ttyUSB0 cs8 9600 ignbrk -brkint -icrnl -imaxbel -opost -onlcr -isig -icanon -iexten -echo -echoe -echok -echoctl -echoke noflsh -ixon -crtscts")
	global Tentando_Quebrar_Senha
		
	print 'ligando hd'
	liga_HDD()
	print 'comando ligar enviado'
	while Tentando_Quebrar_Senha == 1:
		print 'esperando hd'
		espera_hd()
		print 'hd voltou'
		auxEstado = conferir_Estado_HD()

		# NOT ENABLE / NOT EXPIRED
		if auxEstado == 11: 
			print('testando A SENHA: ')
			testa_Senha()
		# NOT ENABLE / EXPIRED
		elif auxEstado == 10: 
			print('EXPIROU: ######################')
			desliga_HDD()
			#time.sleep(1)
			liga_HDD()
			
		# ACHAMOS A SENHA
		elif auxEstado == '01':
			print('ACHAMOS A SENHA!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
			Tentando_Quebrar_Senha = 0



# Start of main()
if __name__ == '__main__':
	sd = sys.argv[1:][0]
	Brutforce()

