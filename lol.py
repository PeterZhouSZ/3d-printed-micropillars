from stl import Solid, Facet, Vector3d

structure = Solid(name='cube')
# South
xy_res = .1
z_res = .05
x=1
y=1
z=1
# South
structure.add_facet(Vector3d(0, -1, 0),
    [
        Vector3d(x * xy_res + 0, y * xy_res + 0, 0 + z * z_res),
        Vector3d(x * xy_res + xy_res, y * xy_res + 0, 0 + z * z_res),
        Vector3d(x * xy_res + xy_res, y * xy_res + 0, z_res + z * z_res)
    ])
structure.add_facet(Vector3d(0, -1, 0),
    [
        Vector3d(x * xy_res + 0, y * xy_res + 0, 0 + z * z_res),
        Vector3d(x * xy_res + xy_res, y * xy_res + 0, z_res + z * z_res),
        Vector3d(x * xy_res + 0, y * xy_res + 0, z_res + z * z_res)
    ])
# Down
structure.add_facet(Vector3d(0, 0, -1),
    [
        Vector3d(x * xy_res + 0, y * xy_res + xy_res, 0 + z * z_res),
        Vector3d(x * xy_res + xy_res, y * xy_res + xy_res, 0 + z * z_res),
        Vector3d(x * xy_res + xy_res, y * xy_res + 0, 0 + z * z_res)
    ])
structure.add_facet(Vector3d(0, 0, -1),
    [
        Vector3d(x * xy_res + 0, y * xy_res + xy_res, 0 + z * z_res),
        Vector3d(x * xy_res + xy_res, y * xy_res + 0, 0 + z * z_res),
        Vector3d(x * xy_res + 0, y * xy_res + 0, 0 + z * z_res)
    ])
# East
structure.add_facet(Vector3d(1, 0, 0),
    [
        Vector3d(x * xy_res + xy_res, y * xy_res + xy_res, 0 + z * z_res),
        Vector3d(x * xy_res + xy_res, y * xy_res + xy_res, z_res + z * z_res),
        Vector3d(x * xy_res + xy_res, y * xy_res + 0, z_res + z * z_res)
    ])
structure.add_facet(Vector3d(1, 0, 0),
    [
        Vector3d(x * xy_res + xy_res, y * xy_res + xy_res, 0 + z * z_res),
        Vector3d(x * xy_res + xy_res, y * xy_res + 0, z_res + z * z_res),
        Vector3d(x * xy_res + xy_res, y * xy_res + 0, 0 + z * z_res)
    ])
# Up
structure.add_facet(Vector3d(0, 0, 1),
    [
        Vector3d(x * xy_res + xy_res, y * xy_res + xy_res, z_res + z * z_res),
        Vector3d(x * xy_res + 0, y * xy_res + xy_res, z_res + z * z_res),
        Vector3d(x * xy_res + 0, y * xy_res + 0, z_res + z * z_res)
    ])
structure.add_facet(Vector3d(0, 0, 1),
    [
        Vector3d(x * xy_res + xy_res, y * xy_res + xy_res, z_res + z * z_res),
        Vector3d(x * xy_res + 0, y * xy_res + 0, z_res + z * z_res),
        Vector3d(x * xy_res + xy_res, y * xy_res + 0, z_res + z * z_res)
    ])
# West
structure.add_facet(Vector3d(-1, 0, 0),
    [
        Vector3d(x * xy_res + 0, y * xy_res + xy_res, z_res + z * z_res),
        Vector3d(x * xy_res + 0, y * xy_res + xy_res, 0 + z * z_res),
        Vector3d(x * xy_res + 0, y * xy_res + 0, 0 + z * z_res)
    ])
structure.add_facet(Vector3d(-1, 0, 0),
    [
        Vector3d(x * xy_res + 0, y * xy_res + xy_res, z_res + z * z_res),
        Vector3d(x * xy_res + 0, y * xy_res + 0, 0 + z * z_res),
        Vector3d(x * xy_res + 0, y * xy_res + 0, z_res + z * z_res)
    ])
# North
structure.add_facet(Vector3d(0, 1, 0),
    [
        Vector3d(x * xy_res + 0, y * xy_res + xy_res, 0 + z * z_res),
        Vector3d(x * xy_res + 0, y * xy_res + xy_res, z_res + z * z_res),
        Vector3d(x * xy_res + xy_res, y * xy_res + xy_res, z_res + z * z_res)
    ])
structure.add_facet(Vector3d(0, 1, 0),
    [
        Vector3d(x * xy_res + 0, y * xy_res + xy_res, 0 + z * z_res),
        Vector3d(x * xy_res + xy_res, y * xy_res + xy_res, z_res + z * z_res),
        Vector3d(x * xy_res + xy_res, y * xy_res + xy_res, 0 + z * z_res)
    ])
with open('cube2.stl', 'wb') as f:
  structure.write_ascii(f)