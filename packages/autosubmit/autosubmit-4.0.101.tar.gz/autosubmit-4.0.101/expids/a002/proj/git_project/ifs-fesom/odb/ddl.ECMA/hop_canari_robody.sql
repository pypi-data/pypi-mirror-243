//
//-- ODB/SQL file 'hop_canari_robody.sql'
//
//   Last updated:  09-Apr-2016 F.Suzat(add vertco_type)
//

READONLY;

SET $kset = 0;

CREATE VIEW hop_canari_robody AS
  SELECT seqno,
         varno,
         vertco_reference_1,
         vertco_type,
         vertco_reference_2,
         obsvalue,
         mf_log_p UPDATED,
         final_obs_error,
         an_depar UPDATED,
         fg_depar UPDATED,
         mf_stddev UPDATED,
         fg_error UPDATED,
         hires@update[1:$NMXUPD] UPDATED,          // possibly updated
         lores@update[1:$NMXUPD] UPDATED,          // possibly updated
         biascorr,
  FROM   index, hdr, body, update[1:$NMXUPD], errstat
  WHERE  kset = $kset
;
