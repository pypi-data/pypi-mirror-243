import json
import re
import os,glob
from gpflib import GPF
import requests
import jieba
import gpflib

def PrintRelation(gpf):
    Relations=gpf.GetRelations()
    for R in Relations:
        Relation=gpf.GetWord(R["U1"])+" "+gpf.GetWord(R["U2"])+"("+R["R"]+")"
        KVs=gpf.GetRelationKVs(R["U1"],R["U2"],R["R"])
        Info=""
        for k in KVs:
            Val=" ".join(KVs[k])
            if len(KVs[k]) > 1:
                Info=Info+k+"=["+Val+"] "
            else:
                Info=Info+k+"="+Val+" "
            print("=>"+Relation)
        if Info != "":
	        print("KV:"+Info)


def PrintUnit(gpf,Type=""):
    if Type =="":
        Type="Type=Chunk|Type=Word|Type=Phrase|Type=Char"	
    GridInfo=gpf.GetGrid()
    for Col in GridInfo:
        for Unit in Col:
            if gpf.IsUnit(Unit,Type):
                Info=""
                KVs=gpf.GetUnitKVs(Unit)
                print("=>",gpf.GetWord(Unit))
                for K in KVs:
                    Val=" ".join(KVs[K])
                    print(K,"=",Val)


def DrawGraph(gpf,Name="",DotPath=".\\Graph\\",OutPath="./"):
    Head='''
    digraph g {
        node [fontname="FangSong"]
        rankdir=TD  '''    
    if Name=="":
        DepHeads=gpf.GetGridKVs("URoot")
        Graph="Graph.png"
    else:
        DepHeads=gpf.GetGridKVs("URoot"+Name+"")
        Graph=Name+"Graph.png"
    Graph=OutPath+Graph
    
    Tree="tree.txt"
    OUT = open(Tree ,"w",encoding="utf8")
    print(Head,file=OUT)
    Inserted={}
			
    for i in range(len(DepHeads)):
        print("Root->"+gpf.GetWord(DepHeads[i])+"\n",file=OUT)
        Roles=gpf.GetUnitKVs(DepHeads[i],"RSub"+Name)
        for j in range(len(Roles)):
            Units=gpf.GetUnitKVs(DepHeads[i],"USub"+Name+"-"+Roles[j])
            for k in range(len(Units)):
                Rel=gpf.GetWord(DepHeads[i])+"->"+gpf.GetWord(Units[k])+"[label="+Roles[j]
                if not Inserted.get(Rel):
                    print(Rel+"]\n",file=OUT)
                    Inserted[Rel]=1
                RS=gpf.GetUnitKVs(Units[k],"RSub"+Name)
                for l in range(len(RS)):
                    UnitFs=gpf.GetUnitKVs(Units[k],"USub"+Name+"-"+RS[l])
                    for m in range(len(UnitFs)):
                        Rel=gpf.GetWord(Units[k])+"->"+gpf.GetWord(UnitFs[m])+"[label="+RS[l]
                        if not Inserted.get(Rel):
                            print(Rel+"]\n",file=OUT)
                            Inserted[Rel]=1
    print("}\n",file=OUT)
    OUT.close()
    Cmd=DotPath+"dot -Tpng "+Tree+" -o "+Graph
    os.system(Cmd)
    Cmd="del "+Tree
    os.system(Cmd)


def DrawNode(gpf,OUT,Root,Name=""):
	if Name == "":
		USub="USub-Link"
	else:
		USub="USub"+Name+"-Link"
	
	V=gpf.GetUnitKVs(Root,USub)
	if len(V) == 0:
		return
	for i in range(len(V)):
		R=" ".join(gpf.GetUnitKVs(V[i],"POS"))
		print(gpf.GetWord(Root)+" -> "+gpf.GetWord(V[i])+' [label="'+R+"\", color=blue]\n",file=OUT)
		DrawNode(gpf,OUT,V[i],Name)

def DrawTree(gpf,Name="",DotPath=".\\Graph\\",OutPath="./"):
    Head='''
digraph g {
    node [fontname="FangSong"]
    rankdir=TD  
'''
    if Name == "":
        Root="URoot-Link"
        Graph="tree.png"
    else:
        Root="URoot"+Name+"-Link"
        Graph=Name+"tree.png"
    Graph=OutPath+Graph
    Tree="tree.txt"
    OUT = open(Tree,"w",encoding="utf8")
    print(Head,file=OUT)
    V=gpf.GetGridKVs(Root)
    if len(V) == 0:
        return
    for i in range(len(V)):
        if len(V) >0:
            print("Root->"+gpf.GetWord(V[i])+"\n",file=OUT)
        DrawNode(gpf,OUT,V[i],Name)
    print("}\n",file=OUT)
    OUT.close()
	
    Cmd=DotPath+"dot -Tpng "+Tree+" -o "+Graph
    os.system(Cmd)
    Cmd="del "+Tree
    #os.system(Cmd)

def Test_Grid():
    gpf = GPF("config.txt")
    Line='{"Type": "Chunk", "Units": ["瑞士球员塞费罗维奇", "率先", "破门", "，", "沙其理", "梅开二度", "。"], "POS": ["NP", "XP", "VP", "w", "NP", "VP", "w"], "Groups": [{"HeadID": 1, "Group": [{"Role": "sbj", "SubID": 0}]}, {"HeadID": 2, "Group": [{"Role": "sbj", "SubID": 0}]}, {"HeadID": 5, "Group": [{"Role": "sbj", "SubID": 4}]}],"ST":"dep"}'
    gpf.AddStructure(Line)
    Grid = gpf.GetGrid()
    for C in Grid:
        for U in C:
            print(U,gpf.GetWord(U))
            
    KV = gpf.GetGridKVs("")
    for K in KV:
        for V in KV[K]:
            print(K,V)

def Test_JSON():
    Line= """
    {"Words": ["瑞士", "率先", "破门", "，", "沙其理", "梅开二度", "。"], 
    "Tags": ["ns", "d", "v", "w", "nr", "i", "w"], 
    "Relations": [{"U1": 2, "U2":0,"R":"A0","KV":"KV1"},
    {"U1": 2, "U2":1,"R":"Mod","KV":"KV2"},
    {"U1": 5, "U2":4,"R":"A0","KV":"KV3"}]} """
    gpf = GPF()
    
    json_data = json.loads(Line)
    Sentence="".join(json_data["Words"])
    gpf.SetText(Sentence)
    Units=[]
    Col=0
    for i in range(len(json_data["Words"])):
        Col=Col+len(json_data["Words"][i])
        print(json_data["Words"][i],Col-1)
        Unit=gpf.AddUnit(Col-1,json_data["Words"][i])
        gpf.AddUnitKV(Unit,"POS",json_data["Tags"][i])
        Units.append(Unit)
        
    for i in  range(len(json_data["Relations"])):
        U1=Units[json_data["Relations"][i]["U1"]]
        U2=Units[json_data["Relations"][i]["U2"]]
        R=json_data["Relations"][i]["R"]
        KV=json_data["Relations"][i]["KV"]
        gpf.AddRelation(U1,U2,R)
        gpf.AddRelationKV(U1,U2,R,"KV",KV)

    GridInfo=gpf.GetGrid()
    for C in GridInfo:
        for U in  C:
            print("=>",gpf.GetWord(U))
	
    Rs = gpf.GetRelations("")
    for R in Rs:
        print(gpf.GetWord(R["U1"]),gpf.GetWord(R["U2"]),R["R"])
    print(gpf.GetText(0,-1))


def Test_TermInfo():
    gpf = GPF()
    Line="称一种无线通讯技术为蓝牙"
    gpf.SetText(Line)
    gpf.AppTable("Segment_Term")
    gpf.RunFSA("Term")
    Units=gpf.GetUnits("Tag=Term")
    for i in range(len(Units)):
        print(gpf.GetWord(Units[i]))     

def Idx_GPF(Name,Path="./data"):
    for file in glob.glob(Path):
        if os.path.isfile(file):
            os.remove(file)

    gpf = GPF(Path)
    FSA="./Examples/"+Name+"/GPF.fsa"
    if os.path.exists(FSA):
        gpf.IndexFSA(FSA)
    Table="./Examples/"+Name+"/GPF.tab"
    if os.path.exists(Table):
        gpf.IndexTable(Table)
   
def Test_Time():
    Line="星期日下午我去图书馆"
    gpf = GPF()
    gpf.SetText(Line)
    gpf.AppTable("Time_Entry")
    gpf.RunFSA("Time")
    Us=gpf.GetUnits("Tag=Time")
    for U in Us:
        print(gpf.GetWord(U))


def Test_DupWord():
    Sent="李明回头看了一看。"
    gpf = GPF()
    Segment=gpf.CallService(Sent,"seg")
    gpf.AddStructure(Segment)
    gpf.RunFSA("DupWord")
    Units=gpf.GetUnits("Tag=DupWord")
    for i in range(len(Units)):
        print(gpf.GetWord(Units[i]))

def Test_Merge():
    Line = "下半场的38分钟，李明攻入第1个球，成功将比分扳平至2-1。"
    gpf = GPF()
    gpf.SetText(Line)
    depseg_struct = gpf.CallService(Line, "depseg")
    gpf.AddStructure(depseg_struct)
    gpf.AppTable("Merge_Dict")
    gpf.RunFSA("Merge")
    phrase_units = gpf.GetUnits("Tag=MatchTime|Tag=Order|Tag=MatchScore")
    for i in range(len(phrase_units)):
        print(gpf.GetWord(phrase_units[i]))

def Test_Mood():
    Sent="李明非常不喜欢他"
    gpf = GPF()
    gpf.SetText(Sent)
    DepStruct=gpf.CallService(gpf.GetText(),"dep")
    gpf.AddStructure(DepStruct)
    Seg=gpf.CallService(gpf.GetText(),"seg")
    gpf.AddStructure(Seg)
    gpf.AppTable("Tab_Mod")
    gpf.RunFSA("Mod2Head")
    gpf.RunFSA("Mod2Prd")
    Logs=gpf.GetLog()
    for log in Logs:
        print(log)
    Units=gpf.GetUnits("Tag=Mood")
    for i in range(len(Units)):
        print(gpf.GetWord(Units[i]))


def Test_WSD():
    gpf=GPF()
    Sentence="这个苹果很甜呀"
    gpf.SetTable("Dict_Info")
    gpf.SetText(Sentence)
    Segment=gpf.CallService(gpf.GetText(),"seg")
    gpf.AddStructure(Segment)
    Units=gpf.GetUnits("Sem=*")
    for i in range(len(Units)):
        Sems=gpf.GetUnitKVs(Units[i],"Sem")
        MaxScore=-10
        WS=""
        for j in range(len(Sems)):
            gpf.RunFSA("WSD","Sem="+Sems[j])
            Score=gpf.GetUnitKVs(Units[i],"Sem_"+Sems[j])
            if len(Score) != 0:
                Score=int(Score[0])
            else:
                Score=0
            if MaxScore < Score:
                MaxScore = Score
                WS=Sems[j]
        if WS != "":
            gpf.AddUnitKV(Units[i],"Sense",WS)
    Units=gpf.GetUnits("Sense=*")
    for i in range(len(Units)):
        WS,=gpf.GetUnitKVs(Units[i],"Sense")
        print(gpf.GetWord(Units[i]),WS)

def Test_SepWord(Type):
    Sent="李明把守的大门被他破了"
    gpf=GPF()
    gpf.SetText(Sent)
    DepStruct=gpf.CallService(gpf.GetText(),"dep")
    gpf.AddStructure(DepStruct)
    Seg=gpf.CallService(gpf.GetText(),"seg")
    gpf.AddStructure(Seg)
    gpf.AppTable("Sep_V")
    if Type == 1:
        gpf.RunFSA("SepV1")
    else:
        gpf.RunFSA("SepV2")
    Units=gpf.GetUnits("Tag=SepWord")
    for  Unit in Units:
        print(gpf.GetWord(Unit))

def Test_CoEvent():
    Sentence="淘气的孩子打碎了一个花瓶。"
    gpf=GPF()
    gpf.SetText(Sentence)
    DepStruct=gpf.CallService(gpf.GetText(),"dep")
    gpf.AddStructure(DepStruct)
    Seg=gpf.CallService(gpf.GetText(),"seg")
    gpf.AddStructure(Seg)
    gpf.AppTable("Co_Event")
    gpf.RunFSA("CoEvent")
    PrintUnit(gpf)
    DrawGraph(gpf)

def Test_DrawTree():
	Line='{"Type":"Tree","Units":["(((王)((阿)(姨)))((((出)(门))((买)(菜)))(了)))"],"ST":"GPF"}'
	#Line="我们大家今天下午在操场集合"
	gpf=GPF()
	#Line=gpf.RunService(Line,"stree")
	gpf.AddStructure(Line)
	print(Line)
	DrawTree(gpf)

def Test_DrawGraph():
    Line='''
    {"Type": "Chunk", "Units": ["瑞士球员塞费罗维奇", "率先", "破门", "，", "沙其理", "梅开二度", "。"], "POS": ["NP", "VP", "VP", "w", "NP", "VP", "w"], "Groups": [{"HeadID": 1, "Group": [{"Role": "sbj", "SubID": 0}]}, {"HeadID": 2, "Group": [{"Role": "sbj", "SubID": 0}]}, {"HeadID": 5, "Group": [{"Role": "sbj", "SubID": 4}]}],"ST":"dep"}'
    '''
    gpf=GPF()
    gpf.AddStructure(Line)
    DrawGraph(gpf)


def Test_Main():
    Idx_GPF("CoEvent")
    Test_CoEvent()

def Test_BCC():
    #Query="VP-PRD[提高~]NP-OBJ[*a]{}Lua"
    # Query="提高{}Context(10)"
    # Query="a的n{}Freq"
    # Query="VP-PRD[]{}Freq"
    Query="(VP-PRD[])NP-OBJ[*(n)]{end($1)=[当]}Freq"
    # Query=".n{}Freq"
    # Query="增强~w{}Freq"
    # Query="是*的w{}Freq"
    # Query="是^的w{}Freq"
    # Query="v了(n){$1=[世界 人类 社会]}Freq" 
    # Query="(v)一(v){$1=$2}Freq" 
    # Query="VP-PRD[]{beg($Q)=[很 非常]}Freq"
    # Query="吃(n){len($1)=3}Freq" 
    Query="VP-PRD[d(v)了]{}Freq($1)" 
    Query="(NP-OBJ[根本*]){}Lua"
    Query="NULL-MOD[]VP-PRD[*n]{}Freq"
    Query="SetMax(102400,102400,20480)"
    Query="(VP-PRD[])NP-OBJ[*(n)]{mid($1)=[吃];len($2)=2}Freq($Q)"
    Query="(NP-OBJ[*根本]){}Freq"
    Query="(VP-PRD[吃])NP-OBJ[*(~)]{len($2)=2}Freq($Q)"
    gpf = GPF()
    Out=gpf.RunService(Query,"hskxw")
    print(Out)
    

def Test_POST():
    Query="(VP-PRD[])NP-OBJ[*n]{mid($1)=[打]}Context()"
    Query="SetMax(10240,10240,2048)"
    Query="(NULL-MOD[])VP-PRD[*a]{beg($1)=[非常]}Freq($Q)"
    Query="(n)一(n){$1=$2}Freq($Q)"
    BCCUrl="http://nlp.blcu.edu.cn/bcc-rmrb/"
    BCCUrl="http://127.0.0.1:8001/struct"
    headers = {'Content-Type': 'text/plain'}
    r = requests.post(BCCUrl, Query, headers=headers,timeout=5000)
    print(r.text)
    return r.text    

def BCC_KV1():
    gpf = GPF() 
    Words ="""爱;爱好;帮;帮忙;包;比;病;差;唱;唱歌;吃;吃饭;出;出来;出去;穿;打;打车;打电话;打开;打球;到;得到;等;点;动;读;读书;对不起;饿;放;放假;放学;飞;干;告诉;给;跟;工作;关;关上;过;还;喝;回;回答;回到;回家;回来;回去;会;记;记得;记住;见;见面;教;叫;介绍;进;进来;进去;觉得;开"""
    Query="AddKV(Class1,{})".format(Words)
    print(Query)
    Ret = gpf.RunService(Query, "hskjc")
    Query="VP-PRD[*(~)]NP-OBJ[*(n)]{mid($1)=[Class1];len($1)<=5}Freq($1+$2,1000)"
    Ret = gpf.RunService(Query, "hskjc")
    print(Ret)
    Ret = gpf.RunService("GetKV()", "hskjc")
    print(Ret)
    gpf.RunService("ClearKV", "hskjc")
    
def BCC_Corpus1():
    gpf=GPF()
    IN=open("./Examples/BuildBCC/Corpus.txt","r")    
    Out=open("./Examples/BuildBCC/treebank.txt","w")
    Num=0
    for Line in IN:
        Num+=1;
        Tree=gpf.CallService(Line.strip(),"stree")
        try:
            Ret=json.loads(Tree.replace('\\','\\\\'),strict=True)
        except:
            continue
        if Ret.get("Units") and len(Ret["Units"]) >0:
            print(json.loads(Tree)["Units"][0],file=Out)
        if Num%50 == 0:
            print("processing:",Num,end="\r")
            
    IN.close()
    Out.close()

def BCC_Corpus2():
    CorpusIn="./Examples/BuildBCC/treebank.txt"
    CorpusOut="./Examples/BuildBCC/treebankEx.txt"
    IN=open(CorpusIn,"r")    
    Out=open(CorpusOut,"w")
    Num=0
    No=0
    for Line in IN:
        Line=Line.strip()
        if Num%100 == 0:
            print("Table %dParts"%No,file=Out)
            print("#Global ID=%d"%No,file=Out)
            No+=1
        Num+=1;
        print("Item:%s"%Line,file=Out)
    IN.close()
    Out.close()


def BCC_DrawTree():
	Line="我们大家今天下午在操场集合"
	gpf=GPF()
	Line=gpf.RunService(Line,"stree")
	gpf.AddStructure(Line)
	DrawTree(gpf)

def BCC_Lua0():
    gpf = GPF()
    Query="VP-PRD[*(v)]NP-OBJ[*(n)]{mid($1)=[Class1];len($1)<=5}Lua($1+$2,1000)"
    Ret = gpf.RunService(Query, "hskjc")
    print(Ret)


    
def BCC_Lua1():
    gpf = GPF()
    Words ="""爱;爱好;帮;帮忙;包;比;病;差;唱;唱歌;吃;吃饭;出;出来;出去;穿;打;打车;打电话;打开;打球;到;得到;等;点;动;读;读书;对不起;饿;放;放假;放学;飞;干;告诉;给;跟;工作;关;关上;过;还;喝;回;回答;回到;回家;回来;回去;会;记;记得;记住;见;见面;教;叫;介绍;进;进来;进去;觉得;开"""
    Query="AddKV(Class1,{})".format(Words)
    Ret = gpf.RunService(Query, "hskjc")
    Query="VP-PRD[*(v)]NP-OBJ[*(n)]{mid($1)=[Class1];len($1)<=5}Lua($1+$2,1000)"
    Ret = gpf.RunService(Query, "hskjc")
    print(Ret)
    Ret = gpf.RunService("GetKV()", "hskjc")
    print(Ret)
    gpf.RunService("ClearKV()", "hskjc")

def BCC_Lua2():
    gpf = GPF()
    Query='''
Handle0=GetAS("$NP-SBJ","","","","","~","","","","0,1")
Handle1=GetAS("击>","打击")
Handle3=JoinAS(Handle0,Handle1,"*")
Handle4=Freq(Handle3,"$1")
Output(Handle4,1000)'''
    Ret=gpf.RunService(Query, "hskjc")
    print(Ret)
    


def BCC_Query():
    gpf = GPF()
    Querys=[]
    Querys.append("(v)一(v){$1=$2}Freq")
    Querys.append("(v)一(v){$1=$2}Freq($Q,100,3)")
    Querys.append("NP-SBJ[*(n)]VP-PRD[*(~)]{end($1)=[车 机 路]}Freq($1+$2)")
    Querys.append("NULL-MOD[ ]VP-PRD[*(~)]{$1=[打击 发回 返回 后悔]}Freq")
    Querys.append("(VP-PRD[])(NP-SBJ[]){len($1)=1;len($2)=2}Freq")
    Querys.append("VP-PRD[*(~)]NP-SBJ[*(n)]{}Freq($1+$2)")
    Querys.append("VP-PRD[*(v)]NP-SBJ[*(n)]{}Lua")
    for Q in Querys:
        Ret=gpf.RunService(Q, "hskjc")
        print("==>",Q)
        print(Ret)

    
def Test():
    gpf = GPF()
    Files=["D:/Xunendong/GPF/Src/pysetup/gpflib/Examples/BuildBCC/treebankTest.txt"]
    Ret=gpf.IndexBCC(Files)
    
def Test1():
    gpf = GPF()
    gpf.SetMax()   
    Ret=gpf.BCCContext("a的")
    print(Ret)

def Test2():
    gpf = GPF()
    Ret=gpf.GetTableItems("GF")
    for I in Ret:
        print(I)
        
def Test3():
    gpf = GPF()
    In=open("./Examples/BuildBCC/Corpus.txt","r")
    Num=0
    for S in In:
        Ret=gpf.Segment(S.strip())
        if Num%10000 == 0:
            print(Num,Ret)
        Num+=1 
    In.close()

def Test4():
    gpf=GPF()
    Ret=gpf.Segment("邱南顾惨叫一声")    
    print(Ret)
           
def Test5():
    In=open("./Examples/BuildBCC/Corpus.txt","r")
    Num=0
    for S in In:
        Ret=jieba.lcut(S)
        if Num%2000 == 0:
            print(Num,Ret)
        Num+=1 
    In.close()

def Test6():
    gpf = GPF()
    gpf.SetMax()   
    Ret=gpf.CallService("a的{}Freq","BCC")
    print(Ret)

def Test7():
    gpf=gpflib.GPF()
    Ret=gpf.POS("荀恩东老师在上课")
    print(Ret)

Test3()