class Vertex:
    def __init__(self, key):
        self.id = key
        self.connectedTo = {}
        self.color = 'white'  
        self.dist = 0  
        self.pred = None  
        self.disc = 0  
        self.fin = 0  

    def addNeighbor(self, nbr, weight=0):
        self.connectedTo[nbr] = weight

    def setColor(self, color):
        self.color = color

    def setDistance(self, d):
        self.dist = d

    def setPred(self, p):
        self.pred = p

    def setDiscovery(self, dtime):
        self.disc = dtime

    def setFinish(self, ftime):
        self.fin = ftime

    def getFinish(self):
        return self.fin

    def getDiscovery(self):
        return self.disc

    def getPred(self):
        return self.pred

    def getDistance(self):
        return self.dist

    def getColor(self):
        return self.color

    def __str__(self):
        return str(self.id) + ' connectedTo: ' + str([x.id for x in self.connectedTo])

    def getConnections(self):
        return self.connectedTo.keys()

    def getId(self):
        return self.id

    def getWeight(self, nbr):
        return self.connectedTo[nbr]


class Graph:
    def __init__(self):
        self.vertList = {}
        self.numVertices = 0

    def addVertex(self, key):
        self.numVertices = self.numVertices + 1
        newVertex = Vertex(key)
        self.vertList[key] = newVertex
        return newVertex

    def getVertex(self, n):
        if n in self.vertList:
            return self.vertList[n]
        else:
            return None

    def __contains__(self, n):
        return n in self.vertList

    def addEdge(self, f, t, cost=0):
        if f not in self.vertList:
            nv = self.addVertex(f)
        if t not in self.vertList:
            nv = self.addVertex(t)
        self.vertList[f].addNeighbor(self.vertList[t], cost)

    def getVertices(self):
        return self.vertList.keys()

    def __iter__(self):
        return iter(self.vertList.values())

    def generateDot(self):
        f = open("graph.txt", "w+")
        f.write("digraph G {\n")
        for v in self:
            for w in v.getConnections():
                f.write(' "%s" -> "%s" \n' % (v.getId(), w.getId()))
        f.write("}")

def missionary_cannibal_graph():
    mc_graph=Graph()
    for mis in range(4):
        for can in range(4):
            for boat in range(2):
                #pomijamy przypadki początkowe, gdzie ludzie i łódka są po różnych stronach rzeki
                if boat==0 and mis==3 and can==3:
                    pass
                elif boat==1 and mis==0 and can==0:
                    pass
                else:
                    #pomijamy przypadki początkowe, które od razu przewidują śmierć misjonarzy
                    if legal_move(mis,can):
                        #na podstawie stanu zagadki generujemy możliwe następne kroki
                        node_id=(mis,can,boat)  
                        new_positions=gen_legal_moves(mis,can,boat)
                        for e in new_positions:
                            #dodajemy je do grafu
                            nid=e
                            mc_graph.addEdge(node_id,nid)
                    else:
                        pass
    return mc_graph



def gen_legal_moves(mis,can,boat):
    new_moves=[]
    #możliwe przypadki, gdy dodajemy liczbę misjonarzy i kanibali
    #lub odejmujemy, w zależności gdzie jest łódka
    move_offset_pl=[(2,0),(1,1),(0,2),(1,0),(0,1)]
    move_offset_min = [(-2, 0), (-1, -1),(0, -2),(-1, 0), (0, -1)]
    if boat==0:
        for i in move_offset_pl:
            new_mis=mis+i[0]
            new_can=can+i[1]
            if legal_move(new_mis,new_can): #sprawdzamy czy ten ruch jest legalny
                new_moves.append((new_mis,new_can,1))
    elif boat==1:
        for i in move_offset_min:
            new_mis=mis+i[0]
            new_can=can+i[1]
            if legal_move(new_mis,new_can):
                new_moves.append((new_mis,new_can,0))
    return new_moves

def legal_move(mis,can):
    #rozpisaliśmy wszystkie przypadki, w których misjonarze nie zostaną zjedzeni
    if can>=0 and can<=3 and mis>=0 and mis<=3:
        if mis==3:
            return True
        elif mis==2 and can==2:
            return True
        elif mis==1 and can==1:
            return True
        elif mis==0:
            return True
    else:
        return False


def mc_tour(path,u,stop):
    #znajdujemy ścieżkę między początkiem a końcem
    u.setColor('gray')
    path.append(u) #dodajemy do listy obecny wierzchołek
    nbr_list=list(u.getConnections())
    i=0
    #sprawdzamy dalsze drogi dla jego sąsiadów
    while i < len(nbr_list) and u!=stop:
        if nbr_list[i].getColor()=="white":
            u=mc_tour(path,nbr_list[i],stop)[0]
        i=i+1
    if u!=stop:        #jeżeli dana ścieżka nie kończy się naszym endem
                       #lub nie ma już wierzchołków do odwiedzenia, to cofamy się
        path.pop()
        u.setColor('white')
    return u,path

def show_boringly(a):
    #jeden ze sposobem przedstawienia naszej ścieżki
    for i in a:
        if i.getId()[2]==0:
            boat="łódka na prawym brzegu"
        else:
            boat="łódka na lewym brzegu"
        print("Krok ",a.index(i),":")
        print("Lewy brzeg: ", "misjonarze: ",i.getId()[0],","," kanibale: ",i.getId()[1],",",boat)


def show_nicely(a):
    #ładniejszy sposób graficzny
    print("misjonarze = ✙ \nkanibale = ☠  \nłódka = ⛵ \n")

    for i in a:
        if i.getId()[2]==0:
            boat=" | ~~~~⛵ | "
        else:boat=" | ⛵~~~~ | "
        print("Krok ",a.index(i),":")
        print("✙"*i.getId()[0]," ","☠"*i.getId()[1],boat,"✙"*(3-i.getId()[0])," ","☠"*(3-i.getId()[1]))

if __name__=="__main__":
    g=missionary_cannibal_graph()
    g.generateDot()
    a=mc_tour([],g.getVertex((3,3,1)),g.getVertex((0,0,0)))[1]
    #show_boringly(a)
    show_nicely(a)



