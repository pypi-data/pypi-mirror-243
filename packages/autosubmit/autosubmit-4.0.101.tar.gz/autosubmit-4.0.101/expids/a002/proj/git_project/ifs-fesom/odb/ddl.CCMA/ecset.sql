//
//-- ODB/SQL file 'ecset.sql'
//
//   Last updated:  02-Feb-2005
//

SET $tslot = -1;

READONLY;

CREATE VIEW ecset AS
  SELECT seqno, // seqno for debugging purposes only
         timeslot@index,
	 obstype, codetype, instrument_type, retrtype, areatype,
         reportype,
         trlat,
// get abnob & mapomm for debugging purposes only
	 abnob, mapomm,
	 body.len,
         kset UPDATED,       // updated
    FROM timeslot_index, index, hdr
   WHERE ($tslot == -1 AND timeslot@timeslot_index > 0) OR (timeslot@timeslot_index == $tslot)
  ORDERBY timeslot@index, reportype, seqno
;
