# -*- coding: utf-8 -*-
 
#
# Freevial
# Questions Importer
#
# Copyright (C) 2007 The Freevial Team
#
# By Carles Oriol i Margarit <carles@kumbaworld.com>
# By Siegfried-Angel Gevatter Pujals <siggi.gevatter@gmail.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

import csv, copy, random
from freevialglob import *

arxius_de_preguntes = [ 'preguntes_ca01.csv', 
						'preguntes_ca02.csv', 
						'preguntes_ca03.csv',
						'preguntes_ca04.csv', 						
						'preguntes_ca05.csv', 
						'preguntes_ca06.csv', 
						'preguntes_cakw.csv', 
						'preguntes_camc.csv' ]


carpeta_de_preguntes = '../'

class CategoriaPreguntes:

	def __init__( self, num ):

		self.versio = 0
		self.nom = ''
		self.data_creacio = ''
		self.data_revisio = ''
		self.autors = ''
		self.descripcio = ''
		self.jugadors = ''
		self.idioma = ''

		self.preguntes = []
		self.preguntes_backup = []
	
		self.num = num

		self.nomimatge = ''
		self.so = ''


	def importQuestions( self, csvFile ):
		""" Imports the questions from a CSV file and returns them in a list. """

		print csvFile

		csv_read = csv.reader( open( csvFile ) )
			
		comptaline  = 0

		for line in csv_read:
			
			comptaline += 1

			if   comptaline == 1: self.versio = int( line[1] )
			elif comptaline == 2: self.nom = unicode( line[1], 'utf-8' )
			elif comptaline == 3: self.data_creacio = unicode( line[1], 'utf-8' )
			elif comptaline == 4: self.data_revisio = unicode( line[1], 'utf-8' )
			elif comptaline == 5: self.autors = unicode( line[1], 'utf-8' )
			elif comptaline == 6: self.descripcio = unicode( line[1], 'utf-8' )			
			elif comptaline == 7: self.jugadors = unicode( line[1], 'utf-8' )
			elif comptaline == 8: self.idioma = unicode( line[1], 'utf-8' )
			elif comptaline == 9: self.nomimatge = unicode( line[1], 'utf-8' )
			elif comptaline == 10: self.so = unicode( line[1], 'utf-8' )

			elif comptaline > 16:

				for num in range(0, 10):
					line[ num ] = unicode(line[ num ], 'utf-8')
				
				for num in (5, 8):
					try:
						line[ num ] = int(line[ num ])
					except ValueError:
						line[ num ] = 0
			
				line[0] = self.num
				self.preguntes.append(line)
		
		self.preguntes_backup = copy.deepcopy( self.preguntes )

		self.shuffleQuestions( )

	def shuffleQuestions( self ):
		""" Returns the given questions list, but shuffled. """

		self.preguntes = copy.deepcopy( self.preguntes_backup )
		
		random.shuffle( self.preguntes )

	def agafaPregunta ( self ):

		if 0 == len(self.preguntes): self.shuffleQuestions()
		
		return self.preguntes.pop()


###########################################

#random.shuffle( arxius_de_preguntes )

categoriespreguntes = []

for num in range(0, len(arxius_de_preguntes) ):
	cat = CategoriaPreguntes( num + 1 )
	cat.importQuestions( os.path.join(carpeta_de_preguntes, arxius_de_preguntes[num]) )
	categoriespreguntes.append( cat )


def textCategoria( ncat ):

	return categoriespreguntes[ncat].nom

def preguntes_autors():

	llista = []

	for num in range(0, 6):	
		llista.append(  categoriespreguntes[num].nom + ": " + categoriespreguntes[num].autors )
	
	return llista

def nomImatgeCategoria( ncat ):

	return categoriespreguntes[ncat].nomimatge

def soCategoria( ncat ):

	return categoriespreguntes[ncat].so

def get_categoriespreguntes( ):

	return categoriespreguntes


