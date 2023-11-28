//
//-- ODB/SQL file 'caviso_robody.sql'
//
//   Last updated:  10-Oct-2001
//

READONLY;

CREATE VIEW caviso_robody AS
  SELECT seqno,
         varno,
         datum_rdbflag@body,
         datum_anflag,
         vertco_reference_1,
         vertco_reference_2,
         mf_log_p,
         obsvalue,
         an_depar,
         fg_depar,
         final_obs_error,
         fg_error,
         qc_a,
         qc_l,
         qc_pge,
  FROM   index, hdr, body, errstat
;
