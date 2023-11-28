//
//-- ODB/SQL file 'varbc_setup_robody.sql'
//

READONLY;

CREATE VIEW varbc_setup_robody AS
  SELECT seqno,
         varbc_ix@body, 
         final_obs_error,
  FROM   index, hdr, body, errstat
;
