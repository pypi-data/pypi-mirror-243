//
//-- ODB/SQL file 'count_orbit.sql'
//
//   Last updated:  01/02/2011
//


set satellite_identifier=-1;
READONLY;
CREATE VIEW count_orbit AS
    SELECT distinct orbit,
    FROM hdr,radiance,sat 
    WHERE datastream=0 and satellite_identifier@sat=$satellite_identifier
;

