//
//-- ODB/SQL file 'robhdr_raingg_get_rr.sql'
//

READONLY; // .. except where  UPDATED qualifier was found

SET $hdr_min = 999;
SET $hdr_max = -1;
SET $tslot = -1;

CREATE VIEW robhdr_raingg_get_rr AS
  SELECT seqno,                         // MDBONM (must be the first index; used to build MLNKH2B)
         gp_number,                     // MDB_GP_NUMBER hdr
         report_rrflag@raingg,          // MDB_REPORT_RRFLAG raingg

  FROM   timeslot_index, index, hdr, raingg

  WHERE  timeslot@timeslot_index == $tslot AND reportype == $hdr_max
;

