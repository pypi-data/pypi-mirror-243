//
//-- ODB/SQL file 'ozone_robhdr_1.sql'
//
//   Last updated:  02-Feb-2005
//

SET $tslot = -1;

CREATE VIEW ozone_robhdr_1 AS
  SELECT seqno  READONLY,              // r/o; MUST BECOME FIRST
         body.len  READONLY,           // r/o
         obstype,                      // r/o
         codetype,                     // r/o
         instrument_type@hdr,          // r/o
         retrtype,                     // r/o
         areatype,                     // r/o
         sensor,                       // possibly updated (in ECMA)
         report_rdbflag,               // r/o
         report_status,                // possibly updated (in ECMA)
         report_event1,                // possibly updated (in ECMA)
         report_event2,                // possibly updated (in ECMA)
         date,                         // r/o
         time,                         // r/o
         lat, lon,                     // r/o
         statid,                       // r/o
         stalt,                        // r/o
         retrsource,                   // r/o
  FROM   timeslot_index, index, hdr, resat
  WHERE	 obstype = $satem
    AND  (codetype = $resat)
    AND  (($tslot == -1 AND timeslot@timeslot_index > 0) OR
(timeslot@timeslot_index == $tslot))
;
