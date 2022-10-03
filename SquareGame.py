from random import choice
from string import  ascii_uppercase


def createTable(row): # Tablonun yatay,dikey,sayı ve harflerin oluşturulma işlemi
    elements = ["ABCDEFGH","1234","---","|"]
    allRows = []
    elementRow = []
    """
      A   B   C   D   G
    1  --- --- --- ---  1
      |   |   |   |   |
    2  --- --- --- ---  2
      |   |   |   |   |
    3  --- --- --- ---  3
      |   |   |   |   |
    4  --- --- --- ---  4
        A   B   C   D 
    """
    def ustaltSatır():
        ustAltSatır = ""
        for i in range(0,row+1):
            if elements[0][i] == "A":
                ustAltSatır+=" "*2+elements[0][i]+" "*3
            else :
                ustAltSatır+=elements[0][i]+" "*3
        allRows.append(ustAltSatır)
         
    ustaltSatır()
    for i in range(0,row+1):
        if i == row  :
            ustaltSatır()
        else:
            satir1=str(i+1)+" "*2+(elements[2]+" "*1)*row+" "*1+str(i+1)
            allRows.append(satir1)
            elementRow.append(satir1)
            if i != row-1 : 
                satir1=" "*2+(elements[-1]+" "*3)*(row+1)
                allRows.append(satir1)
        
    return allRows

def createColumn(col,row): # Tablonun boşluklarını tanımlama ve tanımlanan boşlukların varsayılan değerlerini atama.
    colm = "ABCDEFGH"
    rows = "".join(str(num) for num in range(1,row+1))
    positions = {}
    positions_value = {}
    for i in range(row):
        n = 2 
        for j in range(col+1):
            name = str(rows[i])+str(colm[j])
            positions.update({name:n})
            positions_value.update({name:0})
            n+=4
    return positions , positions_value
    
def squareData(): # Tablodaki var olabilecek kare kombinasyonları bulma.
    data = []
    colm1 = "ABCDEFGH"
    for i in range(0,colm):
        data.append(str(colm1[i])+str(colm1[i+1]))
        
    square = []
    for j in data:
        for i in range(1,colm):
            square.append(str(i)+j[0]+"-"+str(i)+j[1]+"-"+str(i+1)+j[0]+"-"+str(i+1)+j[1])
            
    return square

def play(player,text="2A"): # Kullanıcının verdiği kolonun kullanıcının sembolü ile doldurulması.
    if config["Positions_value"][text] == 0 :
        config["Positions_value"][text] = player
        num = text[0]
        num = int(num)*2 - 1 
        characterNum = config["Positions"][text]
        textRows[num] = textRows[num][:characterNum]+ player + textRows[num][characterNum+1::]
        return True
    else :
        return False
    
def clearCell(player,text="2A"): # Verilen kolondaki sembolün temizlenmesi.
    if config["Positions_value"][text] == 0 :
        return False 
    else :
        config["Positions_value"].update({text:0})
        num = text[0]
        num = int(num)*2 - 1 
        characterNum = config["Positions"][text]
        textRows[num] = textRows[num][:characterNum]+ player + textRows[num][characterNum+1::]
        return True
        
def tableShow(table): # Oluşturulmuş veya değiştirilmiş tablonun görüntülenmesi.
    for tbl in table :
        print(tbl)

def pieceControl(playerCount,player): # Gelen oyuncu ve oyuncu sembolünün oluşturmuş olduğu veya bozmuş olduğu karelerin kontrolü
    for data in squareData():
        x = 0
        for j in data.split("-"):
            if config["Positions_value"][j] == player:
                x+=1
        if x == 4 :
            if playerData[playerCount]["Used_Square"].count(data) == 0 and playerData[playerCount]["SquarePositions"].count(data) == 0:
                playerData[playerCount]["SquarePositions"].append(data)
        elif x == 3 :
            for used_square in playerData[playerCount]["Used_Square"]:
                if used_square.find(data) != -1 :
                    playerData[playerCount]["Used_Square"].remove(used_square)
        
def winControl(): # Oyunda kazananın belirlenmesi
    if playerData["Player1"]["LostPiece"] == 3 :
        playerData["Player1"]["Status"] = 0
        playerData["Player2"]["Status"] = 1
        
    if playerData["Player2"]["LostPiece"] == 3 :
        playerData["Player2"]["Status"] = 0
        playerData["Player1"]["Status"] = 1
        
    for player in playerData :
        if playerData[player]["Status"] == 1 :
            print("{} Kazandı. Sembol({})".format(player,playerData[player]["Symbol"]))
            exit()
                      
def playerPriceCombine(playerCount,playerSymbol,cont): # Taşların oynatılması, taşın dışa atılması vb. işlemlerin yapıldığı kısımdır.
    while True :
        try :
            # Kullanıcıların taşlarını kontrol eder ve eğer taşları bitti ise else çalışır.
            if playerData[playerCount]["Piece"] > 0 :
                py1 = input("{} ({}) [{}]: ".format(playerCount,playerSymbol,playerData[playerCount]["Piece"]))
                result = play(player=playerSymbol,text=py1.upper().strip())
                if result :
                    playerData[playerCount]["Piece"]-=1
                    pieceControl(playerCount,playerSymbol)
                    print("Kare Sayınız : {}".format(len(playerData[playerCount]["SquarePositions"])))
                    break
                else :
                    print("Girdiğiniz alanda başka taş bulunmaktadır.")
                    continue
            else :
                # İlk olarak taşlar bittiği gibi kare kontrolü yapar ve eğer kare yok ise birinci if çalışır bir kere çalışabilmesi için pieceFinished bir arttırılır.
                if finishPice():
                    print("Rakibiniz ve sizde kare bulunmamaktadır. Oyun kuralları gereği ilk oyuncu rakibinin bir taşını devre dışı bırakacak.")
                    out = input("Taşın Kordinatını yazınız (1A) Oynayacak Oyuncu ({}) : ".format(playerSymbol)).strip().upper()
                    if len(out) == 2:
                        if config["Positions_value"][out] != playerSymbol :
                            result = clearCell(player=" ",text=out)
                            playerData[cont]["LostPiece"]-= 1
                            break  
                        else :
                            print("Kendi taşınızın kordinatlarını verdiniz.")
                            config["pieceFinished"] = 0
                            continue
                    else :
                        print("Fazla veya eksik giriş yapıldı.")
                        config["pieceFinished"] = 0
                        continue
                # Burası ise kullanıcını kare kontrolünü sağlar ve eğer kare var ise çalışır ve kullanıcının bir taşının atılmasını sağlar.
                if len(playerData[playerCount]["SquarePositions"]) > 0 :
                    config["pieceFinished"] = 1
                    control = False
                    print("{} Kare sayınız : {} || Karşı oyuncunun taşlarından {} tanesini oyun dışına atabilirsiniz.".format(playerCount,len(playerData[playerCount]["SquarePositions"]),len(playerData[playerCount]["SquarePositions"])))
                    outs = input("Atılacak Taşların Kordinatlarını yazınız (1A-2C) : ").strip().upper().split("-")
                    if len(outs) == len(playerData[playerCount]["SquarePositions"]):
                        for out in outs :
                            piece = config["Positions_value"][out.strip().upper()]
                            if piece != playerSymbol and piece != 0:
                                control = True
                                for i in playerData[cont]["SquarePositions"]+playerData[cont]["Used_Square"]:
                                    if i.find(out.strip().upper()) != -1 :
                                        control = False
                                        print("Girilen verilerlerde kare tespit edildi.")
                                        break
                            else :
                                print("Girilen verilerde sizin taşınız var veya kutu boş")
                                control = False
                                break
                        if control :
                            for pr in outs :
                                result = clearCell(player=" ",text=pr.upper().strip())
                                playerData[cont]["LostPiece"] -= 1
                            for i in playerData[playerCount]["SquarePositions"] :
                                playerData[playerCount]["Used_Square"].append(i)
                            playerData[playerCount]["SquarePositions"].clear()
                            break  
                        else :
                            continue
                
                # Taşın kordinat değişiminin yapıldığı kısımdır.
                else :
                    if config["pieceFinished"] == 0 :
                        config["pieceFinished"] = 1
                        break
                    py1 = input("{} ({}) [{}] Hangi taşı oynayacaksınız? (1a 2a) / Oynatacak taşınız yoksa pas demelisiniz. : ".format(playerCount,playerSymbol,playerData[playerCount]["LostPiece"]))
                    if py1.strip().lower() == "pas":
                        break
                    textSplit = py1.strip().split()
                    if len(textSplit) == 2 :
                        if config["Positions_value"][textSplit[0].upper().strip()] == playerSymbol and config["Positions_value"][textSplit[1].upper().strip()] == 0:
                            if textSplit[1].endswith(textSplit[0][1]) or textSplit[1].startswith(textSplit[0][0]): # Gidilenilecek bölge kontrolü
                                result2 = play(player=playerSymbol,text=textSplit[1].upper().strip())
                                if result2 :
                                    clearCell(player=" ",text=textSplit[0].upper().strip())
                                    pieceControl(playerCount,playerSymbol)
                                    print("Kare Sayınız : {}".format(len(playerData[playerCount]["SquarePositions"])))
                                    if len(playerData[playerCount]["SquarePositions"]) > 0 :
                                        tableShow(textRows)
                                        continue
                                    else :
                                        break
                                else :
                                    print("Girdiğiniz alanda başka taş bulunmaktadır.")
                                    continue
                            else :
                                print("Taşınız verdiğiniz alana ilerleyemez.")
                                continue
                        else :
                            print("Oynatmaya çalıştığınız taş karşı oyuncuya ait veya ilerlemeye çalıştığınız yerde taş var.")
                            continue
                    else :
                        print("Fazla veya yanlış giriş yaptınız.")
                        continue
        except Exception:
            print("Yanlış giriş yaptınız.")
            continue

def finishPice(): # Taşlar bittiğinde oyuncuların karelerinin kontrolü
    if config["pieceFinished"] == 0 :
        if len(playerData["Player1"]["SquarePositions"]) == 0 and len(playerData["Player2"]["SquarePositions"]) == 0 :
            config["pieceFinished"] = 1
            return True
        else :
            return False
    else :
        return False

if __name__ == "__main__":
    letters = ascii_uppercase  # Alfabe
    pieceCombination = {3:6,4:10,5:15,6:21,7:28} # Taş kombini
    start = input("Oyuna başlamak istermisiniz ? (y/n) : ").lower().strip()
    if start != "y":
        exit(0)
        
    player1Symbol = input("Player1 Sembol Giriniz :") # Kullanıcı 1 sembolü
    if player1Symbol == "" : # Eğer kullanıcı 1 sembolü boş verilirse random bir harf verilecek.
        player1Symbol = choice(letters)
        letters = letters.replace(player1Symbol,"") # Birinci kullanıcının harfini alfabeden silme işlemi
    player2Symbol = input("Player2 Sembol Giriniz :") # Kullanıcı 2 sembolü
    if player2Symbol == "" : # Eğer kullanıcı 2 sembolü boş verilirse random bir harf verilecek.
        player2Symbol = choice(letters)
        
    while True :
        try :
            colm = int(input("Yatay Çizgi Sayısı (3-7) : ")) # Tablonun kolon sayısını belirler.
            if colm >= 3 and colm <= 8 : 
                break
        except :
            continue
          
    textRows = createTable(colm) # Tablo oluşturucu çağırma
    column = createColumn(colm,colm) # Tablonun verilerini çağırma
    config = {"Positions":column[0],"Positions_value":column[1],"pieceFinished": 0}

    # playerData : Oyuncu verileri (Taş sayısı, kaybedilen taş sayısı , oyuncu sembolü , kazanım durumu, kare pozisyonları, kullanılan kareler )
    playerData = {"Player1":{"Piece":pieceCombination[colm],"LostPiece":pieceCombination[colm],"Symbol":player1Symbol[0].upper(),"Status":2,"SquarePositions":[],"Used_Square":[]},
                 "Player2":{"Piece":pieceCombination[colm],"LostPiece":pieceCombination[colm],"Symbol":player2Symbol[0].upper(),"Status":2,"SquarePositions":[],"Used_Square":[]}}
    while True :
        print("-"*50)
        tableShow(textRows) # Tabloyu görüntüle
        winControl() # Kazanım kontrolü
        data = list(playerData.keys()) # Kullanıcı verilerinin anahtar kelimeleri
        playerPriceCombine(data[0],playerData[data[0]]["Symbol"],data[1]) # Birinci oyuncu için oynatma işlemi
        winControl() # Kazanım kontrolü
        print("-"*50)
        tableShow(textRows) # Tabloyu görüntüle
        playerPriceCombine(data[1],playerData[data[1]]["Symbol"],data[0]) # İkinci oyuncu için oynatma işlemi
        


