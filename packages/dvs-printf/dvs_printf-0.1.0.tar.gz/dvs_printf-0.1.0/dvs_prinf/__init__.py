"""A Test dvs_printf package."""

from time import sleep
renint = ["a","b","c","d","e","f","g","h","i","c","d","-","l","a","w","t","r","s","v","x","a","z","n","o","p","q","r","s","t"]

def listfunction(a=[],getMet=False):
    newa_a=[]
    for x in a: 
        try:
            res=list(filter(lambda x:isinstance(x,list),x))
            if(len(res)==len(x)):getMet=True
        except:pass
        if getMet:
            for i in x:newa_a.append(str(i).replace("\n",""))
        elif type(x) == dict:
            for i in x:newa_a.append(f"{i}: {x[i]}".replace("\n",""))
        elif (type(x) == list)or(type(x)==tuple)or(type(x) == set):
            newa_a.extend(listfunction(x))
        else:newa_a.append(str(x))
    return newa_a

class printf:    
    ''' 
prints values to a stream.

styl
   different type if printing styles, `default is "typing"`.
speed
   speed of print letter by letter `speed gose to(1 to 6)`, `default a 3`.
intervel
   waiting time between two lines, `default a 2`.
stay
   after styl animetion whether you want the stream OR NOT, `default a False`.

`styl="help" for more info`.'''

    def __init__(self, *values, styl: str | None='typing', speed: int | None = 3, intervel: int | None = 2,  stay=False):
        values = listfunction(values)
        if intervel < 0 : intervel==3
        if styl=="gunshort":speed = (.064/speed) if (speed >= 1 and speed <= 6) else .016
        elif styl=="snip":speed = (.016/speed) if (speed >= 1 and speed <= 6) else .008
        elif styl=="mid":speed = (.16/speed) if (speed >= 1 and speed <= 4) else .08
        else:speed = (.16/speed) if (speed >= 1 and speed <=6) else .08

        if styl == "typing":
            for x in values:
                emty = ""
                x = str(x)
                for y in range(0, len(x)):
                    emty = emty + x[y] if x!=set or tuple else x
                    print(emty+"⎮", end="\r", flush = True)
                    sleep(speed)
                    print(end="\r")
                    print(emty[:len(emty)], end="\r", flush = True)
                print(end="\x1b[2K")
                print(emty,end="\n")
                sleep(intervel)

        elif styl == "headline":
            for x in values:
                emty = ""
                x = str(x)
                for y in range(0, len(x)):
                    emty = emty + x[y].replace("\n","")
                    print(emty+"⎮", end="\r", flush = True)
                    sleep(speed)
                    print(emty[:len(emty)], end="\r", flush = True)
                    print(end="\x1b[2K")
                sleep(intervel)
                for i in range(0, len(x)):
                    delete_last = x[:len(x)-i-1].replace("\n","")
                    print(delete_last+"|", end="\r", flush = True)
                    sleep(speed)
                    print(end="\x1b[2K")
                if stay==True:print(x)
        
        elif styl == "mid":
            for x in values:
                x = str(x) if len(x)%2==0 else str(x)+" "
                lan = len(x)//2
                front,back="",""
                for i in range(lan):
                    front = x[lan-i-1]+front
                    back = back +x[lan+i]
                    print(" "*(lan-i-1)+front+back,end="\r",flush=True)
                    sleep(speed)
                print(end="\x1b[2K")
                if stay==True:print(x)
                sleep(intervel)

        elif styl=="gunshort":
            # stay=False
            for x in values:
                short=""
                len_x = len(x)
                for i in range(len_x):
                    try:
                        next_let = x[i+1] if " " != x[i+1] else "_"
                        index = x[i] if " " != x[i] else "_"
                    except: next_let=" "; index = x[len_x-1]
                    for j in range(len_x-i):
                        print(short+" "*(len_x-j-1-len(short))+index+(" "*j)+f"  <==[{next_let}]=|",end="\r")#*(len(x)-j)
                        sleep(speed)
                    sleep(speed)
                    short = short + x[i]
                if stay==True:
                    print(end="\x1b[2K")
                    print(short)
                else:
                    print(end="\x1b[2K")
                    print(short,end="\r")
                sleep(intervel)

        elif styl == "snip":
            import os
            for x in values:
                short=""
                one = 0
                for i in range(len(x)):
                    try:
                        next_let = x[i+1] if " " != x[i+1] else "_"
                        index = x[i] if " " != x[i] else "_"
                    except: next_let=" "; index = x[len(x)-1]
                    temlen = os.get_terminal_size()[0]
                    for j in range(0,temlen-i-len(short)+one-12):
                        print(short+" "*(temlen-j-len(short)-11)+index+" "*(j)+f" <===[{next_let}]=|",end="\r")#+" "*(temlen-len(short))
                        sleep(speed)
                    sleep(speed)
                    print(end="\x1b[2K")
                    one+=1
                    short=short+x[i]
                if stay==True:print(x)
                else:print(x,end="\r");print(end="\x1b[2K")
                sleep(intervel)

        elif styl == "f2b":
            for x in values:
                x = str(x)
                for y in range(0, len(x)):
                    print(x[y].replace("\n",""), end="", flush = True)
                    sleep(speed)
                sleep(intervel)
                for y in range(0, len(x)+1):
                    print(" "*y, end="\r", flush = True)
                    sleep(speed)
                print(end="\x1b[2K")
                sleep(intervel)
                print(end="\r")

        elif styl=="b2f":
            bigestlen = 0
            for x in values:
                if bigestlen < len(x):
                    bigestlen = len(x)
                else: x = x + " "*(bigestlen-len(x))
                for y in range(0, len(x)):
                    print(x[y], end="", flush = True)
                    sleep(speed)
                sleep(intervel)
                print(end="\r")
                for i in range(0, len(x)):
                    delete_last = x[:len(x)-i-1]
                    print(delete_last, end="  \r", flush = True)
                    sleep(speed)
                    print(end="\x1b[2K")
                sleep(intervel)
                print(end="\r")

        elif styl=="metrix":
            from random import randint
            for ab in values:
                entry = ""
                ab = ""+ab
                astimet = ""
                ab = str(ab)
                for i in range(len(ab)-1): 
                    entry = (entry + ab[i]).replace("\n","")
                    for rex in range(0,7):
                        addentru = "" 
                        for j in range(len(ab)-i-2):
                            _ = randint(5,20)
                            addentru = addentru+renint[_]
                        ren = randint(0,len(renint))-1
                        print(entry+renint[ren]+addentru, end="\r", flush = True)
                        astimet = astimet + entry+renint[ren]+addentru
                        sleep(speed)
                    print(end="\x1b[2K")
                print(ab,end="\r", flush = True)
                sleep(intervel)

        elif styl == "metrix2":
            from random import randint
            for ab in values:
                entry = ""
                ab = ""+ab
                ab = str(ab)
                for i in range(len(ab)-1):
                    entry = entry+ ab[i]
                    for _ in range(randint(5,20)):
                        ren = randint(0,len(renint))-1
                        print(entry+renint[ren], end="\n", flush = True)
                        sleep(speed)
                print(end="\x1b[2K")
                print(ab)
        
        elif styl == "firing":
            import os
            x = "___¯¯ ----¯¯___¯¯----¯ --¯-----¯- -¯---"
            len_x = len(x)
            for i in range(len_x):
                try:
                    next_let = x[i+1] 
                    index = x[i] 
                except: next_let=" "; index = x[len_x-1]
                for j in range(len_x):
                    print("\n\n|\n|")
                    print("|"+" "*(len_x-j-2)+index+(" "*j)+f" <==[{next_let}]=|",end="\r")#*(len(x)-j)
                    print("\n|\n|") 
                    os.system("clear")
                sleep(.08)
            
        elif styl == "help" :
            print("""\n
           >>>>>>>>  DVS_PRINTF Function  <<<<<<<<\n

keywords = printf(values, styl='typing', speed=3, intervel=2, stay=True)
                  
                  
values -->  main value stream can be anythin like
            (string, int, float, list, set, tuple, dict)
            and you can give multiple input as any-data-type
                  
            Ex. printf(str, list, [tuple, set], dict, int,...)
                  

styl -->  style is different type if printing styles
          from this list, each style type works 
          differently according to description below

          [typing, headline, mid, f2b, b2f, gunshort, 
            snip, metrix, metrix2, firing, help ]

           typing   =>  print like typing
           hedLine  =>  print head lines in news
           mid      =>  print line from mid
           f2b      =>  remove word from (back to front)
           b2f      =>  remove word from (front to back)
           gunshort =>  firing the words from short gun
           sniper   =>  sniping the words from end of the terminal
           metrix   =>  print random words to real line 
           metrix2  =>  print 1st word and 2nd random word
           firing   =>  just look like firing the gun

                  
speed -->  speed is printf's animetion speed 
           defult speed is 3, and you can change it from (1 to 6)
           1 = Very Slow  
           2 =   Slow  
           3 =  Mediam
           4 =   Fast
           5 =   Fast+
           6 = Very Fast

           Ex. printf("hello world", speed=2)

                      
intervel -->  intervel is waiting time between printing 
              of two lines (intervel in second) 
              defult intervel is 2, you can set from 0 to grater
                  
              printf("hello world", "hii I am coder", intervel=2)
              >>> hello world 
              (Then wating time of intervel time in second)
              >>> hii I am coder

              Ex. printf("hello world", "hii I am coder", intervel=2)

                  
stay -->  after styl animetion whether you want the stream OR Not
          stay can be True or False, (defult stay = False)
          some type of styl removes printed stream after intervel 
          time. so if you don't want to remove printed streame 
          you can set stay == True, so printed line stay as it is
                  
          but some styles take action on stay 
          whether it is True OR False  
          Ex. ( typing , f2b,  b2f, metrix, metrix2 )

          prints("hello world", styl="headline", stay=True)\n\n""")
            
            for i in values:
                print(i)

        else:
            print("\n\n  >>>>>>>>>>  please enter name in ,styl=  from the list    <<<<<<<<<<<<<   ")
            print("[typing, headline, mid, f2b, b2f, gunshort, sniper, metrix, metrix2, firing, help]\n\n")
            for i in values:
                print(i)

        del values
