import tkinter, random

class Robot:
    id = 0
    kracht = 2500
    kleuren = ["white", "black", "red", "green", "blue", "cyan", "yellow", "magenta"]
    def __init__(zelf, x=0, y=0, kleur="black", grootte_x=50, grootte_y=50, snelheid_x=0, snelheid_y=0):
        zelf.x = x
        zelf.y = y
        zelf.snelheid_x = snelheid_x
        zelf.snelheid_y = snelheid_y
        zelf.grootte_x = grootte_x
        zelf.grootte_y = grootte_y
        zelf.snelheidsverandering = Robot.kracht / (zelf.grootte_x * zelf.grootte_y)
        zelf.kleur = kleur
        if zelf.kleur not in Robot.kleuren:
            zelf.kleur = "black"
        Robot.id += 1
        zelf.id = Robot.id
    # simpele beweging
    def beweeg(zelf, raam):
        global speler
        if raam.pressed["d"]:
            zelf.snelheid_x += zelf.snelheidsverandering
        if raam.pressed["a"]:
            zelf.snelheid_x -= zelf.snelheidsverandering
        if raam.pressed["s"]:
            zelf.snelheid_y += zelf.snelheidsverandering
        if raam.pressed["w"]:
            zelf.snelheid_y -= zelf.snelheidsverandering
        zelf.x += zelf.snelheid_x
        zelf.y += zelf.snelheid_y
        
    def teken(zelf, doek, x, y):
        doek.create_rectangle(zelf.x - x, zelf.y - y , zelf.x + zelf.grootte_x - x, zelf.y + zelf.grootte_y - y, fill = zelf.kleur)
        
class Doek(tkinter.Canvas):
    def __init__(zelf, ouder, **kwargs):
        tkinter.Canvas.__init__(zelf, ouder, **kwargs)
        zelf.bind("<Configure>", zelf.bij_hergroting)
        zelf.hoogte = zelf.winfo_reqheight()
        zelf.breedte = zelf.winfo_reqwidth()

    def bij_hergroting(zelf,event):
        zelf.breedte = event.width
        zelf.hoogte = event.height
        zelf.config(width=zelf.breedte, height=zelf.hoogte)

    def ververs(zelf, objecten, x, y):
        zelf.delete('all')
        x -= zelf.breedte//2
        y -= zelf.hoogte//2
        for i in objecten:
            i.teken(zelf)
            
class Raam:
    def __init__(zelf):
        zelf.pressed = {}
        zelf.scherm = tkinter.Tk()
        zelf.scherm.title("Relativiteitstheorie")
        zelf.doek = Doek(zelf.scherm, width=800, height=800, bg="white", highlightthickness=0, border=0)
        zelf.doek.pack(fill=tkinter.BOTH, expand=tkinter.YES)
        zelf.robots = []
        zelf._set_bindings()
        zelf.teken()

    def _set_bindings(zelf):
        for char in ["w", 'a', 's', 'd']:
            zelf.scherm.bind("<KeyPress-%s>" % char, zelf._pressed)
            zelf.scherm.bind("<KeyRelease-%s>" % char, zelf._released)
            zelf.pressed[char] = False

    def _pressed(zelf, event):
        zelf.pressed[event.char] = True

    def _released(zelf, event):
        zelf.pressed[event.char] = False

    def teken(zelf):
        x, y = int(speler.x + (speler.grootte_x / 2)), int(speler.y - (speler.grootte_y / 2))
        zelf.doek.ververs(zelf.robots, x, y)
        zelf.after(20, zelf.teken)

def main():
    mijn_raam = Raam()

if __name__== "__main__":
    main()
