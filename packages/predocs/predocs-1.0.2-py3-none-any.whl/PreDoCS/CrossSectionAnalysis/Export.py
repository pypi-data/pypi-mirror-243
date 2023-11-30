"""
This file provides methods to export the discreet cross section geometry to ANSYS and BECAS input files.

The code is copied from Airfoil2BECAS (http://www.becas.dtu.dk/software/pre-and-post-processors/airfoil2becas).

Additionally, a geometry and stain/stress export of cross sections to the
EnSight Gold format (PARAVIEW, https://www.paraview.org/) is provided.

.. codeauthor:: Daniel Hardt <daniel@daniel-hardt.de>
.. codeauthor:: Edgar Werthen <Edgar.Werthen@dlr.de>
"""
import os

import numpy as np
from PreDoCS.MaterialAnalysis.CLT import Ply
from PreDoCS.MaterialAnalysis.Materials import IsotropicMaterial, \
    CompositeMaterial
from PreDoCS.util.Logging import get_module_logger
from PreDoCS.util.vector import Vector

log = get_module_logger(__name__)


try:
    from lightworks.mechana.skins.composite import Laminate as Laminate_lw
    from lightworks.mechana.skins.layer import Layer as Layer_lw
except ImportError:
    log.info('Modul lightworks.mechana not found. Material world VCP can not be used.')
    Laminate_lw = None
    Layer_lw = None


def generous_round(t):
    """
    Round up t to the next decade. Return an integer.
    e.g. 9-->10; 10-->100; 11-->100
    """
    return int(10**round(np.log10(t)+0.5))


def _write_node_definition(outfile, nodenumber, coordinates):
    """
    Write a dataline defining one node to the outfile
    """
    outfile.write('%d, ' % (nodenumber))
    for i in range(len(coordinates)):
        coord = coordinates[i]
        outfile.write('%14.8E' % (coord))
        if i < len(coordinates)-1: outfile.write(', ')
    outfile.write('\n')


def _write_element_definition(outfile, elementnumber, nodenumbers):
    """
    Write a dataline defining one element to the outfile
    """
    outfile.write('%d, ' % (elementnumber))
    for i in range(len(nodenumbers)):
        n = nodenumbers[i]
        outfile.write('%d' % (n))
        if i < len(nodenumbers)-1: outfile.write(', ')
    outfile.write('\n')


def _write_n_int_per_line(list_of_int,outfile,n):
    """
    Write the integers in list_of_int to the output file - n integers
    per line, separated by commas"""
    i=0
    for number in list_of_int:
        i=i+1
        outfile.write('%d' %(number ))
        if i < len(list_of_int):
            outfile.write(',  ')
        if i%n == 0:
            outfile.write('\n')
    if i%n != 0:
        outfile.write('\n')


def write_discreet_geometry_to_ABAQUS_file(discreet_geometry, file_name):
    """
    This method to exports the cross section discreet geometry to ANSYS input files.

    Parameters
    ----------
    discreet_geometry: DiscreetCrossSectionGeometry
        The discreet geometry to export.
    file_name: str
        The ANSYS input files to create.
    """
    outfile = open(file_name, 'w')

    nodes = discreet_geometry.nodes
    max_node_id = max([n.id for n in nodes])
    node_jump = generous_round(max_node_id)

    # Generate nodes data
    nodes = []
    deepness_vector = Vector([0, 0, 1])
    for node in discreet_geometry.nodes:
        position = Vector([node.position.x, node.position.y, 0])
        nodes.extend(({'id': node.id, 'position': position},
                      {'id': node.id + node_jump, 'position': position + deepness_vector}))

    # Generate elements data
    elements = []
    for element in discreet_geometry.elements:
        n1 = element.node1.id
        n2 = element.node2.id
        elements.append({'id': element.id, 'nodes': [n1, n2, n2+node_jump, n1+node_jump]})
    #sections = discreet_geometry.sections
    #materials = list({section.material for section in sections})

    # Write nodal coordinates
    outfile.write('**\n')
    outfile.write('********************\n')
    outfile.write('** NODAL COORDINATES\n')
    outfile.write('********************\n')
    outfile.write('*NODE\n')
    for node in nodes:
        _write_node_definition(outfile, node['id'], node['position'])

    # Write element definitions
    outfile.write('**\n')
    outfile.write('***********\n')
    outfile.write('** ELEMENTS\n')
    outfile.write('***********\n')
    outfile.write('*ELEMENT, TYPE=S4, ELSET=BECAS_SECTION\n')
    for element in elements:
        _write_element_definition(outfile, element['id'], element['nodes'])

    # Write new element sets
    outfile.write('**\n')
    outfile.write('***************\n')
    outfile.write('** ELEMENT SETS\n')
    outfile.write('***************\n')
    for component in discreet_geometry.components:
        outfile.write('*ELSET, ELSET=SECTION{}\n'.format(component.id))
        _write_n_int_per_line([e.id for e in discreet_geometry.elements if e.component == component], outfile, 8)

    # Write Shell Section definitions
    outfile.write('**\n')
    outfile.write('****************************\n')
    outfile.write('** SHELL SECTION DEFINITIONS\n')
    outfile.write('****************************\n')
    ply_set = set()
    for component in discreet_geometry.components:
        # -section.midsurface_offset because the n-direction of PreDoCS and ABAQUS is opposed
        # http://abaqus.software.polimi.it/v6.12/books/usb/default.htm?startat=pt06ch29s06abo27.html#usb-elm-eshelloverview
        outfile.write('*SHELL SECTION, ELSET=SECTION{}, COMPOSITE, OFFSET={}\n'.format(component.id, -component.midsurface_offset))
        material = component.material
        if isinstance(material, IsotropicMaterial):
            ply_set.add(material)
            outfile.write('{}, 3, {}, 0\n'.format(material.thickness, material.name))
        elif isinstance(material, CompositeMaterial):
            layer_idx = 0
            for (ply, thickness, orientation) in reversed(material.layup):
                ply_set.add(ply)
                # -orientation because the n-direction of PreDoCS and ABAQUS is opposed
                outfile.write('{}, 3, {}, {}, {}\n'.format(thickness, ply.name, np.rad2deg(-orientation), layer_idx+1))
                layer_idx += 1
        elif Laminate_lw is not None and isinstance(material, Laminate_lw):
            for layer_idx, layer in enumerate(reversed(material.layers)):
                ply_set.add(layer)
                # -orientation because the n-direction of PreDoCS and ABAQUS is opposed
                outfile.write('{}, 3, {}, {}, {}\n'.format(layer.thickness, layer.material.name, -layer.angle, layer_idx+1))
        else:
            raise RuntimeError('Unknown material')

    # Write material properties
    outfile.write('**\n')
    outfile.write('**********************\n')
    outfile.write('** MATERIAL PROPERTIES\n')
    outfile.write('**********************\n')
    for ply in ply_set:
        outfile.write('*MATERIAL, NAME={}\n'.format(ply.material.name if (Layer_lw is not None and isinstance(ply, Layer_lw)) else ply.name))
        if isinstance(ply, IsotropicMaterial):
            outfile.write('*ELASTIC, TYPE=ISOTROPIC\n')
            outfile.write('{mat.E}, {mat.nu}\n'.format(mat=ply))
        elif isinstance(ply, Ply):
            outfile.write('*ELASTIC, TYPE=ENGINEERING CONSTANTS\n')
            outfile.write('{p.E1}, {p.E2}, {p.E3}, {p.nu12}, {p.nu13}, {p.nu23}, {p.G12}, {p.G31}\n'.format(p=ply))
            outfile.write('{}\n'.format(ply.G23))
        elif Layer_lw is not None and isinstance(ply, Layer_lw):
            outfile.write('*ELASTIC, TYPE=ENGINEERING CONSTANTS\n')
            p = ply.material.raw_data
            outfile.write(f"{p['E_11']}, {p['E_22']}, {p['E_33']}, {p['nu_12']}, {p['nu_13']}, {p['nu_23']}, {p['G_12']}, {p['G_13']}\n")
            outfile.write('{}\n'.format(ply.material.raw_data['G_23']))
        outfile.write('*DENSITY\n')
        outfile.write('{}\n'.format(ply.material.density if (Layer_lw is not None and isinstance(ply, Layer_lw)) else ply.density))
        outfile.write('**\n')

    outfile.close()


def _get_num_layers(material):
    if isinstance(material, IsotropicMaterial):
        return 1
    elif isinstance(material, CompositeMaterial):
        return len(material.layup)
    elif Laminate_lw is not None and isinstance(material, Laminate_lw):
        return len(material.layers)
    else:
        return None


def generate_BECAS_input(discreet_geometry, output_dir, temp_input_file='temp.inp', nodal_thickness='min'):
    """
    This method to exports the discreet cross section geometry to BECAS input files.

    Parameters
    ----------
    discreet_geometry: DiscreetCrossSectionGeometry
        The discreet geometry to export.
    output_dir: str
        The directory where to generate the BECAS input files.
    temp_input_file: str (default: 'temp.inp')
        Temporary ANSYS input file.
    nodal_thickness: str (default: 'min')
        Possible values: 'min', 'max', 'average'
        Method used to determine the nodal thickness distribution.
    """
    try:
        import shellexpander.shellexpander as shellexpander
    except ImportError as ex:
        log.error(
            'BECAS shellexpander module not found. '
            'See https://becas.dtu.dk/software/pre-and-post-processors/shellexpander for further details.'
        )
        raise ex

    write_discreet_geometry_to_ABAQUS_file(discreet_geometry, temp_input_file)

    class args: pass

    args.inputfile = temp_input_file
    args.elsets = ['SECTION{}'.format(s.id) for s in discreet_geometry.components]
    args.sections = 'BECAS_SECTION'
    max_num_layers = max([_get_num_layers(s.material) for s in discreet_geometry.components])
    args.layers = max_num_layers
    args.nodal_thickness = nodal_thickness
    args.dominant_elsets = None
    args.centerline = None
    args.subelsets = None
    args.becasdir = output_dir
    args.verbose = True
    args.debug = False
    shellexpander.main(args)


def write_file_from_lines(file_name, lines):
    with open(file_name, 'w') as f:
        for line in lines:
            f.write(line + '\n')


def export_EnSight_Gold(discreet_geometry, export_name, export_dir, load_states=None):
    """
    This method to exports the cross section geometry and PreDoCS cross section analysis results to
    EnSight Gold format (i.e. input for PARAVIEW).
    
    Parameters
    ----------
    discreet_geometry: DiscreetCrossSectionGeometry
        The geometry to export.
    export_name: str
        The name of the model.
    export_dir: str
        The dir where to write the files.
    load_states: dict(IElement, IElementLoadState) (default: None)
        The load states of the eleemnts. None for export only the cross section geometry.
    """
    ## Case
    case_file = \
        ['FORMAT',
         'type: ensight gold',
         'GEOMETRY',
         'model: {}.ensi.geo'.format(export_name),
         'VARIABLE']
    
    
    nodes = []
    elements = []
    
    # Generate geometry
    i = 0
    for element in sorted(discreet_geometry.elements, key=lambda e: e.id):
        p1 = element.node1_midsurface_position + 0.5 * element.thickness_vector
        p2 = p1 + element.length_vector
        p3 = p2 - element.thickness_vector
        p4 = p3 - element.length_vector
        
        nodes += [{'id': i*4+1, 'position': p1},
                  {'id': i*4+2, 'position': p2},
                  {'id': i*4+3, 'position': p3},
                  {'id': i*4+4, 'position': p4}]
        elements.append((element, [i*4+1, i*4+2, i*4+3, i*4+4]))
        i += 1
    
    ## Geometry
    geo_file = \
        ['PreDoCS result data',
         'description line 2',
         'node id given',
         'element id given',
         'part',
         '{:10d}'.format(1),
         'Nodes and elements',
    # Nodes
         'coordinates',
         '{:10d}'.format(len(nodes))]
    geo_file += ['{:10d}'.format(n['id']) for n in nodes]
    geo_file += ['{:12.5e}'.format(n['position'].x) for n in nodes]
    geo_file += ['{:12.5e}'.format(n['position'].y) for n in nodes]
    geo_file += ['{:12.5e}'.format(0) for n in nodes]
    # Elements
    geo_file += ['quad4', 
         '{:10d}'.format(len(elements))]
    geo_file += ['{:10d}'.format(e.id) for e, nodes in elements]
    geo_file += [''.join('{:10d}'.format(n_id) for n_id in nodes) for e, nodes in elements]
    write_file_from_lines(os.path.join(export_dir, '{}.ensi.geo'.format(export_name)), geo_file)
    
    
    ## Node numbers
    nnum_file = \
        ['PreDoCS node numbers',
         'part',
         '{:10d}'.format(1),
         'coordinates']
    nnum_file += ['{:10d}'.format(n['id']) for n in nodes]
    write_file_from_lines(os.path.join(export_dir, '{}.ensi.nnum'.format(export_name)), nnum_file)
    case_file.append('scalar per node: nodenumbers {}.ensi.nnum'.format(export_name))
    
    
    ## Element numbers
    enum_file = \
        ['PreDoCS element numbers',
         'part',
         '{:10d}'.format(1),
         'quad4']
    enum_file += ['{:10d}'.format(e.id) for e, nodes in elements]
    write_file_from_lines(os.path.join(export_dir, '{}.ensi.enum'.format(export_name)), enum_file)
    case_file.append('scalar per element: elementnumbers {}.ensi.enum'.format(export_name))
    
    
    ## Material ID
    materials = sorted(list({e.material for e, nodes in elements}), key=lambda m: m.name)
    matid_file = \
        ['PreDoCS material IDs',
         'part',
         '{:10d}'.format(1),
         'quad4']
    matid_file += ['{:10d}'.format(materials.index(e.material)) for e, nodes in elements]
    write_file_from_lines(os.path.join(export_dir, '{}.ensi.matid'.format(export_name)), matid_file)
    case_file.append('scalar per element: material_id {}.ensi.matid'.format(export_name))
    
    
    ## Material orientation 1
    matori1_file = \
        ['PreDoCS first material direction (thickness)',
         'part',
         '{:10d}'.format(1),
         'quad4']
    matori1_file += ['{:12.5e}'.format(e.thickness_vector.x) for e, nodes in elements]
    matori1_file += ['{:12.5e}'.format(e.thickness_vector.y) for e, nodes in elements]
    matori1_file += ['{:12.5e}'.format(0) for e, nodes in elements]
    write_file_from_lines(os.path.join(export_dir, '{}.ensi.matori1'.format(export_name)), matori1_file)
    case_file.append('vector per element: material_ori_1 {}.ensi.matori1'.format(export_name))
    
    
    ## Material orientation 2
    matori2_file = \
        ['PreDoCS second material direction (length)',
         'part',
         '{:10d}'.format(1),
         'quad4']
    matori2_file += ['{:12.5e}'.format(e.length_vector.x) for e, nodes in elements]
    matori2_file += ['{:12.5e}'.format(e.length_vector.y) for e, nodes in elements]
    matori2_file += ['{:12.5e}'.format(0) for e, nodes in elements]
    write_file_from_lines(os.path.join(export_dir, '{}.ensi.matori2'.format(export_name)), matori2_file)
    case_file.append('vector per element: material_ori_2 {}.ensi.matori2'.format(export_name))
    
    
    ## Material orientation 3
    matori3_file = \
        ['PreDoCS third material direction (beam)',
         'part',
         '{:10d}'.format(1),
         'quad4']
    matori3_file += ['{:12.5e}'.format(0) for e, nodes in elements]
    matori3_file += ['{:12.5e}'.format(0) for e, nodes in elements]
    matori3_file += ['{:12.5e}'.format(1) for e, nodes in elements]
    write_file_from_lines(os.path.join(export_dir, '{}.ensi.matori3'.format(export_name)), matori3_file)
    case_file.append('vector per element: material_ori_3 {}.ensi.matori3'.format(export_name))
    
    if load_states is not None:
        element = next(iter(load_states))
        # Strain states
        strain_states = list(load_states[element].strain_state.keys())
        for strain_state in strain_states:
            strain_state_idx = strain_states.index(strain_state)
            strain_state_file = \
                ['PreDoCS strain state {}: {}'.format(strain_state_idx, strain_state),
                 'part',
                 '{:10d}'.format(1),
                 'quad4']
            strain_state_file += ['{:12.5e}'.format(load_states[e].strain_state[strain_state](e.length/2.)) for e, nodes in elements]
            write_file_from_lines(os.path.join(export_dir, '{}.ensi.strain_state_{}'.format(export_name, strain_state_idx)), strain_state_file)
            case_file.append('scalar per element: {} {}.ensi.strain_state_{}'.format(strain_state, export_name, strain_state_idx))
        # Stress states
        stress_states = list(load_states[element].stress_state.keys())
        for stress_state in stress_states:
            stress_state_idx = stress_states.index(stress_state)
            stress_state_file = \
                ['PreDoCS strain state {}: {}'.format(stress_state_idx, stress_state),
                 'part',
                 '{:10d}'.format(1),
                 'quad4']
            stress_state_file += ['{:12.5e}'.format(load_states[e].stress_state[stress_state](e.length/2.)) for e, nodes in elements]
            write_file_from_lines(os.path.join(export_dir, '{}.ensi.stress_state_{}'.format(export_name, stress_state_idx)), stress_state_file)
            case_file.append('scalar per element: {} {}.ensi.stress_state_{}'.format(stress_state, export_name, stress_state_idx))
    
    
    
    # Write case file
    write_file_from_lines(os.path.join(export_dir, '{}.case'.format(export_name)), case_file)
