# -*- coding: utf-8 -*-
 
##########################################
#
# Freevial
# Estructura de dades globals
#
# Carles 24/08/2007
# RainCT 27/08/2007
#

import os.path, pygame
from pygame.locals import *

DEBUG_MODE = False

class Equip:

	nom = ""
	punts = 0
	figureta = 0

	actiu = False

	def canviaCategoria( self, categoria ):
		# Les tenim desendreçades i això ho complica una mica
		if( categoria == 6 ): self.figureta ^= 0x1
		if( categoria == 5 ): self.figureta ^= 0x2
		if( categoria == 1 ): self.figureta ^= 0x4
		if( categoria == 2 ): self.figureta ^= 0x8
		if( categoria == 4 ): self.figureta ^= 0x10
		if( categoria == 3 ): self.figureta ^= 0x20

	def activaCategoria( self, categoria ):
		# Les tenim desendreçades i això ho complica una mica
		if( categoria == 6 ): self.figureta |= 0x1
		if( categoria == 5 ): self.figureta |= 0x2
		if( categoria == 1 ): self.figureta |= 0x4
		if( categoria == 2 ): self.figureta |= 0x8
		if( categoria == 4 ): self.figureta |= 0x10
		if( categoria == 3 ): self.figureta |= 0x20


class Freevial_globals:
	""" Contains all variables that are commonly used by all components of Freevial. """
	
	mida_pantalla_x = 1024
	mida_pantalla_y = 768
	Limit_FPS = 40

	pantalla = ""
	
	basefolder = '../data'
	
	folders = {
						'base': basefolder,
						'images': os.path.join(basefolder, 'images'),
						'sounds': os.path.join(basefolder, 'sounds'),
						'fonts': os.path.join(basefolder, 'fonts'),
					}

	# Rainct ... aquesta linia no m'agrada gens. però així funciona... segur que tens alguna idea millor
	equips = ( Equip(), Equip(), Equip(), Equip(), Equip(), Equip() )

	jugador_actual = 0

def loadImage( filename ):
	""" Returns a Surface of the indicated image, which is expected to be in the images folder. """
	
	return pygame.image.load( os.path.join(Freevial_globals.folders['images'], str(filename) ))


def loadSound( filename, volume = '' ):
	""" Returns a sound object of the indicated audio file, which is expected to be in the sounds folder. """
	
	obj = pygame.mixer.Sound( os.path.join(Freevial_globals.folders['sounds'], str(filename) ))
	
	if volume != '':
		obj.set_volume( float(volume) )
	
	return obj

def keyPress( event, keys ):
	""" Returns true if the given event is the release of one of the indicated keys. 
	Just a key can be passed or a whole bunch inside a tuple, and in both cases they may be 
	either a string or directly it's pygame object. """
	
	if type(keys) is str or type(keys) is int:
		keys = ( keys, )
	
	
	# Check if any of the indicated keys matches
	found = 0
	for key in keys:
		
		if key[:2] != 'K_':
			key = 'K_' + key
		
		if type(key) is str:
			key = getattr(pygame, key)
		
		if event.type == pygame.KEYUP and event.key == key:
			found = 1
	
	return True if found == 1 else False

def maxPunts( equips ):

	puntsmax = 0

	for compta in range(0,6):
		if( equips[compta].actiu ):
			puntsmax = max( puntsmax, equips[compta].punts )
	
	return puntsmax

def equipsActius( equips ):

	actius = 0

	for compta in range(0,6):
		if( equips[compta].actiu ): actius += 1
	
	return actius

def seguentEquipActiu( equips, actual ):

	actual += 1

	for compta in range(0,6):
		if( equips[(actual + compta) % 6].actiu ): 
			return (actual + compta) % 6
	
	return -1

def anteriorEquipActiu( equips, actual ):

	actual -= 1

	for compta in range(0,6):
		if( equips[(actual - compta ) % 6].actiu ): 
			return (actual - compta ) % 6
	
	return -1

anterior = ""

def escriutecla(  tecla ):

	print tecla
	anterior = tecla
	torna = pygame.key.name( tecla )

	if( torna == 'space'): torna = ' '
	if( torna == 'world 71'): torna = 'ç'
	if( torna in( 'compose', 'left shift', 'right shift', 'left ctrl', 'right ctrl', 'alt gr', 'right alt', 'left alt')): torna = ''

	print pygame.key.get_mods()
	if( pygame.key.get_mods() & 0x1 ): torna = torna.upper()

	return torna


