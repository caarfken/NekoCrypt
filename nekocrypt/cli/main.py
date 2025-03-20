from getpass import getpass
import nekocrypt, os.path, sys

nk = nekocrypt.NekoCrypt()
    
if len(sys.argv) < 3:
    operationType = input("(E)ncrypt or (D)ecrypt? ").lower()
    fileName = input("Enter the file name: ")
else:
    operationType = sys.argv[1].lower()
    fileName = sys.argv[2]

if operationType in ['-e', '--encrypt', "e"]:
    operationType = 'e'
elif operationType in ['-d', '--decrypt', "d"]:
    operationType = 'd'
else:
    print("Invalid operation type. Use '-e' or '--encrypt' for encrypt, '-d' or '--decrypt' for decrypt.")
    exit(1)

if not os.path.isfile(fileName):
    print("No such file.")
    exit(2)

password = getpass("Enter password: ")

with open(fileName, "rb") as file:
    data = file.read()

print("Encrypting/Decrypting...", end="")
if operationType == "e":
    result = nk.encrypt(password, data)
    newFileName = fileName + ".encrypted"
else:
    result = nk.decrypt(password, data)
    newFileName = fileName + ".decrypted"
print("done")

print("Writing result...", end="")
with open(newFileName, "wb") as newFile:
    newFile.write(result)
print("done")

exit()