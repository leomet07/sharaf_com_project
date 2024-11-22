import xmltodict
from pprint import pprint
import math
import cv2
import numpy as np
from datetime import datetime
import os

if not os.path.exists("canvas_saves"):
    os.mkdir("canvas_saves")

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
semi_circle_x_com = 3.3621215
semi_circle_y_com = 0.3937850313
semi_circle_area = 1.875028225
sum_of_all_areas += semi_circle_area
sum_of_all_centroid_x_times_area += semi_circle_x_com * semi_circle_area
sum_of_all_centroid_y_times_area += semi_circle_y_com * semi_circle_area

# circle 1 (fear left eye, id)
fear_one_eye_center = (1.4999141151656, 1.3069686921559)
fear_one_eye_radius = 0.25506110867556045527
fear_one_eye_area = math.pi * math.pow(fear_one_eye_radius, 2)
sum_of_all_areas += fear_one_eye_area
sum_of_all_centroid_x_times_area += fear_one_eye_center[0] * fear_one_eye_radius
sum_of_all_centroid_y_times_area += fear_one_eye_center[1] * fear_one_eye_radius

# circle 2 (fear right eye, id)
fear_two_eye_center = (1.8822820372248, 1.0224210568007)
fear_two_eye_radius = 0.25108949531396575204
fear_two_eye_area = math.pi * math.pow(fear_two_eye_radius, 2)
sum_of_all_areas += fear_two_eye_area
sum_of_all_centroid_x_times_area += fear_two_eye_center[0] * fear_two_eye_radius
sum_of_all_centroid_y_times_area += fear_two_eye_center[1] * fear_two_eye_radius

# Disgust head
disgust_center = [-1.7852387940488, 0.6450660095549]
disgust_point_on_circumference = (-1.2611887819923, 0.1779779553355)
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
print("COM: ", [round(com_x, 4), round(com_y, 4)])
print("Total area: ", round(sum_of_all_areas, 4))
print("Known points: ", c)
print("Edge cases: ", edge_case_polygons)

# EVERYTHING BELOW IS JUST THE SCALE DIAGRAM CREATION/ OUTPUT FILE CREATION
# -------------------------------------------------------------------------------------
# -------------------------------------------------------------------------------------
# -------------------------------------------------------------------------------------
# -------------------------------------------------------------------------------------
# -------------------------------------------------------------------------------------
# -------------------------------------------------------------------------------------

width_i = 11
height_i = 6.16

scale = 300

width_f = width_i * scale
height_f = int(height_i * scale)

canvas = np.zeros((height_f, width_f, 3), np.uint8)
canvas.fill(255)

OUTLINE_COLOR = (0, 50, 0)


def transform_point_to_new_coord_sys(p):
    return (int((p[0] + 5.5) * scale), int(height_f - (p[1] + 3.13) * scale))


def draw_line_on_cv2_image(img, p1, p2):
    cv2.line(
        img,
        transform_point_to_new_coord_sys(p1),
        transform_point_to_new_coord_sys(p2),
        OUTLINE_COLOR,
        1,
    )


def put_text_at_centroid(canvas, text, centroid):
    # INPUT CENTROID HERE HAS NOT BEEN SCALED YET
    cv2.putText(
        canvas,
        text,
        transform_point_to_new_coord_sys(centroid),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.45,  # font size scale
        (0, 0, 255),
        2,  # thickness
        cv2.LINE_AA,
    )


for triangle_name in triangles:
    triangle = triangles[triangle_name]

    v1, v2, v3 = triangle
    draw_line_on_cv2_image(canvas, v1, v2)
    draw_line_on_cv2_image(canvas, v2, v3)
    draw_line_on_cv2_image(canvas, v1, v3)

    centroid = caclulate_centroid_of_triangle(*triangle)
    put_text_at_centroid(canvas, triangle_name, centroid)

cv2.circle(
    canvas,
    transform_point_to_new_coord_sys(disgust_center),
    int(disgust_radius * scale),
    OUTLINE_COLOR,
    1,
)
put_text_at_centroid(canvas, "d1", disgust_center)

cv2.circle(
    canvas,
    transform_point_to_new_coord_sys(joy_center),
    int(joy_radius * scale),
    OUTLINE_COLOR,
    1,
)
put_text_at_centroid(canvas, "j1", joy_center)

cv2.circle(
    canvas,
    transform_point_to_new_coord_sys(fear_one_eye_center),
    int(fear_one_eye_radius * scale),
    OUTLINE_COLOR,
    1,
)
put_text_at_centroid(canvas, "f1", fear_one_eye_center)

cv2.circle(
    canvas,
    transform_point_to_new_coord_sys(fear_two_eye_center),
    int(fear_two_eye_radius * scale),
    OUTLINE_COLOR,
    1,
)
put_text_at_centroid(canvas, "f2", fear_two_eye_center)

cv2.circle(
    canvas,
    transform_point_to_new_coord_sys([com_x, com_y]),
    5,
    (255, 0, 0),
    5,
)  # plot COM
put_text_at_centroid(canvas, "CENTER OF MASS", [com_x, com_y])
cv2.imshow("frame", canvas)

# One singular edge case: Rotated Ellipse
sadness_center = (3.5080485876322, -0.0463498929226)
axes = (
    int(1.092556653751 * scale),
    int(1.092556653751 * scale),
)  # Major, minor, same here because circle
angle = 0
start_angle = 161.5
end_angle = 341.5  # 180 deg seperation bc semi circle
cv2.ellipse(
    canvas,
    transform_point_to_new_coord_sys(sadness_center),
    axes,
    angle,
    start_angle,
    end_angle,
    OUTLINE_COLOR,
    1,
)  # Won't show up in desktop preview but is saved to canvas png so all good
put_text_at_centroid(canvas, "s1", (semi_circle_x_com, semi_circle_y_com))

cv2.line(
    canvas,
    (0, height_f // 2),
    (width_f, height_f // 2),
    (0, 0, 255),
    1,
)
put_text_at_centroid(canvas, "y=0", (-5, -0.1))

cv2.line(
    canvas,
    (width_f // 2, 0),
    (width_f // 2, height_f),
    (0, 0, 255),
    1,
)
put_text_at_centroid(canvas, "x=0", (-0.1, 2.95))

save_filename = f"canvas_saves/canvas_{str(datetime.now()).replace(" ", "_")}.png"
cv2.imwrite(save_filename, canvas)

# cv2.waitKey(0)
# cv2.destroyAllWindows()

with open("table.csv", "w") as table_file:
    table_file.write("triangle_name,x1,y1,x2,y2,x3,y3,x_com,y_com,area\n")
    for triangle_name in triangles:
        triangle = triangles[triangle_name]
        v1, v2, v3 = triangle

        centroid = caclulate_centroid_of_triangle(*triangle)

        table_file.write(
            f"{triangle_name},{round(v1[0], 4)},{round(v1[1], 4)},{round(v2[0], 4)},{round(v2[1], 4)},{round(v3[0], 4)},{round(v3[1], 4)},{round(centroid[0],4)},{round(centroid[1],4)},{round(calculate_area_of_triangle(*triangle), 4)}\n"
        )
    table_file.write("\n")
    table_file.write("circle_name,x,y,r,area\n")
    table_file.write(
        f"d1,{round(disgust_center[0], 4)},{round(disgust_center[1], 4)},{round(disgust_radius, 4)},{round(disgust_area, 4)}\n"
    )
    table_file.write(
        f"j1,{round(joy_center[0], 4)},{round(joy_center[1], 4)},{round(joy_radius, 4)},{round(joy_area, 4)}\n"
    )
    table_file.write(
        f"f1,{round(fear_one_eye_center[0], 4)},{round(fear_one_eye_center[1], 4)},{round(fear_one_eye_radius, 4)},{round(fear_one_eye_area, 4)}\n"
    )
    table_file.write(
        f"f2,{round(fear_two_eye_center[0], 4)},{round(fear_two_eye_center[1], 4)},{round(fear_two_eye_radius, 4)},{round(fear_two_eye_area, 4)}\n"
    )

    table_file.write("\n")
    table_file.write(
        "semi_circle_name,x1,y1,x_com,y_com,most_ccw_x,most_ccw_y,r,area\n"
    )
    table_file.write(
        f"s1,3.50804858,-0.04634989292,{round(semi_circle_x_com, 4)},{round(semi_circle_y_com, 4)},2.471,-0.390,1.092,{round(semi_circle_area,4)}\n"
    )

    table_file.write("\n")
    table_file.write("COM,x1,y1\n")
    table_file.write(f"COM,{round(com_x, 4)},{round(com_y, 4)}\n")
    table_file.write("total_area\n")
    table_file.write(f"{round(sum_of_all_areas,4)}\n")
