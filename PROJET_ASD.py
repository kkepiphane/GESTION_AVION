#!/usr/bin/env python
# coding: utf-8

# # SYSTÈME DE GESTION DE BILLETS D'AVIONS

# In[119]:


import time


# ## Classe vol

# In[120]:


class Vol:
    def __init__(self, numero_vol, destination, date, heure, compagnie_aérienne):
        self.numero_vol = numero_vol  
        self.destination = destination 
        self.date = date 
        self.heure = heure
        self.compagnie_aérienne = compagnie_aérienne
    
    #Comparaison entre deux vol par numero de vol
    def __lt__(self, autre): 
        return self.numero_vol < autre.numero_vol
    
    def __gt__(self, autre):
        return self.numero_vol > autre.numero_vol
    
    def __eq__(self, autre):
        return self.numero_vol == autre.numero_vol
    
    # Affichage de l'objet
    def __str__(self):
        return f"Vol : {self.numero_vol}, Destination : {self.destination}, Date : {self.date}, Heure : {self.heure}, Compagnie : {self.compagnie_aérienne}"


# ## Classe passager

# In[121]:


class Passager:
    def __init__(self, numero_billet, nom, classe, statut):
        self.numero_billet = numero_billet
        self.nom = nom
        self.classe = classe
        self.statut = statut
        self.priorite = self._set_priorite(classe)
    
    # Definition automatique de la priorité en fonction de la classe    
    def _set_priorite(self, classe):
        if classe.lower() == "premiere":
            return 3
        if classe.lower() == "affaire":
            return 2
        if classe.lower() == "economique":
            return 1
        return 0
        
    def set_nom(self, new_nom):
        self.nom = new_nom
        return "Mise à Jour Réussi !!"
    
    def set_classe(self, new_classe):
        self.classe = new_classe
        return "Mise à Jour Réussi !!"
    
    def set_statut(self, new_statut):
        self.statut = new_statut
        return "Mise à Jour Réussi !!"
        
    # Affichage de l'objet 
    def __str__(self):
        return f"NUMERO BILLET : {self.numero_billet}, NOM : {self.nom}, CLASSE : {self.classe}, STATUT : {self.statut}"


# ## File circulaire à Priorité 

# In[122]:


class FileCirculairePriorite:
    def __init__(self, capacite):
        self.capacite = capacite
        self.file = []
        
    def est_vide(self):
        return len(self.file) == 0
    
    def est_pleine(self):
        return len(self.file) == self.capacite
    
    def enfiler(self, passager):
        # Suppression du premier élément si la file est pleine
        if self.est_pleine():
            self.file.pop(0)
        self.file.append(passager)
        return "Ajout reussi !!"
        
    def defiler(self):
        if self.est_vide():
            return "La file est vide"
        
        indice_max = 0
        for i in range(1, len(self.file)):
            if self.file[i].priorite > self.file[indice_max].priorite:
                indice_max = i
        passager_prioritaire = self.file.pop(indice_max)
        return passager_prioritaire.nom
    
    def afficher(self):
        file_triee = sorted(self.file, key=lambda passager: passager.priorite, reverse=True)
        for passager in file_triee:
            print(passager)
        


# ## Table de hachage 

# In[123]:


class TableDeHachage:
    def __init__(self, taille):
        self.taille = taille
        self.table = [[] for _ in range(self.taille)] #Remplissage de la table avec des liste vide 
        
    def hacher(self, cle): #Fonction de hachage pour determiner 
        facteur = 31 #Facteur premier pour eviter les collision
        if type(cle) is int:
            return cle % self.taille
        somme = 0
        for lettre in cle:
            somme = somme * facteur + ord(lettre)
        return somme % self.taille 
    
    def inserer(self, cle, valeur):
        indice = self.hacher(cle)
        
        for i, (k,v) in enumerate(self.table[indice]):
            if k == cle:
                self.table[indice][i] = (cle, valeur) # On met à jour la paire (cle, valeur) dans le cas où la cle exixte déjà 
                return
        self.table[indice].append((cle, valeur)) # On append dans le cas contraire
        
    def rechercher(self, cle):
        indice = self.hacher(cle)
        
        for k, v in self.table[indice]:
            if k == cle:
                return v
        return False
    
    def supprimer(self, cle):
        indice = self.hacher(cle)
        
        for i, (k, v) in enumerate(self.table[indice]):
            if k == cle:
                del self.table[indice][i]
                return (k,v)
        return None
    
    def afficher(self):
        for i, paire in enumerate(self.table):
            print(f"Index {i} : {paire}")
            
        


# ## Arbre binaire de recherche

# In[124]:


class Noeud:
    def __init__(self, vol):
        self.vol = vol
        self.gauche = None
        self.droite = None


# In[125]:


class ABR:
    def __init__(self):
        self.racine = None
        
    def inserer(self, vol):
        
        if not isinstance(vol, Vol):
            return TypeError("Seul les objets de types Vol sont acceptés")
        
        if self.racine is None:
            self.racine = Noeud(vol)
        else:
            self._inserer_rec(self.racine, vol)
        
    
    def _inserer_rec(self, noeud, vol):
        if vol < noeud.vol:
            if noeud.gauche is None:
                noeud.gauche = Noeud(vol)
            else:
                self._inserer_rec(noeud.gauche, vol)
        elif vol > noeud.vol:
            if noeud.droite is None:
                noeud.droite = Noeud(vol)
            else:
                self._inserer_rec(noeud.droite, vol)
    
    def rechercher(self, numero):
        p = self._rechercher_rec(self.racine, numero)
        return p
        
    def _rechercher_rec(self, noeud, numero):
        if noeud is None:
            return False  # La valeur n'est pas trouvée
        if noeud.vol.numero_vol == numero:
            return noeud.vol  # La valeur est trouvée
        if numero < noeud.vol.numero_vol:
            return self._rechercher_rec(noeud.gauche, numero)
        return self._rechercher_rec(noeud.droite, numero)
    
    def rechercher_par_destination(self, destination):
        resultats = []
        self._rechercher_par_destination_rec(self.racine, destination, resultats)
        if len(resultats) == 0:
            return False
        return resultats
    
    def _rechercher_par_destination_rec(self, noeud, destination, resultats):
        if noeud is not None:
            self._rechercher_par_destination_rec(noeud.gauche, destination, resultats)
            
            if noeud.vol.destination.lower() == destination.lower(): #Tout convertir en minuscule
                resultats.append(noeud.vol)
            
            self._rechercher_par_destination_rec(noeud.droite, destination, resultats)
    
    
    def supprimer(self, numero):
        sup = self.rechercher(numero)
        self.racine = self._supprimer_rec(self.racine, numero)
        return f"SUPPRIMÉ {sup}"
    
    def _supprimer_rec(self, noeud, numero):
        if noeud is None:
            return noeud
        
        if numero < noeud.vol.numero_vol:
            noeud.gauche = self._supprimer_rec(noeud.gauche, numero)
        elif numero > noeud.vol.numero_vol:
            noeud.droite = self._supprimer_rec(noeud.droite, numero)
        else:
            # Noeud avec un seul enfant ou sans enfant
            if noeud.gauche is None:
                return noeud.droite
            elif noeud.droite is None:
                return noeud.gauche
            
            # Noeud avec deux enfants 
            successeur = self._valeur_min(noeud.droite)
            noeud.vol = successeur.vol
            noeud.droite = self._supprimer_rec(noeud.droite, successeur.vol.numero_vol)
        
        return noeud
            
    def _valeur_min(self, noeud):
        while noeud.gauche is not None:
            noeud = noeud.gauche
        return noeud
    
    def parcours_infixe(self):
        self._parcours_infixe_rec(self.racine)
        print()
        
    def _parcours_infixe_rec(self, noeud):
        if noeud is not None:
            self._parcours_infixe_rec(noeud.gauche)
            print(noeud.vol)
            self._parcours_infixe_rec(noeud.droite)


# ## Classe principale

# In[126]:


class GestionnaireBillet:
    def __init__(self):
        self.vols = ABR()
        self.passagers = TableDeHachage(11)
        self.file_attente = FileCirculairePriorite(10)
    
    def creer_file_attente(self, longueur):
        self.file_attente = FileCirculairePriorite(longueur)
    
    """GESTION DES VOLS"""
    # ABR
    
    def ajouter_vol(self, vol):
        self.vols.inserer(vol)
    
    def rechercher_vol(self, valeur):
        if type(valeur) is int:
            return self.vols.rechercher(valeur)
        else:
            return self.vols.rechercher_par_destination(valeur)
    
    def lister_vol(self):
        return self.vols.parcours_infixe()
    
    """GESTION DES PASSAGER"""
    # Table de hachage
    
    def ajouter_passager(self, passager):
        self.passagers.inserer(passager.numero_billet, passager)
        return ("Ajout effectué")
    
    def rechercher_passager(self, numero_billet):
        return self.passagers.rechercher(numero_billet)
    
    def modifier_nom_passager(self, numero_billet, new_nom):
        indice = self.passagers.hacher(numero_billet)
        i = 0
        while self.passagers.table[indice][i][0] != numero_billet:
            i +=1
            if i >= len(self.passagers.table[indice]):
                return "Passager Introuvable"
        return self.passagers.table[indice][i][1].set_nom(new_nom)
    
    def modifier_classe_passager(self, numero_billet, new_classe):
        indice = self.passagers.hacher(numero_billet)
        i = 0
        while self.passagers.table[indice][i][0] != numero_billet:
            i +=1
            if i >= len(self.passagers.table[indice]):
                return "Passager Introuvable"
        return self.passagers.table[indice][i][1].set_classe(new_classe)
    
    def modifier_statut_passager(self, numero_billet, new_statut):
        indice = self.passagers.hacher(numero_billet)
        i = 0
        while self.passagers.table[indice][i][0] != numero_billet:
            i +=1
            if i >= len(self.passagers.table[indice]):
                return "Passager Introuvable"
        return self.passagers.table[indice][i][1].set_statut(new_statut)    
    
        
    """GESTION DES FILES D'ATTENTE"""
    # File circulaire à Priorité 
    
    def ajouter_a_file(self, passager):
        self.file_attente.enfiler(passager)
    
    def afficher_file_attente(self):
        return self.file_attente.afficher()
    
    def embarquement(self):
        while len(self.file_attente.file) != 0:
            print(self.file_attente.defiler())
            time.sleep(2)
        return "Embarquement terminé !!"
            
        
        
    


# # Main

# In[129]:


if __name__ == "__main__":
    g = GestionnaireBillet()

    while True:
        print("\n**********************************************")
        print(" Système de Gestion de Billets d'Avion ")
        print("1. Ajouter un vol")
        print("2. Rechercher un vol")
        print("3. Afficher tous les vols")
        print("4. Ajouter un passager")
        print("5. Rechercher un passager")
        print("6. Modifer le nom d'un passager")
        print("7. Modifer la classe d'un passager")
        print("8. Modifer le statut d'un passager")
        print("9. Ajouter un passager à la file d’attente")
        print("10. Afficher la file d'attente")
        print("11. Embarquement")
        print("12. Quitter")
        choix = input("Choisissez une option : ")

        if choix == '1': # Ajouter un vol
            numero_vol = int(input("Entrez le numéro du vol : "))
            destination = input("Entrez la destination : ")
            date = input("Entrez la date du vol : ")
            heure = input("Entrez l'heure du vol : ")
            compagnie_aerienne = input("Entrez la compagnie aérienne : ")
            vol = Vol(numero_vol, destination, date, heure, compagnie_aerienne)
            g.ajouter_vol(vol)
            print("\n**********************************************")
            print(f"Vol Nº {vol.numero_vol} Ajouté !")

        elif choix == '2': #Rechercher un vol
            numero_vol = input("Entrez le numéro du vol à rechercher : ")
            print()
            print("\n**********************************************")
            print(g.rechercher_vol(int(numero_vol)))

        elif choix == '3': # Afficher tous les vols
            print()
            print("\n**********************************************")
            print("\nListe des vols :")
            g.lister_vol()

        elif choix == '4': # Ajouter un passager
            numero_billet = int(input("Entrez le numéro de billet du passager : "))
            nom = input("Entrez le nom du passager : ")
            classe = input("Entrez la classe du passager (première, affaire, économique) : ")
            statut = input("Entrez le statut du passager : ")
            passager = Passager(numero_billet, nom, classe, statut)
            g.ajouter_passager(passager)
            print()
            print("\n**********************************************")
            print(f"Passager Nº {passager.numero_billet} ajouté !!")

        elif choix == '5': #Rechercher un passager
            numero_billet = int(input("Entrez le numéro de billet du passager à rechercher : "))
            print()
            print("\n**********************************************")
            print(g.rechercher_passager(numero_billet))
            
        elif choix == '6':
            numero_billet = int(input("Entrez le numéro de billet du passager : "))
            nom = input("Entrez le nouveau nom du passager : ")
            print()
            print("\n**********************************************")
            print(g.modifier_nom_passager(numero_billet, nom))
        
        
        elif choix == '7':
            numero_billet = int(input("Entrez le numéro de billet du passager : "))
            classe = input("Entrez la nouvelle classe du passager : ")
            print()
            print("\n**********************************************")
            print(g.modifier_classe_passager(numero_billet, classe))
        
        
        elif choix == '8':
            numero_billet = int(input("Entrez le numéro de billet du passager : "))
            statut = input("Entrez le nouveau statut du passager : ")
            print()
            print("\n**********************************************")
            print(g.modifier_statut_passager(numero_billet, statut))
        

        elif choix == '9': #Ajouter un passager à la file d’attente"
            numero_billet = int(input("Entrez le numéro de billet du passager : "))
            p = g.rechercher_passager(numero_billet)
            print()
            print("\n**********************************************")
            g.ajouter_a_file(p)
            print("Ajout Reussi !!")
            
        
        elif choix == '10':
            print()
            print("\n**********************************************")
            print("File d'attente : ")
            g.afficher_file_attente()

            
        elif choix == '11':
            print()
            print("\n**********************************************")
            print(g.embarquement())

        elif choix == '12':
            print("Au revoir!")
            break

        else:
            print("Option invalide. Essayez à nouveau.")


# In[ ]:




