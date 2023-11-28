//
//-- ODB/SQL file 'obatabs_robhdr.sql'
//
//   Last updated:  02-Feb-2005
//

READONLY;

SET $tslot = -1;

CREATE VIEW obatabs_robhdr AS
   SELECT seqno, timeslot@index, obstype, codetype, instrument_type, retrtype, areatype,
// get abnob & mapomm for debugging purposes only
	 abnob, mapomm,
	 body.len,  // r/o (MLNK_hdr2body(2))
         lat, lon,  // r/o
	 trlat  UPDATED, 
         trlon  UPDATED,
         statid // needed for some LELAM-case
    FROM timeslot_index, index, hdr
   WHERE ($tslot == -1 AND timeslot@timeslot_index > 0) OR
(timeslot@timeslot_index == $tslot)
 ORDERBY timeslot@index, seqno
;
