//
//-- ODB/SQL file 'conventional_robhdr_1.sql'
//
//   Last updated:  02-Feb-2005
//

SET $tslot = -1;
SET $kobstype_v = 0; // Must be initialized to zero; used by in_vector()-function

CREATE VIEW conventional_robhdr_1 AS
  SELECT seqno  READONLY,              // r/o; MUST BECOME FIRST
         body.len  READONLY,           // r/o
         obstype,                      // r/o
         codetype,                     // possibly updated (in ECMA)
         instrument_type,              // possibly updated (in ECMA)
         retrtype,                     // possibly updated (in ECMA)
         areatype,                     // possibly updated (in ECMA)
         report_rdbflag,               // possibly updated (in ECMA)
         report_status,                // possibly updated (in ECMA)
         report_event1,                // possibly updated (in ECMA)
         report_event2,                // possibly updated (in ECMA)
         date,                         // r/o
         time,                         // r/o
         sonde_type@conv,              // r/o
         station_type@conv,            // r/o
         lat, lon,                     // r/o
         statid@hdr,                   // r/o
         stalt,                        // r/o
         anemoht@conv,                 // possibly updated (in ECMA)
         baroht@conv,                  // possibly updated (in ECMA)
  FROM   timeslot_index, index, hdr, conv
//  WHERE  obstype IN ($synop, $airep, $dribu, $temp, $pilot, $paob)
  WHERE  in_vector(obstype, $kobstype_v)
    AND	 (($tslot == -1 AND timeslot@timeslot_index > 0) OR (timeslot@timeslot_index == $tslot))
;
