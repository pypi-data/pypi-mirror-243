//
//-- ODB/SQL file 'canaco_robody.sql'
//
//   Last updated:  10-Oct-2001
//

READONLY;

CREATE VIEW canaco_robody AS
  SELECT  seqno,
          varno,
          obstype,
          sortbox,
          entryno,
          datum_anflag@body UPDATED, // CANACO, version#1 updates
          vertco_reference_1,
          vertco_reference_2,
          obs_error,
          repres_error,
          fg_error,
          fg_depar,
          obsvalue,
          mf_log_p,
          mf_stddev
  FROM    index, hdr, body, errstat
  ORDERBY obstype, sortbox
;
