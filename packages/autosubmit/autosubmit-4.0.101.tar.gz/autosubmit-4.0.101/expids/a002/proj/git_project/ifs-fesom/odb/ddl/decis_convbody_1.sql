//
//-- ODB/SQL file 'decis_convbody_1.sql'
//
//   Last updated:  27-Mar-2011
//

READONLY; // .. except those marked with  UPDATED
NOREORDER;

SET $kset = 0;
SET $tslot = -1;

CREATE VIEW decis_convbody_1 AS
  SELECT level@conv_body,                        // r/o
         ppcode@conv_body,                       // r/o
  FROM   timeslot_index, index, hdr, conv, conv_body
  WHERE	 (kset = $kset)
    AND  (($tslot == -1 AND timeslot@timeslot_index > 0) OR (timeslot@timeslot_index == $tslot))
    AND (obstype = $synop OR obstype = $temp OR obstype = $pilot)
    AND (conv.len > 0)
;
