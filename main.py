# bruges til at lave lister over filer og til at oprette directories
import os
# bruges til at kopiere filer i full backup og differential backup
import shutil
# bruges til at skrive timestamps i log
import datetime
# bruges til at sammenligne directories/filer, i differential backup
import filecmp

source = input("Folder to be backed up: ")
destination = input("Destination folder for backup (folder must not already exist): ")

# vælg hvilken type backup der skal køres
print("1. Full backup")
print("2. Differential backup (requires already existing full backup)")
selection = input("Select backup type: ")

# metode der bruges til at logge når der tages backup
def logging(a):
    if os.path.exists('log.csv') is True:
        file = open('log.csv',mode='a+')
        file.write('\n'+str(datetime.now())+','+a+','+source+','+destination)
        file.close()
    # hvis log.csv ikke findes, oprettes en ny fil med header
    elif os.path.exists('log.csv') is False:
        file = open('log.csv',mode='a+')
        file.write('TIME,MODE,SOURCE,DESTINATION')
        file.write('\n'+str(datetime.now())+','+a+','+source+','+destination)
        file.close()

# full backup
if selection == "1":
    # backer det fulde directory up fra a>b
    shutil.copytree(source, destination)
    logging("full")

# differential backup
elif selection == '2':
    # sti til tidligere fuld backup, som sammenlignes mod source
    fullbackup = input("Enter path to full backup: ")
    os.mkdir(str(destination))
    # skriver alle filer og directories i source ind i en liste (common)
    common = os.listdir(source)
    # sammenligner filer som er defineret i common, i fullbackup og source
    match, mismatch, diff = filecmp.cmpfiles(fullbackup,source,common)
    # kopierer filer i diff, til destination
    for file in diff:
        # hvis filen ikke har en extension, er det en mappe (???)
        if "." not in file:
            os.mkdir(str(destination)+"\\"+str(file))
        # hvis filen har en extension, er det en fil, så den kopieres
        elif "." in file:
            shutil.copy(str(source)+"\\"+str(file),destination)
    logging("differential")