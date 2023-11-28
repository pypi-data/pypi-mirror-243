//
//-- ODB/SQL file 'cancer_robody.sql'
//
//   Last updated:  8-Apr-2018 (F.Suzat, add obsvalue)
//

READONLY;

CREATE VIEW cancer_robody AS
  SELECT seqno,
         varno,
         datum_anflag@body UPDATED,
         vertco_reference_1,
         vertco_reference_2,
         mf_log_p,
         obsvalue,
         an_depar,
         fg_depar,
         mf_stddev,
         fg_error,
         final_obs_error,
         qc_l UPDATED,
         qc_a@body UPDATED,
         qc_pge@body UPDATED,
  FROM   index, hdr, body, errstat
;
