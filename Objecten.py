import tkinter, random

class Robot:
    # statische variable
    id = 0
    kracht = 2500
    kleuren = ["black", "red", "green", "blue", "cyan", "yellow", "magenta"]

    def __init__(zelf, x=0, y=0, kleur="black", bkleur="black", ckleur="black", snelheid_x=5, snelheid_y=5, grootte_x=50, grootte_y=50):
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
        zelf.bkleur = bkleur
        if zelf.bkleur not in Robot.kleuren:
            zelf.bkleur = "black"
        zelf.ckleur = ckleur
        if zelf.ckleur not in Robot.kleuren:
            zelf.ckleur = "black"
        Robot.id += 1
        zelf.id = Robot.id
 
    def beweeg(zelf):
        zelf.x += zelf.snelheid_x
        zelf.y += zelf.snelheid_y
        
    def teken(zelf, doek, x, y):
        doek.create_rectangle(zelf.x - x, zelf.y - y , zelf.x + zelf.grootte_x - x, zelf.y + zelf.grootte_y - y, fill = zelf.kleur, outline = zelf.bkleur, width = zelf.grootte_x//10)
        doek.create_oval(zelf.x - x, zelf.y - y, zelf.x + zelf.grootte_x - x, zelf.y + zelf.grootte_y - y, fill = zelf.kleur, outline = zelf.ckleur, width = zelf.grootte_x//10)
        
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
            if robot.x <= x and robot.y >= y and robot.x + robot.grootte_x >= x and robot.y - robot.grootte_y <= y:
                return robot
        return False
            
class Raam:
    def __init__(zelf):
        zelf.pressed = {}
        zelf.scherm = tkinter.Tk()
        zelf.scherm.title("Relativiteitstheorie")
        x = zelf.scherm.winfo_screenwidth()//2
        y = zelf.scherm.winfo_screenheight()//2
        zelf.scherm.geometry("{0}x{1}+{2}+{3}".format(x, y, x - x//2, y - y//2))
        zelf.doek = Doek(zelf.scherm, bg="white", highlightthickness=0, border=0)
        zelf.doek.pack(fill=tkinter.BOTH, expand=tkinter.YES)
        zelf.robots = [Robot(10, 10, kleur = "cyan", bkleur = "green", ckleur = "blue"), Robot(50,50)]
        zelf.speler = Speler(zelf.robots[0])
        zelf.state = False
        zelf._set_bindings()
        zelf.uitvoeren()

    def _set_bindings(zelf):
        zelf.scherm.bind("<Button-1>", zelf._click)
        zelf.scherm.bind("<F11>", zelf._toggle_volledigscherm)
        for char in ["w", 'a', 's', 'd']:
            zelf.scherm.bind("<KeyPress-%s>" % char, zelf._pressed)
            zelf.scherm.bind("<KeyRelease-%s>" % char, zelf._released)
            zelf.pressed[char] = False

    def _toggle_volledigscherm(zelf, event):
        zelf.state = not zelf.state
        zelf.scherm.attributes("-fullscreen", zelf.state)
        
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
        
    def uitvoeren(zelf):
        s = zelf.speler
        x, y = s.x + (s.grootte_x // 2), s.y + (s.grootte_y // 2)
        s.ververs_snelheid(zelf.pressed)
        for i in zelf.robots:
            i.beweeg()
        zelf.hergroepeer()
        zelf.doek.ververs(zelf.robots, x, y)
        zelf.scherm.after(20, zelf.uitvoeren)

def main():
    mijn_raam = Raam()

if __name__== "__main__":
    main()
