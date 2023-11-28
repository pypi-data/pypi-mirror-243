//
//-- ODB/SQL file 'update_desc_2.sql'
//
//   Last updated:  23-Jan-2004
//

UPDATED; // Update modification information (for use by CLOSEDB())

CREATE VIEW update_desc_2 AS
  SELECT moddate, modtime, modby, latlon_rad
    FROM desc
;
