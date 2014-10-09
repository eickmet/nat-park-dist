import csv      #for csv reader and writer
from BeautifulSoup import BeautifulSoup

#This class makes a Adjacent County Directory to return

class County(object):

    def __init__(self,fName="adjCounties.csv",cName="ccnp.csv"):
    #Take in County list.
    #main function is to see if two counties are adjactent to each other.
    #Svg format is class="c00123" code points to code or could search ny id='Kitsap, WA"
        self.adjCounties = {} #[CountyCode] = [county1,county2,county3,..]
        self.countyCodes = {} #CountyNameTo Code ex: 'Washington State' : '02015'
        self.codeCounty = {}  
        self.dist = {}
        self.adjCode = {}
        self.natPark = {}
        self.fileName = fName
        self.codeFile = cName

    def fetch(self):
        self.fetchCountyList()
        self.fetchCountyCodes()
        self.convertAdj()
        self.findMissing12()
        #self.printAll(1)
        #self.test()
        #self.bSoup()
        #self.distanceToNat()

    def printAll(self,col):
        self.printAdjDic(col)
        self.printCodes(col)
        self.printNatParkCounties(col)
        self.printAdjCode(col)

    def fetchCountyList(self):  #Build Adjacent Counties Dic. A county points to an list of its adjacent county
        reader = csv.reader(open(self.fileName),delimiter=',')
        currCounty = '||'    #As not to include first pass avoids [] -
        adjList = []
        for row in reader:
            if row[0] == currCounty:
                adjList.append(row[1])
            else:
                self.adjCounties[currCounty] = adjList
                currCounty = row[0]
                adjList = []
                adjList.append(row[1])
        del self.adjCounties['||']

    def fetchCountyCodes(self): #Build County Code Dictionary so County name correspond to an offical code
        reader = csv.reader(open(self.codeFile),delimiter=',')
        for row in reader:
            if len(row[0]) == 4:
                rowZ = '0' + row[0]
            else:
                rowZ = row[0] 
            c = row[1].strip("[]\"1234567890,.") + " " + row[2]
            self.countyCodes[c] = rowZ
            self.codeCounty[rowZ] = c
            self.dist[rowZ] = 100
            if len(row[3]) > 0:
                #Meaning has national park
                self.natPark[rowZ] = [c,len(row[3])]
                self.dist[rowZ] = 0


    def printCodes(self,col):   #prints County Name and corresponding code
        print "County Codes:"
        counter = 0 
        for i in self.countyCodes:
            if counter < col:
                print "[{}] - {}".format(i,self.countyCodes[i])
                counter += 1
            else:
                return

    def printAdjCode(self,col):
        print "Adjacent Counties in Code Form"
        counter = 0
        for i in self.adjCode:
            if counter < col:
                print "[{}] - {}".format(i,self.adjCode[i])
                counter += 1
            else:
                return


    def printNatParkCounties(self,col):
        counter = 0
        print "National Parks"
        for i in self.natPark:
            if counter < col:
                print "[{}-{}]: {}".format(i,self.natPark[i][0],self.natPark[i][1])
                #counter +=1
            else:
                return

    def printAdjDic(self,col):  #Prints County Name and Adjacent Counties if any
                                #Currently Counties that have no Adjacent Counties are not included in the print as they are not in the dic ex: A few Hawaii County, San Jaun County WA
        print "Adjacent County List:"
        counter = 0
        for i in self.adjCounties:
            if counter < col:
                s = self.listToString(self.adjCounties[i])
                print "[{}]- {}".format(i,s[0:-1])
                counter +=1
            else:
                return
        
    def listToString(self,l):
        s = ''
        for i in l:
            k = "%s," %(i)
            s += k
        return s

    def isAdjacent(self,cA,cB): #Checks to see if two counties are adjacent if C
        countyA = cA.lower()
        countyB = cB.lower()
        if countyB in self.adjCounties[countyA]:
            if countyA in self.adjCounties[countyB]:
                print "{} is Adjacent to {}".format(countyA,countyB)
                return True
            else:
                print "Error:{} is adjacent to {} but {} is not adjacent to {}".format(countyA,countyB,countyB,countyA)
                return False
        else:
            print "{} and {} are not Adjacent.".format(countyA,countyB)
            return False

    def convertToCode(self,countyName):    #Take in county name and state and convert to coded name
        print "County Name: " +countyName
        code = self.countyCodes[countyName]
        return code


    def test(self):
        self.isAdjacent("Archer Texas","Clay Texas")
        self.isAdjacent("Schoolcraft Michigan","Summit Utah")
        self.convertToCode("Kitsap Washington")
    
    def bSoup(self):
        svg = open('Usa_counties.svg','r').read()
        soup = BeautifulSoup(svg,selfClosingTags=['defs','sodipodi:namedview'])
        paths = soup.findAll('path')
        colors = ['#FFFFFF','#F8F8F8']
        path_style = 'font-size:12px;fill-rule:nonzero;stroke:#000000;stroke-opacity:1;stroke-width:0.5;stroke-miterlimit:4;stroke-dasharray:none;stroke-linecap:butt;marker-start:none;stroke-linejoin:bevel;fill:'
        for p in paths:
            if p['class'] not in ["State_Lines","separator"]:
                try:
                    code = p['class']
                    code = code[1:]
                    rate = self.natPark[code]
                    rate = 1 
                except:
                    rate = 0
                    continue
                if rate == 0:
                    color_class = 1
                else:
                    color_class = 0
                color = colors[color_class]
                p['style'] = path_style + color

        print soup.prettify()

    def convertAdj(self):
        count = 0
        for i in self.adjCounties:
            aList = []
            for c in self.adjCounties[i]:
                aList.append(self.convertToCode(c))
            self.adjCode[self.convertToCode(i)] = aList
            count +=1
        print "Count: " ,count


    def distanceToNat(self):
        currDist = 0
        for i in self.dist:
            if currDist == self.dist[i]:
                #Get Adj Counties
                adjC = self.adjCounties[i] # Change THIS

    def findMissing12(self):
        counter = 0
        print "\nThe Missing 12:"
        for i in self.codeCounty:
            #print i +" : " + self.codeCounty[i]
            #if counter > 10:
            #    return
            #counter +=1
            if i not in self.adjCode:
                print i +" : " + self.codeCounty[i]
                counter +=1
        print "Count:",counter

if __name__ == "__main__":
    County().fetch()

#TODO: Map the National Park Counties First 
#TODO: Try for Washington State first before moving up to the entire us
#TODO: Find the correct Shortest Path Algorthm
#TODO: Start from all natpark county and adj then build with surronding counties until as much of the map is full 
#End Goal: 1) Have a project that I can show protential employers. 2) What County/Counties are the furthest away by counties from a national park. Guess is 