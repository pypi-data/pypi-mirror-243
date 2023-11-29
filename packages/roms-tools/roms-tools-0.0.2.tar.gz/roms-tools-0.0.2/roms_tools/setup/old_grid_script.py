import netCDF4
import numpy as np

import matplotlib.pyplot as plt
import copy
from scipy.interpolate import RegularGridInterpolator

import cartopy.crs as ccrs
import matplotlib.pyplot as plt

from datetime import date



def generate_grid(grdname, nx, ny, size_x, size_y, tra_lon, tra_lat, rot):

    r_earth = 6371315.0

    ## Mercator projection around the equator

    if (size_y>size_x):
        length = size_y * 1e3
        nl = ny
        width = size_x * 1e3
        nw = nx
    else:
        length = size_x * 1e3
        nl = nx
        width = size_y * 1e3
        nw = ny

    dlon = length/r_earth
    lon1d = dlon*np.arange(-0.5,nl+1.5,1)/nl - dlon/2
    mul = 1.0
    dlat = width/r_earth
    for it in range(1,101):
        y1 = np.log(np.tan(np.pi/4-dlat/4))
        y2 = np.log(np.tan(np.pi/4+dlat/4))
        y = (y2-y1)*np.arange(-0.5,nw+1.5,1)/nw + y1
        lat1d = 2*np.arctan(np.exp(y)) - np.pi/2
        lat1d = np.arctan(np.sinh(y))
        dlat_cen = 0.5*(lat1d[int(np.round(nw/2)+1)]-lat1d[int(np.round(nw/2)-1)])
        dlon_cen = dlon/nl
        mul = dlat_cen/dlon_cen*length/width*nw/nl
        dlat = dlat/mul

    lon1de = dlon*np.arange(-1,nl+2,1)/nl - dlon/2
    ye = (y2-y1)*np.arange(-1,nw+2)/nw + y1
    lat1de = 2*np.arctan(np.exp(ye)) - np.pi/2
    lat1de = np.arctan(np.sinh(ye))
    lat1de= lat1de/mul

    (lon1,lat1) = np.meshgrid(lon1d,lat1d)
    (lone,late) = np.meshgrid(lon1de,lat1de)
    lonu = 0.5*(lon1[:,:-1]+lon1[:,1:])
    latu = 0.5*(lat1[:,:-1]+lat1[:,1:])
    lonv = 0.5*(lon1[:-1,:]+lon1[1:,:])
    latv = 0.5*(lat1[:-1,:]+lat1[1:,:])

    if (size_y>size_x):
        (lon1,lat1) = rot_sphere(lon1,lat1,90)
        (lonu,latu) = rot_sphere(lonu,latu,90)
        (lonv,latv) = rot_sphere(lonv,latv,90)
        (lone,late) = rot_sphere(lone,late,90)

        lon1 = np.transpose(np.flip(lon1,0))
        lat1 = np.transpose(np.flip(lat1,0))
        lone = np.transpose(np.flip(lone,0))
        late = np.transpose(np.flip(late,1))

        lonu_tmp= np.transpose(np.flip(lonv,0))
        latu_tmp = np.transpose(np.flip(latv,0))
        lonv = np.transpose(np.flip(lonu,0))
        latv = np.transpose(np.flip(latu,0))
        lonu = lonu_tmp
        latu = latu_tmp

    (lon2,lat2) = rot_sphere(lon1,lat1,rot)
    (lonu,latu) = rot_sphere(lonu,latu,rot)
    (lonv,latv) = rot_sphere(lonv,latv,rot)
    (lone,late) = rot_sphere(lone,late,rot)

    (lon3,lat3) = tra_sphere(lon2,lat2,tra_lat)
    (lonu,latu) = tra_sphere(lonu,latu,tra_lat)
    (lonv,latv) = tra_sphere(lonv,latv,tra_lat)
    (lone,late) = tra_sphere(lone,late,tra_lat)

    lon4 = lon3 + tra_lon*np.pi/180
    lonu = lonu + tra_lon*np.pi/180
    lonv = lonv + tra_lon*np.pi/180
    lone = lone + tra_lon*np.pi/180
    lon4[lon4<-np.pi] = lon4[lon4<-np.pi] + 2*np.pi
    lonu[lonu<-np.pi] = lonu[lonu<-np.pi] + 2*np.pi
    lonv[lonv<-np.pi] = lonv[lonv<-np.pi] + 2*np.pi
    lone[lone<-np.pi] = lone[lone<-np.pi] + 2*np.pi
    lat4 = lat3

    # Compute pn and pm
    # pm = 1/dx
    pmu = gc_dist(lonu[:,:-1],latu[:,:-1],lonu[:,1:],latu[:,1:])
    pm = 0*lon4
    pm[:,1:-1] = pmu
    pm[:,0] = pm[:,1]
    pm[:,-1] = pm[:,-2]
    pm = 1/pm

    # pn = 1/dy
    pnv = gc_dist(lonv[:-1,:],latv[:-1,:],lonv[1:,:],latv[1:,:])
    pn = 0*lon4
    pn[1:-1,:] = pnv
    pn[0,:] = pn[1,:]
    pn[-1,:] = pn[-2,:]
    pn = 1/pn


    ## Compute angles of local grid positive x-axis relative to east
    dellat = latu[:,1:]-latu[:,:-1]
    dellon = lonu[:,1:]-lonu[:,:-1]
    dellon[dellon > np.pi] = dellon[dellon > np.pi] - 2*np.pi
    dellon[dellon < -np.pi] = dellon[dellon < -np.pi] + 2*np.pi
    dellon = dellon * np.cos(0.5*(latu[:,1:]+latu[:,:-1]))

    ang = copy.copy(lon4);
    ang_s = np.arctan(dellat/(dellon+1e-16))
    ang_s[(dellon<0) & (dellat<0)] = ang_s[(dellon<0) & (dellat<0)] - np.pi
    ang_s[(dellon<0) & (dellat>=0)] = ang_s[(dellon<0) & (dellat>=0)] + np.pi
    ang_s[ang_s > np.pi] = ang_s[ang_s > np.pi] - np.pi
    ang_s[ang_s < -np.pi] = ang_s[ang_s < -np.pi] + np.pi

    ang[:,1:-1] = ang_s
    ang[:,0]   = ang[:,1]
    ang[:,-1] = ang[:,-2]

    lon4[lon4<0] = lon4[lon4<0] + 2*np.pi
    lone[lone<0] = lone[lone<0] + 2*np.pi

    plot_grid(lon4,lat4)
    save_grid(grdname,nx,ny,lon4,lat4,pm,pn,ang,size_x,size_y,rot,tra_lon,tra_lat,lone,late)

    #return (lon4,lat4,pm,pn,ang,lone,late)


def save_grid(grdname,nx,ny,lon,lat,pm,pn,angle,xsize,ysize,rot,tra_lon,tra_lat,lone,late):

    # This is part of Easy Grid
    #  (c) 2008, Jeroen Molemaker, UCLA

    ROMS_title = 'ROMS grid by Easy Grid. Settings:' + \
    ' nx: ' + str(nx) + ' ny: ' + str(ny) + \
    ' xsize: ' + str(xsize/1e3) + '  ysize: ' + str(ysize/1e3) + \
    ' rotate: ' + str(rot) + ' Lon: ' + str(tra_lon) + ' Lat: ' + str(tra_lat)

    nxp= nx+2
    nyp= ny+2

    # Create the grid file
    create_grid(nxp,nyp,grdname,ROMS_title)

    f0=4*np.pi*np.sin(lat)/(24*3600)

    # Make bathymetry
    hraw = make_topo(lon,lat)

    # Compute the mask
    mask = 0*hraw + 1
    mask[hraw > 0] = 0

    # Fill the grid file
    f = netCDF4.Dataset(grdname, 'r+', format='NETCDF4')
    f['pm'][:,:] = pm
    f['pn'][:,:] = pn
    f['angle'][:,:] = angle
    f['hraw'][:,:] = hraw
    f['f'][:,:] = f0
    f['mask_rho'][:,:] = mask
    f['lon_rho'][:,:] = lon*180/np.pi
    f['lat_rho'][:,:] = lat*180/np.pi
    f['spherical'][:] = 'T'
    f['tra_lon'][:] = tra_lon
    f['tra_lat'][:] = tra_lat
    f['rotate'][:] = rot

    f.close()


def rot_sphere(lon1, lat1, rot):

    (n,m) = np.shape(lon1)
    rot = rot*np.pi/180

    # translate into x,y,z
    # conventions:  (lon,lat) = (0,0)  corresponds to (x,y,z) = ( 0,-r, 0)
    #               (lon,lat) = (0,90) corresponds to (x,y,z) = ( 0, 0, r)
    x1 = np.sin(lon1) * np.cos(lat1)
    y1 = np.cos(lon1) * np.cos(lat1)
    z1 = np.sin(lat1)

    # We will rotate these points around the small circle defined by
    # the intersection of the sphere and the plane that
    # is orthogonal to the line through (lon,lat) (0,0) and (180,0)

    # The rotation is in that plane around its intersection with
    # aforementioned line.

    # Since the plane is orthogonal to the y-axis (in my definition at least),
    # Rotations in the plane of the small circle maintain constant y and are around
    # (x,y,z) = (0,y1,0)

    rp1 = np.sqrt(x1**2 + z1**2)

    ap1 = np.pi/2*np.ones((n,m))
    ap1[np.abs(x1)>1e-7] = np.arctan(np.abs(z1[np.abs(x1)>1e-7] / x1[np.abs(x1)>1e-7]))
    ap1[x1<0] = np.pi - ap1[x1<0]
    ap1[z1<0] = -ap1[z1<0]

    ap2 = ap1 + rot
    x2 = rp1 * np.cos(ap2)
    y2 = y1
    z2 = rp1 * np.sin(ap2)

    lon2 = np.pi/2*np.ones((n,m))
    lon2[abs(y2)>1e-7] = np.arctan(np.abs(x2[np.abs(y2)>1e-7] / y2[np.abs(y2)>1e-7]))
    lon2[y2<0] = np.pi - lon2[y2<0]
    lon2[x2<0] = -lon2[x2<0]

    pr2 = np.sqrt(x2**2 + y2**2)
    lat2 = np.pi/2 * np.ones((n,m))
    lat2[np.abs(pr2)>1e-7] = np.arctan(np.abs(z2[np.abs(pr2)>1e-7] / pr2[np.abs(pr2)>1e-7]))
    lat2[z2<0] = -lat2[z2<0]

    return (lon2,lat2)


def tra_sphere(lon1,lat1,tra):

    # Rotate sphere around its y-axis
    # Part of easy grid
    # (c) 2008, Jeroen Molemaker, UCLA

    (n,m) = np.shape(lon1)
    tra = tra*np.pi/180  # translation in latitude direction

    # translate into x,y,z
    # conventions:  (lon,lat) = (0,0)  corresponds to (x,y,z) = ( 0,-r, 0)
    #               (lon,lat) = (0,90) corresponds to (x,y,z) = ( 0, 0, r)
    x1 = np.sin(lon1) * np.cos(lat1)
    y1 = np.cos(lon1) * np.cos(lat1)
    z1 = np.sin(lat1)

    # We will rotate these points around the small circle defined by
    # the intersection of the sphere and the plane that
    # is orthogonal to the line through (lon,lat) (90,0) and (-90,0)

    # The rotation is in that plane around its intersection with
    # aforementioned line.

    # Since the plane is orthogonal to the x-axis (in my definition at least),
    # Rotations in the plane of the small circle maintain constant x and are around
    # (x,y,z) = (x1,0,0)

    rp1 = np.sqrt(y1**2 + z1**2)

    ap1 = np.pi/2 * np.ones((n,m))
    ap1[np.abs(y1)>1e-7] = np.arctan(np.abs(z1[np.abs(y1)>1e-7] / y1[np.abs(y1)>1e-7]))
    ap1[y1<0] = np.pi - ap1[y1<0]
    ap1[z1<0] = -ap1[z1<0]

    ap2 = ap1 + tra
    x2 = x1
    y2 = rp1 * np.cos(ap2)
    z2 = rp1 * np.sin(ap2)

    ## transformation from (x,y,z) to (lat,lon)
    lon2 = np.pi/2* np.ones((n,m))
    lon2[np.abs(y2)>1e-7] = np.arctan(np.abs(x2[np.abs(y2)>1e-7] / y2[np.abs(y2)>1e-7]))
    lon2[y2<0] = np.pi - lon2[y2<0]
    lon2[x2<0] = -lon2[x2<0]

    pr2 = np.sqrt(x2**2 + y2**2)
    lat2 = np.pi / (2*np.ones((n,m)))
    lat2[np.abs(pr2)>1e-7] = np.arctan(np.abs(z2[np.abs(pr2)>1e-7] / pr2[np.abs(pr2)>1e-7]))
    lat2[z2<0] = -lat2[z2<0]

    return (lon2,lat2)


def gc_dist(lon1,lat1,lon2,lat2):

    # Distance between 2 points along a great circle
    # lat and lon in radians!!
    # 2008, Jeroen Molaker, UCLA

    dlat = lat2-lat1
    dlon = lon2-lon1

    dang = 2*np.arcsin( np.sqrt( np.sin(dlat/2)**2 + np.cos(lat2) * np.cos(lat1) * np.sin(dlon/2)**2 ) )  # haversine function

    r_earth = 6371315.0

    dis = r_earth*dang

    return dis


def create_grid(nx, ny, grdname, title):

    f = netCDF4.Dataset(grdname, 'w', format='NETCDF4')

    one = f.createDimension('one', 1)
    xi_rho = f.createDimension('xi_rho', nx)
    eta_rho = f.createDimension('eta_rho', ny)

    spherical = f.createVariable('spherical','c', ('one'));
    setattr(spherical, 'long_name', "Grid type logical switch")
    setattr(spherical, 'option_T', "spherical")

    angle = f.createVariable('angle','f8', ('eta_rho', 'xi_rho'));
    setattr(angle, 'long_name', "Angle between xi axis and east")
    setattr(angle, 'units', "radians")

    h = f.createVariable('h','f8', ('eta_rho', 'xi_rho'));
    setattr(h, 'long_name', "Final bathymetry at rho-points")
    setattr(h, 'units', "meter")

    hraw = f.createVariable('hraw','f8', ('eta_rho', 'xi_rho'));
    setattr(hraw, 'long_name', "Working bathymetry at rho-points")
    setattr(hraw, 'units', "meter")

    f0 = f.createVariable('f','f8', ('eta_rho', 'xi_rho'));
    setattr(f0, 'long_name', "Coriolis parameter at rho-points")
    setattr(f0, 'units', "second-1")

    pm = f.createVariable('pm','f8', ('eta_rho', 'xi_rho'));
    setattr(pm, 'long_name', "Curvilinear coordinate metric in xi-direction")
    setattr(pm, 'units', "meter-1")

    pn = f.createVariable('pn','f8', ('eta_rho', 'xi_rho'));
    setattr(pn, 'long_name', "Curvilinear coordinate metric in eta-direction")
    setattr(pn, 'units', "meter-1")

    lon_rho = f.createVariable('lon_rho','f8', ('eta_rho', 'xi_rho'));
    setattr(lon_rho, 'long_name', "longitude of rho-points")
    setattr(lon_rho, 'units', "degrees East")

    lat_rho = f.createVariable('lat_rho','f8', ('eta_rho', 'xi_rho'));
    setattr(lat_rho, 'long_name', "latitude of rho-points")
    setattr(lat_rho, 'units', "degrees North")

    mask_rho = f.createVariable('mask_rho','f8', ('eta_rho', 'xi_rho'));
    setattr(mask_rho, 'long_name', "Mask at rho-points")
    setattr(mask_rho, 'units', "land/water (0/1)")

    tra_lon = f.createVariable('tra_lon','f8', ('one'));
    setattr(tra_lon, 'long_name', "Easy grid: Longitudinal translation of base grid")
    setattr(tra_lon, 'units', "degrees East")

    tra_lat = f.createVariable('tra_lat','f8', ('one'));
    setattr(tra_lat, 'long_name', "Easy grid: Latitudinal translation of base grid")
    setattr(tra_lat, 'units', "degrees North")

    rotate = f.createVariable('rotate','f8', ('one'));
    setattr(rotate, 'long_name', "Easy grid: Rotation of base grid")
    setattr(rotate, 'units', "degrees")

    xy_flip = f.createVariable('xy_flip','f8', ('one'));
    setattr(xy_flip, 'long_name', "Easy grid: XY flip of base grid")
    setattr(xy_flip, 'units', "True/False (0/1)")

    f.Title = title
    today = date.today()
    f.Date = today.strftime("%m/%d/%y")
    f.Type = "ROMS grid produced by Easy Grid"

    f.close()


def make_topo(lon, lat):

    toponame = 'etopo5.nc'
    g = netCDF4.Dataset(toponame, 'r')

    topo_lon = g['topo_lon'][:]
    topo_lat = g['topo_lat'][:]
    d = np.transpose(g['topo'][:,:].astype('float64'))
    topo_lon[topo_lon<0] = topo_lon[topo_lon<0] + 360
    topo_lonm = topo_lon-360

    topo_loncat = np.concatenate((topo_lonm, topo_lon), axis=0)
    d_loncat = np.concatenate((d, d), axis=0)

    interp = RegularGridInterpolator((topo_loncat, topo_lat), d_loncat)

    di = interp((lon*180/np.pi,lat*180/np.pi))

    return di


def plot_grid(lon, lat):

    # Define projections
    geodetic = ccrs.Geodetic()
    trans = ccrs.NearsidePerspective(central_longitude=np.mean(lon*180/np.pi), central_latitude=np.mean(lat*180/np.pi))

    lon_deg = lon*180/np.pi - 360
    lat_deg = lat*180/np.pi

    (lo1,la1) = (lon_deg[0,0], lat_deg[0,0])
    (lo2,la2) = (lon_deg[0,-1], lat_deg[0,-1])
    (lo3,la3) = (lon_deg[-1,-1], lat_deg[-1,-1])
    (lo4,la4) = (lon_deg[-1,0], lat_deg[-1,0])

    (min_lo, max_lo) = (np.min(lon_deg), np.max(lon_deg))
    (min_la, max_la) = (np.min(lat_deg), np.max(lat_deg))


    lo1t, la1t = trans.transform_point(lo1, la1, geodetic)
    lo2t, la2t = trans.transform_point(lo2, la2, geodetic)
    lo3t, la3t = trans.transform_point(lo3, la3, geodetic)
    lo4t, la4t = trans.transform_point(lo4, la4, geodetic)

    min_lot, min_lat = trans.transform_point(min_lo, min_la, geodetic)
    max_lot, max_lat = trans.transform_point(max_lo, max_la, geodetic)



    fig = plt.figure(figsize=(10, 10))
    ax = plt.axes(projection=trans)

    ax.plot(
    [lo1t, lo2t, lo3t, lo4t, lo1t],
    [la1t, la2t, la3t, la4t, la1t],
    "ro-"
    )

    ax.coastlines(resolution='50m', linewidth=.5, color='black') # add map
    ax.gridlines()

    plt.show()
