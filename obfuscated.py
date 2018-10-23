""
UM=ImportError
Ud=True
Ut=super
UA=None
Um=str
Uo=ValueError
Uv=type
UE=bool
UG=open
Ui=callable
Ur=staticmethod
Ua=OSError
UO=print
Uw=list
UP=False
Ux=IndexError
US=AttributeError
UB=KeyError
UR=LookupError
Uz=isinstance
UQ=TypeError
Uy=RuntimeError
UK=KeyboardInterrupt
Uf=vars
UC=input
UH=SystemExit
import argparse
us=argparse.ArgumentParser
import base64
uN=base64.b64decode
import errno
uF=errno.EEXIST
import os
ue=os.remove
uc=os.makedirs
uk=os.path
import sys
uY=sys.exgt
uj=sys.exit
uT=sys.stdout
import copy
up=copy.copy
import logging
Ul=logging.propagate
Un=logging.WARNING
Uu=logging.getLogger
uq=logging.StreamHandler
uW=logging.Logger
ug=logging.ERROR
uV=logging.INFO
uh=logging.DEBUG
uX=logging.Formatter
from distutils.util import strtobool
from distutils.spawn import find_executable
from datetime import datetime
Ub=datetime.now
from subprocess import Popen,PIPE
try:
 import configparser
except UM:
 import ConfigParser as configparser
import requests
import pyperclip
UJ=pyperclip.copy
__author__="Sean Pianka"
__email__="pianka@eml.cc"
__version__="2.0.0"
u={"CONFIG_PATH":uk.expanduser("~/.config/pysee/pysee.conf"),"SAVE_DIR":uk.expanduser("~/Pictures/Screenshots"),"MODE":"region","CLIPBOARD":Ud,"UPLOAD":Ud,"LOGGING":Ud,"SAVE":Ud,}
class b(uX):
 U="[*] ERROR: %(msg)s"
 n="[-] DEBUG: %(module)s: %(lineno)d: %(msg)s"
 l="[+] %(msg)s"
 def __init__(J):
  Ut(b,J).__init__(fmt="%(levelno)d: %(msg)s",datefmt=UA)
 def ua(D,OO00O000OOO000OO0):
  L=D._style._fmt
  if OO00O000OOO000OO0.levelno==uh:
   D._style._fmt=b.dbg_fmt
  elif OO00O000OOO000OO0.levelno==uV:
   D._style._fmt=b.info_fmt
  elif OO00O000OOO000OO0.levelno==ug:
   D._style._fmt=b.err_fmt
  M=uX.format(D,OO00O000OOO000OO0)
  D._style._fmt=L
  return M
class uK(uW):
 def __init__(OO000OO0OO0OO0OO0,*O000OO0O0O0O0OO0O,**O00OO0000OO00O000):
  Ut(uK,OO000OO0OO0OO0OO0).__init__(*O000OO0O0O0O0OO0O,**O00OO0000OO00O000)
  d=b()
  t=uq(uT)
  t.setFormatter(d)
  OO000OO0OO0OO0OO0.addHandler(t)
  OO000OO0OO0OO0OO0.setLevel(uV)
A=uK(__name__)
Uu("requests").setLevel(Un)
class uf(configparser.ConfigParser):
 def __init__(m,*OOOO0000OO00O0000,**O00O00O0OOOO00000):
  configparser.ConfigParser.__init__(m,*OOOO0000OO00O0000,**O00O00O0OOOO00000)
  if "config_path"in O00O00O0OOOO00000:
   m.read(kwags["config_path"])
  else:
   m.read(u["CONFIG_PATH"])
 def uO(o,O00OO0OO00000000O):
  o.read(O00OO0OO00000000O)
  if(not uk.exists(uk.split(O00OO0OO00000000O)[0])or not uk.exists(O00OO0OO00000000O)or not o.sections()):
   raise configparser.ParsingError('Unable to parse configuration file, please run "pysee --init".')
 def uw(v,OOOOOO0O00OOOO00O=UA):
  def uP(OOO00OOO0O000OOO0,OO0OO0O00OOOO0O0O,O00O00O0OOOO0O000):
   return OOO00OOO0O000OOO0[OO0OO0O00OOOO0O0O]if OOO00OOO0O000OOO0.get(OO0OO0O00OOOO0O0O)else O00O00O0OOOO0O000
  try:
   v.add_section("Imgur")
  except configparser.DuplicateSectionError:
   pass
  v["Imgur"]["client_id"]=uP(OOOOOO0O00OOOO00O,"ICID",uN("YTBmMDQ5ZDU3YzBiNzc2Cg==").decode('utf-8'))
  v["Imgur"]["client_secret"]=uP(OOOOOO0O00OOOO00O,"ICS","")
  try:
   v.add_section("Preferences")
  except configparser.DuplicateSectionError:
   pass
  v["Preferences"]["CONFIG_PATH"]=u["CONFIG_PATH"]
  v["Preferences"]["TOOL"]=(OOOOOO0O00OOOO00O["TOOL"]if OOOOOO0O00OOOO00O.get("TOOL")in y.valid_tools else u["TOOL"])
  v["Preferences"]["HOST"]=(OOOOOO0O00OOOO00O["HOST"]if OOOOOO0O00OOOO00O.get("HOST")in F.valid_hosts else u["HOST"])
  v["Preferences"]["MODE"]=(OOOOOO0O00OOOO00O["MODE"]if OOOOOO0O00OOOO00O.get("MODE")in y.valid_modes else u["MODE"])
  v["Preferences"]["SAVE_DIR"]=OOOOOO0O00OOOO00O["SAVE_DIR"]or u["SAVE_DIR"]
  for E in["CLIPBOARD","UPLOAD","LOGGING","SAVE"]:
   try:
    v["Preferences"][E]=strtobool(Um(OOOOOO0O00OOOO00O.get(E,"")).lower())
   except Uo:
    v["Preferences"][E]=Um(u[E]).lower()
  for G,O00O000O0OOOO0000 in u.items():
   try:
    u[G]=v.uS("Preferences",G,boolean=Uv(O00O000O0OOOO0000)==UE)
   except configparser.ParsingError as OOO0O00OOOOO0OO0O:
    u[G]=O00O000O0OOOO0000
 def ux(i):
  try:
   uc(uk.dirname(i["Preferences"]["CONFIG_PATH"]))
  except FileExistsError:
   pass
  with UG(i["Preferences"]["CONFIG_PATH"],"w")as O0OO0000OOO00O00O:
   i.write(O0OO0000OOO00O00O)
 def uS(OOOO0O000O0O000O0,OOO0OO00O0O0000OO,OOOO000O0OOO0O0O0,O0OOOO0O00OOO0OOO=UA):
  if O0OOOO0O00OOO0OOO:
   return OOOO0O000O0O000O0.getboolean(OOO0OO00O0O0000OO,OOOO000O0OOO0O0O0)
  return OOOO0O000O0O000O0[OOO0OO00O0O0000OO][OOOO000O0OOO0O0O0]
 def uB(a,O,O00OO00OO0O000000):
  r[a][O]=Um(O00OO00OO0O000000).lower()if Uv(O00OO00OO0O000000)==UE else Um(O00OO00OO0O000000)
class y:
 w={}
 P=["region","full","window"]
 x=["filename"]
 def __init__(S,B,R,**Q):
  S.name=B
  S.command=R
  S.modes={z:Q.get(z,"")for z in y.valid_modes}
  S.flags={K:Q.get(K,"")for K in y.valid_flags}
  if find_executable(B):
   y.valid_tools[B]=S
class F:
 f={}
 def __init__(C,H,N,**O0OOOO0OO0O0OO00O):
  if not Ui(N):
   raise Uo("upload_function must be callable.")
  C.name=H
  C.upload=lambda s:N(s)
  F.valid_hosts[H]=C
 @Ur
 def uR(O0OOO0OOO00OO00OO):
  import imgurpython
  k=uf()
   UL=imgurpython.helpers
   UI=imgurpython.ImgurClient
  c=UI(k.uS("Imgur","client_id"),k.uS("Imgur","client_secret"))
  try:
   e={"name":uk.split(O0OOO0OOO00OO00OO)[-1],"description":"Screenshot taken via PySee",}
   T=c.upload_from_path(O0OOO0OOO00OO00OO,config=e,anon=Ud)
   A.debug("Imgur upload via imgurpython was successful.")
   return T["link"]
  except UL.error.ImgurClientError:
   A.exception("There was an error validating your API keys for imgur.com.\n"+"Go to https://api.imgur.com/oauth2/addclient to receive your"+" own API keys.\n")
   raise
def uz(OOOO0OO000O0OOO0O):
 try:
  uc(OOOO0OO000O0OOO0O)
  return OOOO0OO000O0OOO0O
 except Ua as O0OO000O0O00OOO0O:
  if O0OO000O0O00OOO0O.errno!=uF:
   UO(Um(O0OO000O0O00OOO0O))
   raise Ua("Unable to create directory.")
y("gnome-screenshot","gnome-screenshot",region="-a",window="-w",filename="-f")
y("screencapture","screencapture -Cx",region="-s",window="-w")
y("shutter","shutter",region="-s",window="-w",full="-f",filename="-o")
y("xfce4-screenshooter","xfce4-screenshooter",region="-r",window="-w",full="-f",filename="-s",)
y("scrot","scrot",region="-s",window="-s",full=" ")
u["TOOL"]=Uw(y.valid_tools.keys())[0]
F("imgur",F.uR)
u["HOST"]=Uw(F.valid_hosts.keys())[0]
def uQ(OO00OO0OOOO000O00=UA,O00O0O0OOO000O000=UA,O0OOO0OO00O0O0000=UA,OO0OO0O0O00000OOO=UA,OOO00O00O00OOOO00=UA,OOO000OOO0O000OO0=UA,OO0OOOOO0O00OOO0O=UA,OOO0O0O00O0000O00=UA,):
 if OO00OO0OOOO000O00 is UA:
  OO00OO0OOOO000O00=u["HOST"]
 if O00O0O0OOO000O000 is UA:
  O00O0O0OOO000O000=u["TOOL"]
 if O0OOO0OO00O0O0000 is UA:
  O0OOO0OO00O0O0000=u["MODE"]
 if OO0OO0O0O00000OOO is UA:
  OO0OO0O0O00000OOO=u["CLIPBOARD"]
 if OOO00O00O00OOOO00 is UA:
  OOO00O00O00OOOO00=u["LOGGING"]
 if OOO000OOO0O000OO0 is UA:
  OOO000OOO0O000OO0=u["UPLOAD"]
 if OO0OOOOO0O00OOO0O is UA:
  OO0OOOOO0O00OOO0O=u["SAVE"]
 if OOO0O0O00O0000O00 is UA:
  OOO0O0O00O0000O00=u["SAVE_DIR"]
 uU="png"
 un=r"%Y-%m-%d-%H-%M-%S"
 if not OOO00O00O00OOOO00:
  Ul=UP
 ul=up(y.valid_tools)
 try:
  O00O0O0OOO000O000=O00O0O0OOO000O000.lower()
  ub=y.valid_tools[O00O0O0OOO000O000]
 except(Ux,US):
  A.debug("Invalid tool name provided.")
  ub=UA
  while not ub:
   try:
    O00O0O0OOO000O000,ub=y.valid_tools.popitem()
    if ub.modes[O0OOO0OO00O0O0000]=="":
     A.debug("Found installed tool, but lacked support for desired mode.")
     ub=UA
   except UB:
    uJ='No installed tool supports the mode "{}".'.format(O0OOO0OO00O0O0000)
    A.exception(uJ)
    raise UR(uJ)
 y.valid_tools=ul
 try:
  uI=F.valid_hosts[OO00OO0OOOO000O00]
  OO00OO0OOOO000O00=OO00OO0OOOO000O00.lower()
 except UB:
  A.debug("Invalid host name provided.")
  uI=F.valid_hosts[u["HOST_NAME"]]
 if not Uz(ub,y):
  uJ="Provided capture tool must be a CaptureTool instance."
  A.error(uJ)
  raise UQ(uJ)
 if O0OOO0OO00O0O0000 not in y.valid_modes:
  uJ="Invalid screenshot mode provided."
  A.error(uJ)
  raise UR(uJ)
 if O0OOO0OO00O0O0000 not in ub.modes.keys():
  uJ="Provided tool does not support the desired mode."
  A.error(uJ)
  raise US("Provided tool does not support the desired mode.")
 uL=Ub().strftime(un)
 uz(OOO0O0O00O0000O00)
 uD=uk.join(uk.abspath(OOO0O0O00O0000O00),".".join([uL,uU]))
 try:
  uM=" ".join([ub.command,ub.modes[O0OOO0OO00O0O0000],ub.flags.get("filename",""),uD,])
 except UB:
  uJ="Selected tool does not support the desired mode."
  A.error(uJ)
  raise UR(uJ)
 ud=Popen([uM],shell=Ud,stdout=PIPE,stdin=PIPE,stderr=PIPE)
 try:
  ut,uA=ud.communicate()
  um=ud.wait()
  if um!=0:
   uJ='Screenshot tool process exited with a non-zero return code ({}): stdout: "{}"; stderr: "{}"'.format(um,ut,uA)
   A.error(uJ)
   raise Uy(uJ)
 except UK:
  uJ="Screenshot tool process was exited before the screenshot completed."
  A.error(uJ)
  raise UK(uJ)
 A.info('Local screenshot capture: "{}".'.format(uD))
 if OOO000OOO0O000OO0:
  if not Uz(uI,F):
   uJ="Provided image_host must be a ImageHost instance."
   A.error(uJ)
   raise UQ(uJ)
  uo=uI.upload(uD)
  if not uo:
   uJ="Image upload failed."
   A.error(uJ)
   raise Uy(uJ)
  A.debug("Image upload succeeded.")
  A.info('Image upload: "{}" was uploaded to "{}" at "{}".'.format(uk.split(uD)[-1],OO00OO0OOOO000O00,uo))
 else:
  uo=uD
 if OO0OO0O0O00000OOO:
  UJ(uo)
  A.info('Clipboard copy: "{}" has been copied to your system clipboard.'.format(uo))
 if not OO0OOOOO0O00OOO0O:
  ue(uD)
 Ul=Ud
 return uo
if __name__=="__main__":
 uv=us()
 uv.add_argument("--init",default=UP,help="Initialize PySee and its configuration file information.",action="store_true",)
 uv.add_argument("--mode","-m",metavar="mode",Uv=Um,default=DEFAULTS["MODE"],help="Set the mode to take a screenshot in. Ensure you                         have a screenshot tool installed which supports the                         desired mode.",)
 uv.add_argument("--image-host","-i",metavar="host",Uv=Um,default=DEFAULTS["HOST"],help="Image host name to upload the screenshot to.",action="store",dest="image_host_name",)
 uv.add_argument("--screenshot-tool","-t",metavar="tool",Uv=Um,default=DEFAULTS["TOOL"],help="Name of screenshot program to use.",action="store",dest="tool_name",)
 uv.add_argument("--save-directory","-d",metavar="dir",Uv=Um,default=DEFAULTS["SAVE_DIR"],help="Where to locally save the screenshot.",action="store",dest="save_dir",)
 uv.add_argument("--upload","-u",default=DEFAULTS["UPLOAD"],help="Upload screenshot to an image host after capture.",required=UP,Uv=strtobool,)
 uv.add_argument("--logs","-l",default=DEFAULTS["LOGGING"],help="Output any logged information to the terminal.",required=UP,Uv=strtobool,)
 uv.add_argument("--clipboard","-c",default=DEFAULTS["CLIPBOARD"],help="Copy image URL to system clipboard after capture.",required=UP,Uv=strtobool,)
 uv.add_argument("--save","-s",default=DEFAULTS["SAVE"],help="Save screenshot locally after capture.",required=UP,Uv=strtobool,)
 uv.add_argument("--gui",default=UP,help="Start PySee in GUI mode.",action="store_true")
 ui={OOO000000O0O00OO0:O0O0O0O0OO0OO0000 for OOO000000O0O00OO0,O0O0O0O0OO0OO0000 in Uf(uv.parse_args()).items()if O0O0O0O0OO0OO0000 is not UA}
 ui["mode"]=ui["mode"].lower()
 if ui["mode"]not in y.valid_modes:
  uv.error("Invalid capture mode specified [region,full,window].")
 if ui["init"]:
  cp=uf()
  UO("This utility will walk you through creating your PySee configuration file." "It will cover each required setting and tries to provide sensible defaults.\n" 'PySee\'s configuration file will be stored at "{}".\n' "Press ^C at any time to quit.".format(u["CONFIG_PATH"]))
  ur={}
  try:
   ur["TOOL"]=UC("Screenshot capture tool [{}]: ({}) ".format("|".join(y.valid_tools.keys()),u["TOOL"])).lower()
   ur["HOST"]=UC("Image host [{}]: ({}) ".format("|".join(F.valid_hosts.keys()),u["HOST"])).lower()
   ur["MODE"]=UC("Capture mode [region|full|window]: (region) ").lower()
   ur["SAVE_DIR"]=UC("Screenshot save directory: ({}) ".format(u["SAVE_DIR"]))
   ur["CLIPBOARD"]=UC("Copy uploaded URL to clipboard: (yes) ")
   ur["UPLOAD"]=UC("Upload screenshot after capture: (yes) ")
   ur["LOGGING"]=UC("Print logging information: (yes) ")
   ur["SAVE"]=UC("Save screenshot locally after capture: (yes) ")
   ur["ICID"]=UC("Imgur API Client ID (http://api.imgur.com/oauth2/addclient): (default) ")
   ur["ICS"]=UC("Imgur API Client Secret: (default) ")
  except UK:
   uj()
  cp.update_config(ur)
  cp.write_config()
  if not uk.exists(u["CONFIG_PATH"]):
   raise configparser.ParsingError('Unable to parse configuration file, please run "pysee --init".')
  for k,v in u.items():
   try:
    u[k]=cp.get_val("Preferences",k,boolean=Uv(v)==UE)
   except configparser.ParsingError as e:
    u[k]=v
  UO("PySee is ready to use!")
  uj()
 if ui["gui"]:
  import gui as gui
   UD=gui.main
  UD()
   UD=gui.main
 else:
  try:
   del ui["init"]
   del ui["gui"]
   uQ(**ui)
  except(UK,UH):
   uY()
# Created by pyminifier (https://github.com/liftoff/pyminifier)

