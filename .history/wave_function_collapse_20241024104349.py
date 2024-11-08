import pygame as py
import math
import random as rd

py.init()
# py.display.set_caption("base")



blanc=(255,255,255)
noir=(0,0,0)
gris=(190,190,190)


class Affichage:
    def __init__(self,facteur):
        self.dimensions=(int(1920*facteur),int(1080*facteur))
        self.fenetre=py.display.set_mode(self.dimensions)

        self.nb_cases=30

        self.taille_case=min(self.dimensions[0]//self.nb_cases,self.dimensions[1]//self.nb_cases)


        # initialisation de self.liste_tuiles_possibles
        self.liste_tuiles_possibles=[[1,1,0,0],[1,0,1,0],[0,1,1,1],[1,1,1,1]]

        id_rotations=[]
        for id_tuile in self.liste_tuiles_possibles:
            id_rotations+=self.liste_rotations(id_tuile)
        id_rotations=[list(tupl) for tupl in {tuple(item) for item in id_rotations}]
        self.liste_tuiles_possibles=id_rotations


        self.liste_tuiles=[]
        self.initialiser_liste_tuiles()
        self.pos_tuile_depart=[0,1]

        self.liste_tuiles_a_traiter=[self.liste_tuiles[self.nb_cases*self.pos_tuile_depart[0]+self.pos_tuile_depart[1]]]
        self.liste_tuiles_deja_traites=[]
        
        
        # print(self.liste_tuiles_possibles)
    
    def liste_rotations(self,id_tuile):
        liste_rotations=[id_tuile]
        for _ in range(3):
            liste_rotations.append([liste_rotations[-1][-1]]+liste_rotations[-1][:-1])
        
        return liste_rotations


    
    def initialiser_liste_tuiles(self):
        for j in range(self.nb_cases):
            for i in range(self.nb_cases):
                # tuile=Tuile((j,i),rd.choice(self.liste_tuiles_possibles),self.fenetre,self.taille_case)
                tuile=Tuile((j,i),[-1,-1,-1,-1],self.fenetre,self.taille_case)
                self.liste_tuiles.append(tuile)
    
    def dessiner_tuiles(self):
        for tuile in self.liste_tuiles:
            tuile.dessiner()
    
    def dessiner_grille(self):
        for j in range(0,self.dimensions[1]+1,self.taille_case):
            for i in range(0,self.dimensions[0]+1,self.taille_case):
                py.draw.line(self.fenetre,gris,(0,i),(self.dimensions[1],i),3)
                py.draw.line(self.fenetre,gris,(j,0),(j,self.dimensions[0]),3)
    
    def generer_tuile(self):
        tuile_a_traiter=rd.choice(self.liste_tuiles_a_traiter)
        self.liste_tuiles_a_traiter.remove(tuile_a_traiter)
        indice_tuile_a_traiter=self.nb_cases*tuile_a_traiter.pos[0]+tuile_a_traiter.pos[1]

        # print(tuile_a_traiter.pos,indice_tuile_a_traiter)

        

        # generation des id interdits
        liste_id_interdits=[]

        # nord
        if tuile_a_traiter.pos[1]>=1 and self.liste_tuiles[indice_tuile_a_traiter-1].id!=[-1,-1,-1,-1]:
            if self.liste_tuiles[indice_tuile_a_traiter-1].id[2]==1:
                for id in self.liste_tuiles_possibles:
                    if id[0]!=1:
                        liste_id_interdits.append(id[:])
            elif self.liste_tuiles[indice_tuile_a_traiter-1].id[2]!=1:
                for id in self.liste_tuiles_possibles:
                    if id[0]==1:
                        liste_id_interdits.append(id[:])
        
        # sud
        if tuile_a_traiter.pos[1]<=self.nb_cases-2 and self.liste_tuiles[indice_tuile_a_traiter+1].id!=[-1,-1,-1,-1]:
            if self.liste_tuiles[indice_tuile_a_traiter+1].id[0]==1:
                for id in self.liste_tuiles_possibles:
                    if id[2]!=1:
                        liste_id_interdits.append(id[:])
            elif self.liste_tuiles[indice_tuile_a_traiter+1].id[0]!=1:
                for id in self.liste_tuiles_possibles:
                    if id[2]==1:
                        liste_id_interdits.append(id[:])
        
        # ouest
        if tuile_a_traiter.pos[0]<=self.nb_cases-2 and self.liste_tuiles[indice_tuile_a_traiter+self.nb_cases].id!=[-1,-1,-1,-1]:
            if self.liste_tuiles[indice_tuile_a_traiter+self.nb_cases].id[3]==1:
                for id in self.liste_tuiles_possibles:
                    if id[1]!=1:
                        liste_id_interdits.append(id[:])
            elif self.liste_tuiles[indice_tuile_a_traiter+self.nb_cases].id[3]!=1:
                for id in self.liste_tuiles_possibles:
                    if id[1]==1:
                        liste_id_interdits.append(id[:])
        
        # est
        if tuile_a_traiter.pos[0]>=1 and self.liste_tuiles[indice_tuile_a_traiter-self.nb_cases].id!=[-1,-1,-1,-1]:
            if self.liste_tuiles[indice_tuile_a_traiter-self.nb_cases].id[1]==1:
                for id in self.liste_tuiles_possibles:
                    if id[3]!=1:
                        liste_id_interdits.append(id[:])
            elif self.liste_tuiles[indice_tuile_a_traiter-self.nb_cases].id[1]!=1:
                for id in self.liste_tuiles_possibles:
                    if id[3]==1:
                        liste_id_interdits.append(id[:])
        
        # bords
        

        liste_id_possibles=[]
        for id in self.liste_tuiles_possibles:
            if not id in liste_id_interdits:
                liste_id_possibles.append(id[:])
        
        if liste_id_possibles==[]:
            tuile_a_traiter.id=[0,0,0,0]
        else:
            tuile_a_traiter.id=rd.choice(liste_id_possibles)

        self.liste_tuiles_deja_traites.append(tuile_a_traiter)

        # print(tuile_a_traiter.pos,liste_id_possibles)
        

        liste_tuiles_voisines=self.tuiles_voisines(tuile_a_traiter)
        for tuile in liste_tuiles_voisines:
            if not tuile in self.liste_tuiles_deja_traites and not tuile in self.liste_tuiles_a_traiter:
                self.liste_tuiles_a_traiter.append(tuile)
    
    def tuiles_voisines(self,tuile):
        liste_tuiles_voisines=[]
        for direction in [(0,1),(1,0),(0,-1),(-1,0)]:
            if 0<=tuile.pos[0]+direction[0]<=self.nb_cases-1 and 0<=tuile.pos[1]+direction[1]<=self.nb_cases-1:
                liste_tuiles_voisines.append(self.tuile_depuis_pos((tuile.pos[0]+direction[0],tuile.pos[1]+direction[1])))
        
        return liste_tuiles_voisines
    
    def tuile_depuis_pos(self,pos):
        return self.liste_tuiles[self.nb_cases*pos[0]+pos[1]]
    
    

    def loop(self):
        horloge=py.time.Clock()


        # boucle de jeu
        continuer=True
        while continuer:
            for event in py.event.get():
                if event.type==py.QUIT:
                    continuer=False
                if event.type==py.KEYDOWN:
                    if event.key==py.K_ESCAPE:
                        continuer=False
            horloge.tick(60)
            py.display.set_caption(str(round(horloge.get_fps(),1)))


            self.fenetre.fill(blanc)

            self.dessiner_grille()
            self.dessiner_tuiles()
            
            if self.liste_tuiles_a_traiter!=[]:
                self.generer_tuile()

            py.display.flip()

        py.quit()

class Tuile:
    def __init__(self,pos,id,fenetre,taille):
        self.fenetre=fenetre
        self.taille=taille

        self.pos=pos
        self.id=id

        self.pos_ecran_centre=(self.taille*(pos[0]+0.5),self.taille*(pos[1]+0.5))
    
    def dessiner(self):
        epaisseur=3
        if self.id!=[-1,-1,-1,-1]:
            if self.id[0]==1:
                py.draw.line(self.fenetre,noir,self.pos_ecran_centre,(self.pos_ecran_centre[0],self.pos_ecran_centre[1]-0.5*self.taille),epaisseur)
            if self.id[1]==1:
                py.draw.line(self.fenetre,noir,self.pos_ecran_centre,(self.pos_ecran_centre[0]+0.5*self.taille,self.pos_ecran_centre[1]),epaisseur)
            if self.id[2]==1:
                py.draw.line(self.fenetre,noir,self.pos_ecran_centre,(self.pos_ecran_centre[0],self.pos_ecran_centre[1]+0.5*self.taille),epaisseur)
            if self.id[3]==1:
                py.draw.line(self.fenetre,noir,self.pos_ecran_centre,(self.pos_ecran_centre[0]-0.5*self.taille,self.pos_ecran_centre[1]),epaisseur)


facteur=0.7
affichage=Affichage(facteur)
affichage.loop()