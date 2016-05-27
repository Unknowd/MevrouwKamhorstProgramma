import tkinter, random, math

class Robot:
    # statische variable
    id = 0
    kracht = 2500
    kleuren = ["black", "red", "green", "blue", "cyan", "yellow", "magenta"]

    def __init__(zelf, x=0, y=0, kleur="black", bkleur="black", snelheid_x=random.randint(-10, 10),
                 snelheid_y=random.randint(-10, 10), grootte_x=50, grootte_y=50):
        zelf.x = x
        zelf.y = y
        zelf.snelheid_x = snelheid_x
        zelf.snelheid_y = snelheid_y
        zelf.grootte_x = grootte_x
        zelf.grootte_y = grootte_y
        zelf.snelheidsverandering = Robot.kracht / (zelf.grootte_x * zelf.grootte_y)
        zelf.kleur = kleur
        if zelf.kleur not in Robot.kleuren:
            zelf.kleur = Robot.kleuren[random.randint(0, len(Robot.kleuren) - 1)]
        Robot.kleuren.remove(zelf.kleur)
        zelf.bkleur = bkleur
        if zelf.bkleur not in Robot.kleuren:
            zelf.bkleur = zelf.kleur
        zelf.id = Robot.id
        Robot.id += 1

    def __del__(zelf):
        print(zelf.kleur)
        Robot.kleuren.append(zelf.kleur)

    def beweeg(zelf):
        zelf.x += zelf.snelheid_x
        zelf.y += zelf.snelheid_y

    def teken(zelf, doek):
        if zelf.x > doek.breedte:
            zelf.x = 0
        elif zelf.x < 0:
            zelf.x = doek.breedte
        if zelf.y > doek.hoogte:
            zelf.y = 0
        elif zelf.y < 0:
            zelf.y = doek.hoogte
        doek.create_rectangle(zelf.x, zelf.y, zelf.x + zelf.grootte_x, zelf.y + zelf.grootte_y,
                              fill=zelf.kleur, outline=zelf.bkleur, width=zelf.grootte_x // 10)
        doek.create_rectangle(zelf.x - doek.breedte, zelf.y, zelf.x + zelf.grootte_x - doek.breedte,
                              zelf.y + zelf.grootte_y, fill=zelf.kleur, outline=zelf.bkleur,
                              width=zelf.grootte_x // 10)
        doek.create_rectangle(zelf.x, zelf.y - doek.hoogte, zelf.x + zelf.grootte_x,
                              zelf.y + zelf.grootte_y - doek.hoogte, fill=zelf.kleur, outline=zelf.bkleur,
                              width=zelf.grootte_x // 10)
        doek.create_rectangle(zelf.x - doek.breedte, zelf.y - doek.hoogte,
                              zelf.x + zelf.grootte_x - doek.breedte, zelf.y + zelf.grootte_y - doek.hoogte,
                              fill=zelf.kleur, outline=zelf.bkleur, width=zelf.grootte_x // 10)

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

    def bij_hergroting(zelf, event):
        zelf.breedte = event.width
        zelf.hoogte = event.height
        zelf.config(width=zelf.breedte, height=zelf.hoogte)

    def ververs(zelf, robots, speler, informatieweergeven):
        zelf.delete('all')
        for i in robots:
            i.teken(zelf)
        if informatieweergeven:
            zelf.create_text(5, 0, text = "Snelheden:", fill = "black", font = "-size 30", anchor="nw")
            positieteller = 0
            for robot in robots:
                zelf.create_text(5, positieteller*40+40, text=robot.kleur[0].upper() + robot.kleur[1:] + ": " + str(round(math.sqrt((speler.snelheid_x - robot.snelheid_x) ** 2 + (speler.snelheid_y - robot.snelheid_y) ** 2))), fill=robot.kleur, font="-size 30", anchor="nw")
                positieteller += 1

    def reposition(zelf, robot, x, y):
        robot.x -= x
        robot.y -= y

    def vind_robot(zelf, robots, x, y):
        for robot in robots[::-1]:
            if robot.x <= x and robot.y <= y and robot.x + robot.grootte_x >= x and robot.y + robot.grootte_y >= y:
                return robot
            if robot.x - zelf.breedte <= x and robot.y <= y and robot.x + robot.grootte_x - zelf.breedte >= x and robot.y + robot.grootte_y >= y:
                return robot
            if robot.x <= x and robot.y - zelf.hoogte <= y and robot.x + robot.grootte_x >= x and robot.y + robot.grootte_y - zelf.hoogte >= y:
                return robot
            if robot.x - zelf.breedte <= x and robot.y - zelf.hoogte <= y and robot.x + robot.grootte_x - zelf.breedte >= x and robot.y + robot.grootte_y - zelf.hoogte >= y:
                return robot
        return False

class Raam:
    def __init__(zelf):
        zelf.informatieweergeven = False
        zelf.pressed = {}
        zelf.scherm = tkinter.Tk()
        zelf.scherm.title("Relativiteitstheorie")
        x = zelf.scherm.winfo_screenwidth() // 2
        y = zelf.scherm.winfo_screenheight() // 2
        zelf.scherm.geometry("{0}x{1}+{2}+{3}".format(x, y, x - x // 2, y - y // 2))
        zelf.doek = Doek(zelf.scherm, bg="white", highlightthickness=0, border=0)
        zelf.doek.pack(fill=tkinter.BOTH, expand=tkinter.YES)
        zelf.robots = [Robot(random.randint(0, x), random.randint(0, y), snelheid_x=random.randint(-10, 10),
                             snelheid_y=random.randint(-10, 10)),
                       Robot(random.randint(0, x), random.randint(0, y), snelheid_x=random.randint(-10, 10),
                             snelheid_y=random.randint(-10, 10))]
        zelf.speler = Speler(zelf.robots[0])
        zelf.state = False
        zelf._set_bindings()
        zelf.scherm.after(20, zelf.uitvoeren)

    def _set_bindings(zelf):
        zelf.scherm.bind("<Button-1>", zelf._leftclick)
        zelf.scherm.bind("<Button-2>", zelf._scrollclick)
        zelf.scherm.bind("<F11>", zelf._toggle_volledigscherm)
        zelf.scherm.bind("<KeyPress-r>", zelf.maak_nieuwe_robot)
        zelf.scherm.bind("<KeyPress-i>", zelf.toon_info)
        for char in ["w", "a", "s", "d"]:
            zelf.scherm.bind("<KeyPress-%s>" % char, zelf._pressed)
            zelf.scherm.bind("<KeyRelease-%s>" % char, zelf._released)
            zelf.pressed[char] = False

    def _toggle_volledigscherm(zelf, event):
        zelf.state = not zelf.state
        zelf.scherm.attributes("-fullscreen", zelf.state)

    def _leftclick(zelf, event):
        robot = zelf.doek.vind_robot(zelf.robots, event.x, event.y)
        if robot:
            zelf.speler = Speler(robot)

    def _scrollclick(zelf, event):
        robot = zelf.doek.vind_robot(zelf.robots, event.x, event.y)
        if robot and robot.id != zelf.speler.id:
            del zelf.robots[zelf.robots.index(robot)]

    def _pressed(zelf, event):
        zelf.pressed[event.char] = True

    def _released(zelf, event):
        zelf.pressed[event.char] = False

    def maak_nieuwe_robot(zelf, event):
        if len(Robot.kleuren) != 0:
            zelf.robots.append(Robot(50, 50, snelheid_x=random.randint(-10, 10), snelheid_y=random.randint(-10, 10)))

    def toon_info(zelf, event):
        zelf.informatieweergeven = not zelf.informatieweergeven
    
    def hergroepeer(zelf):
        x, y = zelf.speler.x - zelf.doek.breedte//2, zelf.speler.y - zelf.doek.hoogte//2
        for robot in zelf.robots:
            zelf.doek.reposition(robot, x, y)
        
    def uitvoeren(zelf):
        s = zelf.speler
        s.ververs_snelheid(zelf.pressed)
        for i in zelf.robots:
            i.beweeg()
        zelf.hergroepeer()
        zelf.doek.ververs(zelf.robots, s, zelf.informatieweergeven)
        zelf.scherm.after(20, zelf.uitvoeren)

def main():
    mijn_raam = Raam()
    mijn_raam.scherm.mainloop()

if __name__ == "__main__":
    main()
