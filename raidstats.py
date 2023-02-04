## TAKP Magelo Ripper 
## by Bakastabs

import sys
import datetime
import requests
from bs4 import BeautifulSoup

def main():
    print('Pulling Raid Data for:')

    #Get Current Date and Format
    dt = datetime.datetime.now()
    datestring = dt.strftime("%Y-%m-%d")
    print(datestring)

    #Specify Output File Names and Output Stream
    stats_filename = "raidstats_"+datestring+".txt"
    items_filename = "items.csv"
    original_stdout = sys.stdout # Save a reference to the original standard output

    #Declare Output Lists, URLs, Names and Items
    stats_output = []
    items_output = []

    URL = "https://www.takproject.net/magelo/character.php?char="
    AAURL = "https://www.takproject.net/magelo/aas.php?char="
    names = [
        "Scryll",
        "Scrylline",
        "Lulufoot",
        "Concreet",
        "Mcsteamy",
        "Malfroy",
        "Jung",
        "Bugg",
        "Bibimbap",
        "Twose",
        "Valerius",
        "Biggles",
        "Dibs",
        "Maddil",
        "Plaster",
        "Snoppen",
        "Flashed",
        "Ellasty",
        "Princcess",
        "Meatza",
        "Lorien",
        "Greenbean",
        "Mordrid",
        "Xarik",
        "Morbeas",
        "Deloyalp",
        "Loyal",
        "Deloyald",
        "Soulfire",
        "Succor",
        "Soothe",
        "Wildlord",
        "Dragonfire",
        "Ishaa",
        "Rarlok",
        "Portsn",
        "Milesgloriosus",
        "Masstransit",
        "Marrlowe",
        "Lanjar",
        "Dolk",
        "Ultimum",
        "Boreale",
        "Echus",
        "Brimuk",
        "Brimok",
        "Brimog",
        "Piktonku",
        "Pernille",
        "Bign",
        "Giliath",
        "Sren",
        "Kenuvas",
        "Rakmaz",
        "Kelfox",
        "Kelfas",
        "Kelfious",
        "Uflaks",
        "Nafse",
        "Codesia",
        "Cheesefire",
        "Daolian",
        "Shaolian",
        "Beastolian",
        "Picks",
        "Packs",
        "Pokes",
        "Almerich",
        "Alakron",
        "Almeriz",
        "Grelrok",
        "Grelix",
        "Grelwin",
        "Vizar",
        "Zeah",
        "Einaudi",
        "Field",
        "Jasmin",
        "Krex",
        "Troutt",
        "Sweetie",
        "Oprah",
        "Mina",
        "Burfoot",
        "Rast",
        "Tassle",
        "Lestar",
        "Late",
        "Boodoo",
        "Ganter",
        "Foppo",
        "Vaeldain",
        "Bisben",
        "Cisben",
        "Disben",
        "Kinya",
        "Kincla",
        "Hogz",
        "Hagz",
        "Cana",
        "Gildarts",
        "Mavis",
        "Behdet",
        "Tierra",
        "Estralla",
        "Zagio",
        "Zagiolita",
        "Zagpick",
        "Fulgu",
        "Dagmentar",
        "Nidal",
        "Darkz",
        "Dyneral",
        "Sdcaos",
        "Curapupas",
        "Batsirai",
        "Emnati",
        "Quentil",
        "Scythe",
        "Scythia",
        "Immothep"
    ]

    imp_items = [
    ]

    #Pull Data for Each Person

    for each in names:

        print("Pulling data for "+each)
        #Get Base Magelo Data
        page = requests.get(URL+each)
        soup = BeautifulSoup(page.content, "html.parser")
        try:
            pr = int(soup.find(class_="player-pr").text)
            mr = int(soup.find(class_="player-mr").text)
            dr = int(soup.find(class_="player-dr").text)
            fr = int(soup.find(class_="player-fr").text)
            cr = int(soup.find(class_="player-cr").text)
            avg_resist = round((pr+mr+dr+fr+cr)/5,2)
            
            #Create Base Character Output String
            line = each
            line = line + "," +  soup.find(class_="player-class").text
            line = line + "," +  soup.find(class_="player-hp").text
            line = line + "," +  soup.find(class_="player-mana").text
            line = line + "," +  soup.find(class_="player-ac").text
            line = line + "," +  soup.find(class_="player-atk").text
            line = line + "," +  str(pr)
            line = line + "," +  str(mr)
            line = line + "," +  str(dr)
            line = line + "," +  str(fr)
            line = line + "," +  str(cr)
            line = line + "," +  str(avg_resist)
            line = line + "," +  each
            
            #Begin items
            
            for item in soup.find_all(class_="ItemTitleMid"):
                #print (item)
                for compare in imp_items:
                  #print (compare)
                  #print (item.text)
                  if item.text==compare[0]:
                      #Item Match found add to Output
                      items_output.append([each,item.text,compare[1]])
                      #print ("Matched Item")

            #begin AA parse
            page = requests.get(AAURL+each)
            soup = BeautifulSoup(page.content, "html.parser")
            AApull = soup.find_all("tr")
            AApull.pop(0) #remove first item on list which is the Tab Listing
            AApull.pop(0) #remove second item on list which is the entire TR set

            #Deal with Output
            #init Output Vars
            clean_AAs = []
            spent_aa_total = 0
            unspent_aa_total = 0
            resist_aa_total = 0
            pr_aa_total = 0
            mr_aa_total = 0
            dr_aa_total = 0
            fr_aa_total = 0
            cr_aa_total = 0
            def_aa_total = 0
            mgb_flag = 0
            wood_paragon = 0
            radiant_cure = 0
            scm = 0
            scr = 0
            scrm = 0
            
            #generate clean AA list
            for row in AApull:
                cols = row.find_all("td")
                AAname = cols[0].text.strip()
                AAval = cols[1].text.strip()
                if (AAname != "AA Points:" and AAname != "Points Spent:"):
                    AAval = AAval.split("/",1)[0]
                    
                if AAname != "Title":
                    clean_AAs.append([AAname, AAval])
                    
            #find important AAs
            for each in clean_AAs:
                name = each[0]
                val = int(each[1])
                #ugly if statement for all resist AAs
                if (name == "Innate Fire Protection" or name == "Warding of Solusek"):
                    resist_aa_total = resist_aa_total + int(each[1])
                    fr_aa_total = fr_aa_total + int(each[1])
                                
                elif (name == "Innate Cold Protection" or name == "Blessing of E'ci"):
                    resist_aa_total = resist_aa_total + int(each[1])
                    cr_aa_total = cr_aa_total + int(each[1])

                elif (name == "Innate Magic Protection" or name == "Marr's Protection"):
                    resist_aa_total = resist_aa_total + int(each[1])
                    mr_aa_total = mr_aa_total + int(each[1])
              
                elif (name == "Innate Poison Protection" or name == "Shroud of The Faceless"):
                    resist_aa_total = resist_aa_total + int(each[1])
                    pr_aa_total = pr_aa_total + int(each[1])
               
                elif (name == "Innate Disease Protection" or name == "Bertoxxulous' Gift"):
                    resist_aa_total = resist_aa_total + int(each[1])
                    dr_aa_total = dr_aa_total + int(each[1])

                #check defensives
                elif (name == "Natural Durability" or name == "Combat Stability" or name == "Combat Agility" or name == "Physical Enhancement" or name == "Lightning Reflexes" or name == "Innate Defense" or name == "Planar Durability"):
                    def_aa_total = def_aa_total + val
                #check for mgb
                elif (name == "Mass Group Buff" and val == 1):
                    mgb_flag = 1
                #check wood/paragon
                elif (name == "Spirit of the Wood" or name == "Paragon of Spirit"):
                    wood_paragon = wood_paragon + val
                #check radiant cure
                elif name == "Radiant Cure":
                    radiant_cure = radiant_cure + val
                #check scm
                elif name == "Spell Casting Mastery":
                    scm = scm + val
                #check Spell Casting Reinforcement
                elif name == "Spell Casting Reinforcement":
                    scr = scr + val
                elif name == "Spell Casting Reinforcement Mastery":
                    scrm = scrm + val
                #find spent and unspent AAs
                elif each[0] == "AA Points:":
                    unspent_aa_total = int(each[1])
                elif each[0] == "Point Spent:":
                    spent_aa_total = int(each[1])

            ##Add AA Data to Output
            aa_grand_total = spent_aa_total + unspent_aa_total
            ##print("Spent AAs " + str(spent_aa_total))
            ##print("Unspent AAs " + str(unspent_aa_total))
            ##print("Total Resist AAs " + str(resist_aa_total))
            ##print("Total Fire AAs " + str(fr_aa_total))
            ##print("Total Cold AAs " + str(cr_aa_total))
            ##print("Total Magic AAs " + str(mr_aa_total))
            ##print("Total Poison AAs " + str(pr_aa_total))
            ##print("Total Disease AAs " + str(dr_aa_total))
            line = line + "," +  str(aa_grand_total)
            line = line + "," +  str(spent_aa_total)
            line = line + "," +  str(unspent_aa_total)
            line = line + "," +  str(resist_aa_total)
            line = line + "," +  str(def_aa_total)
            line = line + "," +  str(mgb_flag)
            line = line + "," +  str(wood_paragon)
            line = line + "," +  str(radiant_cure)
            line = line + "," +  str(scm)
            line = line + "," +  str(scr+scrm)

            #append line to output
            stats_output.append(line)
        except Exception as e:
            print(f"Couldn't process data for {each}. Error: {e}")

    #Output to Files
    with open(stats_filename, 'w') as f:
        sys.stdout = f # Change the standard output to the file we created.
        for x in stats_output:
                print(x)

    with open(items_filename, 'w') as f:
        sys.stdout = f # Change the standard output to the file we created.
        for each in items_output:
            print(each[0] + "," + each[1] + "," + each[2])

    sys.stdout = original_stdout # Reset the standard output to its original value

main()
