#-*- coding:utf-8 -*-

import os
import sys
import re

toDelete = set([])
knownCompany = set([])

def renameFile(fpath, order):
	oDir, oFnameExt = os.path.split(fpath)
	oFname, ext = os.path.splitext(oFnameExt)
	bracketTypes = ['【】','[]','()']

	rFname = oFname
	title = ''
	date = []
	company = []
	others = ''

	for bt in bracketTypes:
		bl,br = bt[0],bt[1]
		while rFname.find(bl) != -1:
			sl = rFname.find(bl)
			sr = rFname.find(br)
			if sr > sl:
				toAppend = rFname[sl:sr+1]
				toAppendContent = toAppend[1:-1].strip()
				rFname = rFname[:sl] + rFname[sr+1:]

				if toAppendContent in toDelete:
					continue
				elif toAppendContent in knownCompany:
					company.append(toAppend)
				elif toAppendContent.isdigit() and len(toAppendContent) in [6,8]:
					date.append(toAppend)
				else:
					others += toAppend
			else:
				print('Incomplete bracket {} in {}'.format(bt, fpath))
				break #Incomplete exists

	title = rFname.strip()

	newName = ''
	for c in order:
		if c == 'C':
			newName += ''.join(company)
		elif c == 'D':
			newName += ''.join(date)
		elif c == 'O':
			newName += others
		elif c == 'T':
			newName += title
		else:
			print('Invalid order: {}'.format(order))
			sys.exit(1)

	os.rename(fpath, os.path.join(oDir,newName+ext))

	#print(oFname,ext)
	# squareBrackets = re.findall('\\[(.+?)\\]', oFname)
	# roundBrackets = re.findall('\\((.+?)\\)', oFname)

	
	# for t in squareBrackets:
	# 	rFname = rFname.replace('[{}]'.format(t),'')
	# for t in roundBrackets:
	# 	rFname = rFname.replace('({})'.format(t),'')
	# rFname = rFname.strip()

	# squareBrackets = list(filter(lambda t: t not in toDelete, squareBrackets))
	# roundBrackets = list(filter(lambda t: t not in toDelete, roundBrackets))

	# print(rFname, squareBrackets, roundBrackets)

def nameReorganize(tDir, order):
	for root, dirs, files in os.walk(tDir):
		for fname in files:
			fpath = os.path.join(root,fname)
			renameFile(fpath, order)

def printUsageAndExit():
	print('Usage: python {} <target dir> <token filter file> <known company file> <combination of T/D/C/O')
	print('T : Title')
	print('D : Date')
	print('C : Company')
	print('O : Others')
	sys.exit(1)

if __name__ == '__main__':
	if len(sys.argv) != 5:
		printUsageAndExit()

	tDir = sys.argv[1]
	tDir = os.path.abspath(tDir)

	with open(sys.argv[2], 'r', encoding='utf-8') as iFile:
		for ta in filter(lambda l:len(l.strip()) > 0, iFile.readlines()):
			ta = ta.strip().upper() if ta.isalnum() else ta.strip()
			toDelete.add(ta)

	with open(sys.argv[3], 'r', encoding='utf-8') as iFile:
		for ta in filter(lambda l:len(l.strip()) > 0, iFile.readlines()):
			ta = ta.strip().upper() if ta.isalnum() else ta.strip()
			knownCompany.add(ta)

	order = sys.argv[4].upper()

	if ''.join(sorted(order)) != 'CDOT':
		print('Invalid combination:',order)

	nameReorganize(tDir, order)
