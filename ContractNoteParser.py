import os
import PyPDF2
from PyPDF2 import PdfFileReader, PdfFileWriter
import tabula
import csv

def parse_file(fileName,folderName):
    print(f'Hi, The file name is  {folderName+fileName}')
    pdf_file = open(folderName+fileName,'rb')
    read_pdf = PyPDF2.PdfFileReader(pdf_file)

    password ="VVVV"
    # Check if the opened file is actually Encrypted
    if read_pdf.isEncrypted:
        print ("File is password protected")
        # If encrypted, decrypt it with the password
        read_pdf.decrypt(password)
        writer = PdfFileWriter()

        for i in range(read_pdf.getNumPages()):
            writer.addPage(read_pdf.getPage(i))


    writer.write( open(fileName+"_decrypted", 'wb') )

    # convert PDF into CSV
    tabula.convert_into(fileName+"_decrypted", "samplefiles/output.csv", output_format="csv", pages='all')

    # in the csv delete the files before the keyword "Segment"

    input = open("samplefiles/output.csv", 'rt')
    output = open("samplefiles/output_updated.csv", 'wt')
    second_output = open("consolidated_holdings/consolidated_holdings.csv", 'a')

    writer = csv.writer(output)
    second_writer = csv.writer(second_output)
    toggle=False;
    headerIdentified=False;


    for row in csv.reader(input):
        if (row[0]=="Trade Date"):
            print (row[1]);
            tradeDate=row[1]
        if (row[0]=="Segment"):
            toggle=True;

        # Remove case where the summary table is multipage
        if (row[0]=="BSE-Cash"):
            toggle=False;
        if (row[0]=="NSE-Cash"):
            toggle=False;

        if toggle:
            if (row[0] == "Sub Total" or row[0] == "Total"):
                # Shift thr row by 1.
                #writer.writerow(','.join(row))
                writer.writerow([' ']+row)
            else:
                # check if header has alredy been written then do not write it again
                if (row[0] == "Segment"):
                    if (headerIdentified==False):
                        headerIdentified=True;
                        writer.writerow(row)
                else:
                    writer.writerow(row)
                    # Need to extract the ISIN from the below value
                    security_description = row[1]
                    isin=row[1].split("Cash-", 1)[1].strip()
                    bought = row[2]
                    sold = row[3]
                    total_tx_cost=row[9]

                    print("ISIN : "+isin)
                    print("Security Description:"+security_description)
                    print("Bought:" + bought)
                    print("Sold:" + sold)
                    print("Total Amount:" + total_tx_cost)

                    second_writer.writerow([tradeDate,isin,security_description,bought,sold,total_tx_cost])

    input.close()
    output.close()

    # Remove the decrypted file
    os.remove(fileName+"_decrypted")

    # Remove the full csv file
    os.remove('samplefiles/output.csv')

    # Possibly remove the partial csv file as well
    #os.remove('samplefiles/output_updated.csv')
