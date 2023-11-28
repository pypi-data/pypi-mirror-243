//
//-- ODB/SQL file 'robody_raingg_put_rr.sql'
//

SET $hdr_min = 999;
SET $hdr_max = -1;
SET $tslot = -1;

CREATE VIEW robody_raingg_put_rr AS

  SELECT seqno,                  // r/o MUST BE FIRST hdr
         entryno,                //     
         varno,                  //     MDBVNM         body
         obsvalue,               //     MDBVAR         body
         rrvalue@raingg_body,    //     MDB_RRVALUE    raingg_body
         rrvaluetl@raingg_body,  //     MDB_RRVALUETL  raingg_body
         rrvaluead@raingg_body,  //     MDB_RRVALUEAD  raingg_body
         datum_status@body,      //     MDBDSTA        body
         biascorr,               //     MDBTORB        body
         obs_error,              //     MDBOER         errstat
         repres_error,           //     MDBRER         errstat
         final_obs_error,        //     MDBFOE         errstat

  FROM   timeslot_index, index, hdr, body, errstat, raingg_body

  WHERE  timeslot@timeslot_index == $tslot AND reportype == $hdr_max
    AND  varno == 203
;
