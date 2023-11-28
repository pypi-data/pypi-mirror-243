//
//-- ODB/SQL file 'reprod_seqno_4.sql'
//
//   Last updated:  05-Jul-2005
//

SET $tslot = -1;

READONLY;

CREATE VIEW reprod_seqno_4 AS
  SELECT seqno UPDATED, // The only time seqno is updated ?
         obstype, codetype, // These MUST be be in this order here
         timeslot@timeslot_index, date, time,
         lat, lon,
	 stalt, statid, checksum
    FROM timeslot_index, index, hdr
   WHERE (timeslot@timeslot_index = $tslot OR $tslot = -1)
   ORDER BY timeslot@timeslot_index, obstype, codetype, date, time, lat, lon, stalt, statid, checksum
;
