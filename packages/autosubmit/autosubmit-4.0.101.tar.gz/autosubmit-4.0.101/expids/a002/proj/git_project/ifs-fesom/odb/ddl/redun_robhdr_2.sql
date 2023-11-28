//
//-- ODB/SQL file 'redun_robhdr_2.sql'
//
//   Last updated:  02-Feb-2005
//

READONLY;

SET $tslot = -1;

CREATE VIEW redun_robhdr_2 AS
  SELECT seqno,                        // r/o; MUST BECOME FIRST
         abnob, mapomm,                // r/o
         body.len,                     // r/o
  FROM   timeslot_index, index, hdr
  WHERE	 obstype IN ($synop, $dribu, $temp, $paob)
    AND  (($tslot == -1 AND timeslot@timeslot_index > 0) OR
(timeslot@timeslot_index == $tslot))
;
