//
//-- ODB/SQL file 'obs_boxes_plus.sql'
//
//   Last updated:  24-July-2020
//

READONLY;

CREATE VIEW obs_boxes_plus AS
  SELECT timeslot, obstype, codetype, sensor
    FROM index, hdr
;
