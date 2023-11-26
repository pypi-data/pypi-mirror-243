import numpy as np
from VisualShape3D.plotable import *
from VisualShape3D.geometry import Point,Shape

class Patch(Plotable):
    '''
         A node in the thermal network
    '''
    def __init__(self, vertices=[], indices=[], face_color = 'xkcd:beige',
        edge_color = 'xkcd:olive', alpha=0.5, **kwargs):
        
        # self.copy_vertices(vertice_index)
        self.vertices = list(vertices)
        self.indices = list(indices)
        self.facecolor = face_color 
        self.edgecolor = edge_color 
        self.alpha = alpha
        self.normal = []

    def set_color(self, face_color, edge_color=None):
        self.facecolor = face_color
        if edgecolor :
            self.edgecolor = edge_color

    def set_alpha(self, alpha):
        self.alpha = alpha

    def set_normal(self, x,y,z):
        self.normal = np.array([x,y,z])

    def copy_vertices(self, vertices):
        self.vertices = []
        for v in vertices :
            self.vertices.append(v)

    def reverse_vertices(self):
        a = self.vertices[::-1]  # copy value
        b = self.indices[::-1] 
        a_reverse = a[:-1]
        a_reverse.insert(0, a[-1])
        b_reverse = b[:-1]
        b_reverse.insert(0, b[-1])
        for i,v in enumerate(a_reverse):  # copy pointer
            self.vertices[i] = v

        for i,v in enumerate(b_reverse):  # copy pointer
            self.indices[i] = v

        return self.vertices,self.indices

    def get_vertices(self):
        return self.vertices

# visualization
    def iplot(self, style =None, ax=None,**kwargs):
        if self.hidden :
            return

        if style == None:
            style = ('default','default','default')

        if ax == None :
            ax = self.get_ax()

        plotable3d = self.get_plotable_data()
        ( face_color, edge_color, alpha) = style

        if face_color == 'default': face_color = 't'
        if edge_color == 'default': edge_color = self.edgecolor
        if     alpha  == 'default': alpha = self.alpha

        for polygon in plotable3d:
            polygon.set_facecolor(face_color)
            polygon.set_edgecolor(edge_color)
            polygon.set_alpha(alpha)
            ax.add_collection3d(polygon)
    
    def get_plotable_data(self):
        """
        :returns: matplotlib Poly3DCollection
        :rtype: mpl_toolkits.mplot3d
        """
        import mpl_toolkits.mplot3d as mplot3d
        return [mplot3d.art3d.Poly3DCollection([self.vertices])]

    def get_object(self): return self

    def get_domain(self):
        """
        :return  ndarray([min], [max])
            opposite vertices of the bounding prism for this object
        """
        # Min/max along the column
        vertices = np.array(self.vertices)
        return np.array([vertices.min(axis=0),  # min (x,y,z)
                         vertices.max(axis=0)]) # max (x,y,z)

### Functions for geometry calculation
    def get_seed(self):
        """
        get the dict form of its arguments for a temporary copy :
           Pathch(dict)
        """
        dict_args = {'vertices':self.vertices.copy(),
                     'indces':self.indices.copy(), 
                     'face_color':self.face_color,
                     'edge_color':self.edge_color, 
                     'alpha':self.alpha}
        return dict_args

class Surface(Patch):

    def __init__(self, label, pane, bFront=True, **kwargs):
 
        self.label = label
        self.id = pane.id *2 - 1
        self.iv = pane.front
        self.pane = pane
        self.bFront = bFront
        self.hidden = False

        face_color = pane.front_color
        if self.isNegative(): 
            face_color = pane.back_color
            self.id = self.pane.id *2
            self.iv = pane.back

        super().__init__(pane.vertices, pane.indices,face_color, pane.edge_color,
                         pane.alpha, **kwargs)

        if self.isNegative():
            self.reverse_vertices()
            
    # def __str__(self):
    #     info = f"    face({self.id}) - {self.label} :\n"
    #     for i,v in enumerate(self.vertices):
    #                 info += f"     {self.indices[i]}  {v}\n" 
    #     return info
    def __str__(self):
        info=f"    face({self.id}) = {self.indices} ({self.label})"
        return info

    def print(self): print(self)

    def isNegative(self):
        return self.bFront == False

    def turn_off(self):
        self.hidden = True

    def turn_on(self):
        self.hidden = False
### Functions for geometry calculation
    def get_seed(self):
        """
        get the dict form of its arguments for creating a copy :
           Patch(dict)
        """
        pane = Pane(self.pane.get_seed())
        dict_args = {'label':self.label, 'pane':pane, 'bFront':self.bFront}
        return dict_args

class Pane(object):
    '''
         In charge of hooking one of walls.
         A wall is full of thermal properties of material layers inside
         as well as  optical properties on two surfaces
    '''
    def __init__(self, label, pane_id, front = 0, back = 0, 
                    vertices = [], indices = [],
                    front_color='xkcd:beige',back_color = 'xkcd:chartreuse',
                    edge_color = 'xkcd:olive', alpha=0.5,**kwargs):
 
        self.label = label
        self.front = front
        self.back  = back
        self.vertices = list(vertices)
        self.indices = list(indices)
        self.id = pane_id
        self.wall = None
        self.front_color = front_color
        self.back_color = back_color
        self.edge_color = edge_color
        self.alpha = alpha

    def __str__(self):
        info=f" Pane({self.id}) : {self.label}, "
        "front space {self.front}, back space {self.back}"
        return info

    def get_seed(self):
        arg_dict = {
                    'label':self.label, 
                    'pane_id':self.id, 
                    'front':self.front, 
                    'back':self.back, 
                    'vertices':self.vertices.copy(),
                    'indices':self.indices.copy(),
                    'front_color': self.front_color,
                    'back_color':self.back_color,
                    'edge_color':self.edge_color, 
                    'alpha':self.alpha }
        return arg_dict

class Space(Plotable):
    '''
         A node in the thermal network
    '''
    def __init__(self, iv = 0, surfaces=[], **kwargs):

        self.iv = iv
        self.surfaces = list(surfaces)
        self.surface_number = len(self.surfaces)
        self.hidden = False

        super().__init__()

    def __str__(self):
        info =f'Space({self.iv}) is enclosed by {self.surface_number} surfaces\n'
        for f in self.surfaces :
                info += f.__str__()+'\n' 
        return info

    def print(self): print(self)

    def add_front_surface(self, pane):
        label = f"{pane.label}+"
        surface = Surface(label, pane )
        self.surfaces.append(surface)
        self.surface_number += 1
        return surface

    def add_back_surface(self, pane):
        label = f"{pane.label}-"
        surface = Surface(label, pane, bFront=False)
        self.surfaces.append(surface)
        self.surface_number += 1
        return surface

    def get_surface_number(self):
        return self.surface_number

    def turn_off(self):
        self.hidden = True

    def turn_on(self):
        self.hidden = False
# visualization
    def iplot(self, style = None, ax = None, **kwargs):
        
        if self.hidden :
            return

        if style == None:
            style = ('default','default','default')

        if ax == None :
            ax = self.get_ax()

        bDefault_Face_Color = False
        bDefault_Edge_Color = False
        bDefault_Alpha = False


        face_color = style['facecolor'] if 'facecolor' in style else 't'
        edge_color = style['edgecolor'] if 'edgecolor' in style else 'default'
        alpha      = style['alpha']     if 'alpha'     in style else 'default'

        if face_color == 'default': face_color = 't'
        if face_color == 't':       bDefault_Face_Color = True
        if edge_color == 'default': bDefault_Edge_Color = True
        if     alpha  == 'default': bDefault_Alpha = True

        plotable3d = self.get_plotable_data()
        for i,polygon in enumerate(plotable3d):
            if bDefault_Face_Color : 
                face_color = self.surfaces[i].face_color
            if bDefault_Edge_Color : 
                edge_color = self.surfaces[i].edge_color
            if bDefault_Face_Color : 
                     alpha = self.surfaces[i].alpha

            polygon.set_facecolor(face_color)
            polygon.set_edgecolor(edge_color)
            polygon.set_alpha(alpha)
            ax.add_collection3d(polygon)
    
    def get_plotable_data(self):
        """
        :returns: matplotlib Poly3DCollection
        :rtype: mpl_toolkits.mplot3d
        """
        data_list=[]
        for surface in self.surfaces :
            data_list = data_list + surface.get_plotable_data()

        return data_list
    
    def get_object(self): return self

### Functions for geometry calculation
    def get_seed(self):
        """
        get the dict form of its arguments for creating a copy :
           Patch(dict)
        """
        dict_args = {'iv':self.iv, 'surfaces': self.surfaces}
        return dict_args

    def get_domain(self):
        if self.surfaces != []:
            space_domain = np.vstack([face.get_domain() 
                                    for face in self.surfaces])
        else:
            space_domain = np.ones((0, 3))

        points = space_domain
        return np.array([points.min(axis=0), points.max(axis=0)])

class Building(Plotable):

    def __init__(self, title="default",**kwargs):

        super().__init__()
        
        self.title = title

        self.vertices = []
        self.vertice_number = 0

        self.panes = []
        self.spaces = []
        self.surfaces = dict()
        
        self.space_number = 0
        self.pane_number = 0
        self.surface_number = 0

        self.face_color_front = 'xkcd:beige'
        self.face_color_back =  'xkcd:aqua'
        self.edge_color = 'xkcd:olive'

        self.hidden = False



    def __str__(self):
        info = ""
        info += f"There are {self.space_number} spaces in the building.\n"
        for space in self.spaces:
            info +=space.__str__()+'\n'
        info += f"A complete list of all vertices ( {self.vertice_number} ) : \n"
        for i,v in enumerate(self.vertices):
            info +=f"      {i} {v}\n"
        return info

    def print(self): print(self)

    def turn_off(self):
        self.hidden = True

    def turn_on(self):
        self.hidden = False

    def hide_surface(self,surface_label):
        if surface_label in self.surfaces.keys() :
            self.surfaces[surface_label].turn_off()

    def show_surface(self,surface_label):
        if surface_label in self.surfaces.keys() :
            self.surfaces[surface_label].turn_on()

    def hide_space(self,space_indice):
        for s in self.spaces:
            if s.iv == space_indice :
                s.turn_off()

    def show_surface(self,surface_label):
        if surface_label in self.surfaces.keys() :
            self.surfaces[surface_label].turn_on()

### For visualization
    def get_object(self) : return self

    # def get_domain(self):
    #     if self.vertices != [] :
    #         return np.array([self.vertices.min(axis=0),  # min (x,y,z)
    #                          self.vertices.max(axis=0)]) # max (x,y,z)
    #     points = np.ones((0, 3))
    #     return np.array([points.min(axis=0), points.max(axis=0)])
    def get_domain(self):
        """
        :return   ndarray([min], [max])
        """
        if self.vertices != [] : 
            buidling_domain = np.vstack([ v for v in self.vertices])
        else:
            buidling_domain = np.ones((0, 3))

        points = np.vstack(( buidling_domain,))
        return np.array([points.min(axis=0), points.max(axis=0)])

    def iplot(self, style, ax, **kwargs):
        if self.hidden :
            return

        if self.spaces == [] :
            return

        for each in self.spaces:
            # print(each.iv)
            each.iplot(style, ax)

### Modeling functions
    def addPane(self, label='', shape=None, front=0, back=0, 
                      front_color= 'xkcd:beige', back_color =  'xkcd:aqua', **kwargs):
        self.pane_number += 1
        self.parse({'label':label, 'shape': shape, 'front':front, 'back':back, 
            'front_color':front_color, 'back_color' :back_color})


    def parse(self, input):

        vertices, indices = self.add_vertice(input['shape'])

        iv = input['front']
        jv = input['back'] 

        pane = Pane(input['label'], self.pane_number, iv, jv, 
                    vertices, indices,
                    input['front_color'], input['back_color'])
        self.panes.append(pane)

        space_front = self.add_space( iv )
        space_back  = self.add_space( jv )

        # ip = self.pane_number
        # i = 2*ip-1
        # j = 2*ip

        s1 = space_front.add_front_surface( pane )
        s2 = space_back.add_back_surface( pane)

        # self.surfaces.append(s1)
        # self.surfaces.append(s2)
        self.surfaces[s1.label] = s1
        self.surfaces[s2.label] = s2
        self.surface_number += 2

    def add_vertice(self,shape):
        vertices = list()
        indices = list()
        for P in shape:
            k = self.contain_vertice(P)  
            if k < 0 :

                V = list(P)  # V, P 为两块内存的个独立指针
                i = self.vertice_number
                self.vertice_number += 1
                self.vertices.append(V)

            else :
                V = self.vertices[k]  # 获得指针
                i = k
            
            vertices.append(V)
            indices.append(i)

        return vertices, indices

    def add_space(self, iv):
        if not self.contain_space(iv) :
            space = Space( iv )
            self.spaces.append(space)
            self.space_number += 1
            return space

        else:
            for each in self.spaces:
                if each.iv == iv :
                    return each
        
    def get_space(self,iv):
        if not self.contain_space(iv) :
            return None

        for each in self.spaces :
            if each.iv == iv :
                return each
        
### Helper functions
    def contain_space(self, iv):
        iv_list = [each.iv for each in self.spaces ]
        return iv in iv_list

    def contain_vertice(self, P) :
        a = Point(*list(P))

        for k,v in enumerate(self.vertices) :
            b = Point(*list(v))
            if a == b :
                return k
        return -1

    def add_to_space(self, iv, surface):
        space = self.get_space(iv)
        if not space : 
            self.spaces += Space(iv,surfaces=[surface])
            self.index_space +=1
        else:
            space.surfaces += surface
        return self.index_space


    def box3D(self,W,H):
        # W,H,A,B,C,D = 1.0, 1.0, 0.3, 0.20, 0.50, 0.40
        rect_pane = Shape('rectangle',W,H)
        self.addPane(label='South', shape=rect_pane.move( to = (W,0,0), by = (  0,  0)), front=0, back=1)
        self.addPane(label='East',  shape=rect_pane.move( to = (W,W,0), by = ( 90,  0)), front=0, back=1)
        self.addPane(label='North' ,shape=rect_pane.move( to = (0,W,0), by = (180,  0)), front=0, back=1)
        self.addPane(label='West',  shape=rect_pane.move( to = (0,0,0), by = (270,  0)), front=0, back=1)
        self.addPane(label='top',   shape=rect_pane.move( to = (W,0,H), by = (  0, 90)), front=0, back=1)  
        self.addPane(label='bottom',shape=rect_pane.move( to = (0,0,0), by = (  0,-90)), front=0, back=1)

        return self

    def shift(self,dx,dy,dz):
        dv = [dx,dy,dz]
        for V in self.vertices :
            V[0] = V[0] + dv[0]
            V[1] = V[1] + dv[1]
            V[2] = V[2] + dv[2]


    def initialize(self):
        self.explode_inputs()
        self.view_factors()

    def explode_inputs(self):

        ip,iv_max = 0,0
        for each in self.panes:
            front = each['front']
            back  = each['back'] 

            # i = 2*ip-1
            # j = 2*ip

            i  = self.add_to_surfaces(front,ip)
            j  = self.add_to_surfaces(back,-ip)
            iv = self.add_to_space(front,i)
            jv = self.add_to_space(back,j)

            if front > iv_max : iv_max = front
            if  back > iv_max : iv_max = back
            
            ip += 1

        iv_max +=2

        if jv != iv_max :
            raise ValueError("Inputs are wrong")

    def view_factors(self):
        pass

def test():
    b = Building()
    print(b)

    W,H,A,B,C,D = 1.0, 0.5, 0.3, 0.20, 0.50, 0.40
    shape1 = Shape('rectangle',W,H,A,B,C,D)
    b.addPane(label='first',shape=shape1, front=0, back=1)
    print(b)

    shape2 = shape1.move( to = (0,0,0), by = (45,0))
    b.addPane(label='second',shape=shape2, front=1, back=2)
    b.print()

    b.plot(hideAxes=True)
    b.show()

def demoSpace():
    space = Space(7)
    print(space)

if __name__ == '__main__':
    test()