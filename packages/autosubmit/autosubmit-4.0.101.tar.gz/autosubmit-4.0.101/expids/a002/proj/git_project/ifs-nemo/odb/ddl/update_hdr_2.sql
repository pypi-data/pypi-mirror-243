//
//-- ODB/SQL file 'update_hdr_2.sql'
//
//   Last updated:  03-Oct-2001
//

UPDATED;

CREATE VIEW update_hdr_2 AS
  SELECT 
         lat, lon,  // Updated (degrees -> radians)
         statid,    // Updated (right shifted)
    FROM hdr
;
