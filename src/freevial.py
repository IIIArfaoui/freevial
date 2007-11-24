# -*- coding: utf-8 -*-

#
# Freevial
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
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

import sys
import os.path
import pygame
import gettext
from math import *

from common.globals import GlobalVar, Global

# This is provisionally here for technical reasons...
if '--database' in sys.argv:
	dbpath = ' '.join(sys.argv[1:])
	dbpath = dbpath[dbpath.find('--database ') + 11:]
	if dbpath.find(' ') != -1:
		dbpath = dbpath[:dbpath.find(' ')]
	Global.database = dbpath

from common.freevialglob import *
from score import Score
from preguntador import Preguntador
from roda import Roda

gettext.install('freevial', '/usr/share/locale', unicode=1)

# Version information
VERSION = '1.0'
SERIES = 'gresca'


class Freevial:
	
	def __init__( self ):
		
		Global.game = GlobalVar()
		
		Global.game.screen = ''
		Global.game.rounds = 0
		
		Global.game.teams = []
		for num in range(0, 6): Global.game.teams.append( Equip() )
		
		Global.game.current_team = 0
		Global.game.sfc_credits = ''
	
	
	###########################################
	# Iniciem partida
	#
	def inici( self ):
		
		# inicialize presentation surface
		Global.game.screen = pygame.display.set_mode( ( Global.screen_x, Global.screen_y), HWSURFACE, 32)
		pygame.display.set_caption('Freevial')
		pygame.display.set_icon( loadImage('logo.png') )
		
		if not Global.DEBUG_MODE:
			pygame.mouse.set_visible( False )

			if Global.FS_MODE:
				pygame.display.toggle_fullscreen()
		
		# inicialize sound and text systems
		if not (Global.SOUND_MUTE and Global.MUSIC_MUTE):
			try:
				pygame.mixer.pre_init(44100, -16, 2, 2048)
				pygame.mixer.init()
			except pygame.error, message:
				print _('Sound initialization failed. %s' % message)
				Global.SOUND_MUTE = True
				Global.MUSIC_MUTE = True
		
		pygame.font.init()
		
		Global.game.sfc_credits = createHelpScreen( 'credits', alternate_text = True )
		
		initTextos()
		init_joystick()
	
	###########################################
	#
	# Control principal del programa
	#
	def juguem( self ):
		
		self.inici()
		
		score = roda = fespregunta = None

		while 1:
			
			if not score: score = Score( Global.game )
			
			Global.game.current_team = score.juguem()
			
			if Global.game.current_team != -1:
				
				Global.game.rounds += 1		
				
				if not roda: roda = Roda( Global.game )
				
				resultat = roda.juguem( )
				
				if resultat != 0:
						
					Global.game.teams[ Global.game.current_team ].preguntes_tot[ resultat - 1 ] += 1		
					
					if not fespregunta:	fespregunta = Preguntador( Global.game )
					
					resultat = fespregunta.juguem( resultat )	
					
					if resultat > 0:
						Global.game.teams[ Global.game.current_team ].preguntes_ok[ resultat - 1 ] += 1
						Global.game.teams[ Global.game.current_team ].punts += 1
						
						fig_abans = Global.game.teams[ Global.game.current_team].figureta
						Global.game.teams[ Global.game.current_team].activaCategoria( resultat ) 
						
						if fig_abans != 63 and Global.game.teams[ Global.game.current_team].figureta == 63:
							Global.game.teams[ Global.game.current_team].punts += 2
						
					Global.game.current_team = seguentEquipActiu( Global.game.teams, Global.game.current_team )
			else:
				sys.exit()


if '-h' in sys.argv or '--help' in sys.argv:
	print
	print _('Usage: freevial [OPTIONS]')
	print
	print _('-d, --debug\t\tDebug mode')
	print _('-m, --mute\t\tDisable all sounds and music')
	print _('-f, --fullscreen\tStart in fullscreen mode')
	print _('-l, --locked\t\tStart game in locked mode')
	print _('-h, --help\t\tDisplay this message')
	print _('-v, --version\t\tPrint information about the current version')
	print _('--database <path>\tSet the absolute path to the database file / directory.')
	print _('--no-sound\t\tDisable sound')
	print _('--no-music\t\tDisable music')
	print _('--fps\t\t\tPrint framerate on screen')
	print
	
 	exit( 0 )

if '-v' in sys.argv or '--version' in sys.argv:
	print
	print 'Freevial, a trivia platform for use on community events'
	print 'You are running version %s, which is part of the «%s» series.' % ( VERSION, SERIES )
	print
	print 'https://launchpad.net/freevial/%s' % SERIES
	print ''
	
	sys.exit( 0 )

if '-d' in sys.argv or '--debug' in sys.argv:
	Global.DEBUG_MODE = True

if '-l' in sys.argv or '--locked' in sys.argv:
	Global.LOCKED_MODE = True

if '--fullscreen' in sys.argv or '-f' in sys.argv:
	Global.FS_MODE = True

if '--fps' in sys.argv:
	Global.DISPLAY_FPS = True

if '-m' in sys.argv or '--mute' in sys.argv:
	Global.SOUND_MUTE = True
	Global.MUSIC_MUTE = True

if '--no-sound' in sys.argv:
	Global.SOUND_MUTE = True

if '--no-music' in sys.argv:
	Global.MUSIC_MUTE = True

# For technical reasons, the "--database" option is parsed somewhere
# at the top of this file.

try:
	joc = Freevial()
	joc.juguem()

except KeyboardInterrupt:
	print _('Manual exit.')
	sys.exit()
