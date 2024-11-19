# import xml.etree.ElementTree as ET
import xmltodict
from pprint import pprint

xml = ""
with open("geogebra.xml", "r") as geogebra_xml_file:
    xml = geogebra_xml_file.read()


my_dict = xmltodict.parse(xml)["geogebra"]["construction"]

expressions = my_dict["expression"]
elements = my_dict["element"]
commands = my_dict["command"]

points = {}

c: int = 0
for element in elements:
    if element["@type"] == "point":
        name = element["@label"].lower()
        coords = element["coords"]
        if coords["@z"] == "1":
            c += 1
            x = coords["@x"]
            y = coords["@y"]
            points[name] = [x, y]

edge_case_polygons = []

triangles = {}

for command in commands:
    if command["@name"].lower() == "polygon":
        shape_name = str(command["output"]["@a0"])
        if not shape_name.startswith("t"):  # if not geogebra triangle
            edge_case_polygons.append(shape_name)
            continue
        print(shape_name, command["input"])
        shape_name = shape_name.lower()

        v1_name = command["input"]["@a0"].lower()
        v2_name = command["input"]["@a1"].lower()
        v3_name = command["input"]["@a2"].lower()

        # Map vertices to point
        v1 = points[v1_name]
        v2 = points[v2_name]
        v3 = points[v3_name]

        print([v1, v2, v3])
        # Triangle only

print(len(expressions), len(elements), len(commands))
print("Counted points: ", c)
print("Edge cases: ", edge_case_polygons)
