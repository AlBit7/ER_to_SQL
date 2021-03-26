import json

class ER:

    def __init__(self, db):
        
        self.db = json.loads(db) # converte la stringa json in un dizionario

        try:

            self.entita                = [elemento for elemento in self.db["shapes"]     if elemento["type"] == "Entity"               ]
            self.relazioni             = [elemento for elemento in self.db["shapes"]     if elemento["type"] == "Relationship"         ]
            self.attributi             = [elemento for elemento in self.db["shapes"]     if elemento["type"] == "Attribute"            ]
            self.connettoriDiRelazione = [elemento for elemento in self.db["connectors"] if elemento["type"] == "RelationshipConnector"]
            self.connettoriDiAttributi = [elemento for elemento in self.db["connectors"] if elemento["type"] == "Connector"            ]

        except:

            print("File JSON non valido o diagramma ER in assenza di entità, relazioni o attributi")
            exit()

        # ----------------------- creazione della struttura ----------------------

        self.struttura = {
            "entita": []
        }

        # ------------------------- handling entita -----------------------------

        for tabella in self.entita:

            nomeEntita = tabella["details"]["name"]
            idEntita   = tabella["details"]["id"]
            
            entita = {
                "id": idEntita,
                "nome": nomeEntita,
                "attributi": [],
                "PK": [],
                "FK": []
            }

            for attributo in self.attributi:

                nomeAttributo = attributo["details"]["name"]
                idAttributo   = attributo["details"]["id"]

                for connettore in self.connettoriDiAttributi:

                    tmp = [connettore["source"], connettore["destination"]]
                    if idAttributo in tmp and idEntita in tmp:

                        if attributo["details"]["isUnique"]:
                            entita["PK"].append(nomeAttributo)
                        
                        entita["attributi"].append(nomeAttributo)

            self.struttura["entita"].append(entita)
        
        # ------------------------- handling relazioni -----------------------------

        for relazione in self.relazioni:

            IDa = relazione["details"]["slots"][0]["entityId"]
            IDb = relazione["details"]["slots"][1]["entityId"]
            nomeRelazione = relazione["details"]["name"]

            for entita in self.struttura["entita"]:

                if entita["id"] == IDa:
                    entitaA = entita
                elif entita["id"] == IDb:
                    entitaB = entita

            if relazione["details"]["slots"][0]["cardinality"] == "many" and relazione["details"]["slots"][1]["cardinality"] == "many":

                # realazione molti-molti
                
                tmp = []
                
                for pk in entitaA["PK"]:
                    tmp.append(pk)
                for pk in entitaB["PK"]:
                    tmp.append(pk)

                entita = {
                    "id": relazione["details"]["id"],
                    "nome": nomeRelazione,
                    "attributi": tmp,
                    "PK": tmp,
                    "FK": tmp,
                    "da": [entitaA["nome"], entitaB["nome"]]
                }

                self.struttura["entita"].append(entita)

            elif relazione["details"]["slots"][0]["cardinality"] == "one" and relazione["details"]["slots"][1]["cardinality"] == "one":
                
                # relazione uno-uno

                print("La relazione uno a uno di nome: '{}': connette l'entità '{}' con l'entità '{}'".format(nomeRelazione, entitaA["nome"], entitaB["nome"]))

            else:

                # relazione uno-molti
                
                if relazione["details"]["slots"][0]["cardinality"] == "one":
                    entitaA["FK"] = entitaB["PK"]
                    entitaA["da"] = [entitaB["nome"]]
                else:
                    entitaB["FK"] = entitaA["PK"]
                    entitaB["da"] = [entitaA["nome"]]

    def displaySQL(self):

        ris = ""

        for tabella in self.struttura["entita"]:
            
            ris += "CREATE TABLE " + tabella["nome"] + " ("

            for attributo in tabella["attributi"]:
                ris += "\n\t" + attributo + " type,"
            
            for pk in tabella["PK"]:
                ris += "\n\tPRIMARY KEY (" + pk + ")"

            for i, fk in enumerate(tabella["FK"]):
                ris += ",\n\tFOREIGN KEY (" + fk + ") REFERENCES (" + tabella["da"][i] + ")"
            
            ris += "\n);\n\n"
        
        return ris
""" WIP
    def displayTabelle(self):

        ris = ""

        for tabella in self.struttura["entita"]:

            ris += tabella["nome"] + " ("

            for attributo in tabella["attributi"]:
                ris += attributo + ", "
            
            for pk in tabella["PK"]:
                ris += pk + " PK"

            for i, fk in enumerate(tabella["FK"]):
                ris += ", " + tabella["da"][i] + "_" + fk + " FK"
            
            ris += ")\n"
        
        return ris
"""
# ----------------------- input vari -------------------------

#PATH = "..."
#JSON = open(PATH, "r").read()

#JSON = '{"version":2,"www":"erdplus.com","shapes":[{"type":"Entity","details":{"name":"POST","type":"regular","x":264,"y":152.1666717529297,"id":1}},{"type":"Attribute","details":{"name":"Testo","isDerived":false,"isMultivalued":false,"isOptional":false,"isComposite":false,"isUnique":false,"x":145,"y":47.16667175292969,"id":2}},{"type":"Attribute","details":{"name":"Data","isDerived":false,"isMultivalued":false,"isOptional":false,"isComposite":false,"isUnique":false,"x":120,"y":110.16667175292969,"id":3}},{"type":"Entity","details":{"name":"ACCOUNT","type":"regular","x":646,"y":149.1666717529297,"id":5}},{"type":"Attribute","details":{"name":"idPost","isDerived":false,"isMultivalued":false,"isOptional":false,"isComposite":false,"isUnique":true,"x":128,"y":234.1666717529297,"id":6}},{"type":"Attribute","details":{"name":"nomeUtente","isDerived":false,"isMultivalued":false,"isOptional":false,"isComposite":false,"isUnique":true,"x":625,"y":37.16667175292969,"id":7}},{"type":"Attribute","details":{"name":"password","isDerived":false,"isMultivalued":false,"isOptional":false,"isComposite":false,"isUnique":false,"x":743,"y":37.16667175292969,"id":8}},{"type":"Attribute","details":{"name":"eMail","isDerived":false,"isMultivalued":false,"isOptional":false,"isComposite":false,"isUnique":false,"x":843,"y":92.16667175292969,"id":9}},{"type":"Attribute","details":{"name":"numeroTelefono","isDerived":false,"isMultivalued":false,"isOptional":false,"isComposite":false,"isUnique":false,"x":842,"y":157.1666717529297,"id":10}},{"type":"Attribute","details":{"name":"Nickname","isDerived":false,"isMultivalued":false,"isOptional":false,"isComposite":false,"isUnique":false,"x":645,"y":271.1666717529297,"id":11}},{"type":"Relationship","details":{"name":"scrive","isIdentifying":false,"x":461,"y":129.1666717529297,"slots":[{"slotIndex":0,"minimum":"","maximum":"","participation":"unspecified","cardinality":"one","role":"","entityId":1},{"slotIndex":1,"minimum":"","maximum":"","participation":"unspecified","cardinality":"many","role":"","entityId":5}],"id":23}},{"type":"Relationship","details":{"name":"Like","isIdentifying":false,"x":461,"y":230.1666717529297,"slots":[{"slotIndex":0,"minimum":"","maximum":"","participation":"unspecified","cardinality":"many","role":"","entityId":1},{"slotIndex":1,"minimum":"","maximum":"","participation":"unspecified","cardinality":"many","role":"","entityId":5}],"id":24}},{"type":"Attribute","details":{"name":"dataNascita","isDerived":false,"isMultivalued":false,"isOptional":false,"isComposite":false,"isUnique":false,"x":837,"y":220.1666717529297,"id":25}},{"type":"Attribute","details":{"name":"Ora","isDerived":false,"isMultivalued":false,"isOptional":false,"isComposite":false,"isUnique":false,"x":114,"y":176.1666717529297,"id":27}},{"type":"Attribute","details":{"name":"Foto Allegata","isDerived":false,"isMultivalued":false,"isOptional":false,"isComposite":false,"isUnique":false,"x":264,"y":39.16667175292969,"id":51}}],"connectors":[{"type":"Connector","details":{"id":30},"source":2,"destination":1},{"type":"Connector","details":{"id":31},"source":3,"destination":1},{"type":"Connector","details":{"id":32},"source":6,"destination":1},{"type":"Connector","details":{"id":33},"source":7,"destination":5},{"type":"Connector","details":{"id":34},"source":8,"destination":5},{"type":"Connector","details":{"id":35},"source":9,"destination":5},{"type":"Connector","details":{"id":36},"source":10,"destination":5},{"type":"Connector","details":{"id":37},"source":11,"destination":5},{"type":"Connector","details":{"id":38},"source":25,"destination":5},{"type":"Connector","details":{"id":39},"source":27,"destination":1},{"type":"RelationshipConnector","details":{"slotIndex":0,"id":47},"source":1,"destination":23},{"type":"RelationshipConnector","details":{"slotIndex":1,"id":48},"source":5,"destination":23},{"type":"RelationshipConnector","details":{"slotIndex":0,"id":49},"source":1,"destination":24},{"type":"RelationshipConnector","details":{"slotIndex":1,"id":50},"source":5,"destination":24},{"type":"Connector","details":{"id":52},"source":51,"destination":1}],"width":2000,"height":1000}'

#er = ER(JSON)

#print(er.displaySQL())
# WIP print(er.displayTabelle())



"""

Procedura:

    - leggere il file json
    - lo trasformo in un dizionario
    - separo il dizionario in vari array
    - ogni entità viene trasformata in una tabella

    - gestisco gli attributi:

        - analizzo l'array dei connettori
        - associo i vari attributi alle rispettive identità
    
    - gestisco le relazioni:

        - le differenzio in n-n/1-n/1-1
        - creo le FK
        - creo altre tabelle per le relazioni n-n

"""