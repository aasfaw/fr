from urllib2 import urlopen
from BeautifulSoup import BeautifulSoup

import re, htmlentitydefs
def unescape(text):
    def fixup(m):
        text = m.group(0)
        if text[:2] == "&#":
            try:
                if text[:3] == "&#x":
                    return unichr(int(text[3:-1], 16))
                else:
                    return unichr(int(text[2:-1]))
            except ValueError:
                pass
        else:
            try:
                text = unichr(htmlentitydefs.name2codepoint[text[1:-1]])
            except KeyError:
                pass
        return text
    return re.sub("&#?\w+;", fixup, text)

class frenchword:
    def __init__(self):
        self.word = 'Undefined'
        self.present = []
        self.future = []
        self.imperfect = []
        self.subjunctive = []
        self.conditional = []
        self.passesimple = []
        self.imperfectsubjunctive = []
        self.imperative = []
        self.presentparticiple = 'Undefined'
        self.etreavoir = 'Undefined'
        self.pastparticiple = 'Undefined'

    def setword(self,a):
        self.word = unescape(a)
    def addpresent(self,a):
        self.present.append(unescape(a))
    def addfuture(self,a):
        self.future.append(unescape(a))
    def addimperfect(self,a):
        self.imperfect.append(unescape(a))
    def addsubjunctive(self,a):
        self.subjunctive.append(unescape(a))
    def addconditional(self,a):
        self.conditional.append(unescape(a))
    def addpassesimple(self,a):
        self.passesimple.append(unescape(a))
    def addimperfectsubjunctive(self,a):
        self.imperfectsubjunctive.append(unescape(a))
    def addimperative(self,a):
        self.imperative.append(unescape(a))
    def setpresentparticiple(self,a):
        self.presentparticiple = unescape(a)
    def setetreavoir(self,a):
        self.etreavoir = unescape(a)
    def setpastparticiple(self,a):
        self.pastparticiple = unescape(a)

    def printyourself(self, printfilter="-all"):
        from termcolor import colored
        print colored(self.word.strip() + "\n" + "-"*len(self.word.strip()), "green")
        if "-p-" in printfilter or "-all" in printfilter:
            print "p: " + "; ".join([a[:-1] + "'" + b if a[-1] in ("a","e","i","o","u","h") and b[0] in ("a","e","i","o","u", "h") else a + " " + b for (a,b) in zip(["je","tu","il","nous","vous","ils"], self.present)])
        if "-pc-" in printfilter or "-all-" in printfilter:
            print colored("pc: " + self.etreavoir + "/" + self.pastparticiple, "blue")
        if "-i-" in printfilter or "-all-" in printfilter:
            print colored("i: " + "; ".join([a[:-1] + "'" + b if a[-1] in ("a","e","i","o","u","h") and b[0] in ("a","e","i","o","u", "h") else a + " " + b for (a,b) in zip(["je","tu","il","nous","vous","ils"], self.imperfect)]), "yellow")
        if "-i?-" in printfilter or "-all-" in printfilter:
            print colored("i?: " + " ".join([b + "-" + a + "!" for (a,b) in zip(["tu","nous","vous"], self.imperative)]), "red")
        if "-f-" in printfilter or "-all-" in printfilter:
            print "f: " + "; ".join([a[:-1] + "'" + b if a[-1] in ("a","e","i","o","u", "h") and b[0] in ("a","e","i","o","u", "h") else a + " " + b for (a,b) in zip(["je","tu","il","nous","vous","ils"], self.future)])
        if "-s-" in printfilter or "-all-" in printfilter:
            print "s: " + "; ".join([a[:-1] + "'" + b if a[-1] in ("a","e","i","o","u", "h") and b[0] in ("a","e","i","o","u", "h") else a + " " + b for (a,b) in zip(["je","tu","il","nous","vous","ils"], self.subjunctive)])
        if "-c-" in printfilter or "-all-" in printfilter:
            print "c: " + "; ".join([a[:-1] + "'" + b if a[-1] in ("a","e","i","o","u", "h") and b[0] in ("a","e","i","o","u", "h") else a + " " + b for (a,b) in zip(["je","tu","il","nous","vous","ils"], self.conditional)])
        if "-ps-" in printfilter or "-all-" in printfilter:
            print "ps: " + "; ".join([a[:-1] + "'" + b if a[-1] in ("a","e","i","o","u", "h") and b[0] in ("a","e","i","o","u", "h") else a + " " + b for (a,b) in zip(["je","tu","il","nous","vous","ils"], self.passesimple)])
        if "-is-" in printfilter or "-all-" in printfilter:
            print "is: " + "; ".join([a[:-1] + "'" + b if a[-1] in ("a","e","i","o","u", "h") and b[0] in ("a","e","i","o","u", "h") else a + " " + b for (a,b) in zip(["je","tu","il","nous","vous","ils"], self.imperfectsubjunctive)])
        if "-pp-" in printfilter or "-all-" in printfilter:
            print "pp: " + self.presentparticiple

def getsoup(url):
    page = urlopen(url)
    soup = BeautifulSoup(page)
    return soup

def getword(soup):
    return soup('span', {"class":"fn"})[0].contents[0]

def getworddata(wordname):
    wordsoup = getsoup("http://french.about.com/od/verb_conjugations/a/" + wordname + ".htm")
    thisword = frenchword()
    thisword.setword(getword(wordsoup))
    counter = 1
    for row in wordsoup('div', {"id":"articlebody"})[0]('table')[0]('tr'):
        if counter > 1 and counter < 8:
            thisword.addpresent(row('td')[1]('b')[0].contents[0])
            thisword.addfuture(row('td')[2]('b')[0].contents[0])
            thisword.addimperfect(row('td')[3]('b')[0].contents[0])
            if counter == 2:
                thisword.setpresentparticiple(row('td')[4]('b')[0].contents[0])
            elif counter == 5:
                thisword.setetreavoir(row('td')[5]('b')[0]('a')[0].contents[0])
            elif counter == 6:
                thisword.setpastparticiple(row('td')[5]('b')[0].contents[0])
        elif counter > 9 and counter < 16:
            thisword.addsubjunctive(row('td')[1]('b')[0].contents[0])
            thisword.addconditional(row('td')[2]('b')[0].contents[0])
            thisword.addpassesimple(row('td')[3]('b')[0].contents[0])
            thisword.addimperfectsubjunctive(row('td')[4]('b')[0].contents[0])
        elif counter > 17 and counter < 21:
            thisword.addimperative(row('td')[1]('b')[0].contents[0])
        counter += 1
    return thisword

import sys, time
start_time = time.time()
yaycount, wordcount = 0, 0
if len(sys.argv) > 1:
    if "-sp" in sys.argv:
        selectiveprint = '-'.join(sys.argv[sys.argv.index("-sp") + 1:]) + '-'
    else:
        selectiveprint = "-all-"

    if "-f" in sys.argv:
        words = open(sys.argv[sys.argv.index("-f") + 1]).read().split()
    else:
        if selectiveprint == "-all-":        
            words = sys.argv[1:len(sys.argv)]
        else:
            words = sys.argv[1:sys.argv.index("-sp")]

    import os
    _, termcolsize = os.popen('stty size', 'r').read().split() 
    termcolsize = int(termcolsize)

    for word in words:
        wordcount += 1
        print "-"*termcolsize
        try:
            worddata = getworddata(word)
            worddata.printyourself(selectiveprint)
            yaycount += 1
        except:
            print "Could not conjugate the verb " + '"' + word + '".'
    print "-"*termcolsize
    print  "Conjugated " + str(yaycount) + "/" + str(wordcount) + " verbs in " + str(time.time() - start_time)[0:4] + " seconds."
else:
    print "No verb(s) specified."
