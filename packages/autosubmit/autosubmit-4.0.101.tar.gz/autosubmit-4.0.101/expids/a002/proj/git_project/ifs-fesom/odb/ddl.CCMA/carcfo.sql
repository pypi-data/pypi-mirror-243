//
//-- ODB/SQL file 'carcfo.sql'
//
//   Last updated:  10-May-2018 (F.Suzat add seqno)
//   01/2019  D. Puech  correct UPDATED/READONLY 
//

READONLY;

CREATE VIEW carcfo AS
  SELECT  seqno,
          varno,
          vertco_reference_2 UPDATED,
          mf_log_p UPDATED
  FROM    hdr,body
;
