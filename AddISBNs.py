from Libraryify import addISBNFromUser, testISBNAppending


if __name__ == "__main__":
    filename = "ISBNlibrary.csv"
    #testISBNAppending(filename)
    while True:
        addISBNFromUser(filename)
