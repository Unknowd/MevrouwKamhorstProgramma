import tkinter
class Robot:
    id = 0
    kracht = 2500
    kleuren = ["white", "black", "red", "green", "blue", "cyan", "yellow", "magenta"]
    def __init__(zelf, x=0, y=0, snelheid_x=5, snelheid_y=5, grootte_x=50, grootte_y=50, kleur="black"):
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
    def __init__(zelf):
        zelf.scherm = tkinter.Tk()
        zelf.beeld = tkinter.Frame(zelf.scherm)
        zelf.beeld.pack(fill=tkinter.BOTH, expand=tkinter.YES)
        zelf.doek = Doek(zelf.beeld, width=800, height=800, bg="white", highlightthickness=0)
        zelf.doek.pack(fill=tkinter.BOTH, expand=tkinter.YES)
        zelf.scherm.mainloop()
        
def main():
    mijn_raam = Raam()

if __name__== "__main__":
    main()

robots = []
