# Copyright 2009 Simon Schampijer
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA

"""SetTime Activity: Admin activity to set laptop time"""

from gi.repository import Gtk
import logging

from gettext import gettext as _

from sugar3.activity import activity
from sugar3.graphics.toolbarbox import ToolbarBox
from sugar3.activity.widgets import ActivityButton
from sugar3.activity.widgets import TitleEntry
from sugar3.activity.widgets import StopButton
from sugar3.activity.widgets import ShareButton
from sugar3.activity.widgets import DescriptionItem

import os, sys
from subprocess import call, Popen, PIPE
from toolbar import toolbar

class SetTime(activity.Activity):

    def __init__(self, handle):
        activity.Activity.__init__(self, handle)

        # we do not have collaboration features
        # make the share option insensitive
        self.max_participants = 1

        # toolbar with the new toolbar redesign
        toolbar_box = toolbar(self)
        self.set_toolbar_box(toolbar_box)
        toolbar_box.show()

        pid = Popen('date +"%d %B %Y %R:%S %Z"',stdout=PIPE,stderr=PIPE,shell=True)
        result, err = pid.communicate()
        print 'date 1 result', result, 'err', err
        settime = Gtk.Entry()
        settime.set_text(result[:-1])
        pos = result.rfind(' ')
        self.zone = result[pos+1:]
        settime.connect('activate',self.settime_cb)
        #timeset = Gtk.Label(result)
        box = Gtk.VBox(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        box.pack_start(settime, True, True, 0)
        self.settime = settime
        self.set_canvas(box)
        box.show_all()        

    def settime_cb(self,widget):
        time = widget.get_text()
        pos = time.rfind(' ')
        zone = time[pos+1:]
        time = time[:pos]
        if not zone == self.zone:
            cmd = "su -c 'cp /usr/share/zoneinfo/"+zone+" /etc/localtime'"
            print 'cmd', cmd
            call(cmd, shell=True)
        print 'time', len(time), time
        self.settime.set_text(time)
        cmd = "su -c 'date --set \""+time+"\"'"
        print 'cmd', cmd
        pid = Popen(cmd,stdout=PIPE,stderr=PIPE, shell=True)
        result, err = pid.communicate()
        print 'date result', result, 'err', err
        cmd = "su -c '/usr/sbin/hwclock -w'"
        pid=Popen(cmd, stdout=PIPE, stderr=PIPE,  shell=True)
        result, err = pid.communicate()
        print 'hwclock result', result, 'err', err
        
