# For taking a books ISBN or ISSN and adding it to a spreadsheet with info

import isbnlib
import csv
# Refer to https://github.com/fabiobatalha/crossrefapi for documentation
# on using the crossref API for getting info from ISSNs and DOIs
from crossref.restful import Journals


def createISBNLibraryFile(filename):
    '''
    This function is to create a .csv file given a name for the file
    It will also add in the first row for the file; headings for all book info
    Inputs: filename, name of the file as a string
    Outputs: Creates a file with first row filled in
    '''
    # Get a sample ISBN for header purposes
    sampleISBN = "978-0-099-52848-7"  # Call of Cthulu (Nominal data)
    isbn = isbnlib.canonical(sampleISBN)
    itemKeys = isbnlib.meta(isbn).keys()

    # Open file and write header row
    with open(filename, 'w') as file:
        write = csv.writer(file)
        write.writerow(itemKeys)


def addBookToISBNLibrary(filename, isbnRaw):
    '''
    This function adds an item to the library given the ISBN
    Inputs: filename, name of the library file, isbnRaw, ISBN of
    the item to be added in ISBN-13 format as string (e.g. 978-0-099-52848-7)
    also accepts canonical verson (e.g. 9780099528487)
    Outputs: Writes a new row in the given file
    '''

    # Translate string into ISBN canonical format
    isbn = isbnlib.canonical(isbnRaw)
    itemInfo = isbnlib.meta(isbn)
    ItemValues = itemInfo.values()

    # Write item information into the csv
    with open(filename, 'a', newline='') as file:
        write = csv.writer(file)
        write.writerow(ItemValues)


def testISBNAppending(filename):
    '''
    Test function that just uses a few random ISBNs to check
    whether appending rows to the exisiting csv is working correctly
    '''
    isbnRaws = ["978-0-099-52848-7", "978-0-14-119480-6", "978-0-340-96019-6"]
    for isbn in isbnRaws:
        addBookToISBNLibrary(filename, isbn)


def testISSN(issn):
    # works = Works()
    # info = works.doi('10.2514/8.7231')
    journals = Journals()
    info = journals.journal(issn)
    '''
    info.pop('last-status-check-time')
    info.pop('counts')
    info.pop('breakdowns')
    info.pop('flags')
    info.pop('coverage')
    info.pop('coverage-type')
    print(info)
    for x in info:
        print(x)
    '''
    print(info)


def testISSNAppending(filename):
    '''
    Test function that just uses a few random ISSNs to check
    whether appending rows to the exisiting csv is working correctly
    '''
    issnRaws = ["0002-2667", "1096-1216",  "1000-9361"]
    for issn in issnRaws:
        infoList = getInfoFromISSN(issn)
        addEntryToISSNLibrary(filename, infoList)


def createISSNLibraryFile(filename):
    '''
    Makes a library file for ISSN items, e.g. magazines or other serials
    Inputs: filename, name for the file including .csv
    Outputs: Creates file and fills in header row
    '''
    categoryList = ['ISSN', 'ISSN Type', 'Title',
                    'Publisher', 'Subjects', 'Year',
                    'Month', 'Volume', 'Issue']
    with open(filename, 'w') as file:
        write = csv.writer(file)
        write.writerow(categoryList)


def getInfoFromISSN(issn):
    # Retrieve all information about the ISSN
    journals = Journals()
    info = journals.journal(issn)

    string = ","

    # Retrieve the properties we care about only
    itemTitle = info.get('title')
    itemPub = info.get('publisher')
    itemSubj = info.get('subjects')
    itemISSN = info.get('ISSN')
    itemISSNinfo = info.get('issn-type')

    # Go through non-string entities and format
    string = ""
    # Loop through dict values in list
    for x in itemSubj:
        # Gets all the values from this dict
        # and stores all values in a list
        temp = [*x.values()]
        # Joins the items from the list and seperates with a comma
        temp = ', '.join(map(str, temp))
        # Adds current dict entry (now string of values) to a string
        string = string + temp + ', '
    # Removes trailing ', '
    itemSubj = string[:-2]

    # Join all ISSNs for this item using a ,
    itemISSN = ", ".join(itemISSN)

    string = ""
    # Loop through dict values in list
    for x in itemISSNinfo:
        # Gets all the values from this dict
        # and stores all values in a list
        temp = [*x.values()]
        # Joins the items from the list and seperates with a comma
        temp = ', '.join(map(str, temp))
        # Adds current dict entry (now string of values) to a string
        string = string + temp + ', '
    # Removes trailing ', '
    itemISSNinfo = string[:-2]

    infoList = [itemTitle, itemPub, itemSubj,
                itemISSN, itemISSNinfo]
    return infoList


def addEntryToISSNLibrary(filename, infoList):
    '''
    Appends a new entry to the ISSN library based on the info in it
    Inputs: filename, issn (both strings)
    Outputs: Appends issn information to the given file
    '''
    with open(filename, 'a', newline='') as file:
        write = csv.writer(file)
        write.writerow(infoList)
    print("Entry added")


def getISSNInput():
    # Warning! Theres no error checking on user input here so make sure
    # you do it right or edit in the .csv manually later
    print("Please enter the information about the curent item,"
          "entering N/A if not applicable")
    itemISSN = input("ISSN (including '-'): ")
    itemYear = input("Year item was published: ")
    itemMonth = input("Month item was published: ")
    itemVolume = input("Item volume: ")
    itemNumber = input("Item number: ")
    print("Processing...")
    inputList = [itemISSN, itemYear, itemMonth, itemVolume, itemNumber]
    return inputList


def mergeISSNLists(inputList, infoList):
    mergedList = [infoList[3], infoList[4], infoList[0],
                  infoList[1], infoList[2], inputList[1],
                  inputList[2], inputList[3], inputList[4]]
    return mergedList


if __name__ == "__main__":
    filename1 = "ISBNlibrary.csv"
    filename2 = "ISSNlibrary.csv"

    createISBNLibraryFile(filename1)
    testISBNAppending(filename1)
    # addBookToLibrary(filename, "978-0-099-52848-7")
    # testISSN('0002-2667')
    # testISSN('1096-1216')
    #
    # ISSN Library Builder
    #
    # Build the library file
    #createISSNLibraryFile(filename2)
    # Get input from user
    #inputList = getISSNInput()
    # Retrieve rest of information using ISSN
    #infoList = getInfoFromISSN(inputList[0])
    # Take relevent data from both lists and order them
    #mergedList = mergeISSNLists(inputList, infoList)
    #addEntryToISSNLibrary(filename2, mergedList)
    # testISSN('0002-2667')
    # testISSN('0261-2097')
    # journals = Journals()
    # x = journals.journal('2052-451X')
    # x = journals.journal('0102-311X')
