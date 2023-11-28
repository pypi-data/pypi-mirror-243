//
//-- ODB/SQL file 'new_thinn_robody_3.sql'
//
//   Created:  18-Aug-2009 - Alan Geer - need to distinguish MERIS TCWV from All-Sky
//   31-Mar-2010 - Anne Fouilloux - needed for tcwc (MERIS, etc.) only
//
//

READONLY;

SET $tslot = -1;

CREATE VIEW new_thinn_robody_3 AS
  SELECT seqno,                        // r/o; MUST BECOME FIRST
         entryno,                      // r/o
         datum_status@body UPDATED,                  // possibly updated (in ECMA)
         datum_event1@body UPDATED,                  // possibly updated (in ECMA)
         varno,                        // r/o
  FROM   timeslot_index, index, hdr, body
  WHERE	 (report_status.passive@hdr + report_status.rejected@hdr + report_status.blacklisted@hdr == 0)
    AND  (obstype = $satem)
    AND  (codetype = $tcwc)
    AND  (($tslot == -1 AND timeslot@timeslot_index > 0) OR
(timeslot@timeslot_index == $tslot))
;
