# -*- coding: utf-8 -*-
"""
Written by:     Thomas Cacy
Date:           07/08/2020
Purpose:       Obfuscate the data in gps coordinates by 
               setting the fist to zero

"""
def obfuscate(lat, lon, alt):
    
    #establish origin
    origin_lat = lat[0]
    origin_lon = lon[0]
    origin_alt = alt[0]
    
    #create lists to append
    gps_lat = []
    gps_lon = []
    gps_alt = []
    
    #subtract the origin from the coordinates
    for lat,lon,alt in zip(lat, lon, alt):
        
        gps_lat.append(lat - origin_lat)
        gps_lon.append(lon - origin_lon)
        gps_alt.append(alt - origin_alt)

    return gps_lat,gps_lon,gps_alt