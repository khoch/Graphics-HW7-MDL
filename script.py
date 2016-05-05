import mdl
from display import *
from matrix import *
from draw import *

def run(filename):
    """
    This function runs an mdl script
    """
    color = [255, 255, 255]
    tmp = new_matrix()
    ident( tmp )

    p = mdl.parseFile(filename)

    if p:
        (commands, symbols) = p
    else:
        print "Parsing failed."
        return

    stack = [ tmp ]
    screen = new_screen()
        
    for command in commands:
        temp = []
        if command[0] == 'line':
                add_edge( temp, command[1], command[2], command[3], command[4], command[5], command[6] )
                matrix_mult( temp, stack[-1] )
                draw_lines( temp, screen, color )
                
        elif command[0] == 'circle':
                add_circle( temp, command[1], command[2], 0, command[3], .01 )
                matrix_mult( temp, stack[-1] )
                draw_lines( temp, screen, color )
            
        elif command[0] == 'bezier':
                add_curve( temp, command[1], command[2], command[3], command[4], command[5], command[6], command[7], command[8], .01, 'bezier' )
                matrix_mult( temp, stack[-1] )
                draw_lines( temp, screen, color )
            
        elif command[0] == 'hermite':
                add_curve( temp, command[1], command[2], command[3], command[4], command[5], command[6], command[7], command[8], .01, 'hermite' )
                matrix_mult( temp, stack[-1] )
                draw_lines( temp, screen, color )

        elif command[0] == 'sphere':
                add_sphere( temp, command[1], command[2], 0, command[3], 5 )
                matrix_mult( temp, stack[-1] )
                draw_polygons( temp, screen, color )

        elif command[0] == 'torus':
                add_torus( temp, command[1], command[2], 0, command[3], command[4], 5 )
                matrix_mult( temp, stack[-1] )
                draw_polygons( temp, screen, color )

        elif command[0] == 'box':
                add_box( temp, command[1], command[2], command[3], command[4], command[5], command[6] )
                matrix_mult( temp, stack[-1] )
                draw_polygons( temp, screen, color )


        elif command[0] == 'scale':
                s = make_scale( command[1], command[2], command[3] )
                matrix_mult( s, stack[-1] )

        elif command[0] == 'translate':
                t = make_translate( command[1], command[2], command[3] )
                matrix_mult( t, stack[-1] )

        elif command[0] == 'rotate':
                angle = command[2] * ( math.pi / 180 )
                if command[1] == 'x':
                    r = make_rotX( angle )
                elif command[1] == 'y':
                    r = make_rotY( angle )
                elif command[1] == 'z':
                    r = make_rotZ( angle )
                matrix_mult( r, stack[-1] )

        elif command[0] == 'push':
            stack.append(copy.deepcopy(stack[-1]))
            
        elif command[0] == 'pop':
            stack.pop()
            
        elif command[0] == 'ident':
            ident( transform )

        elif command[0] in ['display', 'save' ]:
            if command[0] == 'display':
                display( screen )

            elif command[0] == 'save':
                c+= 1
                save_extension( screen, command[1] )
        
        elif command[0] == 'quit':
            return    
        elif command[0][0] != '#':
            print 'Invalid command: ' + command[0]
