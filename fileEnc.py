from getpass import getpass
import nekocrypt, os.path, sys

def main():
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
        return
    
    if not os.path.isfile(fileName):
        print("No such file.")
        return
    
    password = getpass("Enter password: ")
    print("Processing Password...", end="")
    password = nk.processPassword(list(password), os.stat(fileName).st_size)
    print("done")
    
    with open(fileName, "rb") as file:
        data = file.read()
    
    print("Encrypting/Decrypting...", end="")
    if operationType == "e":
        result = nk.encrypt(password, data)
        newFileName = fileName + "(Encrypted)"
    else:
        result = nk.decrypt(password, data)
        newFileName = fileName + "(Decrypted)"
    print("done")
    
    print("Writing result...", end="")
    with open(newFileName, "wb") as newFile:
        newFile.write(result)
    print("done")

if __name__ == "__main__":
    main()