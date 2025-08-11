import re 
# Function to extract text from PDF
from PyPDF2 import PdfReader

#do i need to try importing regex instead???/
document = PdfReader("example.pdf")
#STEP 1: EXTRACT UNIT NAME

#########                                                                     Function: find datapoint 1---                        
pgs = len(document.pages)
print ("the number of pages:") 
print (pgs)

### B) extract all data 
### C) SAVE EACH INDEX LOCATION AS A VARIABLE I CAN CALL LATER
### D) MAKE A LINE OF CODE THAT RETRIEVES THE TEXT BETWEEN TWO INDECIES

pagenumber = 0
print ("starting code now")
foundtable = []
pagetable = []
#goal for today - make the data into a variable 
#the following should probably be made into a function I can call
#inputs to the function would be A) PDF name B) item to be searched for (Start) item to be searched for (end)





def scrapePDF (startword, endword):
    for pagenumber in range (pgs):    
        page = document.pages[pagenumber]
        try: 
            data = page.extract_text()
            #TURN ON THE LINE BELOW TO SEE THE DATA BEING READ
            #to see all data remove break in if satement
            #print(data)
        except:
            print ("Scanning failed for page number", pagenumber+1,"if there is data here, Please import data manually... sorry homie")

        wordlength = (startword)
        indexstart = data.find (startword)
        searchlength = len(wordlength)
        endofstartword = (indexstart + searchlength)
        indexend = data.find (endword)
        result = (data[endofstartword:indexend])
        #print   ("beginning search of page", pagenumber, "for the data in between", startword,"and", endword)
       
        if indexstart != -1 and indexend != -1:
                foundtable.append(result)
                print ("MATCH on page", pagenumber+1)
                print (result, "will be added to table and search shall end")
                break
                #if pagenumber = pages
                #print ("")
        #if pagenumber == pgs:            -------------   maybe this needs to be elif? 
           # print ("no result found for", startword, "or", endword, "search will end")
            #break
       
        else: print ("no match for", startword, "or", endword, "found on page", pagenumber+1)

scrapePDF("Unit Overview - ", "Application")
scrapePDF("Airflow", "Total Static Pressure")
scrapePDF("Pressure", "in H2O")

print ("                   ")
print ("                   ")
print ("this is the final result",foundtable)   
print ("                   ")

        #if both of the searches were found then append a found table with the extracted string 

        #I WOULD LIKE TO SEE A FUNCTION HERE THAT CHECKS THE RESULT STRING AND REMOVES BLANKS OR OTHER NON CHARACTERS BEFORE AND AFTER THE INTENDED STRING
        #THE ABOVE CODE WORKS FOR ONE PAGE... HOW DO I MAKE IT WORK FOR MULTIPLE PAGES
'''
def scrapePDFandduplicates (startword, endword):
    for pagenumber in range (pgs):    
        page = document.pages[pagenumber]
        try: 
            data = page.extract_text()
        except:
            print ("Scanning failed for page number", pagenumber+1,"if there is data here, Please import data manually... sorry homie")

        #TURN ON THE LINE BELOW TO SEE ALL DATA THAT IS BEING READ BY THE LINE ABOVE
        #print(data)
        #indexstart = re.search()("Unit Overview", data)
        wordlength = (startword)
        indexstart = data.find (startword)
        searchlength = len(wordlength)
        endofstartword = (indexstart + searchlength)
        #print ("the code says")
        #print (indexstart)
        indexend = data.find (endword)
        #print ("index end found at")
        #print (indexend)
        #print ("THE FINAL RESULT ISSS")
        result = (data[endofstartword:indexend])
        #print (result)
        #print   ("beginning search of page", pagenumber, "for the data in between", startword,"and", endword)
        if indexstart != -1 and indexend != -1:
                foundtable.append(result)
                print ("MATCH on page", pagenumber+1)
                print (result, "will be added to table")
                #if both of the searches were found then append a found table with the extracted string 
        else: print ("no match found on page", pagenumber)

                

        #if both of the searches were found then append a found table with the extracted string 

        #I WOULD LIKE TO SEE A FUNCTION HERE THAT CHECKS THE RESULT STRING AND REMOVES BLANKS OR OTHER NON CHARACTERS BEFORE AND AFTER THE INTENDED STRING
        #THE ABOVE CODE WORKS FOR ONE PAGE... HOW DO I MAKE IT WORK FOR MULTIPLE PAGES
'''


'''
for pagenumber in range (pgs-1):
    try:
        #print (f"scanning page number -- {pagenumber + 1} of {pgs}" )
        page = document.pages[pagenumber]
        data = page.extract_text()
        #TURN ON THE LINE BELOW TO SEE ALL DATA THAT IS BEING READ BY THE LINE ABOVE
        #print(data)
        indexstart = re.search()("Unit Overview", data)
        indextest = data.find ("Unit Overview")
        print ("the code says")
        print (indextest)
        if indexstart != None: 
            print ("agghhh this is NOT WORKING FOR MEEE")
            print(indexstart)
            foundtable.append(indexstart)
            pagetable.append(pagenumber-1)
            print (indexstart)
            print (data)
        indexend = re.search ("Application", data)
        if indexend != None:
            foundtable.append(indexend)
            print ("                            PAGE SCAN COMPLETE")
            print(foundtable)
            #there could be an issue with the way I'm printing 
        print (data)
    except: 
        #learn more about "except" in python
        #maybe I need a line like - is data a string or is data null. if data is null make it a string
        print (" done)")
        #example one is if the pdf has a blank page it will shit the bed
'''
# THE PROBLEM HERE IS THAT THE PDF IS READING A BLANK PAGE AND THEN CUTS THE PROGRAM SHORT BECAUSE IT DOESN'T KNOW WHAT TO DOOOOOO
#print (foundtable)

#start = foundtable [0]
#end = foundtable [1]
#pagenumber = pagetable[0]
#print (start , end)

# we are going to re-write this for loop from scratch to see if that would fix it 
'''
for pagenumber in range (pgs-1):

    page = document.pages[pagenumber]
#instead of printing on the next line I should make a parameter for what I will search for
    data = (page.extract_text())
    #print (data)
    result = re.search ("Unit Overview", data)
    print (result)
    #If match is found, save as a variable?
    if result != None:
        print ("bingo")
        endspan = result.end
        print(f"End span of match on page {pagenumber + 1}")
        pagenumber += 1
        print (f"the new page number is {pagenumber}")

    if pgs == pagenumber -1:
        print ("test line a make break on page")
        break

'''


print ("THIS IS A LONG LINE OF TEXT TO VERIFY THAT MY CODE IS MOVING TO THIS LINE")

### find required daata       (re.search(data, "Unit Overview"))

### index location of data point
#print (result)
   

'''
for page in reader.pages:
    if "/Annots" in page:
        for annot in page["/Annots"]:
            subtype = annot.get_object()["/Subtype"]
            if subtype == "/Text":
                print(annot.get_object()["/Contents"])
### C) find "unit overview"
### D) Extract all data untiil next line 
#########                                                                 -------------------------------------
#GENERAL ROADMAP
#create a 1-1 pdf that shows the data in excel and where it comes from in the pdf

#EXTRACT THE REQUIRED ELEMENTS FROM THE PDF

#FORMAT THE DATA IN EXCEL   
'''
'''
# Function to process extracted data (you can modify based on your data structure)
def process_text_to_dataframe(text):
    # Assuming each line in PDF corresponds to a row in Excel
    data = [line.split() for line in text.split('\n') if line]  # Modify as per your PDF structure
    df = pd.DataFrame(data)
    return df

# Function to write data to Excel
def write_data_to_excel(df, excel_path):
    with pd.ExcelWriter(excel_path, engine='openpyxl') as writer:
        df.to_excel(writer, index=False)

# Main function to run the process
def pdf_to_excel(pdf_path, excel_path):
    pdf_text = extract_text_from_pdf(pdf_path)
    df = process_text_to_dataframe(pdf_text)
    write_data_to_excel(df, excel_path)
    print(f"Data successfully written to {excel_path}")

# Example usage:
pdf_path = 'input.pdf'
excel_path = 'output.xlsx'

pdf_to_excel(pdf_file, excel_file)

'''