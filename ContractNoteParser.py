import os
import PyPDF2
from PyPDF2 import PdfFileReader, PdfFileWriter
import tabula
import csv


def parse_file(fileName):
    print(f'Hi, The file name is  {fileName}')
    pdf_file = open(fileName,'rb')
    read_pdf = PyPDF2.PdfFileReader(pdf_file)

    password ="VIK1706"
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
    writer = csv.writer(output)
    toggle=False;
    for row in csv.reader(input):
        print (row[0]);
        if (row[0]=="Segment"):
            toggle=True;

        if toggle:
            if (row[0] == "Sub Total" or row[0] == "Total"):
                # Shift thr row by 1.
                #writer.writerow(','.join(row))
                writer.writerow([' ']+row)
            else:
                writer.writerow(row)
    input.close()
    output.close()

    # Remove the decrypted file
    os.remove(fileName+"_decrypted")

    # Remove the full csv file
    os.remove('samplefiles/output.csv')



