#! /usr/bin/env python
# cpcmrt
# 2020-01-20 (Y-m-d)
#  install pcscd python-pyscard python-pil
import os
import io
import binascii
import sys
import codecs
import requests
import getpass
import json
import time
import pyqrcode
import csv
from prompt_toolkit import prompt
from PIL import Image
from smartcard.System import readers
from smartcard.util import HexListToBinString, toHexString, toBytes

server = 'https://account-regis.ku.ac.th:8443'
# Check card
SELECT = [0x00, 0xA4, 0x04, 0x00, 0x08]
THAI_CARD = [0xA0, 0x00, 0x00, 0x00, 0x54, 0x48, 0x00, 0x01]
# CID
CMD_CID = [0x80, 0xb0, 0x00, 0x04, 0x02, 0x00, 0x0d]
# TH Fullname
CMD_THFULLNAME = [0x80, 0xb0, 0x00, 0x11, 0x02, 0x00, 0x64]
# EN Fullname
CMD_ENFULLNAME = [0x80, 0xb0, 0x00, 0x75, 0x02, 0x00, 0x64]
# Date of birth
CMD_BIRTH = [0x80, 0xb0, 0x00, 0xD9, 0x02, 0x00, 0x08]
# Gender
CMD_GENDER = [0x80, 0xb0, 0x00, 0xE1, 0x02, 0x00, 0x01]
# Card Issuer
CMD_ISSUER = [0x80, 0xb0, 0x00, 0xF6, 0x02, 0x00, 0x64]
# Issue Date
CMD_ISSUE = [0x80, 0xb0, 0x01, 0x67, 0x02, 0x00, 0x08]
# Expire Date
CMD_EXPIRE = [0x80, 0xb0, 0x01, 0x6F, 0x02, 0x00, 0x08]
# Address
CMD_ADDRESS = [0x80, 0xb0, 0x15, 0x79, 0x02, 0x00, 0x64]
# Photo_Part1/20
CMD_PHOTO1 = [0x80, 0xb0, 0x01, 0x7B, 0x02, 0x00, 0xFF]
# Photo_Part2/20
CMD_PHOTO2 = [0x80, 0xb0, 0x02, 0x7A, 0x02, 0x00, 0xFF]
# Photo_Part3/20
CMD_PHOTO3 = [0x80, 0xb0, 0x03, 0x79, 0x02, 0x00, 0xFF]
# Photo_Part4/20
CMD_PHOTO4 = [0x80, 0xb0, 0x04, 0x78, 0x02, 0x00, 0xFF]
# Photo_Part5/20
CMD_PHOTO5 = [0x80, 0xb0, 0x05, 0x77, 0x02, 0x00, 0xFF]
# Photo_Part6/20
CMD_PHOTO6 = [0x80, 0xb0, 0x06, 0x76, 0x02, 0x00, 0xFF]
# Photo_Part7/20
CMD_PHOTO7 = [0x80, 0xb0, 0x07, 0x75, 0x02, 0x00, 0xFF]
# Photo_Part8/20
CMD_PHOTO8 = [0x80, 0xb0, 0x08, 0x74, 0x02, 0x00, 0xFF]
# Photo_Part9/20
CMD_PHOTO9 = [0x80, 0xb0, 0x09, 0x73, 0x02, 0x00, 0xFF]
# Photo_Part10/20
CMD_PHOTO10 = [0x80, 0xb0, 0x0A, 0x72, 0x02, 0x00, 0xFF]
# Photo_Part11/20
CMD_PHOTO11 = [0x80, 0xb0, 0x0B, 0x71, 0x02, 0x00, 0xFF]
# Photo_Part12/20
CMD_PHOTO12 = [0x80, 0xb0, 0x0C, 0x70, 0x02, 0x00, 0xFF]
# Photo_Part13/20
CMD_PHOTO13 = [0x80, 0xb0, 0x0D, 0x6F, 0x02, 0x00, 0xFF]
# Photo_Part14/20
CMD_PHOTO14 = [0x80, 0xb0, 0x0E, 0x6E, 0x02, 0x00, 0xFF]
# Photo_Part15/20
CMD_PHOTO15 = [0x80, 0xb0, 0x0F, 0x6D, 0x02, 0x00, 0xFF]
# Photo_Part16/20
CMD_PHOTO16 = [0x80, 0xb0, 0x10, 0x6C, 0x02, 0x00, 0xFF]
# Photo_Part17/20
CMD_PHOTO17 = [0x80, 0xb0, 0x11, 0x6B, 0x02, 0x00, 0xFF]
# Photo_Part18/20
CMD_PHOTO18 = [0x80, 0xb0, 0x12, 0x6A, 0x02, 0x00, 0xFF]
# Photo_Part19/20
CMD_PHOTO19 = [0x80, 0xb0, 0x13, 0x69, 0x02, 0x00, 0xFF]
# Photo_Part20/20
CMD_PHOTO20 = [0x80, 0xb0, 0x14, 0x68, 0x02, 0x00, 0xFF]

def main():
    testConnect()

def testConnect():
	try:
		address = server + '/status'
		s = requests.get(address, timeout=5)
		y = json.loads(s.text)
		
	except:
		print('Error: Could not connect to server.')
		sys.exit()

	if y["status"] == "ok":
		login()
	else:
		print('Error: Could not connect to server.')
		sys.exit()


def login():
	client_id = input("Enter Client ID: ")
	client_secret = prompt("Enter Client Secret: ", is_password=True)
	address = server + '/client'
	data = {'client_id': client_id, 'client_secret': client_secret}
	r = requests.post(address, data=data)
	#print(r.text)
	y = json.loads(r.text)
	if y["client"] == 1:
		menu()
	else:
		print('Error: Not a privileged client.')
		pass
	
def menu():
    print("************MAIN MENU**************")
    print()

    choice = input("""
                      A: Smartcard Reader
                      B: View Student details
                      C: Search by ID number
                      Q: Quit/Log Out

                      Please enter your choice: """)

    if choice == "A" or choice =="a":
        readCard()
        pass
    elif choice == "B" or choice =="b":
        #viewstudentdetails()
        pass
    elif choice == "C" or choice =="c":
        #searchbyid()
        pass
    elif choice=="Q" or choice=="q":
    	sys.exit(1)
    else:
        print("You must only select either A,B,C, or Q.")
        print("Please try again")
        menu()

def readCard():
	# Thailand ID Smartcard
	def thai2unicode(data):
		result = ''
		result = bytes(data).decode('tis-620')
		return result.strip();
		
	def getData(cmd, req = [0x00, 0xc0, 0x00, 0x00]):
		readCarddata, sw1, sw2 = connection.transmit(cmd)
		data, sw1, sw2 = connection.transmit(req + [cmd[-1]])
		return [data, sw1, sw2];

	def getIdcode():
		std_id = input("Enter Student ID: ")
		if std_id.isdigit():
			return std_id
		elif std_id == None or not std_id:
			return ''
		else:
			getIdcode()

	# Get all the available readers
	readerList = readers()
	print ('Available readers:')
	for readerIndex,readerItem in enumerate(readerList):
		print(readerIndex, readerItem)

	# Select reader
	try:
		#readerSelectIndex = 0
		readerSelectIndex = int(input("Select reader[0]: ") or "0")
		reader = readerList[readerSelectIndex]
		print ("Using:", reader)
		connection = reader.createConnection()
		connection.connect()
		atr = connection.getATR()
		print ("ATR: " + toHexString(atr))
		if (atr[0] == 0x3B & atr[1] == 0x67):
			req = [0x00, 0xc0, 0x00, 0x01]
		else:
			req = [0x00, 0xc0, 0x00, 0x00]
		pass
	except:
		print('Error: Could not load smartcard reader.')
		time.sleep(1)
		print()
		menu()

	print()
	idcode = getIdcode()
	print()

	# Check cardsleep
	data, sw1, sw2 = connection.transmit(SELECT + THAI_CARD)
	print ("Select Applet: %02X %02X" % (sw1, sw2))
	# CID
	data = getData(CMD_CID, req)
	cid = thai2unicode(data[0])

	data = getData(CMD_ENFULLNAME, req)
	en_name = thai2unicode(data[0])
	#print ("TH Fullname: " +  thai2unicode(data[0]))
	
	if cid:
		print ("IDCARDNO: " + cid)
		print ("IDCODE: " + idcode)
		address = server + '/student_regis'
		data = {'idcardno': cid, 'idcode': idcode}
		r = requests.post(address, data=data)
		y = json.loads(r.text)
		#print(r.text)
		
		if y['student'] == 'already':
			print('Error: user already')
		elif y['student'] == 'userfound':
			print('Error: user not found')
		else:
			#print(y['student'])
			result = y['student']
			print()
			print('==================================================')
			print()
			print("Identification Number: " +  cid)
			print("Account: " + result['cn'])
			print("token: " + result['token'])
			print()
			print('==================================================')

			link_to_post = server + '/activate/' + result['token'] + '/' + result['cn']
			url = pyqrcode.create(link_to_post)
			url.png('./static/images/url.png', scale=7)
			#print("Printing QR code")
			#print(url.terminal())

			#export csv
			cn = result['cn'] 
			nms = [[cn,en_name]]
			f = open('./static/cn.csv', 'w')
			with f:
			    writer = csv.writer(f)
			    writer.writerows(nms)

			
	# TH Fullname
	#data = getData(CMD_THFULLNAME, req)
	#print ("TH Fullname: " +  thai2unicode(data[0]))
	#print(thai2unicode2(data[0])))
	# EN Fullname
	#data = getData(CMD_ENFULLNAME, req)
	#print ("EN Fullname: " + thai2unicode(data[0]))
	# Date of birth
	#data = getData(CMD_BIRTH, req)
	#print( "Date of birth: " + thai2unicode(data[0]))
	# Gender
	#data = getData(CMD_GENDER, req)
	#print ("Gender: " + thai2unicode(data[0]))
	# Card Issuer
	#data = getData(CMD_ISSUER, req)
	#print ("Card Issuer: " + thai2unicode(data[0]))
	# Issue Date
	#data = getData(CMD_ISSUE, req)
	#print ("Issue Date: " + thai2unicode(data[0]))
	# Expire Date
	#data = getData(CMD_EXPIRE, req)
	#print ("Expire Date: " + thai2unicode(data[0]))
	# Address
	#data = getData(CMD_ADDRESS, req)
	#print ("Address: " + thai2unicode(data[0]))
	'''
	# PHOTO
	photo = getData(CMD_PHOTO1, req[0])
	photo += getData(CMD_PHOTO2, req[0])
	photo += getData(CMD_PHOTO3, req[0])
	photo += getData(CMD_PHOTO4, req[0])
	photo += getData(CMD_PHOTO5, req[0])
	photo += getData(CMD_PHOTO6, req[0])
	photo += getData(CMD_PHOTO7, req[0])
	photo += getData(CMD_PHOTO8, req[0])
	photo += getData(CMD_PHOTO9, req[0])
	photo += getData(CMD_PHOTO10, req[0])
	photo += getData(CMD_PHOTO11, req[0])
	photo += getData(CMD_PHOTO12, req[0])
	photo += getData(CMD_PHOTO13, req[0])
	photo += getData(CMD_PHOTO14, req[0])
	photo += getData(CMD_PHOTO15, req[0])
	photo += getData(CMD_PHOTO16, req[0])
	photo += getData(CMD_PHOTO17, req[0])
	photo += getData(CMD_PHOTO18, req[0])
	photo += getData(CMD_PHOTO19, req[0])
	photo += getData(CMD_PHOTO20, req[0])
	data = HexListToBinString(photo)
	f = open(cid + ".jpg", "wb")
	f.write (data)
	f.close
	'''
	print()
	menu()

#the program is initiated, so to speak, here
main()