//
//-- ODB/SQL file 'pre_thinn_robhdr_5.sql'
//
//   Last updated:  05-Mar-2003
//

READONLY;

SET $tslot = -1;

CREATE VIEW pre_thinn_robhdr_5 AS
  SELECT seqno,                        // r/o; MUST BECOME FIRST
         body.len,                     // r/o
	     date,                     // r/o
	     time,                     // r/o
         codetype,                     // r/o
         instrument_type,              // r/o
         retrtype,                     // r/o
         areatype,                     // r/o
         obstype,                      // r/o
         report_status  UPDATED,              // possibly updated (in ECMA)
         report_event1  UPDATED,              // possibly updated (in ECMA)
         sensor,                       // r/o
         gen_centre,                   // r/o
         QI_fc@satob,                   // r/o
         QI_nofc@satob,                   // r/o
         comp_method,                  // r/o
         trlat, trlon,                 // r/o
         lat, lon,                     // r/o
         thinningkey[1:$NUMTHBOX] UPDATED,      // u
         thinningtimekey UPDATED       // u
  FROM   timeslot_index, index, hdr, sat, satob
  WHERE	 (report_status.passive@hdr + report_status.rejected@hdr + report_status.blacklisted@hdr == 0)
    AND  (obstype = $satob)
    AND  (codetype =  90)
    AND  (($tslot == -1 AND timeslot@timeslot_index > 0) OR
(timeslot@timeslot_index == $tslot))
;
