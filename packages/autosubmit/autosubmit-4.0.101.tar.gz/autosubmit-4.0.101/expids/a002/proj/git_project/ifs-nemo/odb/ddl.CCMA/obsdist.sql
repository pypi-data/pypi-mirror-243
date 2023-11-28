//
//-- ODB/SQL file 'obsdist.sql'
//
//   Created:  22-Jun-2009
//

READONLY; // the view is treated as read/only

CREATE VIEW obsdist AS
  SELECT distinct obstype,codetype, sensor                //  r/o
    FROM hdr
      WHERE (distribtype = 1)
;
