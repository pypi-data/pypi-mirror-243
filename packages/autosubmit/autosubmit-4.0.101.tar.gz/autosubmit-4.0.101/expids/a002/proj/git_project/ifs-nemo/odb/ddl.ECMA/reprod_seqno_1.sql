//
//-- ODB/SQL file 'reprod_seqno_1.sql'
//
//   Last updated:  05-Jul-2005
//

SET $tslot = -1;

READONLY;

CREATE VIEW reprod_seqno_1 AS
  SELECT seqno UPDATED, // The only time seqno is updated ?
         bufrtype, subtype,
         timeslot@timeslot_index, date, time,
         lat, lon,
	 stalt, statid
    FROM timeslot_index, index, hdr
   WHERE (timeslot@timeslot_index = $tslot OR $tslot = -1)
ORDER BY timeslot@timeslot_index, bufrtype, subtype, date, time, lat, lon, stalt, statid
;
