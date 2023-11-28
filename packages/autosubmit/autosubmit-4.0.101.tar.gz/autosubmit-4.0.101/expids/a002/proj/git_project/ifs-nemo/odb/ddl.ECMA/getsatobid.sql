//
//-- ODB/SQL file 'getsatobid.sql'
//
//   Last updated:  30-Jun-2005
//

READONLY;

CREATE VIEW getsatobid AS
     SELECT DISTINCT
            satellite_identifier@sat,
            codetype,
            comp_method
       FROM hdr, sat, satob
      WHERE obstype = $satob
    ORDERBY satellite_identifier@sat, 
            codetype,   
            comp_method
;
