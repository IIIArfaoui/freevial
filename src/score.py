# -*- coding: utf-8 -*-
 
#
# Freevial
# Teams and Puntuation
#
# Copyright (C) 2007, 2008 The Freevial Team
#
# By Carles Oriol <carles@kumbaworld.com>
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
from random import randint
import pygame
from math import *
from pygame.locals import *

from common.globals import Global
from common.freevialglob import *
from common.events import EventHandle
from common.events import waitForMouseRelease
from common.dialog_question import fesPregunta
from endscreen import Visca
from selcat import *


class Score:

	def __init__( self, game ):
		
		self.game = game
		game.skin.set_domain( 'score' )		
		
		self.help_overlay = createHelpScreen( 'score' )
		
		self.help_on_screen = helpOnScreen( HOS_SCORE_MODE0 )
		self.maxim_equips = game.skin.configGetInt( 'max_teams', domain = 'game' )
		
		self.score_color_text = game.skin.configGetRGB( 'color_text' )
		self.score_mida_text = game.skin.configGetInt( 'mida_text')
		
		self.score_fons = game.skin.configGet( 'background')
		self.score_mascara_de_fons = game.skin.configGet( 'background_mask')
		self.score_element = game.skin.configGet( 'element')
		self.score_element_sel = game.skin.configGet( 'sel_element')
		self.score_element_sobre = game.skin.configGet( 'element_sobre')
		self.score_element_sel_offsetx = game.skin.configGetInt( 'sel_element_offsetx')
		self.score_element_sel_offsety = game.skin.configGetInt( 'sel_element_offsety')
		self.score_teams_offsetx = game.skin.configGetInt( 'teams_offsetx')
		self.score_teams_offsety = game.skin.configGetInt( 'teams_offsety')
		self.score_resultat_visible = game.skin.configGet( 'resultat_visible')
		self.score_figureta_visible = game.skin.configGet( 'figureta_visible') 
		self.score_figureta_mode = game.skin.configGet( 'figureta_mode') # 0 - del 0 al 63 combinacions 1 - del 0 al 5 figures individuals
		self.score_figureta_mascara = game.skin.configGet( 'figureta_mask')
		
		self.score_figureta_offsetx = game.skin.configGetInt( 'figureta_offsetx')
		self.score_figureta_offsety = game.skin.configGetInt( 'figureta_offsety')
		
		self.score_figureta_individual_pos = game.skin.configGetEval( 'figureta_individual_pos' )
		
		self.score_figureta_show_hide = game.skin.configGet( 'figureta_show_hide') # 0 - Es mostren les parts aconseguides, 1 - S'amaguen les parts aconseguides
		
		self.score_so_sub = game.skin.configGet( 'sub_sound')
		self.score_so_sub_vol = game.skin.configGet( 'sub_sound_vol')
		self.score_so_sub2 = game.skin.configGet( 'sub_sound2')
		self.score_so_sub2_vol = game.skin.configGet( 'sub_sound2_vol')
		
		self.score_ok = game.skin.configGet( 'ok')
		self.score_ok_vol = game.skin.configGet( 'ok_vol')
		
		self.score_locked = game.skin.configGet( 'locked')
		self.score_locked_pos = (game.skin.configGetInt( 'locked_pos_X'),game.skin.configGetInt( 'locked_pos_Y'))
		
		self.score_so_de_fons = game.skin.configGet( 'background_sound')
		self.score_so_de_fons_vol = game.skin.configGet( 'background_sound_vol')

		self.score_desplaca_el_fons = game.skin.configGet( 'move_background') # True o False = no hi ha scroll vertical
		self.score_ones_al_fons = game.skin.configGet( 'background_waves') # True o False = quiet
		
		
		self.score_caixes = game.skin.configGetEval( "boxes_coord" )
		
		self.show_corrects = game.skin.configGetBool( "show_corrects" )
		if self.show_corrects:
			self.corrects_coord = game.skin.configGetEval( "corrects_coord" )
			self.total_corrects = game.skin.configGetInt( "total_corrects" )
		
		self.final_stats = game.skin.configGetBool( "final_stats" )
 		
		#------------------------------------------
		
		self.ypos = 0
		self.mou_fons = 0
		#-----------------------------------------------
		
		self.figureta = game.skin.LoadImageRange( 'figureta_mask', 64, 2)		
	
		self.mascara_de_fons = game.skin.LoadImage( 'background_mask' )
		self.fons = game.skin.LoadImage( 'background' )
		self.element_score = game.skin.LoadImage( 'element' )
		self.seleccio_score = game.skin.LoadImage( 'sel_element' )
		self.so_sub = game.skin.LoadSound( 'sub_sound', 'sub_sound_vol' )
		self.so_sub2 = game.skin.LoadSound( 'sub_sound2', 'sub_sound2_vol' )
		self.so_ok = game.skin.LoadSound( 'ok', 'ok_vol' )
		self.sfc_llum = game.skin.LoadImage( 'locked' )
		
		if self.show_corrects:
			self.correct_done_image = game.skin.LoadImage( 'correct_done_image' ) if game.skin.configGet( "correct_done_image" ) != "" else None
			self.correct_notdone_image = game.skin.LoadImage( 'correct_notdone_image' ) if game.skin.configGet( "correct_notdone_image" ) != "" else None
		
		self.sfc_cursor = game.skin.render_text( "_", (self.score_color_text), self.score_mida_text, 1)
	
	def barra_pos( self, total, posicio, color, ample, alt ):

		sfc = pygame.Surface( ( ample, alt), pygame.SRCALPHA, 32 )
		pygame.draw.rect(sfc, color, (0,0,ample-1,alt-1), 2)

		ample_rect = ample - 8

		pygame.draw.rect(sfc, (color[0], color[1], color[2], 64), (4, 4, ample_rect, alt - 8))
		if total != 0 and posicio != 0: 
			pos_ample = ( posicio * ample_rect ) / total 
			pygame.draw.rect(sfc, color, (4, 4, pos_ample, alt - 8))

		return sfc
	
	def show_end_screen( self, startsound = False ):
		
		winner_team = self.game.skin.teamsGuanyador( self.game.teams )
		
		if count_not_empty(Global.game.teams, attr = 'name') == 1:
			winner_team = 1
		#######print Global.game.teams, count_not_empty(Global.game.teams, attr = 'name'), winner_team
		if winner_team > -1:
			if startsound:
				self.so_ok.play()
			visca = Visca( self.game )
			resultat = visca.juguem( self.game, Global.game.teams[ winner_team ].nom )
			self.game.skin.LoadSound( 'background_sound', 'background_sound_vol', music = 1 ).play( -1 )
		else:
			print "\a"
	
	def juguem( self ):
		
		self.game.skin.set_domain( 'score' )
		frate = frameRate( Global.fps_limit )
		
		waitForMouseRelease( )
		
		self.game.screen.fill( (0,0,0,0) )
		
		ypos = escriu = atzar = mou_fons = mostra_ajuda = mostra_credits = mostra_estad = 0
		element_seleccionat = self.game.current_team
		nou_grup = 1 if ( teamsActius( self.game.teams ) == 0 ) else 0
		
		# Modes: 0 (choosing teams), 1 (playing),  2 (game ended)
		mode = 1
		
		if nou_grup: mode = 0
		if self.game.skin.teamsGuanyador( self.game.teams ) != -1: 
			mode = 2
			mostra_estad = 1
			element_seleccionat = game.skin.teamsGuanyador( self.game.teams )
			self.so_ok.play()
		else:
			self.game.skin.LoadSound( 'background_sound', 'background_sound_vol', music = 1 ).play( -1 )
		
		surten = 0
		mostrada_victoria = False
		
		self.help_on_screen.activitat()
		
		while 1:
			
			if mode == 2:
				if frate.segons() < 4.1 and int(frate.segons()) > surten:
					surten = int( frate.segons() )

					self.so_ok.play(1)

				if frate.segons() > 4.1 and not mostrada_victoria:
					self.show_end_screen()
					mostrada_victoria = True
			
			# Event iterator
			for event in pygame.event.get():
				
				eventhandle = EventHandle(event)
				
				self.help_on_screen.activitat(event)
				
				if eventhandle.keyUp('F1') or (not escriu and eventhandle.keyUp('h')):
					mostra_ajuda ^= 1
					mostra_credits = 0
				
				if eventhandle.keyDown('F2'):
					mostra_credits ^= 1
					mostra_ajuda = 0
				
				if escriu and not mostra_ajuda and not mostra_credits:
				
					if eventhandle.isClick('primary') or eventhandle.keyUp('RETURN', 'ESCAPE', 'KP_ENTER'):
						escriu = 0
						if self.game.teams[element_seleccionat].nom == '' and eventhandle.isKey('ESCAPE'):
							self.game.teams[element_seleccionat].actiu = 0
					
					elif eventhandle.isDown():
						
						if eventhandle.isKey('BACKSPACE'):
							if len(self.game.teams[element_seleccionat].nom) > 0:
								newname = self.game.teams[element_seleccionat].nom[:-1]
						else:
							newname = self.game.teams[element_seleccionat].nom + eventhandle.str()
						
						if newname != None:
							sfc = self.game.skin.render_text( newname, (self.score_color_text), self.score_mida_text, 1)
							
							if sfc.get_width() < 340:
								# Name isn't too long, accept the new character
								self.game.teams[element_seleccionat].nom = newname
								self.game.teams[element_seleccionat].sfc_nom = sfc
				
				else:
					
					if eventhandle.keyUp('q', 'ESCAPE'):
						if not mostra_ajuda and not mostra_credits:
							if not Global.LOCKED_MODE:
								if fesPregunta( self.game.screen , valorText( HOS_QUIT ), (valorText( HOS_YES ), valorText( HOS_NO )), color = self.game.skin.configGetRGB( "game_question_color", "game" ) ) == 0:
									if not Global.MUSIC_MUTE:
										pygame.mixer.music.fadeout( 500 )
										pygame.time.wait( 500 )
									return -1
						else:
							mostra_ajuda = mostra_credits = 0
					
					if mode == 0:
						
						if eventhandle.keyUp('RIGHT', 'LEFT'):
							element_seleccionat += 1 if (0 == (element_seleccionat % 2)) else -1 
							self.so_sub.play()
						
						if eventhandle.keyUp('DOWN'): 
							element_seleccionat = (element_seleccionat + 2) % self.game.skin.configGetInt( "max_teams", "game" )
							self.so_sub.play()
						
						if eventhandle.keyUp('UP'): 
							element_seleccionat = (element_seleccionat - 2) % self.game.skin.configGetInt( "max_teams", "game" )
							self.so_sub.play()
						
						if eventhandle.keyUp('a'):
							nou_grup = 1
						
						if eventhandle.keyUp('n'):
							if self.game.teams[element_seleccionat].actiu:
								escriu ^= 1
							else:
								nou_grup = 1
						
						if eventhandle.keyUp('PAGEDOWN') and teamsActius( self.game.teams ) >= 1:
							element_seleccionat = seguentEquipActiu( self.game.teams, element_seleccionat )
							self.so_sub.play()
						
						if eventhandle.keyUp('PAGEUP') and teamsActius( self.game.teams ) >= 1:
							element_seleccionat = anteriorEquipActiu( self.game.teams, element_seleccionat )
							self.so_sub.play() 
						
						if eventhandle.keyUp('r') and teamsActius( self.game.teams ) > 0:
							atzar = randint(15, 50)
							mode = 1
					
					if eventhandle.keyUp('z'): 
						if self.game.teams[element_seleccionat].actiu:
							self.game.teams[element_seleccionat].punts += 1
					
					if eventhandle.keyUp('x'): 
						if self.game.teams[element_seleccionat].actiu and self.game.teams[element_seleccionat].punts > 0:
							self.game.teams[element_seleccionat].punts -= 1
					
					if self.game.teams[element_seleccionat].actiu:
						for num in range(1, 7):
							if eventhandle.keyUp(str(num), 'KP' + str(num)):
								self.game.teams[element_seleccionat].canviaCategoria( num-1 )
					
					if eventhandle.isClick('primary') or eventhandle.keyUp('RETURN', 'SPACE', 'KP_ENTER'):

						if mode == 1:
							if not Global.MUSIC_MUTE:
								pygame.mixer.music.fadeout( 2000 )
							return element_seleccionat

						elif mode == 0:
							if self.game.teams[element_seleccionat].actiu and eventhandle.keyUp('SPACE') :
								atzar = int( randint(25, 60) )
								mode = 1
							else:
								if self.game.teams[element_seleccionat].actiu: escriu ^= 1
								else: nou_grup = 1
						else:
							if fesPregunta( self.game.screen , valorText( HOS_NEW_GAME ), (valorText( HOS_YES ), valorText( HOS_NO )), color = self.game.skin.configGetRGB( "game_question_color", "game" )) == 0:
								mode = 0
								mostra_estad = 0 
				
								for equip in self.game.teams:
									for num in range(0, 6): 
										equip.preguntes_tot[num] = 0
										equip.preguntes_ok[num] = 0
									equip.punts = 0
									equip.figureta = 0				
					
					if eventhandle.keyUp('s'): 
						mostra_estad ^= 1
					
					if eventhandle.keyUp('m'):
						replaceModes = {
								0: 1,
								1: 0,
								2: 1,
							}
						mode = replaceModes[ mode ]

					if eventhandle.keyUp('e') and not Global.LOCKED_MODE :
						self.show_end_screen( startsound = True )
						mostrada_victoria = True
					
					if eventhandle.keyUp('l'): 
						Global.LOCKED_MODE = (not Global.LOCKED_MODE)

					if eventhandle.keyUp('k', 'F3', 'F5') and mode == 0:
						selcat = SelCat( self.game )
						selcat.juguem( mode )

			if nou_grup == 1:
				self.so_sub.play()
				nou_grup = 0
				self.game.teams[element_seleccionat].actiu ^= 1
				if self.game.teams[element_seleccionat].actiu and self.game.teams[element_seleccionat].nom == "": escriu ^= 1

			if atzar != 0 and teamsActius( self.game.teams ) >= 2:
				element_seleccionat = seguentEquipActiu( self.game.teams, element_seleccionat )
				atzar -= 1
				self.so_sub2.play()
			else:
				atzar = 0
			
			if self.score_desplaca_el_fons != "False":
				# Animem el fons
				self.ypos += 1
				self.ypos %= Global.screen_y
			
			xpinta = 0
			
			if self.score_ones_al_fons:
				self.mou_fons += 8
				

			# Pintem el fons animat
			for num in range(0, 768):
				
				if self.score_ones_al_fons:
					xpinta = cos((float(self.mou_fons +num)) / 100.0) * 20
			
				self.game.screen.blit( self.fons, (xpinta, num), (0, (self.ypos + num) % 768, 1024, 1) )
			
			self.game.screen.blit( self.mascara_de_fons, (0, 0) )
			# pintem les puntuacions

			for num in range(0, self.maxim_equips):
				ycaixa = self.score_caixes[num][1]
				xcaixa = self.score_caixes[num][0]

				if element_seleccionat == num and self.score_element_sobre != "True":
					for compta in range( 0, self.seleccio_score.get_height() ):
						desp = 0 if not mode else ( cos( frate.segons() * 10.0 + (float(compta)/10.0) ) * 2.0 )
						self.game.screen.blit( self.seleccio_score, (xcaixa + self.score_element_sel_offsetx + desp, ycaixa + self.score_element_sel_offsety + compta), (0,compta, self.seleccio_score.get_width(),1) )

				
				if self.game.teams[num].actiu:
					
					self.game.screen.blit( self.element_score, (xcaixa, ycaixa ) )
					
					if self.score_figureta_visible == 'True':
						self.game.screen.blit( self.figureta[self.game.teams[num].figureta], (xcaixa + self.score_figureta_offsetx, ycaixa + self.score_figureta_offsety ) )

					if self.game.teams[num].sfc_nom:
						self.game.screen.blit( self.game.teams[num].sfc_nom, (xcaixa + self.score_teams_offsetx , ycaixa + self.score_teams_offsety ) )
					ampletext = self.game.teams[num].sfc_nom.get_width() if self.game.teams[num].sfc_nom else 0
					if escriu and num == element_seleccionat:
						if (int(time.time() * 4) % 2) == 0: 
							self.game.screen.blit( self.sfc_cursor, (xcaixa + self.score_teams_offsetx + ampletext, ycaixa + self.score_teams_offsety )) 
							
					color = (128,0,0) if (maxPunts(self.game.teams) > self.game.teams[num].punts ) else (0,128,0)
					pinta = self.game.skin.render_text( str(self.game.teams[num].punts).zfill(2), color, 150, 1)
					if self.score_resultat_visible == 'True':
						self.game.screen.blit( pinta, (xcaixa + 200, ycaixa - 15) )

					if mostra_estad and self.final_stats:
						for cat in range(0,6):
							self.game.screen.blit( self.barra_pos( self.game.teams[num].preguntes_tot[cat], self.game.teams[num].preguntes_ok[cat],  colorsCategories()[cat], 50, 14 ), (xcaixa + 140, ycaixa + 21 + cat * 16) )
				
					
					if self.show_corrects:
						for compta in range(0, self.total_corrects):
							if self.game.teams[num].punts > compta:
								if self.correct_done_image != None:
									self.game.screen.blit( self.correct_done_image, (xcaixa + self.corrects_coord[compta][0], ycaixa + self.corrects_coord[compta][1] ))
							else:
								if self.correct_notdone_image != None:
									self.game.screen.blit( self.correct_notdone_image, (xcaixa + self.corrects_coord[compta][0], ycaixa + self.corrects_coord[compta][1] ))
						
				if element_seleccionat == num and self.score_element_sobre == "True":
					for compta in range( 0, self.seleccio_score.get_height() ):
						desp = 0 if not escriu else ( cos( frate.segons() * 10.0 + (float(compta)/10.0) ) * 2.0 )
						self.game.screen.blit( self.seleccio_score, (xcaixa + self.score_element_sel_offsetx + desp, ycaixa + self.score_element_sel_offsety + compta), (0,compta, self.seleccio_score.get_width(),1) )
			
			
			if Global.LOCKED_MODE: 
				self.game.screen.blit( self.sfc_llum, (0, 0) )
			
			if mostra_ajuda: self.game.screen.blit( self.help_overlay, (0,0))
			if mostra_credits: self.game.screen.blit( self.game.sfc_credits, (0,0))
			
			self.help_on_screen.draw( self.game.screen, (350, 740), HOS_SCORE_MODEW if escriu else mode)
			
			frate.next( self.game.screen )
			
			# Exchange self.game.screen buffers
			pygame.display.flip()

		return 0
