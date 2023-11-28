//
//-- ODB/SQL file 'camelo_robody.sql'
//
//   Last updated:  10-Oct-2001
//

UPDATED;

CREATE VIEW camelo_robody AS
  SELECT seqno READONLY,
         varno READONLY,
         datum_rdbflag@body,
         datum_anflag,
         vertco_reference_1,
         vertco_reference_2,
         obsvalue,
         mf_log_p,
         final_obs_error,
         obs_error,
         repres_error,
         pers_error
  FROM   index, hdr, body, errstat
;
