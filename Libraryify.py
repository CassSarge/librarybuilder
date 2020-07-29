# For taking a books ISBN or ISSN and adding it to a spreadsheet with info

import isbnlib
import csv
# Refer to https://github.com/fabiobatalha/crossrefapi for documentation
# on using the crossref API for getting info from ISSNs and DOIs
from crossref.restful import Works
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
    works = Works()
    journals = Journals()
    # info = works.doi('10.2514/8.7231')
    info = journals.journal(issn)
    info.pop('last-status-check-time')
    info.pop('counts')
    info.pop('breakdowns')
    info.pop('flags')
    info.pop('coverage')
    info.pop('coverage-type')
    print(info)
    for x in info:
        print(x)


def createISSNLibraryFile(filename):
    '''
    Makes a library file for ISSN items, e.g. magazines or other serials
    Inputs: filename, name for the file including .csv
    Outputs: Creates file and fills in header row
    '''
    categoryList = ['Title', 'Publisher', 'Subjects',
                    'ISSN', 'ISSN Type']
    with open(filename, 'w') as file:
        write = csv.writer(file)
        write.writerow(categoryList)


def addEntryToISSNLibrary(filename, issn):
    '''
    Appends a new entry to the ISSN library based on the info in it
    Inputs: filename, issn (both strings)
    Outputs: Appends issn information to the given file
    '''
    journals = Journals()
    info = journals.journal(issn)
    itemTitle = info.get('title')
    itemPub = info.get('publisher')
    itemSubj = info.get('subjects')
    itemISSN = info.get('ISSN')
    itemISSNinfo = info.get('issn-type')
    infoList = [itemTitle, itemPub, itemSubj, itemISSN, itemISSNinfo]
    with open(filename, 'a', newline='') as file:
        write = csv.writer(file)
        write.writerow(infoList)


def testISSNAppending(filename):
    '''
    Test function that just uses a few random ISSNs to check
    whether appending rows to the exisiting csv is working correctly
    '''
    issnRaws = ["0002-2667", "1096-1216",  "1000-9361"]
    for issn in issnRaws:
        addEntryToISSNLibrary(filename, issn)


if __name__ == "__main__":
    filename1 = "ISBNlibrary.csv"
    filename2 = "ISSNlibrary.csv"
    createISBNLibraryFile(filename1)
    testISBNAppending(filename1)
    # addBookToLibrary(filename, "978-0-099-52848-7")
    # testISSN('0002-2667')
    # testISSN('1096-1216')
    createISSNLibraryFile(filename2)
    testISSNAppending(filename2)
    # addEntryToISSNLibrary(filename2, '0002-2667')
