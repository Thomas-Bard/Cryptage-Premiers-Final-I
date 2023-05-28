from PIL import Image, ImageDraw
from utils import format_primes
import random
import math

def crypt(primes : list[int]) -> int:
    filename = input("Fichier :")
    img = Image.open(filename)
    if img.width * img.height > 1e6:
        print("[ERROR] Image trop grande !")
        print("[INFO] Abandon procédure")
        return -1
    seed = input("Entrez une clé :")
    random.seed(seed)
    shuffled = primes
    print("[INFO] Mélange de la liste...")
    random.shuffle(shuffled)
    print("[INFO] Cryptage...")
    n = 1
    print("[INFO] Dimensions " + str(img.width) + "x" + str(img.height))
    for x in range(img.width):
        for y in range(img.height):
            c = img.getpixel((x,y))
            if sum(c)/len(c) > 127:
                n*=shuffled[(x*img.height)+y]
                #print((x*img.height)+y)
    print("[INFO] Cryptage effectué avec succès !")
    print("[INFO] Dimensions " + str(img.width) + "x" + str(img.height))
    print("[DEBUG] n = " + hex(n))
    return n

def decrypt(primes : list[int]) -> Image.Image:
    filename = input("Entrez le nom du fichier")
    content = None
    with open(filename, "rb") as file:
        content = file.read()
        temp : int = 0
        temp = temp.from_bytes(content, 'little')
        print("[DEBUG] n = " + str(temp))
        content = temp
        file.close()
    seed = input("Entrez la clé :")
    dim = input("Entrez les dimensions de l'image (longueurxlargeur):")
    dim=dim.split("x")
    w = int(dim[0])
    h = int(dim[1])
    if w*h > 1e6:
        print("[FATAL] Image trop grande")
        print("[INFO] Abandon...")
        exit(-7)
    shuffled = primes
    random.seed(seed)
    random.shuffle(shuffled)
    print("[INFO] Décryptage...")
    img = Image.new("RGB", (w,h))
    for x in range(img.width):
        for y in range(img.height):
            if content % shuffled[x*img.height + y] == 0:
                img.putpixel((x,y), (255,255,255))
    print("[INFO] Décryptage terminé")
    return img

if __name__ == "__main__":
    print("[INFO] Formattage des premiers...")
    primes = None
    try:
        primes = format_primes("primes.txt")
    except FileNotFoundError:
        print("[FATAL] Fichier non trouvé !")
        print("[INFO] Abandon")
        exit(-1)
    except:
        print("[FATAL] Erreur lors du formattage. Vérifiez l'intégrité du fichier")
        print("[INFO] Abandon")
        exit(-2)
    finally:
        print("[INFO] Formattage effectué avec succès !")
    print("\n" * 5)
    print("1. Crypter une image")
    print("2. Décrypter une image")
    print("3. Quitter")
    choix = input(">>")
    match choix:
        case '1':
            n = crypt(primes)
            filename = input("Nom du fichier crypté :")
            with open(filename, "wb") as file:
                file.write(n.to_bytes((int(math.log2(n))+1)//8 + 1, 'little'))
                file.close()
            print("[INFO] Fichier sauvegardé")
            print("[INFO] Programme terminé")
            exit(0)
        case '2':
            img = decrypt(primes)
            filename = input("Enregistrer l'image sous:")
            img.save(filename)
            print("[INFO] Image enregistrée")
            print("[INFO] Programme terminé")
            exit(0)
        case '3':
            exit(0)
        case any:
            print("Merci d'entrer un choix correct")
    