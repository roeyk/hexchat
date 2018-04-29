# Common-Users
# Copyright (2018) Roey Katz

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

__module_name__ = "common-users"
__module_version__ = "1.0"
__module_description__ = "show a list of other channels shared by you and other users in the channel"

# note: this file goes in ~/.config/hexchat/addons/

# next steps:
# 1. fix any bugs [done!]
# 2. hook it into a callable command (say, /common) [done!]
# 3. hook it so that it runs when joining a new channel (really?)
# 4. optimization: cache user channel lists in a dict instead of repeatedly calling get_list("users") [done!]

import hexchat

# the /common command callback - note, we do nothing with the supplied params
def common_cb(word=None, word_eol=None, userdata=None):

    global hexchat
    context = hexchat.get_context()    
    
    # get list of users in the current channel and construct a dict from it
    user_list = hexchat.get_list("users")
    names_dict = {u.nick:[] for u in user_list}
    channel_list = hexchat.get_list("channels")
    
    # get current channel name and current user nick
    cur_channel_name = context.get_info('channel')
    cur_nick = context.get_info('nick')
    
    # cache user lists in a dict of channelname : user lists
    channels_dict = {c.channel:c.context.get_list("users") for c in channel_list}

    # for every user in the current channel...
    for u in user_list:
        
      # (skipping over ourselves)
      if u.nick == cur_nick: continue
        
      # ...loop through userlists of other channels...
      for c in channel_list:
          
          # (skipping our current channel we're both on)
          if c.channel==cur_channel_name:  continue
          
          # ...to see if they share that channel in common with us
          c_user_list = [c_u.nick for c_u in channels_dict[c.channel]]

          # if we do share another channel in common, add it to the names_dict
          if u.nick in c_user_list:
            names_dict[u.nick].append(c.channel)
                
    # for every user in the current channel...
    for n in names_dict.keys():
        
        # (skipping over users who don't share any other channels with us)
        if len(names_dict[n])==0:  continue

        # print that user's list of common channels they share with us
        chans = ', '.join(sorted(names_dict[n]))        
        hexchat.prnt('{} ({}): {}'.format(n, len(names_dict[n]), chans))

        
# main function: set up the hook callback ("/common")
if __name__=="__main__":
    hexchat.hook_command("COMMON", common_cb, help="/COMMON show a list of other channels shared by you and other users in the channel")
