#!/usr/bin/env python
import tkinter, random, math

__author__ = "Pim and Sven"
__status__ = "Development"
__maintainer__ = "Pim and Sven"
__credits__ = ["Pim", "Sven", "Pieter Schutz"]
__copyright__ = "Copyright 2016, Pim and Sven"
__license__ = "GNU GPL"

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

class Robot:
    # statische variable
    kracht = 2500
    
    id = 0
    kleuren = {"black", "red", "green", "blue", "cyan", "yellow", "magenta"}

    def __init__(zelf, x=0, y=0, kleur="", snelheid_x=None,
                 snelheid_y=None, grootte_x=50, grootte_y=50):
        if snelheid_x == None:
            snelheid_x = random.random()*4-2
        if snelheid_y == None:
            snelheid_y = random.random()*4-2
        zelf.x = x
        zelf.y = y
        zelf.snelheid_x = snelheid_x
        zelf.snelheid_y = snelheid_y
        zelf.grootte_x = grootte_x
        zelf.grootte_y = grootte_y
        zelf.toon_snelheid = False
        zelf.snelheidsverandering = Robot.kracht / (zelf.grootte_x * zelf.grootte_y)
        zelf.kleur = kleur
        if zelf.kleur not in Robot.kleuren:
            zelf.kleur = Robot.kleuren.pop()
        else:
            Robot.kleuren.remove(zelf.kleur)
        zelf.id = Robot.id
        Robot.id += 1

    def __del__(zelf):
        Robot.kleuren.add(zelf.kleur)
    
    def beweeg(zelf):
        zelf.x += zelf.snelheid_x
        zelf.y += zelf.snelheid_y

    def teken(zelf, doek, speler):
        if zelf.x > doek.breedte:
            zelf.x = 0
        elif zelf.x < 0:
            zelf.x = doek.breedte
        if zelf.y > doek.hoogte:
            zelf.y = 0
        elif zelf.y < 0:
            zelf.y = doek.hoogte
        doek.create_rectangle(zelf.x, zelf.y, zelf.x + zelf.grootte_x, zelf.y + zelf.grootte_y,
                              fill=zelf.kleur, outline=zelf.kleur)
        doek.create_rectangle(zelf.x - doek.breedte, zelf.y, zelf.x + zelf.grootte_x - doek.breedte,
                              zelf.y + zelf.grootte_y, fill=zelf.kleur, outline=zelf.kleur)
        doek.create_rectangle(zelf.x, zelf.y - doek.hoogte, zelf.x + zelf.grootte_x,
                              zelf.y + zelf.grootte_y - doek.hoogte, fill=zelf.kleur, outline=zelf.kleur)
        doek.create_rectangle(zelf.x - doek.breedte, zelf.y - doek.hoogte,
                              zelf.x + zelf.grootte_x - doek.breedte, zelf.y + zelf.grootte_y - doek.hoogte,
                              fill=zelf.kleur, outline=zelf.kleur)
        if zelf.toon_snelheid:
            doek.create_text(zelf.x, zelf.y, fill=zelf.kleur, text=format(math.sqrt((speler.snelheid_x - zelf.snelheid_x) ** 2 + (speler.snelheid_y - zelf.snelheid_y) ** 2), '.2f'), font='-size 20', anchor="sw")
            doek.create_text(zelf.x - doek.breedte, zelf.y, fill=zelf.kleur, text=format(math.sqrt((speler.snelheid_x - zelf.snelheid_x) ** 2 + (speler.snelheid_y - zelf.snelheid_y) ** 2), '.2f'), font='-size 20', anchor="sw")

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
            i.teken(zelf, speler)
        if informatieweergeven:
            zelf.create_text(5, 0, text = "Snelheden:", fill = "black", font = "-size 30", anchor="nw")
            positieteller = 0
            for robot in robots:
                zelf.create_text(5, positieteller*40+40, text=robot.kleur[0].upper() + robot.kleur[1:] + ": " + format(math.sqrt((speler.snelheid_x - robot.snelheid_x) ** 2 + (speler.snelheid_y - robot.snelheid_y) ** 2), '.2f'), fill=robot.kleur, font="-size 30", anchor="nw")
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
        zelf.robots = [Robot(random.randint(0, x), random.randint(0, y)),
                       Robot(random.randint(0, x), random.randint(0, y))]
        zelf.speler = zelf.robots[0]
        zelf.state = False
        zelf._set_bindings()
        zelf.scherm.after(20, zelf.uitvoeren)

    def _set_bindings(zelf):
        zelf.scherm.bind("<Button-1>", zelf._leftclick)
        zelf.scherm.bind("<Button-2>", zelf._scrollclick)
        zelf.scherm.bind("<Button-3>", zelf._rightclick)
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
            zelf.speler = robot

    def _scrollclick(zelf, event):
        robot = zelf.doek.vind_robot(zelf.robots, event.x, event.y)
        if robot and robot.id != zelf.speler.id:
            del zelf.robots[zelf.robots.index(robot)]

    def _rightclick(zelf, event):
        robot = zelf.doek.vind_robot(zelf.robots, event.x, event.y)
        if robot:
            robot.toon_snelheid = not robot.toon_snelheid
        
    def _pressed(zelf, event):
        zelf.pressed[event.char] = True

    def _released(zelf, event):
        zelf.pressed[event.char] = False

    def maak_nieuwe_robot(zelf, event):
        if len(Robot.kleuren) is not 0:
            zelf.robots.append(Robot(random.randint(0, zelf.doek.breedte), random.randint(0, zelf.doek.hoogte)))

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
