class Robot:
    id = 0
    kracht = 2500
    def __init__(zelf, x=0, y=0, snelheid_x=5, snelheid_y=5, grootte_x=50, grootte_y=50, kleur="black"):
        zelf.x = x
        zelf.y = y
        zelf.snelheid_x = snelheid_x
        zelf.snelheid_y = snelheid_y
        zelf.grootte_x = grootte_x
        zelf.grootte_y = grootte_y
        zelf.snelheidsverandering = Robot.kracht / (zelf.grootte_x * zelf.grootte_y)
        zelf.kleur = kleur
        Robot.id += 1
        zelf.id = Robot.id
    # simpele beweging
    def beweeg(zelf, richting=""):
        if "R" in list(richting):
            zelf.snelheid_x += snelheidsverandering
        if "L" in list(richting):
            zelf.snelheid_x -= snelheidsverandering
        if "O" in list(richting):
            zelf.snelheid_y += snelheidsverandering
        if "N" in list(richting):
            zelf.snelheid_y -= snelheidsverandering
        zelf.x += zelf.snelheid_x
        zelf.y += zelf.snelheid_y
