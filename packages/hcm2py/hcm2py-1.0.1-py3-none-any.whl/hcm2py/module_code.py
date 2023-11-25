import pyperclip
import requests
import math
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import pygame
from pygame.locals import QUIT
from pygame.locals import QUIT, KEYDOWN, K_ESCAPE, K_w, K_a, K_s, K_d, K_e, K_q,K_LEFT,K_RIGHT

string = ""
connections = ""
builds = ""
buildvalues = ""
parts = []
active=False


index_counter = 1
should_paste=True
active = 0

def ascii_to_number(char):
    if len(char) == 1:
        return ord(char)
    else:
        raise ValueError("Input must be a single character")
def createBlockCustom(string):
    items = string.split(',')
    if(len(items[5])>2):
        if(len(items[5].split("+"))>2):
            parts.append({"x": items[1], "y": items[2], "z": items[3], "index": index_counter, "part": items[0], "r": items[5].split("+")[0], "g": items[5].split("+")[1], "b": items[5].split("+")[2]})
            return
        else:
            parts.append({"x": items[1], "y": items[2], "z": items[3], "index": index_counter, "part": items[0], "freq": items[5]})
            return
    parts.append({"x": items[1], "y": items[2], "z": items[3], "index": index_counter, "part": items[0], "freq": items[5]})
def createWire(start_x, start_y, start_z, end_x, end_y, end_z):
    global connections
    connections += f"{xyztoindex(start_x, start_y, start_z)},{xyztoindex(end_x, end_y, end_z)};"
def createBlock(x, y, z, part, specialparams=None):
    global index_counter
    global parts
    freq = 0
    part_names_to_values = {
        'nor': 0,
        'not': 0,
        'and': 1,
        'or': 2,
        'xor': 3,
        'input': 4,
        'inp': 4,
        'flipflop': 5,
        'toggle': 5,
        'led': 6,
        'light': 6,
        'sound': 7,
        'conductor': 8,
        'cond': 8,
        'nand': 10,
        'xnor': 11,
        'random': 12,
        'rand': 12,
        'letter': 13,
        'tile' : 14,
    }
    if isinstance(part, str) and not part.isdigit():
        part_lower = part.lower()
        if part_lower in part_names_to_values:
            part = part_names_to_values[part_lower]
        else:
            print('hcm2py Error : idk what a '+part+' is, its not in my list of blocks')
    if part==6 or part==14:
        r=255
        g=255
        b=255
    if part==12:
        freq=329.63
    if part==13:
        if specialparams:
            if isinstance(specialparams,str):
                specialparams = ascii_to_number(specialparams)
        freq=65
    if specialparams is not None:
        if isinstance(specialparams, (int, float)):
            if isinstance(specialparams, int) or isinstance(specialparams, float):
                r = g = b = None
                freq = specialparams
            else:
                print("Error: specialparams should be an array of 3 numbers (RGB) or a single number.")
                return
        elif len(specialparams) == 3:
            r, g, b = specialparams
            freq = None
        else:
            print("Error: specialparams should be an array of 3 numbers (RGB) or a single number.")
            return
    if part == 6 or part==14:
        parts.append({"x": x, "y": y, "z": z, "index": index_counter, "part": part, "r": r, "g": g, "b": b,'active':active})
        index_counter += 1
    elif part == 7 or part == 12 or part == 13:
            parts.append({"x": x, "y": y, "z": z, "index": index_counter, "part": part, "freq": freq,'active':active})
            index_counter += 1
    else:
        parts.append({"x": x, "y": y, "z": z, "index": index_counter, "part": part,'active':active})
        index_counter += 1
def xyztoindex(x, y, z):
    for item in parts:
        if item["x"] == x and item["y"] == y and item["z"] == z:
            return str(item["index"]) 
def checkForBlock(x, y, z):
    for item in parts:
        if item["x"] == x and item["y"] == y and item["z"] == z:
            return True
    return False       
def createWireIndex(index1,index2):
    global connections
    connections += str(index1)+","+str(index2)+";"
def createCustomBuilding(Type, x, y, z, rotX, rotY, rotZ, value=None):
    global builds
    global buildvalues
    types = ['Sign', 'Door', 'Graph', 'MassiveMemory', 'MassMemory', 'KeyInput', 'QwertyKeyInput']
    
    corrected_type = Type.capitalize()
    if corrected_type in types:
        if value is None:
            if corrected_type == 'Sign':
                value = '68636d327079'
            rotX_rad = math.radians(rotX)
            rotY_rad = math.radians(rotY)
            rotZ_rad = math.radians(rotZ)
            R00 = math.cos(rotZ_rad) * math.cos(rotY_rad)
            R01 = -math.sin(rotZ_rad) * math.cos(rotX_rad) + math.cos(rotZ_rad) * math.sin(rotY_rad) * math.sin(rotX_rad)
            R02 = math.sin(rotZ_rad) * math.sin(rotX_rad) + math.cos(rotZ_rad) * math.sin(rotY_rad) * math.cos(rotX_rad)

            R10 = math.sin(rotZ_rad) * math.cos(rotY_rad)
            R11 = math.cos(rotZ_rad) * math.cos(rotX_rad) + math.sin(rotZ_rad) * math.sin(rotY_rad) * math.sin(rotX_rad)
            R12 = -math.cos(rotZ_rad) * math.sin(rotX_rad) + math.sin(rotZ_rad) * math.sin(rotY_rad) * math.cos(rotX_rad)

            R20 = -math.sin(rotY_rad)
            R21 = math.cos(rotY_rad) * math.sin(rotX_rad)
            R22 = math.cos(rotY_rad) * math.cos(rotX_rad)
            builds += f"{Type},{x},{y},{z},{R00},{R01},{R02},{R10},{R11},{R12},{R20},{R21},{R22};"
            buildvalues += f"{value};"
        else:
            print('Invalid Type, valid types: Sign, Door, Graph, MassiveMemory, MassMemory, KeyInput, QwertyKeyInput')
def text_to_hexadecimal(text):
    bytes_text = text.encode('utf-8')
    hexadecimal_text = bytes_text.hex()
    return hexadecimal_text
def paste_to_dpaste(content):
    dpaste_api_url = "https://dpaste.org/api/"
    payload = {
        "lexer": "python",
        "content": content
    }
    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }

    try:
        response = requests.post(dpaste_api_url, data=payload, headers=headers)
        response.raise_for_status()

        dpaste_link = response.text.strip()
        print("dpaste.org link:", dpaste_link[1:-1] + "/raw")
        return dpaste_link[1:-1] + "/raw"
    except requests.exceptions.HTTPError as errh:
        print("HTTP Error:", errh)
    except requests.exceptions.ConnectionError as errc:
        print("Error Connecting:", errc)
    except requests.exceptions.Timeout as errt:
        print("Timeout Error:", errt)
    except requests.exceptions.RequestException as err:
        print("Something went wrong:", err)
def number_to_binary(num, numofbits):
    binary_num = bin(num)[2:]
    binary_num = binary_num.zfill(numofbits)
    return binary_num
def import_build(input_string, offset_x=0, offset_y=0, offset_z=0):
    global index_counter
    import_connections = input_string.split("?")
    import_connections = import_connections[1]
    import_connections = import_connections.split(";")
    input_string = input_string.split("?")[0]
    import_parts = input_string.split(";")
    for i in range(len(import_parts)):
        items = import_parts[i].split(",")
        parts.append({"x": int(items[2])+offset_x, "y": int(items[3])+offset_y, "z": int(items[4])+offset_z, "index": index_counter, "part": items[0]})
        index_counter+=1
    if(len(import_connections)>1):
        for i in range(len(import_connections)):
            wires = import_connections[i].split(",")
            createWireIndex(int(wires[0])+index_counter-3,int(wires[1])+index_counter-3)
def cube(x1, y1, z1, x2, y2, z2, part, specialparams=None):
    for x in range(abs(x2 - x1)):
        for y in range(abs(y2 - y1)):
            for z in range(abs(z2 - z1)):
                if specialparams:
                    createBlock(x + x1, y + y1, z + z1, part, specialparams)
                else:
                    createBlock(x + x1, y + y1, z + z1, part)
def getString():
    global string
    return string
def getBlocks():
    global parts
    return parts
def getConnections():
    global connections
    return connections
def getBuilds():
    global builds
    return builds
def getBuildvalues():
    global buildvalues
    return buildvalues
def getIndex():
    global index_counter
    return index_counter
def printBlockNums():
    types = ['NOR', 'AND', 'OR', 'XOR', 'Input', 'FLIPFLOP', 'LED', 'Sound', 'Conductor', 'NAND', 'XNOR', 'Random', 'Letter']
    for i in types:
        indx=types.index(i)
        if indx<8:
            add=0
        else:
            add=1
        print(i + " : " + str(indx+add))
def set_should_paste(bool):
    global should_paste
    should_paste=bool
def finish():
    global string
    global connections
    global builds
    global buildvalues
    
    for item in parts:
        if item["part"] == 6 or item["part"] == "6" or item["part"] == 14 or item["part"] == "14":
            string += f";{item['part']},{item['active']},{item['x']},{item['y']},{item['z']},{item['r']}+{item['g']}+{item['b']}"
        elif item["part"] in [7, 12, 13, "7", "12", "13"]:
            string += f";{item['part']},{item['active']},{item['x']},{item['y']},{item['z']},{item['freq']}"
        else:
            string += f";{item['part']},{item['active']},{item['x']},{item['y']},{item['z']},"

    string = string[1:]
    connections = connections[:-1]
    builds = builds[:-1]
    buildvalues = buildvalues[:-1]
    string += f"?{connections}?{builds}?{buildvalues}"
    if should_paste:
        pyperclip.copy(paste_to_dpaste(string))
    else:
        print("String copied to clipboard:")
        print(string)
        pyperclip.copy(string) 
def render():
    def resize(width, height):
        glViewport(0, 0, width, height)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(45, (width / height), 0.1, 50.0)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

    def draw_3d_cube(position, size, color):
        x, y, z = position

        glBegin(GL_QUADS)
        glColor3fv(color)
        glVertex3f(x, y, z)
        glVertex3f(x + size, y, z)
        glVertex3f(x + size, y + size, z)
        glVertex3f(x, y + size, z)
        glVertex3f(x, y, z + size)
        glVertex3f(x + size, y, z + size)
        glVertex3f(x + size, y + size, z + size)
        glVertex3f(x, y + size, z + size)
        glVertex3f(x, y, z)
        glVertex3f(x, y + size, z)
        glVertex3f(x, y + size, z + size)
        glVertex3f(x, y, z + size)
        glVertex3f(x + size, y, z)
        glVertex3f(x + size, y + size, z)
        glVertex3f(x + size, y + size, z + size)
        glVertex3f(x + size, y, z + size)
        glVertex3f(x, y + size, z)
        glVertex3f(x + size, y + size, z)
        glVertex3f(x + size, y + size, z + size)
        glVertex3f(x, y + size, z + size)
        glVertex3f(x, y, z)
        glVertex3f(x + size, y, z)
        glVertex3f(x + size, y, z + size)
        glVertex3f(x, y, z + size)
        glEnd()

    def draw_3d_parts():
        for part in parts:
            default_color = (255, 255, 255)
            colors = {'0': (125, 0, 0), '1': (0, 0, 125), '2': (0, 125, 0), '3': (255, 182, 193), '4': (255, 165, 0), '5': (20, 20, 20), '7': (20, 20, 20)}

            if part['part'] == 6 or part['part'] == 14:
                color = (part['r'], part['g'], part['b'])
            else:
                color = colors.get(part['part'], default_color)

            normalized_color = (color[0] / 255.0, color[1] / 255.0, color[2] / 255.0)
            draw_3d_cube((part['x'], part['y'], part['z']), 1, normalized_color)

    pygame.init()

    screen_width, screen_height = 800, 600
    screen = pygame.display.set_mode((screen_width, screen_height), pygame.OPENGL | pygame.DOUBLEBUF)
    pygame.display.set_caption("HCM2PY 3D Renderer")
    camx, camy, camz = 0, 0, -5


    clock = pygame.time.Clock()
    angle = 180.0
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                return
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    return

        keys = pygame.key.get_pressed()
        speed = 0.2 

        if keys[K_w]:
            camz += speed
        elif keys[K_s]:
            camz -= speed  

        if keys[K_a]:
            camx += speed 
        elif keys[K_d]:
            camx -= speed  

        if keys[K_q]:
            camy += speed 
        elif keys[K_e]:
            camy -= speed  
        if keys[K_LEFT]:
            angle -= 5 
        elif keys[K_RIGHT]:
            angle += 5 
        screen.fill((200,200,200));
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glEnable(GL_DEPTH_TEST)
        glLoadIdentity()
        gluPerspective(45, (screen_width / screen_height), 0.1, 50.0)
        
        

        glTranslatef(camx, camy, camz)
        glRotate(angle,0,1,0)
        

        draw_3d_parts()
        
        pygame.display.flip()
        clock.tick(30)
def set_active(bool):
    global active
    if bool==True:
        active=1
    else:
        active=0
    