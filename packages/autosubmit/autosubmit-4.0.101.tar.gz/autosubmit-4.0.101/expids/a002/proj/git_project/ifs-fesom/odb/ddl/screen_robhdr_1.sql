//
//-- ODB/SQL file 'screen_robhdr_1.sql'
//
//   Last updated:  02-Feb-2005
//

READONLY; // For printing statistics only

SET $tslot = -1;

CREATE VIEW screen_robhdr_1 AS
  SELECT seqno,                        // r/o; MUST BECOME FIRST
         abnob, mapomm,                // r/o
         body.len,                     // r/o
         obstype,                      // r/o
         report_status,                       // r/o
         report_event1,                       // r/o
         lat, lon,                     // r/o
  FROM   timeslot_index, index, hdr
  WHERE  (($tslot == -1 AND timeslot@timeslot_index > 0) OR (timeslot@timeslot_index == $tslot))
;
