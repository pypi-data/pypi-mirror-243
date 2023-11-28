//
//-- ODB/SQL file 'count_scanpos.sql'
//
//   Last updated:  01/02/2011
//


set satellite_identifier=-1;
READONLY;
CREATE VIEW count_scanpos AS
    SELECT orbit,
           time,
           count(scanpos) 
    FROM hdr,radiance,sat 
    WHERE datastream=0 and satellite_identifier@sat=$satellite_identifier
    order by orbit,time
;

