import csv
import json
from soup_creator import create_soup


class Persona5:
    def __init__(self):
        self.persona = []
        self.not_used = []
        self.soup = create_soup("https://megamitensei.fandom.com/wiki/List_of_Persona_5_Royal_Personas")

        arcana = self.soup('table', {'class': 'table p5'})
        arcana_l = len(arcana)

        for arc in range(arcana_l):
            pname = arcana[arc].findAll('a')
            pname_l = len(pname)
            for pn in range(pname_l):
                name = pname[pn].text
                if pname[pn].previous_element.previous_element.previous_element != '**':
                    self.persona.append(name)

        # Редачь персон, которые не подходят под ссылки
        # persona[persona.index("Jack-o'-Lantern")] = "Pyro_Jack"
        self.persona[self.persona.index("Phoenix")] = "Feng_Huang"
        self.persona[self.persona.index("Kushinada")] = "Kushinada-Hime"
        self.persona[self.persona.index("Seth")] = "Seth_(demon)"
        self.persona[self.persona.index("Messiah")] = "Messiah_(Persona)"
        self.persona[self.persona.index("Messiah Picaro")] = "Messiah_(Persona)"
        self.persona[self.persona.index("Kamu Susanoo")] = "Kamu_Susano-o"
        self.persona[self.persona.index("Vanadies")] = "Freya"
        self.persona.remove("Orpheus (F)")
        self.persona.remove("Freya")

        self.persona = [pers for pers in self.persona if "Picaro" not in pers]

    def parse_data(self, link):
        page_soup = create_soup(link)

        pers_name = link.split("/")[-1]

        origin = page_soup.find("div", {"data-source": "origin"})
        origin = origin.text if origin else "-"

        divs = []
        span = ""
        tables = {}

        ids = ["Persona_5_2", "Persona_5_|_Royal", "Persona_5_/_Royal", "Persona_5_Royal_2",
               "Persona_5_Royal", "Persona 5 Royal"]

        for id in ids:
            span = page_soup.find("span", attrs={"id": id})
            if span != None:
                h_tag = span.find_parent("h3")
                # Condition for Ippon-Datara
                if h_tag.find_parent("i"):
                    divs = h_tag.find_parent("i").next_sibling.find_all("div", attrs={"class": "tabbertab"})
                else:
                    divs = h_tag.next_sibling.next_sibling.find_all("div", attrs={"class": "tabbertab"})
                break
        # For Raoul and Cendrillon
        if span == None or divs == []:
            if pers_name == "Cendrillon":
                div = page_soup.find("div", attrs={"title": "Level 99"})
                table = div.find("table")
            else:
                table = page_soup.find("table", attrs={"style": "min-width:650px;text-align:center; "
                                                                "background: #222; border:2px solid #f41000; "
                                                                "border-radius:10px; font-size:75%; "
                                                                "font-family:verdana;"})
            tables[0] = table

        persona_names = ["Persona(P5R)", "Persona (P5R)", "Original ", "Royal Persona",
                         "Picaro ", "Picaro", "Female (Royal only) ", "Female Picaro (Royal only) ",
                         "Persona", "Royal", "Level 99 ", "Persona ", "Level 99", "Persona 5 Royal"]

        divs_len = [True for i in range(0, len(divs)) if len(divs[i].find_all("div")) > 20]
        if tables == {}:
            if divs_len == [] and pers_name != "Mercurius" or pers_name == "Berith":
                for div in divs:
                    title = div.get("title")
                    if title in persona_names:
                        table = div.find("table")
                        tables[title] = table
            else:
                for div in reversed(divs):
                    title = div.get("title")
                    if len(div.find_all("div")) > 20:
                        break
                    elif title in persona_names:
                        table = div.find("table")
                        tables[title] = table
                    if pers_name == "Mercurius":
                        break
        rows = []
        for title, table in tables.items():
            # Если это персона без характеристик, как Prometheus, Vanadies
            if pers_name == "Berith" and title == "Persona 5 Royal":
                self.not_used.append(link)
                continue
            elif title == "Persona" and len(tables) > 1 and pers_name != "Eligor" and pers_name != "Berith":
                self.not_used.append(link)
                continue
            lvl_arc_iter = -1
            try:
                lvl = table.findAll('table', {'class': 'customtable'})[0].findAll('td')[lvl_arc_iter].text.strip()
                if lvl == "Irritable" or lvl == "Inherited":
                    lvl_arc_iter -= 1
                    lvl = table.findAll('table', {'class': 'customtable'})[0].findAll('td')[lvl_arc_iter].text.strip()
                else:
                    lvl = int(lvl)
            except ValueError:
                self.not_used.append(link)
                continue
            except AttributeError:
                self.not_used.append(link)
                continue

            lvl_arc_iter -= 1
            arc = table.findAll('table', {'class': 'customtable'})[0].findAll('td')[lvl_arc_iter].text.strip()

            stat = []
            for j in range(0, 5):
                tmp = table.findAll('table', {'class': 'customtable'})[0].table.findAll('td')[3 * j + 1].text
                tmp = tmp.strip()
                if tmp == "--":
                    stat.append("-")
                else:
                    stat.append(int(tmp))

            elem = []
            for j in range(0, 6):
                tmp = table.findAll('table', {'class': 'customtable'})[1].findAll('td')[j].text
                tmp = tmp.strip()
                elem.append(tmp)

            skills = table.findAll('table', {'class': 'customtable'})[2].findAll('tr')[2:]
            skill_set = []
            for j in range(len(skills)):
                sp = {}
                try:
                    skill = list(filter(None, skills[j].text.split('\n')))
                    if 'S' in skill[3]:
                        skill[3] = None
                    elif skill[3] == 'Innate':
                        skill[3] = lvl
                    elif len(skill[3]) > 3:
                        skill[3] = str(skill[3])
                    else:
                        skill[3] = int(skill[3])
                    sp.update({'name': skill[0],
                               'level': skill[3]})
                    skill_set.append(sp)
                except IndexError:
                    continue

            skill_set = {'skills': skill_set}
            skill_set = json.dumps(skill_set)

            if "Picaro" in str(title):
                pers_name += " " + str(title)
            print(pers_name)
            rows.append([pers_name, origin, arc, lvl, stat[0], stat[1], stat[2], stat[3],
                         stat[4], elem[0], elem[1], elem[2],
                         elem[3], elem[4], elem[5], skill_set])
        return rows

    def write_to_csv(self):
        links = []
        for p in self.persona:
            links.append('https://megamitensei.fandom.com/wiki/' + p.replace(' ', '_'))

        headers = ['Name', 'Arcana', 'Base level', 'Strength', 'Magic', 'Endurance', 'Agility', 'Luck', 'Inherit',
                   'Reflects', 'Absorbs',
                   'Block', 'Resists', 'Weak', 'List of Skills']

        with open('persona5_original.csv', 'w', encoding='utf-8', newline='\n') as f:
            writer = csv.writer(f)
            writer.writerow(headers)
            for link in links:
                rows = self.parse_data(link)
                if type(rows) is list:
                    for row in rows:
                        writer.writerow(row)
                elif rows != 0:
                    writer.writerow(rows)
        f.close()
