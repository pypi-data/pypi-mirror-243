//
//-- ODB/SQL file 'decis_robhdr_4.sql'
//
//   Last updated:  27-Apr-2015
//

READONLY; // .. except those marked with  UPDATED

SET $kset = -1;
SET $tslot = -1;

CREATE VIEW decis_robhdr_4 AS
  SELECT seqno,                        // r/o; MUST BECOME FIRST
         abnob, mapomm,                // r/o
         body.len,                     // r/o
         report_event1 UPDATED,               // possibly updated (in ECMA)
         report_event2 UPDATED,               // possibly updated (in ECMA)
         report_status UPDATED,               // possibly updated (in ECMA)
         codetype UPDATED,             // possibly updated (in ECMA)
         instrument_type UPDATED,             // possibly updated (in ECMA)
         retrtype UPDATED,             // possibly updated (in ECMA)
         areatype UPDATED,             // possibly updated (in ECMA)
         satellite_identifier,         // r/o
         cellno,                       // r/o
         prodflag,                     // r/o
         wvc_qf,                       // r/o
         nretr_amb,                    // r/o
         lat, lon,
  FROM   timeslot_index, index, hdr, sat, scatt
  WHERE	 (obstype = $scatt)
    AND  (kset = $kset OR $kset = -1)
    AND  (($tslot == -1 AND timeslot@timeslot_index > 0) OR (timeslot@timeslot_index == $tslot))
;