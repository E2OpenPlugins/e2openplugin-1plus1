# -*- coding: UTF-8 -*-
# for localized messages
from . import _

from Plugins.Plugin import PluginDescriptor

def main(session, **kwargs):
    from miniCalc import miniCalcScreen
    session.open(miniCalcScreen)

def Plugins(**kwargs):
	return [
		PluginDescriptor(
			name="1plus1",
			description=_("A simple arithmetic calculator"),
			where = PluginDescriptor.WHERE_PLUGINMENU,
			icon="./icon.png",
			fnc=main)
		]
