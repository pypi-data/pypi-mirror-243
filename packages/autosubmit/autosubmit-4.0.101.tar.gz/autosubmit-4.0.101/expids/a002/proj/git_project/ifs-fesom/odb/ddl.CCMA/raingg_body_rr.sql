//
//-- ODB/SQL file 'raingg_body_rr.sql'
//

SET $tslot = -1;
SET $kset = 0;

CREATE VIEW raingg_body_rr AS

  SELECT seqno  READONLY,          // MDBONM (used to build MLNKH2B)
         rrvalue@raingg_body,      // MDB_RRVALUE    raingg_body
         rrvaluetl@raingg_body,    // MDB_RRVALUETL  raingg_body
         rrvaluead@raingg_body,    // MDB_RRVALUEAD  raingg_body

  FROM   timeslot_index, index, hdr, raingg_body

  WHERE  (($tslot == -1 AND timeslot@timeslot_index > 0) OR (timeslot@timeslot_index == $tslot))
          AND kset = $kset 
          AND reportype >= $synop_rg6h AND reportype <= $synop_rg24h
 ORDERBY seqno
;
