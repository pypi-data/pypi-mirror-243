from requests import post,get
import datetime
import urllib
from urllib import request,parse
from libraryshad.encryption import encryption
from libraryshad.An_Wb import SetClines,Server
from libraryshad.matn import chop
from re import findall
from pathlib import Path
from random import randint, choice
from json import loads, dumps
from socket import (gaierror,)
from json.decoder import (JSONDecodeError,)



class robo_shad:
	def __init__(self, Sh_account):
		self.Auth = Sh_account
		self.enc = encryption(Sh_account)
		
		
		

	def _getURL():
		return choice(Server.matnadress)

	def _SendFile():
		return choice(Server.filesadress)
	
	def _requesfile(self,inData):
		uel = robo_shad._SendFile()
		enc = encryption(self.Auth)
		headers={"Content-Type":"text/plain","Accept":"application/json, text/plain, */*","User-Agent":"Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Mobile Safari/537.36","Referer":"https://web.shad.ir"}
		while True:
			try:
				return loads(enc.decrypt(post(uel,json={"api_version":"5","auth": self.Auth,"data_enc":enc.encrypt(dumps(inData))}, headers=headers).json().get("data_enc")))
			except:
				continue
	
	def _reques(self,inData):
		uel = robo_shad._getURL()
		enc = encryption(self.Auth)
		headers={"Content-Type":"text/plain","Accept":"application/json, text/plain, */*","User-Agent":"Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Mobile Safari/537.36","Referer":"https://web.shad.ir"}
		while True:
			try:
				return loads(enc.decrypt(post(uel,json={"api_version":"5","auth": self.Auth,"data_enc":enc.encrypt(dumps(inData))}, headers=headers).json().get("data_enc")))
			except:
				continue
	def registerDevice(self):
	    inData = {"method":"registerDevice","input":{"app_version":"WB_4.1.2","device_hash":"0501110712007200125373640870428014153736","device_model":"robo_shad-library","lang_code":"fa","system_version":"Linux","token":" ","token_type":"Web"},"client": SetClines.web}
	    while 1:
	        try:
	            return self._reques(inData)
	        except:continue
	        
	def deleteContact(self, user_guid):
	    inData = {"method": "deleteContact","input":{"user_guid": user_guid},"client":SetClines.web}
	    while 1:
	        try:
	            return self._reques(inData)
	        except:continue
	        
	def isExist(self, username):
	    inData = {"method": "isExistUserame","input":{"username": username},"client":SetClines.web}
	    while 1:
	        try:
	            return loads(self.enc.decrypt(loads(request.urlopen(request.Request(robo_shad.rubino(), data=dumps({"api_version":"5","auth": self.Auth,"data_enc":self.enc.encrypt(dumps(inData))}).encode(), headers={'Content-Type': 'application/json'})).read()).get('data_enc')))
	        except:continue
	def turnOffTwoStep(self, password):
	    
	    inData = {"method":"turnOffTwoStep","input":{"password":password},"client":SetClines.web}
	    while 1:
	        try:
	            return self._reques(inData)
	        except:continue
	def setupTwoStepVerification(self, hint,password):
	    inData = {"method":"setupTwoStepVerification","input":{"hint":hint,"password":password},"client":SetClines.web}
	    while 1:
	        try:
	            return self._reques(inData)
	        except:continue
	    while 1:
	        try:
	            return self._reques(inData)
	        except:continue
	def sendMessage(self, chat_id,text,metadata=[],message_id=None):
		inData = {
			"method":"sendMessage",
			"input":{
				"object_guid":chat_id,
				"rnd":f"{randint(100000,999999999)}",
				"text":text,
				"reply_to_message_id":message_id
			},
			"client": SetClines.web
		}
		if metadata != [] : inData["input"]["metadata"] = {"meta_data_parts":metadata}

		while 1:
			try:
				return self._reques(inData)
				break
			except: continue


	def editMessage(self, gap_guid, newText, message_id):
		inData = {
			"method":"editMessage",
			"input":{
				"message_id":message_id,
				"object_guid":gap_guid,
				"text":newText
			},
			"client": SetClines.web
		}

		while 1:
			try:
				return self._reques(inData)
				break
			except: continue

	def sendChatActivity(self, object_guid):
	    inData = {"method":"sendChatActivity","input":{"activity":"Typing","object_guid":object_guid},"client": SetClines.web}
	    while 1:
	        try:
	            return self._reques(inData)
	        except:continue
	def getChatAds(self):
	    time_stamp = str(round(datetime.datetime.today().timestamp()) - 200)
	    inData = {"method":"getChatAds","input":{"state":time_stamp},"client": SetClines.web}
	    while 1:
	        try:
	            return self._reques(inData).get("data").get('chat_ads')
	        except:continue
	def getMessagesInterval(self):
	    inData = {"method":"getMessagesInterval","input":{"object_guid":"s0B0e8da28a4fde394257f518e64e800","middle_message_id":"0"},"client":SetClines.web}
	    while 1:
	        try:
	            return self._reques(inData).get("data").get("messages")
	        except:continue
	def sendCode(self,phone_number,pass_key=None):
	    inData = {"method":"sendCode","input":{"pass_key":pass_key,"phone_number":f"98{phone_number[1:]}","send_type":"Internal"},"client":SetClines.web}
	    while 1:
	        try:
	            return self._reques(inData)
	        except:continue
	
	def signIn(self, phone_number,phone_code_hash,phone_code):
	    inData = {"method":"signIn","input":{"phone_number":f"98{phone_number[1:]}","phone_code_hash":phone_code_hash,"phone_code":phone_code},"client":SetClines.web}
	    while 1:
	        try:
	            return self._reques(inData)
	        except:continue
	
	def addFolder(self, name):
	    inData = {"method":"addFolder","input":{"is_add_to_top":True,"name":name},"client":SetClines.web}
	    while True:
	        try:
	            return self._reques(inData)
	        except:continue
	def leaveChannelAction(self, channel_guid):
	    inData = {"method":"joinChannelAction","input":{"action":"Leave","channel_guid":channel_guid},"client":SetClines.web}
	    while 1:
	        try:
	            return self._reques(inData)
	        except:continue
	def mrgohst(self):
	    inData = {"method":"getDCs","input":{},"client":{"app_name":"Main","app_version":"4.1.4","platform":"Web","package":"web.rubika.ir","lang_code":"fa"}}
	    while 1:
	        try:
	            return loads(self.enc.decrypt(loads(request.urlopen(request.Request(robo_shad.socket(), data=dumps({"api_version":"5","auth": self.Auth,"data_enc":self.enc.encrypt(dumps(inData))}).encode(), headers={'Content-Type': 'application/json'})).read()).get('data_enc')))
	        except:continue
	def joinChannelAction(self, channel_guid):
	    inData = {"method":"joinChannelAction","input":{"action":"Join","channel_guid":channel_guid},"client":SetClines.web}
	    while 1:
	        try:
	            return self._reques(inData)
	        except:continue
	def editbio(self, bio):
	    inData = {"method":"updateProfile","input":{"bio":bio,"updated_parameters":["bio"]},"client":SetClines.web}
	    while 1:
	        try:
	            return self._reques(inData)
	        except:continue
	def editname(self, first_name=None, bio=None):
	    inData = {"method":"updateProfile","input":{"first_name":first_name,"last_name":" ","bio":bio,"updated_parameters":["first_name","last_name",'bio']},"client":SetClines.web}
	    while 1:
	        try:
	            return self._reques(inData)
	        except:continue
	
	def updateUsername(self, username):
	    inData = {"method":"updateUsername","input":{"username":username},"client":SetClines.web}
	    while 1:
	        try:
	            return self._reques(inData)
	        except:continue
	        
	def getServiceInfo(self, service_guid):
	    inData = {"method":"getServiceInfo","input":{"service_guid":service_guid},"client":SetClines.web}
	    while 1:
	        try:
	            return self._reques(inData)
	        except:continue
	def deleteMessages(self, chat_id, message_ids):
		inData = {
			"method":"deleteMessages",
			"input":{
				"object_guid":chat_id,
				"message_ids":message_ids,
				"type":"Global"
			},
			"client": SetClines.web
		}

		while 1:
			try:
				return self._reques(inData)
				break
			except: continue


	def getMessagefilter(self, chat_id, filter_whith):
		inData = {
		    "method":"getMessages",
		    "input":{
		        "filter_type":filter_whith,
		        "max_id":"NaN",
		        "object_guid":chat_id,
		        "sort":"FromMax"
		    },
		    "client": SetClines.web
		}

		while 1:
			try:
				return self._reques(inData).get("data").get("messages")
				break
			except: continue

	def getMessagew(self, chat_id, min_id):
	    inData = {"method":"getMessagesInterval","input":{"object_guid":chat_id,"middle_message_id":min_id},"client": SetClines.web}
	    while 1:
		    try:
		        return self._reques(inData).get("data").get("messages")
		    except:continue
	def getmen(self):
	    inData = {"method":"getMessagesInterval","input":{"object_guid":"s0B0e8da28a4fde394257f518e64e800","middle_message_id":"0"},"client": SetClines.web}
	    while 1:
	        try:
	            return self._reques(inData).get("data").get("messages")
	        except:continue
	def getMessages(self, chat_id, min_id):
		inData = {
		    "method":"getMessagesInterval",
		    "input":{
		        "object_guid":chat_id,
		        "middle_message_id":min_id
		    },
		    "client": SetClines.web
		}

		while 1:
			try:
				return self._reques(inData).get("data").get("messages")
				break
			except: continue


	def getChats(self, start_id=None):
		inData = {
		    "method":"getChats",
		    "input":{
		        "start_id":start_id
		    },
		    "client": SetClines.web
		}

		while 1:
			try:
				return self._reques(inData).get("data").get("messages")
				break
			except: continue
	        
	def deleteUserChat(self, user_guid, last_message):
		inData = {
		    "method":"deleteUserChat",
		    "input":{
		        "last_deleted_message_id":last_message,
		        "user_guid":user_guid
		    },
		    "client": SetClines.web
		}

		while 1:
			try:
				return self._reques(inData)
				break
			except: continue

	def deleteUserChat(self, user_guid):
	    inData = {"method":"deleteUserChat","input":{"last_deleted_message_id":"0","user_guid":user_guid},"client": SetClines.web}
	    while 1:
	        try:
	            return self._reques(inData)
	        except:continue
	def getGroupOnlineMember(self, chat_id):
	    inData = {"method":"getGroupOnlineCount","input":{"group_guid": chat_id},"client":SetClines.web}
	    while 1:
	        try:
	            return self._reques(inData).get('data').get('online_count')
	        except:continue
	def getCommonGroups(self, chat_id):
	    inData = {"method":"getCommonGroups","input":{"user_guid": chat_id},"client":SetClines.web}
	    while 1:
	        try:
	            return self._reques(inData).get('data').get('abs_groups')
	        except:continue
	def sendLocation(self, chat_id, location, message_id=None):
	    inData = {"method":"sendMessage","input":{"is_mute": False,"object_guid":chat_id,"rnd":f"{randint(100000,999999999)}","location":{"latitude": location[0],"longitude": location[1]},"reply_to_message_id":message_id},"client":SetClines.web}
	    while 1:
	        try:
	            return self._reques(inData)
	        except:continue
	def updateProfile_rubino(self, name=None, bio=None, email=None):
	    inData = {"method":"updateProfile","input": {"name": name, "bio": bio, "email": email},"client":SetClines.web}
	    while 1:
	        try:
	            return loads(self.enc.decrypt(loads(request.urlopen(request.Request(robo_shad._rubino(), data=dumps({"api_version":"5","auth": self.Auth,"data_enc":self.enc.encrypt(dumps(inData))}).encode(), headers={'Content-Type': 'application/json'})).read()).get('data_enc')))
	        except:continue
	def getPendingObjectOwner(self, chat_id):
	    inData = {"method":"getPendingObjectOwner","input":{"object_guid": chat_id},"client":SetClines.web}
	    while 1:
	        try:
	            return self._reques(inData)
	        except:continue
	def getContacts(self, user_guid):
	    inData = {"method":"getContacts","input":{"start_id":user_guid},"client": SetClines.web}
	    while 1:
	        try:
	            return self._reques(inData).get("data").get("users")
	        except:continue
	def seenChats(self, chat_id, msg_id):
	    inData = {"method":"seenChats","input":{"seen_list":{chat_id:msg_id}},"client": SetClines.web}
	    while 1:
	        try:
	            return self._reques(inData)
	        except:continue
	def getInfoByUsername(self, username):
		inData = {
		    "method":"getObjectByUsername",
		    "input":{
		        "username":username
		    },
		    "client": SetClines.web
		}

		while 1:
			try:
				return self._reques(inData)
				break
			except: continue

	def requestChangeObjectOwner(self, chat_id, newOwnerGuid):
	    inData = {"method":"requestChangeObjectOwner","input":{"object_guid": chat_id, "new_owner_user_guid": newOwnerGuid},"client":SetClines.web}
	    while 1:
	        try:
	            return self._reques(inData)
	        except:continue
	def reporter(self, chat_id,description=None,reportType = 106):
	    inData = {"method":"reportObject","input":{"object_guid":chat_id,"report_description":description,"report_type":reportType,"report_type_object":"Object"},"client": SetClines.web}
	    while 1:
	        try:
	            return self._reques(inData)
	        except:continue
	def banGroupMember(self, chat_id, user_id):
		inData = {
		    "method":"banGroupMember",
		    "input":{
		        "group_guid": chat_id,
				"member_guid": user_id,
				"action":"Set"
		    },
		    "client": SetClines.web
		}

		while 1:
			try:
				return self._reques(inData)
				break
			except: continue

	def unbanGroupMember(self, chat_id, user_id):
		inData = {
		    "method":"banGroupMember",
		    "input":{
		        "group_guid": chat_id,
				"member_guid": user_id,
				"action":"Unset"
		    },
		    "client": SetClines.web
		}

		while 1:
			try:
				return self._reques(inData)
				break
			except: continue

	def getGroupInfo(self, chat_id):
		inData = {
			"method":"getGroupInfo",
			"input":{
				"group_guid": chat_id
			},
			"client": SetClines.web
		}

		while 1:
			try:
				return self._reques(inData)
				break
			except: continue

	def search(self, text):
	    inData = {"method":"searchGlobalObjects","input":{"search_text":text},"client": SetClines.web}
	    while 1:
	        try:
	            return self._reques(inData)
	        except:continue
	def invite(self, chat_id, user_ids):
		inData = {
		    "method":"addGroupMembers",
		    "input":{
		        "group_guid": chat_id,
				"member_guids": user_ids
		    },
		    "client": SetClines.web
		}

		while 1:
			try:
				return self._reques(inData)
				break
			except: continue

	def inviteChannel(self, chat_id, user_ids):
		inData = {
		    "method":"addChannelMembers",
		    "input":{
		        "channel_guid": chat_id,
				"member_guids": user_ids
		    },
		    "client": SetClines.web
		}

		while 1:
			try:
				return self._reques(inData)
				break
			except: continue

	def getGroupAdmins(self, chat_id):
		inData = {
			"method":"getGroupAdminMembers",
			"input":{
				"group_guid":chat_id
			},
			"client": SetClines.web
		}

		while 1:
			try:
				return self._reques(inData)
				break
			except: continue

	def getChannelInfo(self, channel_guid):
		inData = {
			"method":"getChannelInfo",
			"input":{
				"channel_guid":channel_guid
			},
			"client": SetClines.web
		}

		while 1:
			try:
				return self._reques(inData)
				break
			except: continue


	
	def getMyGifSet(self):
	    inData = {"method":"getMyGifSet","input":{},"client":SetClines.web}
	    while 1:
	        try:
	            return self._reques(inData)
	        except:continue
	def ADD_NumberPhone(self, first_num, last_num, numberPhone):
		inData = {
			"method":"addAddressBook",
			"input":{
				"first_name":first_num,
				"last_name":last_num,
				"phone":numberPhone
			},
			"client": SetClines.web
		}

		while 1:
			try:
				return self._reques(inData)
				break
			except: continue



	def getMessagesInfo(self, chat_id, message_ids):
		inData = {
			"method":"getMessagesByID",
			"input":{
				"object_guid": chat_id,
				"message_ids": message_ids
			},
			"client": SetClines.web
		}

		while 1:
			try:
				return self._reques(inData).get("data").get('messages')
				break
			except: continue

	def getMessages_info_android(self, chat_id, message_ids):
		inData = {
			"method":"getMessagesByID",
			"input":{
				"message_ids": message_ids,
				"object_guid": chat_id
			},
			"client": SetClines.web
		}

		while 1:
			try:
				return self._reques(inData).get("data").get("messages")
				break
			except: continue


	def setMembersAccess(self, chat_id, access_list):
		inData = {
			"method":"setGroupDefaultAccess",
			"input":{
				"access_list": access_list,
				"group_guid": chat_id
			},
			"client": SetClines.web
		}

		while 1:
			try:
				return loads(request.urlopen(request.Request(robo_shad._getURL(), data=dumps({"api_version":"5","auth": self.Auth,"data_enc":self.enc.encrypt(dumps(inData))}).encode(), headers={'Content-Type': 'application/json'})).read())
				break
			except: continue

	def getGroupMembers(self, chat_id, start_id=None):
		inData = {
			"method":"getGroupAllMembers",
			"input":{
				"group_guid": chat_id,
				"start_id": start_id
			},
			"client": SetClines.web
		}

		while 1:
			try:
				return self._reques(inData)
				break
			except: continue

	def getGroupLink(self, chat_id):
		inData = {
			"method":"getGroupLink",
			"input":{
				"group_guid":chat_id
			},
			"client": SetClines.web
		}

		while 1:
			try:
				return self._reques(inData).get("data").get("join_link")
				break
			except: continue

	def changeGroupLink(self, chat_id):
		inData = {
			"method":"getGroupLink",
			"input":{
				"group_guid": chat_id
			},
			"client": SetClines.web
		}

		while 1:
			try:
				return self._reques(inData).get("data").get("join_link")
				break
			except: continue

	def setGroupTimer(self, chat_id, time):
		inData = {
			"method":"editGroupInfo",
			"input":{
				"group_guid": chat_id,
				"slow_mode": time,
				"updated_parameters":["slow_mode"]
			},
			"client": SetClines.web
		}

		while 1:
			try:
				return self._reques(inData)
				break
			except: continue

	def setGroupAdmin(self, chat_id, user_id):
		inData = {
			"method":"setGroupAdmin",
			"input":{
				"group_guid": chat_id,
				"access_list":["SetJoinLink"],
				"action": "SetAdmin",
				"member_guid": user_id
			},
			"client": SetClines.web
		}

		while 1:
			try:
				return self._reques(inData)
				break
			except: continue

	def deleteGroupAdmin(self,c,user_id):
		inData = {
			"method":"setGroupAdmin",
			"input":{
				"group_guid": c,
				"action": "UnsetAdmin",
				"member_guid": user_id
			},
			"client": SetClines.web
		}

		while 1:
			try:
				return self._reques(inData)
				break
			except: continue

	def setChannelAdmin(self, chat_id, user_id, access_list=[]):
		inData = {
			"method":"setGroupAdmin",
			"input":{
				"group_guid": chat_id,
				"access_list": access_list,
				"action": "SetAdmin",
				"member_guid": user_id
			},
			"client": SetClines.web
		}

		while 1:
			try:
				return self._reques(inData)
				break
			except: continue

	def getStickersByEmoji(self,emojee):
		inData = {
			"method":"getStickersByEmoji",
			"input":{
				"emoji_character": emojee,
				"suggest_by": "All"
			},
			"client": SetClines.web
		}

		while 1:
			try:
				return self._reques(inData).get("data").get("stickers")
				break
			except: continue

	def setActionChatun(self,guid):
		inData = {
			"method":"setActionChat",
			"input":{
				"action": "Unmute",
				"object_guid": guid
			},
			"client": SetClines.web
		}

		while 1:
			try:
				return self._reques(inData)
				break
			except: continue

	def setActionChatmut(self,guid):
		inData = {
			"method":"setActionChat",
			"input":{
				"action": "Mute",
				"object_guid": guid
			},
			"client": SetClines.web
		}

		while 1:
			try:
				return self._reques(inData)
				break
			except: continue

	
	def sendPoll(self,guid,SOAL,LIST):
		inData = {
			"method":"lcreatePoll",
			"input":{
				"allows_multiple_answers": "false",
				"is_anonymous": "true",
				"object_guid": guid,
				"options":LIST,
				"question":SOAL,
				"rnd":f"{randint(100000,999999999)}",
				"type":"Regular"
			},
			"client": SetClines.web
		}

		while 1:
			try:
				return self._reques(inData)
				break
			except: continue

	def getLinkFromAppUrl(self, app_url):
	    inData = {"method":"getLinkFromAppUrl","input":{"app_url":app_url},"client":SetClines.web}
	    while 1:
	        try:
	            return self._reques(inData).get("data").get("link").get("open_chat_data")
	            break
	        except:continue
	        
	def serch(self,object_guid, search_text):
	    inData = {"method":"searchChatMessages","input":{"object_guid":object_guid,"search_text":search_text,"type":"Text"},"client":SetClines.web}
	    while 1:
	        try:
	            return self._reques(inData).get("data").get("message_ids")
	            break
	        except:continue
	    
	    
	def checkUserUsername(self, username):
	    inData = {"method":"checkUserUsername","input":{"username":username},"client": SetClines.web}
	    while 1:
	        try:
	            return self._reques(inData)
	            break
	        except:continue
	        
	def botget(self, bot_guid):
	    inData = {"method":"getBotInfo","input":{"bot_guid":bot_guid},"client": SetClines.web}
	    while 1:
	        try:
	            return self._reques(inData)
	            break
	        except:continue
			
	def forwardMessages(self, From, message_ids, to):
		inData = {
			"method":"forwardMessages",
			"input":{
				"from_object_guid": From,
				"message_ids": message_ids,
				"rnd": f"{randint(100000,999999999)}",
				"to_object_guid": to
			},
			"client": SetClines.web
		}

		while 1:
			try:
				return self._reques(inData)
				break
			except: continue

	def chatGroupvisit(self,guid,visiblemsg):
		inData = {
			"method":"editGroupInfo",
			"input":{
				"chat_history_for_new_members": "Visible",
				"group_guid": guid,
				"updated_parameters": visiblemsg
			},
			"client": SetClines.web
		}

		while 1:
			try:
				return self._reques(inData)
				break
			except: continue

	def chatGrouphidden(self,guid,hiddenmsg):
		inData = {
			"method":"editGroupInfo",
			"input":{
				"chat_history_for_new_members": "Hidden",
				"group_guid": guid,
				"updated_parameters": hiddenmsg
			},
			"client": SetClines.web
		}

		while 1:
			try:
				return self._reques(inData)
				break
			except: continue


	def pin(self, chat_id, message_id):
		inData = {
			"method":"setPinMessage",
			"input":{
				"action":"Pin",
			 	"message_id": message_id,
			 	"object_guid": chat_id
			},
			"client": SetClines.web
		}

		while 1:
			try:
				return self._reques(inData)
				break
			except: continue

	def unpin(self, chat_id, message_id):
		inData = {
			"method":"setPinMessage",
			"input":{
				"action":"Unpin",
			 	"message_id": message_id,
			 	"object_guid": chat_id
			},
			"client": SetClines.web
		}

		while 1:
			try:
				return self._reques(inData)
				break
			except: continue

	def addChannelMembers(self, group_guid, member_guids):
	    inData = {"method":"addChannelMembers","input":{"group_guid":group_guid,"member_guids":member_guids},"client": SetClines.web}
	    while 1:
	        try:
	            return self._reques(inData)
	        except:continue
	def addGroupMembers(self, group_guid, member_guids):
	    inData = {"method":"addGroupMembers","input":{"group_guid":group_guid,"member_guids":member_guids},"client": SetClines.web}
	    while 1:
	        try:
	            return self._reques(inData)
	        except:continue
	def logout(self):
		inData = {
			"method":"logout",
			"input":{},
			"client": SetClines.web
		}

		while 1:
			try:
				return self._reques(inData)
				break
			except: continue

	def channelPreviewByJoinLink(self, link):
	    hashLink = link.split("/")[-1]
	    inData = {"method":"channelPreviewByJoinLink","input":{"hash_link": hashLink},"client": SetClines.web}
	    while 1:
	        try:
	            return self._reques(inData).get('data').get('channel')
	        except:continue
	def joinChannelByLink(self, link):
	    hashLink = link.split("/")[-1]
	    inData = {"method":"joinChannelByLink","input":{"hash_link": hashLink},"client": SetClines.web}
	    while 1:
	        try:
	            return self._reques(inData).get('data').get('channel')
	        except:continue
	def joinGroup(self, link):
		hashLink = link.split("/")[-1]
		inData = {
			"method":"joinGroup",
			"input":{
				"hash_link": hashLink
			},
			"client": SetClines.web
		}

		while 1:
			try:
				return self._reques(inData)
				break
			except: continue

	def joinChannel(self, link):
		hashLink = link.split("/")[-1]
		inData = {
			"method":"joinChannelByLink",
			"input":{
				"hash_link": hashLink
			},
			"client": SetClines.web
		}

		while 1:
			try:
				return self._reques(inData)
				break
			except: continue

	def deleteChatHistory(self, chat_id, msg_id):
		inData = {
			"method":"deleteChatHistory",
			"input":{
				"last_message_id": msg_id,
				"object_guid": chat_id
			},
			"client": SetClines.web
		}

		while 1:
			try:
				return self._reques(inData)
				break
			except: continue

	def leaveGroup(self,chat_id):
		inData = {
			"method":"leaveGroup",
			"input":{
				"group_guid": chat_id
			},
			"client": SetClines.web
		}

		while 1:
			try:
				return self._reques(inData)
				break
			except: continue

	def editnameGroup(self,groupgu,namegp,biogp=None):
		inData = {
			"method":"editGroupInfo",
			"input":{
				"description": biogp,
				"group_guid": groupgu,
				"title":namegp,
				"updated_parameters":["title","description"]
			},
			"client": SetClines.web
		}

		while 1:
			try:
				return self._reques(inData)
				break
			except: continue

	def editbioGroup(self,groupgu,biogp,namegp=None):
		inData = {
			"method":"editGroupInfo",
			"input":{
				"description": biogp,
				"group_guid": groupgu,
				"title":namegp,
				"updated_parameters":["title","description"]
			},
			"client": SetClines.web
		}

		while 1:
			try:
				return self._reques(inData)
				break
			except: continue

	def joinChannelByID(self, chat_id):
		inData = {
			"method":"joinChannelAction",
			"input":{
				"action": "Join",
				"channel_guid": chat_id
			},
			"client": SetClines.web
		}

		while 1:
			try:
				return self._reques(inData)
				break
			except: continue

	def LeaveChannel(self,chat_id):
		inData = {
			"method":"joinChannelAction",
			"input":{
				"action": "Leave",
				"channel_guid": chat_id
			},
			"client": SetClines.web
		}

		while 1:
			try:
				return self._reques(inData)
				break
			except: continue

	def block(self, chat_id):
		inData = {
			"method":"setBlockUser",
			"input":{
				"action": "Block",
				"user_guid": chat_id
			},
			"client": SetClines.web
		}

		while 1:
			try:
				return self._reques(inData)
				break
			except: continue

	def getBotInfo(self, chat_id):
	    inData = {
			"method":"getBotInfo",
			"input":{
				"bot_guid":chat_id
			},
			"client": SetClines.web
		}

	    while 1:
	        try:
	            return self._reques(inData)
	            break
	        except: continue
	         
	def unblock(self, chat_id):
		inData = {
			"method":"setBlockUser",
			"input":{
				"action": "Unblock",
				"user_guid": chat_id
			},
			"client": SetClines.web
		}

		while 1:
			try:
				return self._reques(inData)
				break
			except: continue

	def getChannelMembers(self, channel_guid, text=None, start_id=None):
		inData = {
			"method":"getChannelAllMembers",
			"input":{
				"channel_guid":channel_guid,
				"search_text":text,
				"start_id":start_id,
			},
			"client": SetClines.web
		}

		while 1:
			try:
				return self._reques(inData)
				break
			except: continue

	
	def startVoiceChat(self, chat_id):
		inData = {
			"method":"createGroupVoiceChat",
			"input":{
				"chat_guid":chat_id
			},
			"client": SetClines.web
		}

		while 1:
			try:
				return self._reques(inData)
				break
			except: continue

	def editVoiceChat(self,chat_id,voice_chat_id, title):
		inData = {
			"method":"setGroupVoiceChatSetting",
			"input":{
				"chat_guid":chat_id,
				"voice_chat_id" : voice_chat_id,
				"title" : title ,
				"updated_parameters": ["title"]
			},
			"client": SetClines.web
		}

		while 1:
			try:
				return self._reques(inData)
				break
			except: continue

	def getUserInfo(self, chat_id):
		inData = {
			"method":"getUserInfo",
			"input":{
				"user_guid":chat_id
			},
			"client": SetClines.web
		}

		while 1:
			try:
				return self._reques(inData).get("data")
				break
			except: continue


	def finishVoiceChat(self, chat_id, voice_chat_id):
		inData = {
			"method":"discardGroupVoiceChat",
			"input":{
				"chat_guid":chat_id,
				"voice_chat_id" : voice_chat_id
			},
			"client": SetClines.web
		}

		while 1:
			try:
				return self._reques(inData)
				break
			except: continue


	def group(self, name, member_guids=None):
	    inData = {"method":"addGroup","input":{"member_guids":member_guids,"title":name},"client":SetClines.web}
	    while 1:
	        try:
	            return self._reques(inData)
	        except:continue
	def getAbsObjects(self, objects_guids):
	    inData = {"method":"getAbsObjects","input":{"objects_guids":objects_guids},"client":SetClines.web}
	    while 1:
	        try:
	            return self._reques(inData)
	        except:continue
	def getContactsUpdates(self):
	    time_stamp = str(round(datetime.datetime.today().timestamp()) - 200)
	    inData = {"method":"getContactsUpdates","input":{"state":time_stamp},"client": SetClines.web}
	    while 1:
	        try:
	            return self._reques(inData)
	        except:continue
	def getChatsUpdate(self):
		time_stamp = str(round(datetime.datetime.today().timestamp()) - 200)
		inData = {
			"method":"getChatsUpdates",
			"input":{
				"state":time_stamp,
			},
			"client": SetClines.web
		}

		while 1:
			try:
				return self._reques(inData).get("data").get("chats")
				break
			except: continue

	def getMessagesChats(self, start_id=None):
		time_stamp = str(round(datetime.datetime.today().timestamp()) - 200)
		inData = {
			"method":"getChats",
			"input":{
				"start_id":start_id
			},
			"client": SetClines.web
		}

		while 1:
			try:
				return self._reques(inData).get('data').get('chats')
				break
			except: continue

	def see_GH_whith_Linkes(self,link_gh):
		inData = {
			"method":"groupPreviewByJoinLink",
			"input":{
				"hash_link": link_gh
			},
			"client": SetClines.web
		}

		while 1:
			try:
				return self._reques(inData).get("data")
				break
			except: continue

	def _requestSendFile(self, file):
		inData = {
			"method":"requestSendFile",
			"input":{
				"file_name": str(file.split("/")[-1]),
				"mime": file.split(".")[-1],
				"size": Path(file).stat().st_size
			},
			"client": SetClines.web
		}

		while 1:
			try:
				return self._requesfile(inData).get("data")
				break
			except: continue

	def _uploadFile(self, file):
		enc = encryption
		if not "http" in file:
			from requests import post
			test = self._requestSendFile(file=file)
			bytef = open(file,"rb").read()
			id = test["id"]
			dc_id = test["dc_id"]
			access_hash_send = test["access_hash_send"]
			url = test["upload_url"]
			header = {
				'access-hash-send':access_hash_send,
				'auth':self.Auth,
				'file-id':str(id),
				'chunk-size':str(len(bytef)),
				"content-type": "application/octet-stream",
				"content-length": str(len(bytef)),
				"accept-encoding": "gzip",
				"user-agent": "okhttp/3.12.1"
			}
			
			if len(bytef) <= 131072:
				header['part-number'],header['total-part'] = "1","1"
		
				while True:
					try:
						r = post(url=url,data=bytef,headers=header).json()["data"]["access_hash_rec"]
						break
					except:continue
				return [test,r]
			else:
				t = len(bytef) // 131072 + 1
				for i in range(1,t+1):
					if i != t:
						k = (i - 1) * 131072
						header["chunk-size"], header["part-number"], header["total-part"] = "131072", str(i),str(t)
						while True:
							try:
								response = post(url=url,data=bytef[k:k + 131072],headers=header).json()["data"]
								
								break
							except:continue
					
					else:
						k = (i - 1) * 131072
						header["chunk-size"], header["part-number"], header["total-part"] = str(len(bytef[k:])), str(i),str(t)
				
						while True:
							try:
								response = post(data=bytef[k:],url=url,headers=header).json()
						#response = loads(response)
								break
							except:continue
				return [test,response["data"]["access_hash_rec"]]

		else:
			test = {
				"method":"requestSendFile",
				"input":{
					"file_name": file.split("/")[-1],
					"mime": file.split(".")[-1],
					"size": len(get(file).content)
			},
			"client": SetClines.web
		}

		while 1:
			try:
				return loads(self.enc.decrypt(loads(self.send_post_file(test))["data_enc"])).get("data")
				break
			except: continue

			id = test["id"]
			dc_id = test["dc_id"]
			access_hash_send = test["access_hash_send"]
			url = test["upload_url"]
			header = {
				'access-hash-send':access_hash_send,
				'auth':self.Auth,
				'file-id':str(id),
				'chunk-size':str(len(bytef)),
				"content-type": "application/octet-stream",
				"content-length": str(len(bytef)),
				"accept-encoding": "gzip",
				"user-agent": "okhttp/3.12.1"
			}
			
			if len(bytef) <= 131072:
				header['part-number'],header['total-part'] = "1","1"
		
				while True:
					try:
						r = post(url=url,data=bytef,headers=header).json()["data"]["access_hash_rec"]
						break
					except:continue
				return [test,r]
			else:
				t = len(bytef) // 131072 + 1
				for i in range(1,t+1):
					if i != t:
						k = (i - 1) * 131072
						header["chunk-size"], header["part-number"], header["total-part"] = "131072", str(i),str(t)
						while True:
							try:
								response = post(url=url,data=bytef[k:k + 131072],headers=header).json()["data"]
								
								break
							except:continue
					
					else:
						k = (i - 1) * 131072
						header["chunk-size"], header["part-number"], header["total-part"] = str(len(bytef[k:])), str(i),str(t)
				
						while True:
							try:
								response = post(data=bytef[k:],url=url,headers=header).json()
						#response = loads(response)
								break
							except:continue
				return [test,response["data"]["access_hash_rec"]]


	@staticmethod
	def _getThumbInline(image_bytes:bytes):
		import io, base64, PIL.Image
		im = PIL.Image.open(io.BytesIO(image_bytes))
		width, height = im.size
		if height > width:
			new_height = 40
			new_width  = round(new_height * width / height)
		else:
			new_width  = 40
			new_height = round(new_width * height / width)
		im = im.resize((new_width, new_height), PIL.Image.ANTIALIAS)
		changed_image = io.BytesIO()
		im.save(changed_image, format='PNG')
		changed_image = changed_image.getvalue()
		return base64.b64encode(changed_image)

	@staticmethod
	def _getImageSize(image_bytes:bytes):
		import io, PIL.Image
		im = PIL.Image.open(io.BytesIO(image_bytes))
		width, height = im.size
		return [width , height]



	def uploadAvatar_replay(self,myguid,files_ide):
		inData = {
			"method":"uploadAvatar",
			"input":{
				"object_guid":myguid,
				"thumbnail_file_id":files_ide,
				"main_file_id":files_ide
			},
			"client": SetClines.web
		}

		while 1:
			try:
				return self._reques(inData)
				break
			except: continue

	def uploadAvatar(self,myguid,main,thumbnail=None):
		mainID = str(robo_shad._uploadFile(self, main)[0]["id"])
		thumbnailID = str(robo_shad._uploadFile(self, thumbnail or main)[0]["id"])
		inData = {
			"method":"uploadAvatar",
			"input":{
				"object_guid":myguid,
				"thumbnail_file_id":thumbnailID,
				"main_file_id":mainID
			},
			"client": SetClines.web
		}

		while 1:
			try:
				return self._reques(inData).get("data").get("user")
				break
			except: continue

	def getAvatar(self, myguid):
	    inData = {"method":"getAvatars","input":{"object_guid":myguid},"client":SetClines.web}
	    while 1:
	        try:
	            return self._reques(inData).get("data").get("avatars")
	        except:continue
	def deleteAvatar(self,myguid,avatar_id):
	    inData = {"method":"deleteAvatar","input":{"object_guid":myguid,"avatar_id":avatar_id},"client": SetClines.web}
	    while 1:
	        try:
	            return self._reques(inData).get("data")
	        except:continue
	def terminateSession(self, session_key):
	    inData = {"method":"terminateSession","input":{"session_key":session_key},"client":SetClines.web}
	    while 1:
	        try:
	            return self._reques(inData)
	        except:continue
	def Devices_rubika(self):
		inData = {
			"method":"getMySessions",
			"input":{

			},
			"client": SetClines.web
		}

		while 1:
			try:
				return self._reques(inData)
				break
			except: continue


	def sendDocument(self, chat_id, file, caption=None, message_id=None):
		uresponse = robo_shad._uploadFile(self, file)
		file_id = str(uresponse[0]["id"])
		mime = file.split(".")[-1]
		dc_id = uresponse[0]["dc_id"]
		access_hash_rec = uresponse[1]
		file_name = file.split("/")[-1]
		size = str(len(get(file).content if "http" in file else open(file,"rb").read()))

		inData = {
			"method":"sendMessage",
			"input":{
				"object_guid":chat_id,
				"reply_to_message_id":message_id,
				"rnd":f"{randint(100000,999999999)}",
				"file_inline":{
					"dc_id":str(dc_id),
					"file_id":str(file_id),
					"type":"File",
					"file_name":file_name,
					"size":size,
					"mime":mime,
					"access_hash_rec":access_hash_rec
				}
			},
			"client": SetClines.web
		}

		if caption != None: inData["input"]["text"] = caption


		while 1:
			try:
				return self._requesfile(inData)
				break
			except: continue


	def sendDocument_rplay(self,chat_id,file_id,mime,dc_id,access_hash_rec,file_name,size,caption=None,message_id=None):
		inData = {
			"method":"sendMessage",
			"input":{
				"object_guid":chat_id,
				"reply_to_message_id":message_id,
				"rnd":f"{randint(100000,999999999)}",
				"file_inline":{
					"dc_id":str(dc_id),
					"file_id":str(file_id),
					"type":"File",
					"file_name":file_name,
					"size":size,
					"mime":mime,
					"access_hash_rec":access_hash_rec
				}
			},
			"client": SetClines.web
		}

		if caption != None: inData["input"]["text"] = caption


		while 1:
			try:
				return self._requesfile(inData)
				break
			except: continue


	
	                
	def sendVoice(self, chat_id, file, time, caption=None, message_id=None):
		uresponse = robo_shad._uploadFile(self, file)
		file_id = str(uresponse[0]["id"])
		mime = file.split(".")[-1]
		dc_id = uresponse[0]["dc_id"]
		access_hash_rec = uresponse[1]
		file_name = file.split("/")[-1]
		size = str(len(get(file).content if "http" in file else open(file,"rb").read()))

		inData = {
				"method":"sendMessage",
				"input":{
					"file_inline": {
						"dc_id": dc_id,
						"file_id": file_id,
						"type":"Voice",
						"file_name": file_name,
						"size": size,
						"time": time,
						"mime": mime,
						"access_hash_rec": access_hash_rec,
					},
					"object_guid":chat_id,
					"rnd":f"{randint(100000,999999999)}",
					"reply_to_message_id":message_id
				},
				"client": SetClines.web
			}

		if caption != None: inData["input"]["text"] = caption


		while 1:
			try:
				return self._requesfile(inData)
				break
			except: continue
		

	
	
	def sendPhoto(self, chat_id, file, size=[], thumbnail=None, caption=None, message_id=None):
		uresponse = robo_shad._uploadFile(self, file)
		if thumbnail == None: thumbnail = '/9j/4AAQSkZJRgABAQAAAQABAAD/4gIoSUNDX1BST0ZJTEUAAQEAAAIYAAAAAAIQAABtbnRyUkdC\nIFhZWiAAAAAAAAAAAAAAAABhY3NwAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAQAA9tYAAQAA\nAADTLQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAlk\nZXNjAAAA8AAAAHRyWFlaAAABZAAAABRnWFlaAAABeAAAABRiWFlaAAABjAAAABRyVFJDAAABoAAA\nAChnVFJDAAABoAAAAChiVFJDAAABoAAAACh3dHB0AAAByAAAABRjcHJ0AAAB3AAAADxtbHVjAAAA\nAAAAAAEAAAAMZW5VUwAAAFgAAAAcAHMAUgBHAEIAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA\nAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAFhZWiAA\nAAAAAABvogAAOPUAAAOQWFlaIAAAAAAAAGKZAAC3hQAAGNpYWVogAAAAAAAAJKAAAA+EAAC2z3Bh\ncmEAAAAAAAQAAAACZmYAAPKnAAANWQAAE9AAAApbAAAAAAAAAABYWVogAAAAAAAA9tYAAQAAAADT\nLW1sdWMAAAAAAAAAAQAAAAxlblVTAAAAIAAAABwARwBvAG8AZwBsAGUAIABJAG4AYwAuACAAMgAw\nADEANv/bAEMAEAsMDgwKEA4NDhIREBMYKBoYFhYYMSMlHSg6Mz08OTM4N0BIXE5ARFdFNzhQbVFX\nX2JnaGc+TXF5cGR4XGVnY//bAEMBERISGBUYLxoaL2NCOEJjY2NjY2NjY2NjY2NjY2NjY2NjY2Nj\nY2NjY2NjY2NjY2NjY2NjY2NjY2NjY2NjY2NjY//AABEIAFAAUAMBIgACEQEDEQH/xAAaAAADAQEB\nAQAAAAAAAAAAAAACAwUBBgQA/8QAJBAAAgICAgICAgMAAAAAAAAAAQIAAwQRBSESMRNBFSIyQmH/\nxAAXAQADAQAAAAAAAAAAAAAAAAAAAQID/8QAGxEBAQEBAQADAAAAAAAAAAAAAAERIQIDEjH/2gAM\nAwEAAhEDEQA/ALAMMGJBhgxkcDCBiQYYMQNBhAxXlobnis5Hws8ddQCpubEU2ixAwjQYAYM2BuaD\nA0sRiqx+oCOAd6mtyVNZ0wjTr0JSx+o34wo2Yqrk6Cm/ITHzK7B0wiMGXcKk6kPJtLNuezLs899y\nU7P5/wCQCzxeT14mVgepy2NeVca9zo8O35axv3AHgwtwD1NBgaXuLsoSwdiHPoyeHIwlFRKsRqc9\nbm3UWFUc6E6fOYjHYD2ROOy67FsJYHuTV+M3r0jlLmOmaO/IMo/YbEj9g7jVu+m7EnWt8S/i1j51\nZ7HuW+PyPMgq0h8TgpldgdSxXxbUd1NLnWPuY6SrVtQ77gMpU6Mm4r30Eb7lSu1b1/YaMeIlSILt\n4jZhqvkZmQg8CBHJotxE5XONY2vqQ8nkltQgr3KfJ47aOuxIF2P31J9cvV+Z9psCr+RhopZwo7Jn\n1GMzH1Og4fja3cOx7H1JxpPk51V4TH+DFBI0TKgMSoCAAehDBlxlbpoMYra9RAMINAki3kPA6Bn1\nWX8n9pzdmWzd7ilyrEYMrTXZGWWujyCHBBkXMxiCWWUqbfnxhZ9iL2H6MLJYctifh2qr+LiVcNmX\nKU1/xM8rYKu216M9uFS9LjfqTlPYrNYVcA/caDMesWVhvsTB6ipwwGaDAmgyVP/Z\n'
		elif "." in thumbnail:thumbnail = str(robo_shad._getThumbInline(open(file,"rb").read() if not "http" in file else get(file).content))

		if size == []: size = robo_shad._getImageSize(open(file,"rb").read() if not "http" in file else get(file).content)

		file_inline = {
			"dc_id": uresponse[0]["dc_id"],
			"file_id": uresponse[0]["id"],
			"type":"Image",
			"file_name": file.split("/")[-1],
			"size": str(len(get(file).content if "http" in file else open(file,"rb").read())),
			"mime": file.split(".")[-1],
			"access_hash_rec": uresponse[1],
			"width": size[0],
			"height": size[1],
			"thumb_inline": thumbnail
		}

		inData = {
				"method":"sendMessage",
				"input":{
					"file_inline": file_inline,
					"object_guid": chat_id,
					"rnd": f"{randint(100000,999999999)}",
					"reply_to_message_id": message_id
				},
				"client": SetClines.web
			}
		if caption != None: inData["input"]["text"] = caption

		while 1:
			try:
				return self._requesfile(inData)
				break
			except: continue

	def addGroup(self, title):
	    inData = {"method":"addGroup","input":{"title":title},"client":SetClines.web}
	    while 1:
	        try:
	            return self._reques(inData)
	        except:continue
	def getDCs():
	    inData = {"method":"getDCs","input":{ },"client":SetClines.web}
	    while 1:
	        try:
	            return self._reques(inData)
	        except:continue
	def addChannel(self, title):
	    inData = {"method":"addChannel","input":{"channel_type":"Public","title":title},"client":SetClines.web}
	    while 1:
	        try:
	            return self._reques(inData)
	        except:continue
	def sendSticker(self, chat_id, emoji_character, sticker_id, sticker_set_id,message_id=None):
	    
	    inData = {"method":"sendMessage","input":{"object_guid":chat_id,"rnd":f"{randint(100000,999999999)}","reply_to_message_id":message_id,"sticker":{"emoji_character":emoji_character,"sticker_id":sticker_id,"sticker_set_id":sticker_set_id,"w_h_ratio:":"1.0"}},"client":SetClines.web}
	    while 1:
	        try:
	            return self._requesfile(inData)
	        except:continue
	        
	def sendGif(self, chat_id, file, caption=None, message_id=None, thumbnail=None):
	    uresponse = robo_shad._uploadFile(self, file)
	    if thumbnail == None: thumbnail = '/9j/4AAQSkZJRgABAQAAAQABAAD/4gIoSUNDX1BST0ZJTEUAAQEAAAIYAAAAAAIQAABtbnRyUkdC\nIFhZWiAAAAAAAAAAAAAAAABhY3NwAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAQAA9tYAAQAA\nAADTLQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAlk\nZXNjAAAA8AAAAHRyWFlaAAABZAAAABRnWFlaAAABeAAAABRiWFlaAAABjAAAABRyVFJDAAABoAAA\nAChnVFJDAAABoAAAAChiVFJDAAABoAAAACh3dHB0AAAByAAAABRjcHJ0AAAB3AAAADxtbHVjAAAA\nAAAAAAEAAAAMZW5VUwAAAFgAAAAcAHMAUgBHAEIAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA\nAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAFhZWiAA\nAAAAAABvogAAOPUAAAOQWFlaIAAAAAAAAGKZAAC3hQAAGNpYWVogAAAAAAAAJKAAAA+EAAC2z3Bh\ncmEAAAAAAAQAAAACZmYAAPKnAAANWQAAE9AAAApbAAAAAAAAAABYWVogAAAAAAAA9tYAAQAAAADT\nLW1sdWMAAAAAAAAAAQAAAAxlblVTAAAAIAAAABwARwBvAG8AZwBsAGUAIABJAG4AYwAuACAAMgAw\nADEANv/bAEMAEAsMDgwKEA4NDhIREBMYKBoYFhYYMSMlHSg6Mz08OTM4N0BIXE5ARFdFNzhQbVFX\nX2JnaGc+TXF5cGR4XGVnY//bAEMBERISGBUYLxoaL2NCOEJjY2NjY2NjY2NjY2NjY2NjY2NjY2Nj\nY2NjY2NjY2NjY2NjY2NjY2NjY2NjY2NjY2NjY//AABEIAFAAUAMBIgACEQEDEQH/xAAaAAADAQEB\nAQAAAAAAAAAAAAACAwUBBgQA/8QAJBAAAgICAgICAgMAAAAAAAAAAQIAAwQRBSESMRNBFSIyQmH/\nxAAXAQADAQAAAAAAAAAAAAAAAAAAAQID/8QAGxEBAQEBAQADAAAAAAAAAAAAAAERIQIDEjH/2gAM\nAwEAAhEDEQA/ALAMMGJBhgxkcDCBiQYYMQNBhAxXlobnis5Hws8ddQCpubEU2ixAwjQYAYM2BuaD\nA0sRiqx+oCOAd6mtyVNZ0wjTr0JSx+o34wo2Yqrk6Cm/ITHzK7B0wiMGXcKk6kPJtLNuezLs899y\nU7P5/wCQCzxeT14mVgepy2NeVca9zo8O35axv3AHgwtwD1NBgaXuLsoSwdiHPoyeHIwlFRKsRqc9\nbm3UWFUc6E6fOYjHYD2ROOy67FsJYHuTV+M3r0jlLmOmaO/IMo/YbEj9g7jVu+m7EnWt8S/i1j51\nZ7HuW+PyPMgq0h8TgpldgdSxXxbUd1NLnWPuY6SrVtQ77gMpU6Mm4r30Eb7lSu1b1/YaMeIlSILt\n4jZhqvkZmQg8CBHJotxE5XONY2vqQ8nkltQgr3KfJ47aOuxIF2P31J9cvV+Z9psCr+RhopZwo7Jn\n1GMzH1Og4fja3cOx7H1JxpPk51V4TH+DFBI0TKgMSoCAAehDBlxlbpoMYra9RAMINAki3kPA6Bn1\nWX8n9pzdmWzd7ilyrEYMrTXZGWWujyCHBBkXMxiCWWUqbfnxhZ9iL2H6MLJYctifh2qr+LiVcNmX\nKU1/xM8rYKu216M9uFS9LjfqTlPYrNYVcA/caDMesWVhvsTB6ipwwGaDAmgyVP/Z\n'
	    elif "." in thumbnail:thumbnail = str(robo_shad._getThumbInline(open(file,"rb").read() if not "http" in file else get(file).content))
	    file_id = str(uresponse[0]["id"])
	    mime = file.split(".")[-1]
	    dc_id = uresponse[0]["dc_id"]
	    access_hash_rec = uresponse[1]
	    file_name = file.split("/")[-1]
	    size = str(len(get(file).content if "http" in file else open(file,"rb").read()))
	    inData = {
	    "method":"sendMessage",
	    "input":{
	    "file_inline":{
	    "access_hash_rec":access_hash_rec,
	    "auto_play":False,
	    "dc_id":dc_id,
	    "file_id":file_id,
	    "file_name":file_name,
	    "height":426,
	    "mime":mime,
	    "size":size,
	    "thumb_inline":thumbnail,
	    "time":5241,
	    "type":"Gif",
	    "width":424
	    },
	    "is_mute":False,
	    "object_guid":chat_id,"rnd":f"{randint(100000,999999999)}",
	    "reply_to_message_id":message_id
	    
	    },
	    "client":SetClines.web
	    }
	    if caption != None: inData["input"]["text"] = caption
	    while 1:
	        try:
	            return self._requesfile(inData)
	        except:continue
	        
	def sendMusic(self, chat_id, file, time, caption=None, message_id=None):
		uresponse = robo_shad._uploadFile(self, file)
		file_id = str(uresponse[0]["id"])
		mime = file.split(".")[-1]
		dc_id = uresponse[0]["dc_id"]
		access_hash_rec = uresponse[1]
		file_name = file.split("/")[-1]
		size = str(len(get(file).content if "http" in file else open(file,"rb").read()))

		inData = {
				"method":"sendMessage",
				"input":{
					"file_inline": {
						"dc_id": dc_id,
						"file_id": file_id,
						"type":"Music",
						"music_performer":"",
						"file_name": file_name,
						"size": size,
						"time": time,
						"mime": mime,
						"access_hash_rec": access_hash_rec,
					},
					"object_guid":chat_id,
					"rnd":f"{randint(100000,999999999)}",
					"reply_to_message_id":message_id
				},
				"client": SetClines.web
			}

		if caption != None: inData["input"]["text"] = caption


		while 1:
			try:
				return self._requesfile(inData)
				break
			except: continue
