//
//   Blacklisting default header query
//
//   == ALWAYS keep black*1.sql to black*10.sql consistent! ==
//

READONLY; // Except entries those marked with  UPDATED

SET $kset = 0;
SET $tslot = -1;

CREATE VIEW black_robhdr_9 AS
  SELECT seqno, // BLACKLIST CORE HDR START. SEQNO MUST COME FIRST
         abnob,
         mapomm,
         body.len,
         obstype,
         codetype,
         instrument_type@hdr,
         retrtype,
         areatype,
         date,
         time,
         report_status  UPDATED,
         report_blacklist  UPDATED,
         stalt,
         lat,
         lon,
         orography,
         statid,
         reportype,
         source,
         sensor, // BLACKLIST CORE HDR END
  FROM   timeslot_index, index, hdr, modsurf,
  WHERE	 (obstype = $radar)
    AND  (kset = $kset)
    AND  (($tslot == -1 AND timeslot@timeslot_index > 0) OR (timeslot@timeslot_index == $tslot))
;
