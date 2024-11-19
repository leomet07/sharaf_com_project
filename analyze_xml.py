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
    )  # Centroid is COM # Spreads [v1, v2, v3] into v1, v2, v3 params
    area = calculate_area_of_triangle(*triangle)
    sum_of_all_areas += area
    sum_of_all_centroid_x_times_area += centroid[0] * area
    sum_of_all_centroid_y_times_area += centroid[1] * area


# Manually add edge cases
# Semi circle 1 (sadness head)
sum_of_all_areas += 1.875028225
sum_of_all_centroid_x_times_area += 3.3621215 * 1.875028225
sum_of_all_centroid_y_times_area += 0.3937850313 * 1.875028225
# circle 1 (fear left eye, id)
sum_of_all_areas += 0.2043799831
sum_of_all_centroid_x_times_area += 0.2550611087 * 0.2043799831
sum_of_all_centroid_y_times_area += 1.01771365 * 0.2043799831
# circle 2 (fear right eye, id)
sum_of_all_areas += 0.2141552227
sum_of_all_centroid_x_times_area += 0.2610894953 * 0.2141552227
sum_of_all_centroid_y_times_area += 1.306968692 * 0.2141552227

# Disgust head
disgust_center = [-1.7852387940488, 0.6450660095549]
disgust_point_on_circumference = [-2.2835886135613, 1.2037805304659]
disgust_radius = get_dist(disgust_center, disgust_point_on_circumference)
disgust_area = math.pi * math.pow(disgust_radius, 2)
sum_of_all_areas += disgust_area
sum_of_all_centroid_x_times_area += disgust_center[0] * disgust_area
sum_of_all_centroid_y_times_area += disgust_center[1] * disgust_area

# Joy Head
joy_center = [0.0098426979343, 1.5207934851762]
joy_point_on_circumference = [0.4204548060243, 0.8437203282265]
joy_radius = get_dist(joy_center, joy_point_on_circumference)
joy_area = math.pi * math.pow(joy_radius, 2)
sum_of_all_areas += joy_area
sum_of_all_centroid_x_times_area += joy_center[0] * joy_area
sum_of_all_centroid_y_times_area += joy_center[1] * joy_area

com_x = sum_of_all_centroid_x_times_area / sum_of_all_areas
com_y = sum_of_all_centroid_y_times_area / sum_of_all_areas
print([com_x, com_y])

print(len(expressions), len(elements), len(commands))
print("Counted points: ", c)
print("Edge cases: ", edge_case_polygons)

# print("Tests: ")
# print(calculate_area_of_triangle([0, 0], [5, 0], [0, 5]))
# print(caclulate_centroid_of_triangle([0, 0], [5, 0], [0, 5]))
