def pointInHitbox(point, element):
    if (point[0] >= element.x and
            point[0] <= (element.x + element.width) and
            point[1] >= element.y and
            point[1] <= (element.y + element.height)):
        return True
    return False


def collide(element1, element2):
    if True in [pointInHitbox(point, element2)
                for point in element1.getPoints()]:
        return True
    return False
