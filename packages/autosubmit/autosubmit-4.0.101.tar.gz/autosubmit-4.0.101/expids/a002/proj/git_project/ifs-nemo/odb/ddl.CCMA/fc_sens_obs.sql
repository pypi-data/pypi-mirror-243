
//-- ODB/SQL file 'fc_sens_obs.sql'
//
//   Last updated:  27-Apr-2010
//

CREATE VIEW fc_sens_obs AS
  SELECT seqno, entryno, fc_sens_obs
    FROM hdr,body
    WHERE datum_status.passive@body=0
;
