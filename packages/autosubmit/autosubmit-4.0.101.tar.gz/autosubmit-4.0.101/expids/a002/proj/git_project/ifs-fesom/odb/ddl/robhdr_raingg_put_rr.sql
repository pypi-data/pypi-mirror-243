//
//-- ODB/SQL file 'robhdr_raingg_put_rr.sql'
//

SET $hdr_min = 999;
SET $hdr_max = -1;
SET $tslot = -1;

CREATE VIEW robhdr_raingg_put_rr AS
  SELECT seqno,                       // r/o MUST BE FIRST hdr
         mapomm,                      // r/o MDB_MAPOMM_AT_INDEX index
         gp_number,                   // MDB_GP_NUMBER hdr
         time,                        // MDBETM
         report_status,               // MDBRST hdr
         report_event1,               // MDBREV1 hdr
         report_rrflag@raingg,        // MDB_REPORT_RRFLAG raingg

  FROM   timeslot_index, index, hdr, raingg
  WHERE  timeslot@timeslot_index == $tslot AND reportype == $hdr_max
