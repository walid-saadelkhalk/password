# coding: utf-8

import hashlib
import json
import random

#partie pour hacher le mot de passe
def calculer_hashage_sha256(codage):
    hachage = hashlib.sha256()
    hachage.update(codage.encode('utf-8'))
    return hachage.hexdigest()



#partie pour enregistrer le mot de passe dans le fichier json
def enregistrement(bibliotheque_mdp, hash_mdp, password, index):
    bibliotheque_mdp[hash_mdp] = "Mot de passe hache " + str(index)
    with open("bibliotheque_mdp.json", "w") as fichier:
        json.dump(bibliotheque_mdp, fichier, indent=4)




#partie pour lire le fichier json
def lecture():
    try:
        with open("bibliotheque_mdp.json", "r") as fichier:
            bibliotheque_mdp = json.load(fichier)
            resultats = []
            for index, (hash_mdp, password) in enumerate(bibliotheque_mdp.items(), start=1):
                resultat = {"index": index, "hash_mdp": hash_mdp, "password": password}
                resultats.append(resultat)
            return resultats
    except FileNotFoundError:
        print("Aucun fichier de bibliothèque trouvé.")
        return []



#message d'acceuil
print( "Votre mot de passe doit contenir au moins:\n -8 caracteres\n -Une majuscule\n -Une minuscule\n -Un chiffre\n -Un caractere special\n") 



#liste des caractères spéciaux et interdits
special = ["-", "_", "!", "?", ".", ",", ":", "*", "+", "=", "`", "|", "°", "#", "@", "€", "£"]
interdit = [ ';', "\ ", "/", '(', ')', '{', '}',"[", "]", "~", '<', '>', '&', '$', '%', '"', "'"]


#generateur de mot de passe aléatoire
def generer_mot_de_passe(taille):
    caracteres = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-_!?.,:*+=`|°#@€£"
    mot_de_passe = ''.join(random.choice(caracteres) for _ in range(taille))
    return mot_de_passe



# choix de menu/ creation de mot de passe et verification de la validité/ enregistrement dans le fichier json/ lecture du fichier json
def mot_de_passe():
    global special, interdit 

    bibliotheque_mdp = {}
    index = 1

    while True:
        choix = input("Veuillez taper 1 pour créer un mot de passe.\nVeuillez taper 2 pour lire la bibliothèque.\n Veuillez taper 3 pour quitter.\n Appuyez sur la touche 'Entrée'.\n")

        #partie pour créer un mot de passe
        if choix == "1":

            decision = input("Voulez-vous générer un mot de passe aléatoire ? (oui/non) : ")

            #partie pour créer un mot de passe manuellement
            if decision == "non":
                hash_mdp = None
                
                password = input("Veuillez saisir votre mot de passe : ")
                minuscule = sum(caractere.islower() for caractere in password)
                majuscule = sum(caractere.isupper() for caractere in password)
                chiffre = sum(caractere.isdigit() for caractere in password)
                espace = sum(caractere.isspace() for caractere in password)

                special_autorise = sum(caractere in special for caractere in password)
                special_interdit = sum(caractere in interdit for caractere in password)
                
                #partie pour vérifier la validité du mot de passe
                if minuscule < 1:
                    print("\nLe mot de passe doit contenir au moins une lettre minuscule.\n")
                elif majuscule < 1:
                    print("\nLe mot de passe doit contenir au moins une lettre majuscule.\n")
                elif chiffre < 1:
                    print("\nLe mot de passe doit contenir au moins un chiffre.\n")
                elif len(password) < 8:
                    print("\nLe mot de passe doit contenir au moins 8 caractères.\n")
                elif espace > 0:
                    print("\nLe mot de passe ne doit pas contenir d'espace.\n")
                elif special_interdit:
                    print("\nLe mot de passe ne doit pas contenir de caractère interdit.\n Les caractères interdits sont:", '  '.join(interdit), "\n Les caractères spéciaux autorisés sont: ", '  '.join(special), "\n")
                elif special_autorise < 1:
                    print("\nLe mot de passe doit contenir au moins un caractère spécial.\n")
                else:
                    hash_mdp = calculer_hashage_sha256(password)
                    print("\nMot de passe valide")
                    print("\nMot de passe haché:", hash_mdp, "\n")

                    #partie pour enregistrer le mot de passe dans le fichier json
                    enregistrement(bibliotheque_mdp, hash_mdp, password, index)
                    index += 1 
            
            
            #partie pour créer un mot de passe aléatoire
            elif decision == "oui":
                while True:
                    taille = int(input("Veuillez saisir le nombre de caracteres du mot de passe( compris entre 8 et 20) : "))
                    if taille < 8 or taille > 20:
                        print("\n Les caracteres doivent etre compris entre 8 et 20\n")
                        
                
                    else:
                        mot_de_passe = generer_mot_de_passe(taille)
                        hash_mdp = calculer_hashage_sha256(mot_de_passe)
                        print("\nMot de passe généré :", mot_de_passe)
                        print("\nMot de passe haché :", hash_mdp, "\n")
                        enregistrement(bibliotheque_mdp, hash_mdp, mot_de_passe, index)
                        index += 1
                        break
                

            else:
                print("Veuillez taper oui ou non.\n")
                continue
        

        #partie pour lire le fichier json
        elif choix == "2":
            resultats = lecture()
            for resultat in resultats:
                print(f"\n Mot de passe haché {resultat['index']} : {resultat['hash_mdp']}\n")
            


        #partie pour quitter le programme
        elif choix == "3":
            print("Au revoir.")
            break

        else:
            print("Veuillez taper 1, 2 ou 3.")
            

mot_de_passe()




