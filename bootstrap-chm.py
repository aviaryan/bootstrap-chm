from bs4 import BeautifulSoup
import os
import shutil, errno
import re


ENC = 'utf-8'
HSTR = "<OBJECT type=\"text/sitemap\">\n" + "<param name=\"Name\" value=\"{0}\">\n" + "<param name=\"Local\" value=\"{1}\">\n" + "</OBJECT>\n"
NOJS = 1


def copyanything(src, dst):
	# copy tree from src to dst
	# Taken from Stack Overflow (dont have the link)
	try:
		shutil.copytree(src, dst)
	except OSError as exc: # python >2.5
		if exc.errno == errno.ENOTDIR:
			shutil.copy(src, dst)
		else: raise
	return


def initFile(f):
	'''
	initFile(f):
		f = file path
	Purpose - 
		Clears extra JS and stuff from HTML file that should not be in the CHM doc
	'''

	# Not using BS as it had some issues with encoding

	fpt = open(f, 'r', encoding=ENC)
	st = fpt.read()
	fpt.close()

	if NOJS == 1:
		mobj = re.findall("(?ims)<script.*?</script>", st) # remove all scripts
	else:
		mobj = re.findall("(?ims)<script>.*?</script>", st) # remove only online scripts

	for k in mobj:
		st = st.replace(k,'')
	
	# remove online jquery
	mobj = re.findall('<script src.*ajax.*jquery.*</script>', st)
	for k in mobj:
		st = st.replace(k,'')
		break
	# add local jquery
	mobj = re.findall('<script.*dist.*bootstrap\.js.*</script>', st)
	for k in mobj:
		jstr = k.replace('bootstrap.js', 'jquery-1.11.2.min.js')
		st = st.replace(k,k + jstr)
		break

	fpt = open(f, 'w', encoding=ENC)
	fpt.write(st)
	return


def makeHHC(f):
	'''
	makeHHC(f):
		f = file path
	Purpose -
		Makes HHC HTML string from a Bootstrap documentation file
	'''
	f2 = f[6:] # remove build

	soup = BeautifulSoup(open(f, 'r', encoding=ENC), 'html.parser')
	navs = soup.body.find("ul", class_ = "bs-docs-sidenav")

	prec = ("<li>" + HSTR).format(soup.title.string.replace('· Bootstrap', '').strip(), f2) # page entry - remove  · Bootstrap

	if navs == None:
		return prec + '</li>\n'

	for k in navs.find_all("ul"): # in the end
		del k['class']

	for k in navs.find_all("li"):
		name = k.a.string
		value = f2 + k.a['href']
		hh_str = (HSTR).format(name, value)
		k.a.replace_with(hh_str)

	navs = str(navs).replace('&lt;', '<').replace('&gt;', '>')
	return prec + navs + '</li>\n'


def makeFile(f, d):
	'''
	makeHHPFile(f, d):
		f = file path to make
		d = data to be added
	Purpose - 
		Makes Contents.hhc, Index.hhk and Bootstrap.hhp file
	'''
	copyanything(f, 'build\\' + f)
	p = 'build\\' + f
	fptr = open(p, 'r')
	data = fptr.read()
	fptr.close()
	data = data + '\n' + d
	fptr = open(p, 'w')
	fptr.write(data)
	fptr.close()
	return

##################
# M A I N
##################

fileList = []
contents = ''

if os.path.isdir('build'):
	shutil.rmtree('build')
copyanything('src', 'build')

if NOJS:
	for root, dirs, files in os.walk('build'):
		for i in dirs:
			if i == 'js':
				shutil.rmtree(os.path.join(root, i))

# build file index
for item in os.listdir('build'):
	item = 'build\\' + item
	if os.path.isfile(item):
		fileList += [item]
		if item.endswith('.html'):
			initFile(item)
	elif os.path.isdir(item):
		for root, dirs, files in os.walk(item):
			for name in files:
				tmp = os.path.join(root, name)
				fileList += [tmp]
				if tmp.endswith('.html'):
					print(tmp)
					initFile(tmp)
			# if NOJS:
			# 	dirs[:] = [d for d in dirs if d not in ['js']]

# build hhc data from interested files
helpFiles = ['index.html', 'getting-started', 'css', 'components', 'javascript', 'customize', 'examples', 'migration', 'about', 'browser-bugs']

for item in helpFiles:
	item = 'build\\' + item
	if os.path.isfile(item):
		contents += makeHHC(item)
	elif item == 'build\\examples':
		st = ("<li>" + HSTR + "<ul>").format('Examples', '')
		for j in os.listdir(item):
			for k in os.listdir(item + '\\' + j):
				if k.endswith('.html'):
					st += makeHHC(item + '\\' + j + '\\' + k)
		contents += st + '</ul></li>\n'
	else:
		for j in os.listdir(item):
			if j.endswith('.html'):
				contents += makeHHC(item + '\\' + j)


# BS fails to remove ul with multiple class. So
s = re.findall('(?i)<ul.*?>', contents)
for k in s:
	contents = contents.replace(k, '<ul>')

makeFile('Contents.hhc', contents + '\n</ul></body></html>')
makeFile('Index.hhk', contents + '\n</ul></body></html>')
makeFile('Bootstrap.hhp', '\n'.join( [s[6:] for s in fileList] )) # remove build/