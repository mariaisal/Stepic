__author__ = 'Vera'
import operator
fin = open('input.txt', 'r')
fout=open('output.txt', 'w')
M=int(fin.readline())
N=int(fin.readline())

Spectrum=[int(x) for x in (fin.readline().split(' '))]

acid=[]
d_cs={}


def get_conv(Spectrum):
    d={}
    ans=[]
    conv=[]
    for i in range(len(Spectrum)):
        for j in range(i+1,len(Spectrum)):
            if i!=j:
                c=abs(Spectrum[i]-Spectrum[j])
                if c >= 57 and c<=200:
                    conv.append(c)
    for c in conv:
        if c in d.keys():
            d[c]+=1
        else:
            d[c]=1
    val=d.values()
    val.sort()
    val_m=val[-M]
    for c in d.keys():
        if d[c]>= val_m:
            ans.append(c)

    print(d)
    return ans

conv=get_conv(Spectrum)
print (conv)
def Expand(List):
    List_t=[]
    for peptide in List:
        for value in conv:
            temp_peptide=peptide[:]
            temp_peptide.append(value)
            List_t.append(temp_peptide)
    return List_t

def Mass(peptide):
    mass=0
    for i in peptide:
        mass=mass+i
    return mass

def Cyclospectrum(Peptide):
    if str(Peptide) in d_cs.keys():
        return d_cs[str(Peptide)]
    else:
        li=[]
        fm=0
        Peptide_t=Peptide[1:]
        for j in range(len(Peptide_t)):
            fm+=Peptide_t[j]
            m=0
            for i in range(len(Peptide_t)-1):
                li.append((m+Peptide_t[(j+i)%len(Peptide_t)]))
                m+=Peptide_t[(j+i)%len(Peptide_t)]
        li.append(0)
        li.append(fm)
        li.sort()
        d_cs[str(Peptide)]=li
        return li

def spectrum(Peptide):
    li=[]
    for j in range(1, len(Peptide)):
        m=0
        for i in range(len(Peptide)-j):
            li.append(m+Peptide[(j+i)])
            m+=Peptide[(j+i)]
    li.append(0)
    li.sort()
    return li

def Score(spectrum_peptide, Spectrum):
    Spectrum_t=Spectrum[:]
    score=0
    for p in spectrum_peptide:
        if p in Spectrum_t:
            Spectrum_t.remove(p)
            score=score+1
    return score

def Cut(Leaderboard, Spectrum, N):
    d={}
    ans=[]
    for p in Leaderboard:
        d['-'.join(str(x) for x in p)]=Score(Cyclospectrum(p),Spectrum)
    v=sorted(d.values())
    v_t= v[len(v)-N:]
    for key in d.keys():
        if d[key] in v_t:
            ans.append([int(x) for x in key.split('-')])
    return ans

def LEADERBOARDCYCLOPEPTIDESEQUENCING(Spectrum, N):


    Leaderboard=[]
    Leaderboard_tmp=[]
    peptide0=[]
    peptide0.append(0)
    Leaderboard.append(peptide0)
    Leaderboard_tmp=Leaderboard[:]
    LeaderPeptide=peptide0
    Spectrum.sort()
    parentMass = Spectrum[-1]
    leaderScore = 0
    Leader_TEMP=[]
    while len(Leaderboard_tmp)!=0:
        Leaderboard = Expand(Leaderboard)
        d_cs.clear()
        print('Here!')
        Leaderboard_tmp=Leaderboard[:]
        for Peptide in Leaderboard_tmp:
            if Mass(Peptide) == parentMass:
                if Score(Cyclospectrum(Peptide), Spectrum) >= leaderScore:
                    LeaderPeptide = Peptide
                    Leader_TEMP.append(LeaderPeptide)
                    leaderScore = Score(Cyclospectrum(LeaderPeptide), Spectrum)
                    #print(LeaderPeptide,Score(Cyclospectrum(LeaderPeptide), Spectrum))
            elif Mass(Peptide) > parentMass:
                Leaderboard.remove(Peptide)
        Leaderboard = Cut(Leaderboard, Spectrum, N)
        Leaderboard_tmp=Leaderboard[:]
    scorelp=[]
    for lp in Leader_TEMP:
        scorelp.append(Score(Cyclospectrum(lp),Spectrum))
    #print(Leader_TEMP)
    m = max(scorelp)
    print(m)
    for i in range(len(Leader_TEMP)):
        if scorelp[i]==m:
            leader=Leader_TEMP[i]
            print(leader,Score(Cyclospectrum(leader),Spectrum),'!')
            fout.write("-".join(str(x) for x in leader[1:])+" ")
LEADERBOARDCYCLOPEPTIDESEQUENCING(Spectrum,N)
fin.close()
fout.close()
