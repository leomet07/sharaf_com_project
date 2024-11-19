# import xml.etree.ElementTree as ET
import xmltodict
from pprint import pprint
import math

xml = ""
with open("geogebra.xml", "r") as geogebra_xml_file:
    xml = geogebra_xml_file.read()


def convert_vertex_to_float(v_str):
    return [float(v_str[0]), float(v_str[1])]


def caclulate_centroid_of_triangle(v1, v2, v3):
    x_c = (v1[0] + v2[0] + v3[0]) / 3.0
    y_c = (v1[1] + v2[1] + v3[1]) / 3.0
    return [x_c, y_c]


def get_dist(v1, v2):
    return math.sqrt(math.pow(v1[0] - v2[0], 2) + math.pow(v1[1] - v2[1], 2))


def calculate_area_of_triangle(v1, v2, v3):
    s1 = get_dist(v1, v2)
    s2 = get_dist(v2, v3)
    s3 = get_dist(v1, v3)
    perimeter = s1 + s2 + s3
    semiperimeter = perimeter / 2.0
    return math.sqrt(
        semiperimeter
        * (semiperimeter - s1)
        * (semiperimeter - s2)
        * (semiperimeter - s3)
    )


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
        v1 = convert_vertex_to_float(points[v1_name])
        v2 = convert_vertex_to_float(points[v2_name])
        v3 = convert_vertex_to_float(points[v3_name])

        triangles[shape_name] = [v1, v2, v3]
        # Triangle only

sum_of_all_centroid_x_times_area = 0
sum_of_all_centroid_y_times_area = 0
sum_of_all_areas = 0

for triangle_name in triangles:
    triangle = triangles[triangle_name]
    centroid = caclulate_centroid_of_triangle(
        *triangle
    )  # Spreads [v1, v2, v3] into v1, v2, v3 params
    area = calculate_area_of_triangle(*triangle)
    sum_of_all_areas += area
    sum_of_all_centroid_x_times_area += centroid[0] * area
    sum_of_all_centroid_y_times_area += centroid[1] * area

com_x = sum_of_all_centroid_x_times_area / sum_of_all_areas
com_y = sum_of_all_centroid_y_times_area / sum_of_all_areas
print([com_x, com_y])

print(len(expressions), len(elements), len(commands))
print("Counted points: ", c)
print("Edge cases: ", edge_case_polygons)

# print("Tests: ")
# print(calculate_area_of_triangle([0, 0], [5, 0], [0, 5]))
# print(caclulate_centroid_of_triangle([0, 0], [5, 0], [0, 5]))
