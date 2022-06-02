import PySimpleGUI as sg
import urllib.request
import json
import io
import re
import os
import webbrowser
from PIL import Image

PREV_WID = 1600
PREV_HI = 900
ICON_SIZE = 50
TOOT_WID = 25
NAME_WID = 15

def getImg(url, wid, hi):
	print("getImg")

	r = urllib.request.urlopen(url).read()
	imgBin = io.BytesIO(r)
	pImg = Image.open(imgBin)
	pImg.thumbnail((wid, hi))
	imgBin=io.BytesIO()
	pImg.save(imgBin, format="PNG")

	return imgBin.getvalue()

def updateWnd(postI, imgI):
	wnd["image"].update(data=posts[postI].picBin[imgI], size=(PREV_WID, PREV_HI))
	wnd["icon"].update(data=posts[postI].iconBin, size=(ICON_SIZE, ICON_SIZE))
	wnd["username"].update(posts[postI].username)
	wnd["id"].update("@" + posts[postI].id)
	wnd["toot"].update(posts[postI].toot)
	print(str(postI+1) + "/" + str(len(posts)) + ", " + str(imgI+1) + "/" + str(len(posts[postI].picBin)))

def getPosts(url):
	print(url)
	with urllib.request.urlopen(url) as r:
		rjson = json.loads(r.read().decode("UTF-8"))
		rheader = r.info()
		#prevR = 'https://(?!.*https://(?!.*rel="next")).*(?=>; *rel="prev")'
		#prev = re.search(prevR, rheader["link"]).group(0)
		nextR = 'https://(?!.*https://(?!.*rel="prev")).*(?=>; *rel="next")'
		next = re.search(nextR, rheader["link"]).group(0)

		for p in rjson:
			pdata = post(p)
			if len(pdata.picURL):
				posts.append(pdata)

	return next

def untag(str):
	str = re.sub("<br.*?/>", "\n", str)
	str = re.sub("</p>", "\n\n", str)
	str = re.sub("<.*?>", "", str)

	return str

class post:
	def __init__(self, pjson):
		self.imgLoaded = False
		self.id = pjson["account"]["acct"]
		self.username = pjson["account"]["display_name"]
		self.iconURL = pjson["account"]["avatar_static"]
		self.toot = untag(pjson["content"])
		self.tootURL = pjson["url"]
		self.picURL = []
		for p in pjson["media_attachments"]:
			if p["type"] == "image":
				self.picURL.append(p["url"])

	def loadImg(self):
		if not self.imgLoaded:
			self.picBin = []
			for pic in self.picURL:
				self.picBin.append(getImg(pic, PREV_WID, PREV_HI))
			self.iconBin = getImg(self.iconURL, ICON_SIZE, ICON_SIZE)
			self.imgLoaded = True

#
#initialize
#

#openUI
sg.theme("LightBlue5")
openL = [
	[sg.Text("閲覧するサーバーのドメインを入力")],
	[sg.InputText(key="domainName")],
	[sg.Button("OK", key="ok_btn")]
]
wnd = sg.Window("picViewer", openL)
wnd.finalize()

while True:
	e, v = wnd.read()
	if e == sg.WIN_CLOSED:
		quit()
	if e == "ok_btn":
		m_domain = v["domainName"]
		if not m_domain.startswith("https://"):
			m_domain = "https://" + m_domain
		break

posts = []
URL = m_domain + "/api/v1/timelines/public?local=true"

#print(URL)
opener = urllib.request.build_opener()
opener.addheaders = [("User-Agent", "mstdnPicView")]
urllib.request.install_opener(opener)

#UI
l_image = [[sg.Image(size=(PREV_WID, PREV_HI), key="image")]]
l_name =[
	[sg.Text("username", size=(NAME_WID, 1), key="username")],
	[sg.Text("@ID", size=(NAME_WID, 1), key="id")]
]
l_info = [
	[sg.Image(size=(ICON_SIZE, ICON_SIZE), key="icon", enable_events=True), sg.Column(l_name)],
	[sg.Text("toot", size=(TOOT_WID, 40), key="toot", enable_events=True)]
]
l_button = [
	[sg.Button("<", key="prevBtn", size=(5, 3)), sg.Button("保存", key="saveBtn", size=(8, 3)), sg.Button(">", key="nextBtn", size=(5, 3))],
]

l_rUnit =[
	[sg.Frame("info", l_info, vertical_alignment="top")],
	[sg.Frame("btn", l_button, vertical_alignment="bottom")]
]

layout = [[sg.Frame("preview", l_image, key="imageF"), sg.Column(l_rUnit)]]

wnd = sg.Window("mstdnPicView", layout)
wnd.finalize()

URL = getPosts(URL)
postI = 0
imgI = 0
posts[postI].loadImg()
updateWnd(postI, imgI)

#main loop
while True:
	e, v = wnd.read()

	if e == "nextBtn":
		if imgI < len(posts[postI].picBin)-1:
			imgI = imgI + 1
			print("next pic")
		elif postI < len(posts)-1:
			postI = postI + 1
			imgI = 0
			posts[postI].loadImg()
			print("next toot")
		elif postI == len(posts)-1:
			URL = getPosts(URL)
			postI = postI + 1
			imgI = 0
			posts[postI].loadImg()
			print("load next toot\nnext toot")
		updateWnd(postI, imgI)

	if e == "prevBtn":
		if imgI > 0:
			imgI = imgI - 1
			print("prev pic")
		elif postI > 0:
			postI = postI -1
			imgI = len(posts[postI].picBin) -1
			print("prev toot")
		updateWnd(postI, imgI)

	if e == "saveBtn":
		if not os.path.isdir("img/"):
			os.mkdir("img")
		fname = "img/" + os.path.basename(posts[postI].picURL[imgI])
		if not os.path.isfile(fname):
			urllib.request.urlretrieve(posts[postI].picURL[imgI], fname)
			print("save pic")

	if e == "toot":
		webbrowser.open(posts[postI].tootURL, new=0, autoraise=True)

	if e == sg.WIN_CLOSED:
		break