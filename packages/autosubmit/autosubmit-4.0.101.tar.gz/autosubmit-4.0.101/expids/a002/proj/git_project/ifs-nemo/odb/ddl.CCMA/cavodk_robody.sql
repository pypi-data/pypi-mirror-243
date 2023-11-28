//
//-- ODB/SQL file 'cavodk_robody.sql'
//
//   Last updated:  10-Oct-2001
//

READONLY;

CREATE VIEW cavodk_robody AS
  SELECT  seqno,
          varno,
          datum_anflag@body UPDATED,
          vertco_reference_2,
          obs_error,
          repres_error,
          fg_error,
          fg_depar,
          mf_log_p,
          mf_stddev,
         qc_l UPDATED
  FROM    index, hdr, body, errstat
;
