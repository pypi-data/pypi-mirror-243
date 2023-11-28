//
//-- ODB/SQL file 'raingg_rr.sql'
//

SET $tslot = -1;
SET $kset = 0;

CREATE VIEW raingg_rr AS
  SELECT seqno,                    // MDBONM (must be the first index; used to build MLNKH2B)
         report_rrflag@raingg,     // MDB_REPORT_RRFLAG  raingg

  FROM   timeslot_index, index, hdr, raingg

  WHERE  (($tslot == -1 AND timeslot@timeslot_index > 0) OR (timeslot@timeslot_index == $tslot))
     AND kset = $kset 
     AND reportype >= $synop_rg6h AND reportype <= $synop_rg24h
 ORDERBY seqno
;

