import csv  # for csv reader and writer
from BeautifulSoup import BeautifulSoup

# This class makes a Adjacent County Directory to return


class County(object):

    def __init__(self, fName="adjCounties.csv", cName="ccnp.csv"):
        # Take in County list.
        # main function is to see if two counties are adjactent to each other.
        # Svg format is class="c00123" code points to code or could search ny
        # id='Kitsap, WA"
        self.adjCounties = {}  # [CountyCode] = [county1,county2,county3,..]
        # CountyNameTo Code ex: 'kitsap washington' : '02015'
        self.countyCodes = {}
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
        # self.findMissing12()
        # self.printAll(1)
        # self.test()
        # self.bSoup()
        self.distanceController()
        self.bSoup()

    def printAll(self, col):
        self.printAdjDic(col)
        self.printCodes(col)
        self.printNatParkCounties(col)
        self.printAdjCode(col)

    # Build Adjacent Counties Dic. A county points to an list of its adjacent
    # county
    def fetchCountyList(self):
        reader = csv.reader(open(self.fileName), delimiter=',')
        counter = 0
        currCounty = '||'  # As not to include first pass avoids [] -
        adjList = []
        for row in reader:
            counter += 1
            if row[0].strip() == currCounty:
                adjList.append(row[1].strip())
            else:
                self.adjCounties[currCounty] = adjList
                currCounty = row[0].strip()
                adjList = []
                adjList.append(row[1].strip())
        self.adjCounties[currCounty] = adjList
        del self.adjCounties['||']

    # Build County Code Dictionary so County name correspond to an offical code
    def fetchCountyCodes(self):
        reader = csv.reader(open(self.codeFile), delimiter=',')
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
                # Meaning has national park
                self.natPark[rowZ] = [c, len(row[3])]
                self.dist[rowZ] = 0

    def printCodes(self, col):  # prints County Name and corresponding code
        print "County Codes:"
        counter = 0
        for i in self.countyCodes:
            if counter < col:
                print "[{}] - {}".format(i, self.countyCodes[i])
                counter += 1
            else:
                return

    def printAdjCode(self, col):
        print "Adjacent Counties in Code Form"
        counter = 0
        for i in self.adjCode:
            if counter < col:
                print "[{}] - {}".format(i, self.adjCode[i])
                counter += 1
            else:
                return

    def printNatParkCounties(self, col):
        counter = 0
        print "National Parks"
        for i in self.natPark:
            if counter < col:
                print "[{}-{}]: {}".format(
                    i, self.natPark[i][0], self.natPark[i][1])
                # counter +=1
            else:
                return

    # Prints County Name and Adjacent Counties if any
    def printAdjDic(self, col):
                                # Currently Counties that have no Adjacent
                                # Counties are not included in the print as they
                                # are not in the dic ex: A few Hawaii County,
                                # San Jaun County WA
        print "Adjacent County List:"
        counter = 0
        for i in self.adjCounties:
            if counter < col:
                s = self.listToString(self.adjCounties[i])
                print "[{}]- {}".format(i, s[0:-1])
                counter += 1
            else:
                return

    def listToString(self, l):
        s = ''
        for i in l:
            k = "%s," % (i)
            s += k
        return s

    # Checks to see if two counties are adjacent if C
    def isAdjacent(self, cA, cB):
        countyA = cA.lower()
        countyB = cB.lower()
        if countyB in self.adjCounties[countyA]:
            if countyA in self.adjCounties[countyB]:
                print "{} is Adjacent to {}".format(countyA, countyB)
                return True
            else:
                print "Error: Missing adjacent county that should be there"
                print countyA, countyB
                return False
        else:
            print "{} and {} are not Adjacent.".format(countyA, countyB)
            return False

    # Take in county name and state and convert to coded name
    def convertToCode(self, countyName):
        # print "County Name: " +countyName
        code = self.countyCodes[countyName]
        return code

    def test(self):
        self.isAdjacent("Archer Texas", "Clay Texas")
        self.isAdjacent("Schoolcraft Michigan", "Summit Utah")
        self.convertToCode("Kitsap Washington")

    def bSoup(self):
        svg = open('Usa_counties.svg', 'r').read()
        soup = BeautifulSoup(
            svg,
            selfClosingTags=[
                'defs',
                'sodipodi:namedview'])
        paths = soup.findAll('path')
        # So I have 18? Levels of Colors to use to best diplay my the data i am wanting to display
        #First Will be black or dark green 
        #Then a notacibly different color of green
        #Moves until  


        colors = ['#004529','#006837','#238443','#41ab5d','#78c679','#addd8e','#d9f0a3','#f7fcb9','#ffffe5','#fff7bc','#fee391','#fec44f','#fe9929','#ec7014','#cc4c02','#993404','#662506','#1e0b02','#060200','#ffffff']
        

        '''           |         
                PineGreen
                (HasNatPark)            
        '''                            
        ''' colors2 = [
            '#00441b',
            '#006d2c',
            '#238b45',
            '#41ae76',
            '#66c2a4',
            '#99d8c9',
            '#ccece6',
            '#e5f5f9',
            '#f7fcfd',
            '#e0ecf4',
            '#bfd3e6',
            '#9ebcda',
            '#8c96c6',
            '#8c6bb1',
            '#88419d',
            '#810f7c',
            '#4d004b',
            '#',
            '#101010'] '''

        # colors = ['#FFFFFF','#F8F8F8']
        part1 = 'font-size:12px;fill-rule:nonzero;stroke:#000000;'
        part2 = 'stroke-opacity:1;stroke-width:0.5;stroke-miterlimit:4;'
        part3 = 'stroke-dasharray:none;stroke-linecap:butt;marker-start:none;'
        part4 = 'stroke-linejoin:bevel;fill:'
        path_style = part1 + part2 + part3 + part4
        # 49006a
        # 7a0177
        # 8e0152
        # ae017e
        # c51b7d
        # dd3497
        # de77ae
        # f1b6da
        # fde0ef
        # f7f7f7
        # e6f5d0
        # b8e186
        # 7fbc41
        # 4d9221
        # 238b45
        # 276419
        # 006d2c
        # 00441b

        # e0ecf4','#bfd3e6','#9ebcda','#8c96c6','#8c6bb1','#88419d',
        # '#810f7c','#4d004b']
        # print "Colors Length: ",len(colors)
        # print "self.dist len:",len(self.dist)
        # print "self.countyCodes len:",len(self.countyCodes)
        # print "self.codeCounty len:",len(self.codeCounty)
        # print "self.adjCounties len:",len(self.adjCounties)
        # print "self.adjCode len:",len(self.adjCode)




        for p in paths:
            if p['class'] not in ["State_Lines", "separator"]:
                try:
                    code = p['class']
                    code = code[1:]
                    rate = self.dist[code]
                except:
                    rate = 99
                    continue
                if rate < len(colors) - 1:
                    color_class = rate
                else:
                    # print "Has no distance:",code
                    # print code,self.codeCounty[code]
                    color_class = len(colors) - 1
                # print "Color_class:",color_class
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
            count += 1

    def distanceToNat(self, currD):
        currDist = currD
        for i in self.dist:
            # print self.codeCounty[i],i,self.dist[i]
            iDist = self.dist[i]
            if iDist == currDist:  # should end up being currDist
                # if iDist == 0:
                    # print "NatParkCounty: ",self.codeCounty[i],i,self.dist[i]
                # else:
                    # print "County: ",self.codeCounty[i],i,self.dist[i]
                adjC = self.adjCode[i]
                for a in adjC:
                    distAC = self.dist[a]
                    if distAC == 100:
                        self.dist[a] = currDist + 1
                        # print "\tNo Dist",a,self.codeCounty[a],self.dist[a]
            # self.distanceToNat(1)

                # need to get the adjacent counties and increment these

    def distanceController(self):
        for n in range(0, 18):
            self.distanceToNat(n)
            # print n,"Number Left: ", self.checkNumberDone()

    def checkNumberDone(self):
        cccc = 0
        for i in self.dist:
            if self.dist[i] == 100:
                cccc += 1

        return cccc

    def findMissing12(self):
        counter = 0
        # print "\nThe Missing few:"
        for i in self.codeCounty:
            # print i +" : " + self.codeCounty[i]
            # if counter > 10:
            #    return
            # counter +=1
            if i not in self.adjCode:
                # print i +" : " + self.codeCounty[i]
                counter += 1

        # print "Count:",counter

if __name__ == "__main__":
    County().fetch()

# Issue with Suffolk County, NY not showing up probably from not having enough colors
# The colors seem to be a little weird East of missiplii is good but west looks to cluttered
# Try with lke 10 colors or 12 ans just combine 
# Now use self.dist to populate the map
# 'Furthest away' from nat park is Suffolk county, New York at 18 counties
# Get colors
# Add to map should be easy