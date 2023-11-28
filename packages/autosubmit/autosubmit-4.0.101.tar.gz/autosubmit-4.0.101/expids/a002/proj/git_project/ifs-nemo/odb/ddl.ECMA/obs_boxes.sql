//
//-- ODB/SQL file 'obs_boxes.sql'
//
//   Last updated:  18-May-2001
//

READONLY;

CREATE VIEW obs_boxes AS
  SELECT timeslot, obstype
    FROM index, hdr
;
