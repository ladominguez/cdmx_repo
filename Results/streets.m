CDMX_streets = shaperead("1ra_Red_vial_primaria_acceso_controlado_cdmx_09_23.shp");
nstreets = size(CDMX_streets);


% Plotting main streets
for i = 1:nstreets
   lon = CDMX_streets(i).X;
   lat = CDMX_streets(i).Y;
        % p1(1) = line(lon,lat,lon*0+10000,'color',[0 0 1],'linewidth',0.8);
   p1(1) = line(lon,lat,lon*0+10000,'color',[0.5 0.5 0.5],'linewidth',0.4);
   hold on
end