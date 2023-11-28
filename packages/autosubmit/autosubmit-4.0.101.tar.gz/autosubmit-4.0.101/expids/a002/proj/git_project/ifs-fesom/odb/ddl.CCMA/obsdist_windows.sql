//
//-- ODB/SQL file 'obsdist_windows.sql'
//
//   Created:  22-Jun-2009
//

READONLY; // the view is treated as read/only

CREATE VIEW obsdist_windows AS
  SELECT distinct window_offset                //  r/o
    FROM hdr
      WHERE (distribtype = 1)
;
