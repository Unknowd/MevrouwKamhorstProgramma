import tkinter

class Robot:
    id = 0
    kracht = 2500
    kleuren = ["white", "black", "red", "green", "blue", "cyan", "yellow", "magenta"]
    def __init__(zelf, x=0, y=0, kleur="black", snelheid_x=5, snelheid_y=5, grootte_x=50, grootte_y=50):
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
    def beweeg(zelf, richting=0):
        if richting & 1 == 1:
            zelf.snelheid_x += snelheidsverandering_x
        if richting & 2 == 2:
            zelf.snelheid_x -= snelheidsverandering_x
        if richting & 4 == 4:
            zelf.snelheid_y += snelheidsverandering_y
        if richting & 8 == 8:
            zelf.snelheid_y -= snelheidsverandering_y
        zelf.x += zelf.snelheid_x
        zelf.y += zelf.snelheid_y

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
    global robots
    def __init__(zelf):
        zelf.scherm = tkinter.Tk()
        zelf.scherm.title("Relativiteitstheorie")
        zelf.doek = Doek(zelf.scherm, width=x, height=y, bg="white", highlightthickness=0, border=0)
        zelf.doek.pack(fill=tkinter.BOTH, expand=tkinter.YES)
        zelf.teken(zelf.doek)
        zelf.scherm.mainloop()

    def teken(zelf, doek):
        ijkpunt = [speler.x + (speler.grootte_x / 2), speler.y - (speler.grootte_y / 2)]
        for robot in robots:
            doek.create_rectangle(robot.x + ((x / 2) - ijkpunt[0]), -robot.y + ((y / 2) + ijkpunt[1]), robot.x + ((x / 2) - ijkpunt[0]) + robot.grootte_x, -robot.y + ((y / 2) + ijkpunt[1]) + robot.grootte_y, fill = robot.kleur)

x = 800
y = 800
robots = [Robot(200, 100, "cyan"), Robot(600, 0, "red"), Robot(190, 0)]
speler = Speler(2)

def main():
    mijn_raam = Raam()

if __name__== "__main__":
    main()
