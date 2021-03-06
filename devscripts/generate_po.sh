#! /bin/sh

#
# Freevial
# PO File Generator
#
# Copyright (C) 2007 The Freevial Team
#
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

xgettext ./src/*.py ./src/*/*.py \
	--default-domain=freevial \
	--output-dir=./data/po/ \
	--output=freevial.pot \
	--language=Python \
	--keyword=_ \
	--copyright-holder="The Freevial Team" \
	--msgid-bugs-address="freevial-dev@eurion.net"
