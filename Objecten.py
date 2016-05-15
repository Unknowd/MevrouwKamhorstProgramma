import tkinter, random

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
    def beweeg(zelf):
        zelf.x += zelf.snelheid_x
        zelf.y += zelf.snelheid_y
        
    def teken(zelf, doek, x, y):
        doek.create_rectangle(zelf.x - x, zelf.y - y , zelf.x + zelf.grootte_x - x, zelf.y + zelf.grootte_y - y, fill = zelf.kleur)

class Speler(Robot):
    def __init__(zelf, robot):
        zelf.__dict__ = robot.__dict__

    def ververs_snelheid(zelf, l):
        if l["d"]:
            zelf.snelheid_x += zelf.snelheidsverandering
        if l["a"]:
            zelf.snelheid_x -= zelf.snelheidsverandering
        if l["s"]:
            zelf.snelheid_y += zelf.snelheidsverandering
        if l["w"]:
            zelf.snelheid_y -= zelf.snelheidsverandering

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
            i.teken(zelf, x, y)

    def far_away(zelf, robot, x, y):
        robot.x -= x
        robot.y -= y
        return abs(robot.x) > 4 * zelf.breedte or abs(robot.y) > 4 * zelf.hoogte

    def vind_robot(zelf, robots, x, y):
        for robot in robots:
            if robot.x <= x and robot.y <= y and robot.x + robot.grootte_x >= x and robot.y + robot.grootte_y >= y:
                print("happend")
                return robot
        return False
            
class Raam:
    def __init__(zelf):
        zelf.pressed = {}
        zelf.scherm = tkinter.Tk()
        zelf.scherm.title("Relativiteitstheorie")
        zelf.doek = Doek(zelf.scherm, width=800, height=800, bg="white", highlightthickness=0, border=0)
        zelf.doek.pack(fill=tkinter.BOTH, expand=tkinter.YES)
        zelf.robots = [Robot(10, 10), Robot(50,50)]
        zelf.speler = Speler(zelf.robots[0])
        zelf._set_bindings()
        zelf.teken()

    def _set_bindings(zelf):
        zelf.scherm.bind("<Button-1>", zelf._click)
        for char in ["w", 'a', 's', 'd']:
            zelf.scherm.bind("<KeyPress-%s>" % char, zelf._pressed)
            zelf.scherm.bind("<KeyRelease-%s>" % char, zelf._released)
            zelf.pressed[char] = False
            
    def _click(zelf, event):
        robot = zelf.doek.vind_robot(zelf.robots, event.x, event.y)
        if robot:
            zelf.speler = Speler(robot)
                
    def _pressed(zelf, event):
        zelf.pressed[event.char] = True

    def _released(zelf, event):
        zelf.pressed[event.char] = False

    def hergroepeer(zelf):
        x, y = zelf.speler.x - zelf.doek.breedte//2 + zelf.speler.grootte_x//2, zelf.speler.y - zelf.doek.hoogte//2 - zelf.speler.grootte_y//2
        zelf.robots = [robot for robot in zelf.robots if not zelf.doek.far_away(robot, x, y)]
        
    def teken(zelf):
        s = zelf.speler
        x, y = s.x + (s.grootte_x // 2), s.y - (s.grootte_y // 2)
        s.ververs_snelheid(zelf.pressed)
        for i in zelf.robots:
            i.beweeg()
        zelf.doek.ververs(zelf.robots, x, y)
        zelf.hergroepeer()
        zelf.scherm.after(20, zelf.teken)

def main():
    mijn_raam = Raam()

if __name__== "__main__":
    main()
