//
//-- ODB/SQL file 'ecset_sat.sql'
//
//   Last updated:  02-Feb-2005
//

SET $tslot = -1;
SET $kset = 0;


READONLY;

CREATE VIEW ecset_sat AS
  SELECT seqno, // seqno for debugging purposes only
         timeslot@index,
         reportype,
	 abnob, mapomm,
	 body.len,
         zenith,
    FROM timeslot_index, index, hdr, sat
   WHERE (($tslot == -1 AND timeslot@timeslot_index > 0) OR (timeslot@timeslot_index == $tslot))
         AND  kset = $kset
  ORDERBY timeslot@index, reportype, seqno
;
