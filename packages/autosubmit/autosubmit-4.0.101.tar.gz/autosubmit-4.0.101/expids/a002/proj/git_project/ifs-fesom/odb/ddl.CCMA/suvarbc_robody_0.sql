//
//-- ODB/SQL file 'suvarbc_robody_0.sql'
//
//   Last updated:  19-Mar-2004
//

READONLY;

CREATE VIEW suvarbc_robody_0 AS
  SELECT seqno  READONLY,              // r/o; MUST COME FIRST
         vertco_reference_1,           // possibly updated
         final_obs_error,              // possibly updated
         fg_depar,                     // possibly updated
  FROM   index, hdr, body, errstat
  WHERE  obstype = $satem
;
