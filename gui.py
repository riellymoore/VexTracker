import sys
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtWidgets import *
from info import *

countryList = ['','(US) United States', '(AU) Australia', '(CA) Canada', '(CN) China', '(CO) Columbia', '(HK) Hong Kong', '(MX) Mexico', '(NZ) New Zealand', '(UK) United Kingdom','(SG) Singapore']


class SearchWindow(QWidget):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("VexTracker")
        self.setWindowIcon(QIcon('./vextrackericon.png'))
        self.setGeometry(0,0,0,0)
        self.setFixedSize(self.size())
        self.children = [] #place to save child window refs


        outerLayout = QVBoxLayout()
        topLayout = QFormLayout()
        filtersLayout = QGridLayout()
        checksLayout = QGridLayout()

        #Nest the layouts
        
        outerLayout.addLayout(topLayout)
        outerLayout.addLayout(filtersLayout)  
        filtersLayout.addLayout(checksLayout,2,0,1,2)  

        #Create Search Bar Widget

        self.searchBar = QLineEdit(self)
        self.searchBar.setPlaceholderText("Event/Team Name e.g \'2915U\'")

        #Create a Search Button Widget
        
        self.searchButton = QPushButton("Search", self)
        self.searchButton.setToolTip('Search with the selected Queries')
        self.searchButton.clicked.connect(self.search)

        #Create A Search Widget for Searching by ID

        self.searchID = QLineEdit(self)
        self.searchID.setPlaceholderText("Event ID or Team ID e.g \'129267\'")

        #Create a ComboBox Widget for Filters

        self.querySelectorCombo = QComboBox()
        self.querySelectorCombo.addItems(['Teams','Events'])
        self.querySelectorCombo.setToolTip('Search for \'Teams\' or \'Events\'')
        self.querySelectorCombo.currentIndexChanged.connect(self.queryChange)

        #Create a ComboBox Widget for Event Level Filter

        self.eventLevelCombo = QComboBox()
        self.eventLevelCombo.addItems(['','World','National','State','Signature','Other'])
        self.eventLevelCombo.setToolTip('Search based on event Level \'All\', \'World\', \'National\', \'State\', \'Signature\' or \'Other\'')
        self.eventLevelCombo.setEnabled(False) #Disable by default because Teams cannot be searched by event level

        #Create a ComboBox Widget for Event Type Filter

        self.eventTypeCombo = QComboBox()
        self.eventTypeCombo.addItems(['','Tournament', 'League', 'Workshop','Virtual'])
        self.eventTypeCombo.setToolTip('Search based on event Type \'All\', \'Tournament\', \'League\', \'Workshop\' or \'Virtual\'')
        self.eventTypeCombo.setEnabled(False) #Disable by default because Teams cannot be searched by event type

        #Create two CheckBox Widgets for Team Program

        self.teamVRCCheck = QCheckBox()
        self.teamVIQCCheck = QCheckBox()
        self.teamVEXUCheck = QCheckBox()
        
        self.teamVRCCheck.setText('VRC')   #id:1
        self.teamVIQCCheck.setText('VIQC') #id:41
        self.teamVEXUCheck.setText('VexU') #id:4

        #Create a ComboBox Widget for Team Grade Filter

        self.teamGradeCombo = QComboBox()
        self.teamGradeCombo.addItems(['','College', 'High School', 'Middle School'])
        self.teamGradeCombo.setToolTip('Search based on team school type \'All\', \'College\', \'High School\' or \'Middle School\'')

        #Create a ComboBox Widget for Team Country Filter

        self.teamCountryCombo = QComboBox()
        self.teamCountryCombo.addItems(countryList)
        self.teamCountryCombo.setToolTip('Search based on team Country')
        self.teamCountryCombo.setStyleSheet("QComboBox { combobox-popup: 0; }")
        self.teamCountryCombo.setMaxVisibleItems(8)

        # Add Everything to a Layout

        topLayout.addRow("Search Bar:", self.searchBar)
        topLayout.addRow("Search By ID:", self.searchID)
        filtersLayout.addWidget(self.querySelectorCombo, 0, 0, 1, 2)
        filtersLayout.addWidget(self.eventLevelCombo, 1, 0)
        filtersLayout.addWidget(self.eventTypeCombo, 1,1)
        checksLayout.addWidget(self.teamVRCCheck,0,0)
        checksLayout.addWidget(self.teamVIQCCheck,0,1)
        checksLayout.addWidget(self.teamVEXUCheck, 0,3)
        filtersLayout.addWidget(self.teamGradeCombo,3,0)
        filtersLayout.addWidget(self.teamCountryCombo,3,1)
        filtersLayout.addWidget(self.searchButton, 4,0,1,2)

        self.setLayout(outerLayout)


    def queryChange(self):

        if self.querySelectorCombo.currentText() == 'Teams':
            self.eventLevelCombo.setEnabled(False)
            self.eventTypeCombo.setEnabled(False)
            self.teamVIQCCheck.setEnabled(True)
            self.teamVRCCheck.setEnabled(True)
            self.teamVEXUCheck.setEnabled(True)
            self.teamGradeCombo.setEnabled(True)
            self.teamCountryCombo.setEnabled(True)

        if self.querySelectorCombo.currentText() == 'Events':
            self.eventLevelCombo.setEnabled(True)
            self.eventTypeCombo.setEnabled(True)
            self.teamVIQCCheck.setEnabled(False)
            self.teamVRCCheck.setEnabled(False)
            self.teamVEXUCheck.setEnabled(False)
            self.teamGradeCombo.setEnabled(False)
            self.teamCountryCombo.setEnabled(False)
            


    def search(self):

        programVIQC = ''
        programVRC = ''
        number = ''
        grade = 'grade%5B%5D=College&grade%5B%5D=High%20School&grade%5B%5D=Middle%20School'
        programVIQC = ''
        programVRC = ''
        programVEXU = ''
        level = 'level%5B%5D=World&level%5B%5D=State&level%5B%5D=National&level%5B%5D=Signature'
        type = 'eventTypes%5B%5D=Tournament&eventTypes%5B%5D=League&eventTypes%5B%5D=Workshop&eventTypes%5B%5D=Virtual'
        region= ''


        id = "id%5B%5D={0}".format(self.searchID.text())
        if not self.searchID.text(): id = ''
        search = self.searchBar.text()
        self.searchBool = False

        if self.querySelectorCombo.currentText() == 'Teams':
            if search: number = "number%5B%5D={0}".format(search)
            if self.teamCountryCombo.currentText(): region = "country%5B%5D={0}".format(self.teamCountryCombo.currentText()[1:3])
            if self.teamGradeCombo.currentText(): grade = "grades%5B%5D={0}".format(self.teamGradeCombo.currentText().replace(" ", "%20"))
            if self.teamVIQCCheck.isChecked(): programVIQC = "program%5B%5D=41"
            if self.teamVRCCheck.isChecked(): programVRC = "program%5B%5D=1"
            if self.teamVEXUCheck.isChecked(): programVEXU="program%5B%5D=4"
            self.request = 'teams?page=1&{0}&{1}&{2}&{3}&{4}&{5}'.format(number,region,grade,programVIQC,programVRC,programVEXU)
            self.items = search_team_info(self.request,0)
            

        if self.querySelectorCombo.currentText() == 'Events':
            self.searchBool = True
            if self.eventLevelCombo.currentText(): level = 'level%5B%5D={0}'.format(self.eventLevelCombo.currentText())
            if self.eventTypeCombo.currentText(): type = 'eventType%5B%5D={0}'.format(self.eventTypeCombo.currentText())
            self.request = 'events?page=1&{0}&{1}'.format(level,type)
            print(self.request)
            self.items = search_event_info(self.request,0,"")
        
        self.createChildInstance()
        

    def createChildInstance(self):
        child = ListChild(self.items, self.searchBool, self.request)
        child.show()
        self.children.append(child)


class ListChild(QWidget):
    def __init__(self, items, searchBool, request):
        super().__init__()
        self.items = items
        self.request = request
        self.searchBool = searchBool

        self.setWindowTitle("VexTracker Search Instance")
        self.setWindowIcon(QIcon('./vextrackericon.png'))
        self.setGeometry(0,0,1000,400)
        #self.setFixedSize(self.size())
        #self.setParent(SearchWindow)
        self.children = [] #place to save child window refs

        outerLayout = QVBoxLayout()
        mainLayout = QHBoxLayout()
        buttonLayout= QHBoxLayout()

        #create and nest layouts

        self.searchList = QListWidget(self)
        #self.searchList.setFixedSize(500,340)
        self.searchList.setFont(QFont("Arial",20))
        
        self.searchList.itemClicked.connect(self.listClicked)
 
        self.updateList()


        #Create a Previous Page Button Widget
        
        self.prevButton = QPushButton("Previous Page", self)
        self.prevButton.setToolTip('Previous Page')
        self.prevButton.clicked.connect(self.prevPage)

        #Create a Next Page Button Widget
        
        self.nextButton = QPushButton("Next Page", self)
        self.nextButton.setToolTip('Next Page')
        self.nextButton.clicked.connect(self.nextPage)

        #Add everything to a layout

        mainLayout.addWidget(self.searchList)
        buttonLayout.addWidget(self.prevButton)
        buttonLayout.addWidget(self.nextButton)

        outerLayout.addLayout(mainLayout)
        outerLayout.addLayout(buttonLayout)

        self.setLayout(outerLayout)

        # Enable/Disable Next/Previous Page Buttons 

        self.updateButtons()


    def updateButtons(self):
        if self.page == 1:
            self.prevButton.setEnabled(False)
        if self.page == self.last_page:
            self.nextButton.setEnabled(False)
        if self.page != self.last_page:
            self.nextButton.setEnabled(True)
        if self.page != 1:
            self.prevButton.setEnabled(True)


    def nextPage(self):
        sPage = self.request.find('=') + 1
        ePage = self.request.find('&')

        current_page = self.request[sPage:ePage]
        newrequest = self.request.replace("page={0}".format(current_page), "page={0}".format(self.page+1))
        if self.searchBool:
            self.items = search_event_info(newrequest,0,"")
        else:
            self.items = search_team_info(newrequest,0)
        self.updateList()
        self.updateButtons()

        
    def prevPage(self):
        sPage = self.request.find('=') + 1
        ePage = self.request.find('&')

        current_page = self.request[sPage:ePage]
        newrequest = self.request.replace("page={0}".format(current_page), "page={0}".format(self.page-1))
        if self.searchBool:
            self.items = search_event_info(newrequest,0,"")
        else:
            self.items = search_team_info(newrequest,0)
        self.updateList()
        self.updateButtons()


    def updateList(self):

        self.page = self.items[0]
        self.last_page = self.items[1]

        del self.items[0]
        del self.items[0]

        self.setWindowTitle("VexTracker Search Instance page {0} of {1}".format(self.page, self.last_page))
        
        self.searchList.clear()

        if not self.searchBool:
            for elm in range(len(self.items)):
                self.searchList.addItem("{0}".format(self.items[elm][1].replace("number:", "")))
        if self.searchBool:
            for elm in range(len(self.items)):
                self.searchList.addItem("{0}".format(self.items[elm][1].replace("name:","")))
        self.searchList.update()

    def listClicked(self):
        if not self.searchBool:
            item = "number:{0}".format(self.searchList.currentItem().text())
        if self.searchBool:
            item = "name:{0}".format(self.searchList.currentItem().text())
        
        for i in range(len(self.items)):
            if item == self.items[i][1]:
                self.item = self.items[i]
                self.createChildInstance()
                break


    def createChildInstance(self):
        child = elementInfo(self.item, self.searchBool)
        child.show()
        self.children.append(child)

    
class elementInfo(QWidget):
    def __init__(self, item, searchBool):
        super().__init__()

        self.item = item
        self.searchBool = searchBool
        
        if self.searchBool:
            self.setWindowTitle("VexTracker Event Info Instance")
        else:
            self.setWindowTitle("VexTracker Team Info Instance")

        self.setWindowIcon(QIcon('./vextrackericon.png'))
        self.setGeometry(0,0,600,600)
        self.setStyleSheet("QLabel{font-size: 12pt;}")

        outLayout = QVBoxLayout()
        outerlabelLayout = QGridLayout()

        listLayout = QGridLayout()
        self.setLayout(outLayout)

        #create all Layouts

        self.idLabel = QLabel("{0}".format(item[0]))
        self.numberLabel = QLabel("{0}".format(item[1]))
        self.robotnameLabel = QLabel("{0}".format(item[2]))
        self.locationLabel = QLabel("{0}".format(item[3]))
        self.programLabel = QLabel("{0}".format(item[4]))


        if searchBool: #if events
            teams = search_event_teams("{0}".format(item[0].replace("id: ", "")))
            awards = search_event_awards("{0}".format(item[0].replace("id: ", "")))

            self.awardList = QListWidget(self)
            self.awardList.setFixedSize(400,300)
            self.awardList.setFont(QFont("Arial", 15))

            self.teamList = QListWidget(self)
            self.teamList.setFixedSize(400,300)
            self.teamList.setFont(QFont("Arial", 13))

            self.awardLabel = QLabel("Awards:")
            self.teamLabel = QLabel("Teams:")
            self.awardLabel.setAlignment(Qt.AlignBottom)
            self.teamLabel.setAlignment(Qt.AlignBottom)

            for award in range(len(awards)):
               self.awardList.addItem("{0}{1}".format(awards[award][0],awards[award][1]))
            
            for team in range(len(teams)):
                self.teamList.addItem("{0}, {1}".format(teams[team][0],teams[team][1]))

            listLayout.addWidget(self.awardLabel,3,0)
            listLayout.addWidget(self.teamLabel,3,1)
            listLayout.addWidget(self.awardList,4,0)
            listLayout.addWidget(self.teamList,4,1)
            pass
        if not searchBool: #if team
            rankings = search_team_events("{0}".format(item[0].replace("id: ", "")))
            awards = search_team_awards("{0}".format(item[0].replace("id: ", "")))

            self.awardList = QListWidget(self)
            self.awardList.setFixedSize(400,300)
            self.awardList.setFont(QFont("Arial", 15))

            self.rankingList = QListWidget(self)
            self.rankingList.setFixedSize(400,300)
            self.rankingList.setFont(QFont("Arial", 13))

            self.awardLabel = QLabel("Awards:")
            self.rankLabel = QLabel("Rankings:")
            self.awardLabel.setAlignment(Qt.AlignBottom)
            self.rankLabel.setAlignment(Qt.AlignBottom)

            for award in range(len(awards)):
                self.awardList.addItem("{0}, {1}".format(awards[award][1],awards[award][0]))
            
            for ranking in range(len(rankings)):
                self.rankingList.addItem("{0}, rank:{1}, {2}".format(rankings[ranking][2],rankings[ranking][1],rankings[ranking][0]))

            listLayout.addWidget(self.awardLabel,3,0)
            listLayout.addWidget(self.rankLabel,3,1)
            listLayout.addWidget(self.awardList,4,0)
            listLayout.addWidget(self.rankingList,4,1)

        #create labels for data

        outerlabelLayout.addWidget(self.idLabel, 1 ,3) #id
        outerlabelLayout.addWidget(self.numberLabel,0,4) #number
        outerlabelLayout.addWidget(self.robotnameLabel,0,2) #team name
        outerlabelLayout.addWidget(self.locationLabel,1,6) #robotname
        outerlabelLayout.addWidget(self.programLabel,1,1) #location

        self.idLabel.setAlignment(Qt.AlignCenter) #id
        self.programLabel.setAlignment(Qt.AlignLeft) #location
        self.robotnameLabel.setAlignment(Qt.AlignLeft) #team name
        self.locationLabel.setAlignment(Qt.AlignRight) #robotname
        self.numberLabel.setAlignment(Qt.AlignRight) #number

        #add everything to a Layout

        outLayout.addLayout(outerlabelLayout)
        outLayout.addLayout(listLayout)


        #nest Layouts

def main():
    app = QApplication(sys.argv)
    win = SearchWindow()
    win.show()
    sys.exit(app.exec_())
        

if __name__ == '__main__':
    main()
