class Robot:
    snelheidsverandering_x = 1
    snelheidsverandering_y = 1
    def __init__(zelf, x=0, y=0, snelheid_x=5, snelheid_y=5, grootte_x=50, grootte_y=50):
       zelf.x = x
       zelf.y = y
       zelf.snelheid_x = snelheid_x
       zelf.snelheid_y = snelheid_y
       zelf.grootte_x = grootte_x
       zelf.grootte_y = grootte_y
    # simpele beweging
    def beweeg(zelf, richting=""):
        if "R" in list(richting):
            zelf.snelheid_x += snelheidsverandering_x
        if "L" in list(richting):
            zelf.snelheid_x -= snelheidsverandering_x
        if "O" in list(richting):
            zelf.snelheid_y += snelheidsverandering_y
        if "N" in list(richting):
            zelf.snelheid_y -= snelheidsverandering_y
        zelf.x += zelf.snelheid_x
        zelf.y += zelf.snelheid_y


