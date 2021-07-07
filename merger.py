# REMEMBER TO RUN WITH PYTHON3

# csv module to read and write csv files
# glob module finds all pathnames matching specified pattern
# using os to find file size for mergin algo
import csv, glob, os

########## Functions ##############

# function takes csv file read object and return rows in that file
def createDataRows(csvreader):
    rows = []

    # iterate each row and add to rows array
    for row in csvreader:
        rows.append(row)

    return rows

# Where the magic happens ;)
# take in first file and second file being read
def appendNewData(original, newData):

    # iterate over the original file and use enumerate function to access index
    # all files should have same indexes based on universal headers
    for index, value in enumerate(original):
        # skip EventID and Title data cells
        if index == 0 or index == 1:
            continue
        # remainder of content is compared
        if original[index] != newData[index]:
            # as long as string does not already exits in that cell it will be appended
            if original[index].find(newData[index]) == -1:
                original[index] = original[index] + ' | ' + newData[index]

    return original

# read original and file file to be merged
def readAndModify(file1, file2):
    # initialize modified data
    modifiedData = []
    headers = []

    # open file in read mode and assign it a variable for file object
    # third argument encoding system for Unicode (to not get hexidecimal values while parsing)
    with open(file1, 'r', encoding='utf-8') as reader1, open(file2, 'r', encoding='utf-8') as reader2:
        # create csv reader object from file object
        csvreader1 = csv.reader(reader1)
        csvreader2 = csv.reader(reader2)

        # checks if first master is being used (blank file)
        newMaster = os.stat(file1).st_size == 0

        # extract headers from master or merge file
        if newMaster == True:
            headers = next(csvreader2)
        else:
            headers = next(csvreader1)

        # extracting rest of data from each file
        rows1 = createDataRows(csvreader1)
        rows2 = createDataRows(csvreader2)

        # iterate over both data sets
        # if rows are both at index 1 (Title Header)
        # use appendNewData function to compare that row in both files
        ogTitles = []
        for x in rows1:
            ogTitles.append(x[1])
            append = False
            for y in rows2:
                if x[1] == y[1]:
                    append = True

                if append == True:
                    appendNewData(x,y)
                    append = False

        # if a new blank master is being used there is no data
        # second set of rows will populate master (merger file)
        if newMaster == True:
            modifiedData = rows2
        else:
            modifiedData = rows1

        # no need to check for new rows on blank master
        # all rows are copied on first pass
        if newMaster == False:
            # check merge file for new rows not in master (skip headers)
            for y in rows2[1:]:
                found = y[1] not in ogTitles
                if found == True:
                    print(found, y[1])
                    modifiedData.append(y)

        # close opened files after reading
        reader1.close()
        reader2.close()

    return [headers, modifiedData]

# open master, write headers (results[0]), write data (results[1])
def writeNewFile(results):
    with open('master.csv', mode='w') as master:
        master_writer = csv.writer(master)

        master_writer.writerow(results[0])

        for x in results[1]:
            master_writer.writerow(x)

    master.close()

########## Main ##############
if __name__ == "__main__":
    # create new master file
    with open('master.csv', mode='w') as master:
        pass
    master.close()

    # list of files with ext .csv in current working directory
    files = glob.glob("*.csv")

    print('Merging the following Files:\n')
    # iterate over the list of files and merge into master file
    for file in files:
        if file == 'master.csv':
            if os.stat(file).st_size == 0:
                continue
        print(file)
        result = readAndModify('master.csv', file)
        writeNewFile(result)

    print('\nmaster.csv has been created/updated')
    print('\nMerging complete')

