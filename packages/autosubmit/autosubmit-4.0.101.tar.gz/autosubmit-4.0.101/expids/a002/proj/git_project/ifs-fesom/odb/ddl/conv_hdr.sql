//
//-- ODB/SQL file 'conv_hdr.sql'
//
//   Last updated:  27-Mar-2011
//

READONLY; // .. except where  UPDATED qualifier was found

SET $tslot = -1;
SET $kset = 0;

CREATE VIEW conv_hdr AS
  SELECT seqno,                        // r/o; MUST BECOME FIRST
         anemoht@conv,                 // r/o
         flight_dp_o_dt,               // r/o
  FROM   timeslot_index, index, hdr, conv
  WHERE	 (($tslot == -1 AND timeslot@timeslot_index > 0) OR
(timeslot@timeslot_index == $tslot))
    AND  kset = $kset
 ORDERBY seqno
;
