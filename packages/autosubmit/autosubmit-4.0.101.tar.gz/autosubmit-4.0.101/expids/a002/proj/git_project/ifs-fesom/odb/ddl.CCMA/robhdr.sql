//
//-- ODB/SQL file 'robhdr.sql'
//
//   Last updated:  07-Nov-2002
//

READONLY; // .. except where  UPDATED qualifier was found

SET $tslot = -1;
SET $kset = 0;

CREATE VIEW robhdr AS
  SELECT seqno,                        // r/o; MUST BECOME FIRST
         retrtype UPDATED,             // possibly updated, MUST BE SECOND for Aeolus
         abnob, mapomm, maptovscv,     // r/o
         sensor,                       // r/o
         reportype,                    // r/o
         body.len,                     // r/o
         obstype,                      // r/o
         retrtype  UPDATED,            // r/o
         date, time,                   // r/o
         stalt  UPDATED,               // possibly updated (in ECMA)
         statid,                       // r/o
         lat, lon,                     // r/o
         sat.offset,                   // r/o for Aeolus processing
         timeslot@index,               // r/o for Aeolus processing
         codetype UPDATED,             // possibly updated
         instrument_type UPDATED,      // possibly updated
         areatype UPDATED,             // possibly updated
         report_event1  UPDATED,       // possibly updated
         report_status  UPDATED,       // possibly updated
         lsm           UPDATED,  // Basic surface params at obs locations, archived during screening
         seaice        UPDATED,
         orography     UPDATED,
         tsfc          UPDATED,
         albedo        UPDATED,
         windspeed10m  UPDATED,
         u10m          UPDATED,
         v10m          UPDATED,
         t2m           UPDATED,
         snow_depth    UPDATED,
  FROM   timeslot_index, index, hdr, modsurf
  WHERE	 (($tslot == -1 AND timeslot@timeslot_index > 0) OR
(timeslot@timeslot_index == $tslot))
    AND  kset = $kset
  ORDERBY seqno
;
