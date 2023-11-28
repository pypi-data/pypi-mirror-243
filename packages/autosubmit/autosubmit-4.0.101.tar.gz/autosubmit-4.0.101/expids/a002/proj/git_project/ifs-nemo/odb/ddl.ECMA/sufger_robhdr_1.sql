//
//-- ODB/SQL file 'sufger_robhdr_1.sql'
//
//   Last updated:  02-Feb-2005
//

READONLY;

SET $tslot = -1;
SET $kset = 0;

CREATE VIEW sufger_robhdr_1 AS
  SELECT seqno,                        // r/o; MUST BECOME FIRST
         abnob, mapomm,                // r/o
         body.len,                     // r/o
         obstype,                      // r/o
         codetype,                     // r/o
         instrument_type,                     // r/o
         retrtype,                     // r/o
         areatype,                     // r/o
         lat, lon,                     // r/o
         timeslot@timeslot_index,      // r/o
  FROM   timeslot_index, index, hdr
  WHERE	 (($tslot == -1 AND timeslot@timeslot_index > 0) OR (timeslot@timeslot_index == $tslot))
    AND  kset = $kset
;
