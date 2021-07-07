# REMEMBER TO RUN WITH PYTHON3

# importing built in python csv module
import csv

#Functions

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
    headers1 = []
    headers2 = []

    # open file in read mode and assign it a variable for file object
    # third argument encoding system for Unicode (to not get hexidecimal values while parsing)
    with open(file1, 'r', encoding='utf-8') as reader1, open(file2, 'r', encoding='utf-8') as reader2:

        # create csv reader object from file object
        csvreader1 = csv.reader(reader1)
        csvreader2 = csv.reader(reader2)

        # extracting field names through first rows
        headers1 = next(csvreader1)
        headers2 = next(csvreader2)

        # extracting rest of data from each file
        rows1 = createDataRows(csvreader1)
        rows2 = createDataRows(csvreader2)

        # iterate over both data sets
        # if rows are both at index 1 (Title Header)
        # use appendNewData function to compare that row in both files
        for x in rows1:
            append = False
            for y in rows2:
                if x[1] == y[1]:
                    append = True

                if append == True:
                    appendNewData(x,y)
                    append = False

        modifiedData = rows1

        # close opened files after reading
        reader1.close()
        reader2.close()

    return [headers1, modifiedData]

def writeNewFile(results):
    # create
    with open('master.csv', mode='w') as master:
        master_writer = csv.writer(master)

        master_writer.writerow(results[0])

        for x in results[1]:
            master_writer.writerow(x)

    master.close()

# main
if __name__ == "__main__":
    print('Input files to be merged.\n')
    print('First file must be the "Master" file.\n')
    print('Master File: ')

    # csv file names
    file1 = input()
    print("\nName of file to be merged: ")
    file2 = input()

    print('Merging Files')

    results = readAndModify(file1, file2)

    writeNewFile(results)

    print('Merging Complete')




