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
        richting = 0
        if zelf.id != speler.id:
            richting = random.randint(0, 15)
        else:
            if raam.pressed["w"]: richting += 4
            if raam.pressed["a"]: richting += 2
            if raam.pressed["s"]: richting += 8
            if raam.pressed["d"]: richting += 1
        if richting & 1 == 1:
            zelf.snelheid_x += zelf.snelheidsverandering
        if richting & 2 == 2:
            zelf.snelheid_x -= zelf.snelheidsverandering
        if richting & 4 == 4:
            zelf.snelheid_y += zelf.snelheidsverandering
        if richting & 8 == 8:
            zelf.snelheid_y -= zelf.snelheidsverandering
        zelf.x += zelf.snelheid_x
        zelf.y += zelf.snelheid_y
    def teken(zelf, doek, ijkpunt):
        doek.create_rectangle(zelf.x + ((x / 2) - ijkpunt[0]), -zelf.y + ((y / 2) + ijkpunt[1]), zelf.x + ((x / 2) - ijkpunt[0]) + zelf.grootte_x, -zelf.y + ((y / 2) + ijkpunt[1]) + zelf.grootte_y, fill = zelf.kleur)

class Speler():
    def __init__(zelf, robotid):
        for robot in robots:
            if robot.id == robotid:
                zelf.__class__ = Robot
                zelf.__dict__ = robot.__dict__
        
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

class Raam:
    def __init__(zelf):
        zelf.pressed = {}
        zelf.scherm = tkinter.Tk()
        zelf.scherm.title("Relativiteitstheorie")
        zelf.doek = Doek(zelf.scherm, width=x, height=y, bg="white", highlightthickness=0, border=0)
        zelf.doek.pack(fill=tkinter.BOTH, expand=tkinter.YES)
        zelf._set_bindings()
        zelf.teken(zelf.doek)
        zelf.doek.mainloop()
        zelf.scherm.mainloop()

    def _set_bindings(zelf):
        for char in ["w", 'a', 's', 'd']:
            zelf.scherm.bind("<KeyPress-%s>" % char, zelf._pressed)
            zelf.scherm.bind("<KeyRelease-%s>" % char, zelf._released)
            zelf.pressed[char] = False

    def _pressed(zelf, event):
        zelf.pressed[event.char] = True

    def _released(zelf, event):
        zelf.pressed[event.char] = False

    def teken(zelf, doek):
        zelf.doek.delete("all")
        for robot in robots:
            robot.beweeg(zelf)
        ijkpunt = [speler.x + (speler.grootte_x / 2), speler.y - (speler.grootte_y / 2)]
        for robot in robots:
            robot.teken(doek, ijkpunt)
        zelf.doek.after(20, zelf.teken, doek)

x = 800
y = 800
robots = [Robot(200, 100, "cyan", 200, 200), Robot(600, 0, "red"), Robot(190, 0)]
speler = Speler(2)

def main():
    mijn_raam = Raam()

if __name__== "__main__":
    main()
