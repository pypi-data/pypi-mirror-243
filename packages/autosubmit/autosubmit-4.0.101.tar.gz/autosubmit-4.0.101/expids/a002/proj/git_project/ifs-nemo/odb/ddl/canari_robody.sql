//
//-- ODB/SQL file 'canari_robody.sql'
//
//   09-Apr-2016 F.Suzat(add vertco_type,hires,lores)
//   Jan-2019 D.P. mise à jour UPDATED // robody.sql
//

UPDATED;

SET $kset = 0;

CREATE VIEW canari_robody AS
  SELECT seqno READONLY,
         varno READONLY,
         vertco_reference_1,
         vertco_type,
         vertco_reference_2,
         obsvalue,
         mf_log_p,
         final_obs_error,
         an_depar,
         fg_depar,
         mf_stddev,
         fg_error,
         hires@update[1:$NMXUPD],   
         lores@update[1:$NMXUPD],  
         biascorr,
  FROM   index, hdr, body, errstat, update[1:$NMXUPD]
  WHERE  kset = $kset
  ORDERBY seqno
;
